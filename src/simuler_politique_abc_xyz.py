#!/usr/bin/env python3
"""Segmentation ABC/XYZ et simulation d'une politique de stock différenciée.

Exécution : python src/simuler_politique_abc_xyz.py
Dépendance : bibliothèque standard Python uniquement.

ABC repose sur la valeur de demande estimée (Demande x prix de vente simulé).
XYZ répartit les SKU en trois groupes relatifs selon le CV de la demande mensuelle.
"""
from __future__ import annotations

import csv
import math
import statistics
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "cosmetics_supply_chain_36m.csv"
OUTPUT = ROOT / "outputs"
OUTPUT.mkdir(exist_ok=True)

JOURS_REVUE = 30
POLITIQUE = {
    "AX": 10, "AY": 12, "AZ": 15,
    "BX": 7, "BY": 9, "BZ": 12,
    "CX": 3, "CY": 5, "CZ": 8,
}


def lire_donnees():
    uniques, vus = [], set()
    with SOURCE.open(encoding="utf-8-sig", newline="") as fichier:
        for ligne in csv.DictReader(fichier):
            cle = (ligne["SKU"], ligne["Date"])
            if cle in vus:
                continue
            vus.add(cle)
            uniques.append(ligne)
    groupes = defaultdict(list)
    for ligne in uniques:
        groupes[ligne["SKU"]].append(ligne)
    for groupe in groupes.values():
        groupe.sort(key=lambda x: x["Date"])
    return uniques, groupes


def jours_du_mois(date_iso):
    annee, mois, _ = map(int, date_iso.split("-"))
    suivant = date(annee + 1, 1, 1) if mois == 12 else date(annee, mois + 1, 1)
    return (suivant - date(annee, mois, 1)).days


def classer_sku(groupes):
    profils = []
    for sku, lignes in groupes.items():
        demandes = [float(x["Demand_Units"]) for x in lignes]
        moyenne = statistics.fmean(demandes) if demandes else 0
        cv = statistics.pstdev(demandes) / moyenne if moyenne else 0
        valeur = sum(
            float(x["Demand_Units"]) * float(x["Price_EUR"]) for x in lignes
        )
        profils.append({
            "SKU": sku,
            "lignes": lignes,
            "Marque_Fictive": lignes[0]["Brand"],
            "Categorie": lignes[0]["Product_Type"],
            "Sous_Categorie": lignes[0]["Subcategory"],
            "Valeur_Demande_EUR": valeur,
            "CV_Demande_Mensuelle": cv,
            "Delai_Fournisseur_Moyen_Jours": statistics.fmean(
                float(x["Lead_Time_Days"]) for x in lignes
            ),
            "Demande_Historique": sum(float(x["Demand_Units"]) for x in lignes),
            "Ventes_Historiques": sum(float(x["Units_Sold"]) for x in lignes),
            "Ruptures_Historiques": sum(int(float(x["Stockout_Flag"])) for x in lignes),
        })

    valeur_totale = sum(x["Valeur_Demande_EUR"] for x in profils)
    cumul = 0
    for profil in sorted(profils, key=lambda x: (-x["Valeur_Demande_EUR"], x["SKU"])):
        part = profil["Valeur_Demande_EUR"] / valeur_totale if valeur_totale else 0
        cumul += part
        profil["Part_Valeur_Demande"] = part
        profil["Part_Cumulee_Valeur"] = cumul
        profil["Classe_ABC"] = "A" if cumul <= 0.80 else ("B" if cumul <= 0.95 else "C")

    # Terciles empiriques : X = demande la plus stable ; Z = la plus variable.
    cv_tries = sorted(profils, key=lambda x: (x["CV_Demande_Mensuelle"], x["SKU"]))
    seuil_x = cv_tries[len(cv_tries) // 3 - 1]["CV_Demande_Mensuelle"]
    seuil_y = cv_tries[(2 * len(cv_tries)) // 3 - 1]["CV_Demande_Mensuelle"]
    for profil in profils:
        cv = profil["CV_Demande_Mensuelle"]
        profil["Classe_XYZ"] = "X" if cv <= seuil_x else ("Y" if cv <= seuil_y else "Z")
        profil["Classe_ABC_XYZ"] = profil["Classe_ABC"] + profil["Classe_XYZ"]
        profil["Jours_Stock_Securite"] = POLITIQUE[profil["Classe_ABC_XYZ"]]
    return profils, seuil_x, seuil_y


def simuler(profils, jours_securite_par_sku):
    demande_totale = ventes_servies = 0
    sku_mois = mois_avec_rupture = 0
    stock_journalier_total = jours_sku = 0
    commandes = unites_commandees = unites_recues = 0
    couverture_cloture = stock_initial_ajoute = stock_final = transit_final = 0
    mensuel = {}
    stats_abc = {c: {"demande": 0, "servies": 0, "ruptures": 0, "sku_mois": 0, "sku": 0}
                 for c in "ABC"}
    stats_xyz = {c: {"demande": 0, "servies": 0, "ruptures": 0, "sku_mois": 0, "sku": 0}
                 for c in "XYZ"}
    stats_cellules = {}

    for profil in profils:
        sku = profil["SKU"]
        classe_abc = profil["Classe_ABC"]
        classe_xyz = profil["Classe_XYZ"]
        classe = profil["Classe_ABC_XYZ"]
        securite = jours_securite_par_sku(profil)
        for stats in (stats_abc[classe_abc], stats_xyz[classe_xyz]):
            stats["sku"] += 1
        stats_cellules.setdefault(
            classe, {"demande": 0, "servies": 0, "ruptures": 0, "sku_mois": 0, "sku": 0}
        )
        stats_cellules[classe]["sku"] += 1

        lignes = profil["lignes"]
        premiere = lignes[0]
        jours_initiaux = jours_du_mois(premiere["Date"])
        delai_initial = max(1, round(float(premiere["Lead_Time_Days"])))
        stock_ouverture = int(float(premiere["Opening_Stock"]))
        stock_cible_initial = math.ceil(
            float(premiere["Forecast_Units"]) / jours_initiaux
            * (delai_initial + securite)
        )
        stock = max(stock_ouverture, stock_cible_initial)
        stock_initial_ajoute += stock - stock_ouverture
        transit = defaultdict(int)

        for ligne in lignes:
            date_debut = date.fromisoformat(ligne["Date"])
            nb_jours = jours_du_mois(ligne["Date"])
            demande = int(float(ligne["Demand_Units"]))
            prevision = float(ligne["Forecast_Units"])
            delai = max(1, round(float(ligne["Lead_Time_Days"])))
            prevision_journaliere = prevision / nb_jours
            ventes_mois = non_servies_mois = commandes_mois = 0
            quantite_commandee_mois = recus_mois = stock_journalier_mois = 0

            for jour in range(nb_jours):
                date_courante = date_debut + timedelta(days=jour)
                recu = transit.pop(date_courante, 0)
                if recu:
                    stock += recu
                    unites_recues += recu
                    recus_mois += recu

                # Revue mensuelle le premier jour du mois.
                if jour == 0:
                    en_transit = sum(transit.values())
                    niveau_cible = prevision_journaliere * (
                        delai + JOURS_REVUE + securite
                    )
                    position_stock = stock + en_transit
                    quantite = max(0, math.ceil(niveau_cible - position_stock))
                    if quantite:
                        date_arrivee = date_courante + timedelta(days=delai)
                        transit[date_arrivee] += quantite
                        commandes += 1
                        commandes_mois += 1
                        unites_commandees += quantite
                        quantite_commandee_mois += quantite

                demande_jour = (
                    math.floor(demande * (jour + 1) / nb_jours)
                    - math.floor(demande * jour / nb_jours)
                )
                servi = min(stock, demande_jour)
                non_servi = demande_jour - servi
                stock -= servi
                ventes_mois += servi
                non_servies_mois += non_servi
                demande_totale += demande_jour
                ventes_servies += servi
                stock_journalier_mois += stock
                stock_journalier_total += stock
                jours_sku += 1

            rupture = int(non_servies_mois > 0)
            sku_mois += 1
            mois_avec_rupture += rupture
            couverture = stock / prevision_journaliere if prevision_journaliere else 0
            couverture_cloture += couverture
            stock_final += stock

            for stats in (stats_abc[classe_abc], stats_xyz[classe_xyz], stats_cellules[classe]):
                stats["demande"] += demande
                stats["servies"] += ventes_mois
                stats["ruptures"] += rupture
                stats["sku_mois"] += 1

            cle = ligne["Date"]
            mensuel.setdefault(cle, {
                "Date": cle, "Demande": 0, "Ventes_Servies_Scenario": 0,
                "Demande_Non_Satisfaite": 0, "SKU_Mois": 0,
                "SKU_Mois_Avec_Rupture": 0, "Commandes": 0,
                "Unites_Commandees": 0, "Unites_Recues": 0,
                "Stock_Journalier_Somme": 0, "Stock_Cloture_Total": 0,
                "Couverture_Cloture_Somme": 0, "Jours": nb_jours,
            })
            m = mensuel[cle]
            m["Demande"] += demande
            m["Ventes_Servies_Scenario"] += ventes_mois
            m["Demande_Non_Satisfaite"] += non_servies_mois
            m["SKU_Mois"] += 1
            m["SKU_Mois_Avec_Rupture"] += rupture
            m["Commandes"] += commandes_mois
            m["Unites_Commandees"] += quantite_commandee_mois
            m["Unites_Recues"] += recus_mois
            m["Stock_Journalier_Somme"] += stock_journalier_mois
            m["Stock_Cloture_Total"] += stock
            m["Couverture_Cloture_Somme"] += couverture

        transit_final += sum(transit.values())

    lignes_mensuelles = []
    for cle in sorted(mensuel):
        m = mensuel[cle]
        stock_moyen_total = m["Stock_Journalier_Somme"] / m["Jours"]
        demande_journaliere = m["Demande"] / m["Jours"]
        lignes_mensuelles.append({
            "Date": cle,
            "Demande": m["Demande"],
            "Ventes_Servies_Scenario": m["Ventes_Servies_Scenario"],
            "Demande_Non_Satisfaite": m["Demande_Non_Satisfaite"],
            "Taux_Service_Scenario": m["Ventes_Servies_Scenario"] / m["Demande"] if m["Demande"] else 0,
            "SKU_Mois_Avec_Rupture": m["SKU_Mois_Avec_Rupture"],
            "Taux_Rupture_Scenario": m["SKU_Mois_Avec_Rupture"] / m["SKU_Mois"] if m["SKU_Mois"] else 0,
            "Commandes": m["Commandes"],
            "Unites_Commandees": m["Unites_Commandees"],
            "Unites_Recues": m["Unites_Recues"],
            "Stock_Moyen_Total_Unites": stock_moyen_total,
            "Stock_Cloture_Total_Unites": m["Stock_Cloture_Total"],
            "Couverture_Fin_Mois_Moyenne_Jours": m["Couverture_Cloture_Somme"] / m["SKU_Mois"] if m["SKU_Mois"] else 0,
            "Couverture_Moyenne_Stock_Journalier_Jours": stock_moyen_total / demande_journaliere if demande_journaliere else 0,
        })

    return {
        "demande": demande_totale,
        "servies": ventes_servies,
        "taux_service": ventes_servies / demande_totale if demande_totale else 0,
        "taux_rupture": mois_avec_rupture / sku_mois if sku_mois else 0,
        "demande_non_satisfaite": demande_totale - ventes_servies,
        "couverture_cloture_jours": couverture_cloture / sku_mois if sku_mois else 0,
        "couverture_journaliere_jours": stock_journalier_total / demande_totale if demande_totale else 0,
        "commandes": commandes,
        "unites_commandees": unites_commandees,
        "unites_recues": unites_recues,
        "stock_final": stock_final,
        "transit_final": transit_final,
        "stock_initial_ajoute": stock_initial_ajoute,
        "stats_abc": stats_abc,
        "stats_xyz": stats_xyz,
        "stats_cellules": stats_cellules,
        "lignes_mensuelles": lignes_mensuelles,
    }


def exporter(nom, lignes):
    if not lignes:
        return
    with (OUTPUT / nom).open("w", encoding="utf-8-sig", newline="") as fichier:
        writer = csv.DictWriter(fichier, fieldnames=list(lignes[0]))
        writer.writeheader()
        writer.writerows(lignes)


def main():
    lignes, groupes = lire_donnees()
    profils, seuil_x, seuil_y = classer_sku(groupes)

    historique_demande = sum(float(x["Demand_Units"]) for x in lignes)
    historique_servies = sum(float(x["Units_Sold"]) for x in lignes)
    historique_ruptures = sum(int(float(x["Stockout_Flag"])) for x in lignes)
    historique_couverture = sum(
        float(x["Stock_Cover_Months"]) * jours_du_mois(x["Date"]) for x in lignes
    ) / len(lignes)

    uniforme = simuler(profils, lambda x: 10)
    differencie = simuler(profils, lambda x: x["Jours_Stock_Securite"])

    segmentation = []
    for p in sorted(profils, key=lambda x: (-x["Valeur_Demande_EUR"], x["SKU"])):
        segmentation.append({
            "SKU": p["SKU"], "Marque_Fictive": p["Marque_Fictive"],
            "Categorie": p["Categorie"], "Sous_Categorie": p["Sous_Categorie"],
            "Classe_ABC": p["Classe_ABC"], "Classe_XYZ": p["Classe_XYZ"],
            "Classe_ABC_XYZ": p["Classe_ABC_XYZ"],
            "Valeur_Demande_EUR": round(p["Valeur_Demande_EUR"], 2),
            "Part_Valeur_Demande": round(p["Part_Valeur_Demande"], 6),
            "Part_Cumulee_Valeur": round(p["Part_Cumulee_Valeur"], 6),
            "CV_Demande_Mensuelle": round(p["CV_Demande_Mensuelle"], 6),
            "Jours_Stock_Securite": p["Jours_Stock_Securite"],
            "Delai_Fournisseur_Moyen_Jours": round(p["Delai_Fournisseur_Moyen_Jours"], 1),
            "Taux_Service_Historique": round(p["Ventes_Historiques"] / p["Demande_Historique"], 6),
            "Taux_Rupture_Historique": round(p["Ruptures_Historiques"] / len(p["lignes"]), 6),
        })

    total_valeur = sum(p["Valeur_Demande_EUR"] for p in profils)
    synthese_classes = []
    for classe in sorted(differencie["stats_cellules"]):
        st = differencie["stats_cellules"][classe]
        membres = [p for p in profils if p["Classe_ABC_XYZ"] == classe]
        synthese_classes.append({
            "Classe_ABC_XYZ": classe,
            "Nombre_SKU": len(membres),
            "Part_Valeur_Demande": sum(p["Valeur_Demande_EUR"] for p in membres) / total_valeur if total_valeur else 0,
            "CV_Moyen": statistics.fmean(p["CV_Demande_Mensuelle"] for p in membres),
            "Jours_Stock_Securite": POLITIQUE[classe],
            "Demande_Scenario": st["demande"],
            "Ventes_Servies_Scenario": st["servies"],
            "Taux_Service_Scenario": st["servies"] / st["demande"] if st["demande"] else 0,
            "SKU_Mois_Avec_Rupture": st["ruptures"],
            "Taux_Rupture_SKU_Mois": st["ruptures"] / st["sku_mois"] if st["sku_mois"] else 0,
        })

    performance_abc = []
    for classe in "ABC":
        f = uniforme["stats_abc"][classe]
        a = differencie["stats_abc"][classe]
        membres = [p for p in profils if p["Classe_ABC"] == classe]
        performance_abc.append({
            "Classe_ABC": classe, "Nombre_SKU": len(membres),
            "Part_Valeur_Demande": sum(p["Valeur_Demande_EUR"] for p in membres) / total_valeur if total_valeur else 0,
            "Taux_Service_Fixe_10j": f["servies"] / f["demande"] if f["demande"] else 0,
            "Taux_Service_ABC_XYZ": a["servies"] / a["demande"] if a["demande"] else 0,
            "Taux_Rupture_Fixe_10j": f["ruptures"] / f["sku_mois"] if f["sku_mois"] else 0,
            "Taux_Rupture_ABC_XYZ": a["ruptures"] / a["sku_mois"] if a["sku_mois"] else 0,
            "Demande_Non_Satisfaite_Fixe_10j": f["demande"] - f["servies"],
            "Demande_Non_Satisfaite_ABC_XYZ": a["demande"] - a["servies"],
        })

    comparaison = [
        {"Scenario": "Historique de référence",
         "Taux_Service": historique_servies / historique_demande,
         "Taux_Rupture_SKU_Mois": historique_ruptures / len(lignes),
         "Demande_Non_Satisfaite": historique_demande - historique_servies,
         "Couverture_Moyenne_Fin_Mois_Jours": historique_couverture},
        {"Scenario": "Réapprovisionnement uniforme · 10 jours",
         "Taux_Service": uniforme["taux_service"],
         "Taux_Rupture_SKU_Mois": uniforme["taux_rupture"],
         "Demande_Non_Satisfaite": uniforme["demande_non_satisfaite"],
         "Couverture_Moyenne_Fin_Mois_Jours": uniforme["couverture_cloture_jours"],
         "Nombre_Commandes": uniforme["commandes"],
         "Unites_Commandees": uniforme["unites_commandees"],
         "Stock_Initial_Supplementaire": uniforme["stock_initial_ajoute"]},
        {"Scenario": "Politique différenciée ABC/XYZ",
         "Taux_Service": differencie["taux_service"],
         "Taux_Rupture_SKU_Mois": differencie["taux_rupture"],
         "Demande_Non_Satisfaite": differencie["demande_non_satisfaite"],
         "Couverture_Moyenne_Fin_Mois_Jours": differencie["couverture_cloture_jours"],
         "Nombre_Commandes": differencie["commandes"],
         "Unites_Commandees": differencie["unites_commandees"],
         "Stock_Initial_Supplementaire": differencie["stock_initial_ajoute"]},
    ]

    exporter("segmentation_abc_xyz.csv", segmentation)
    exporter("synthese_classes_abc_xyz.csv", synthese_classes)
    exporter("performance_par_classe_abc.csv", performance_abc)
    exporter("comparaison_reappro_uniforme_vs_abc_xyz.csv", comparaison)
    exporter("synthese_mensuelle_abc_xyz.csv", differencie["lignes_mensuelles"])

    print("SEGMENTATION ABC/XYZ ET SIMULATION")
    print(f"SKU classés : {len(profils)}")
    print(f"Seuil CV X : {seuil_x:.3f} ; seuil CV Y : {seuil_y:.3f}")
    print(f"Taux de service avec politique ABC/XYZ : {differencie['taux_service']:.1%}")
    print(f"Taux de rupture SKU-mois : {differencie['taux_rupture']:.1%}")
    print("Fichiers créés dans outputs/.")


if __name__ == "__main__":
    main()
