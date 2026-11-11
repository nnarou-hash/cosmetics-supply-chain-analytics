#!/usr/bin/env python3
"""Simule un réapprovisionnement périodique avec délais fournisseurs réels du jeu simulé.

Exécution : python src/simuler_reapprovisionnement.py
Dépendance : bibliothèque standard Python uniquement.

Le modèle utilise la demande et les prévisions simulées, mais recalcule les commandes
et les réceptions. Il ne réutilise pas le champ Receipts de l'historique initial.
"""
from __future__ import annotations

import csv
import math
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "cosmetics_supply_chain_36m.csv"
OUTPUT = ROOT / "outputs"
OUTPUT.mkdir(exist_ok=True)

JOURS_REVUE = 30
JOURS_SECURITE_TESTES = (0, 5, 7, 10, 15)
SCENARIO_RETENU = 10


def lire_donnees():
    """Conserve une seule ligne par couple SKU-mois, dans l'ordre du fichier."""
    uniques = []
    vus = set()
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
    if mois == 12:
        suivant = date(annee + 1, 1, 1)
    else:
        suivant = date(annee, mois + 1, 1)
    return (suivant - date(annee, mois, 1)).days


def simuler(groupes, jours_securite, jours_revue=JOURS_REVUE):
    demande_totale = ventes_servies = 0
    sku_mois = mois_avec_rupture = 0
    somme_stock_journalier = 0
    commandes = unites_commandees = unites_recues = 0
    stock_final_total = commandes_en_transit = stock_initial_ajoute = 0
    somme_couverture_cloture = 0
    mensuel = {}

    for sku, lignes in groupes.items():
        premiere = lignes[0]
        nb_jours_initial = jours_du_mois(premiere["Date"])
        delai_initial = max(1, round(float(premiere["Lead_Time_Days"])))
        prevision_initiale = float(premiere["Forecast_Units"])
        stock_ouverture = int(float(premiere["Opening_Stock"]))
        point_depart = math.ceil(
            prevision_initiale / nb_jours_initial * (delai_initial + jours_securite)
        )
        stock = max(stock_ouverture, point_depart)
        stock_initial_ajoute += stock - stock_ouverture
        commandes_en_attente = defaultdict(int)

        for ligne in lignes:
            date_debut = date.fromisoformat(ligne["Date"])
            nb_jours = jours_du_mois(ligne["Date"])
            demande = int(float(ligne["Demand_Units"]))
            prevision = float(ligne["Forecast_Units"])
            delai = max(1, round(float(ligne["Lead_Time_Days"])))
            prevision_journaliere = prevision / nb_jours

            ventes_mois = demande_manquante = 0
            commandes_mois = quantite_commandee_mois = recus_mois = 0
            stock_journalier_mois = 0

            for jour in range(nb_jours):
                date_courante = date_debut + timedelta(days=jour)

                # Les réceptions arrivent avant la consommation du jour.
                quantite_recue = commandes_en_attente.pop(date_courante, 0)
                if quantite_recue:
                    stock += quantite_recue
                    unites_recues += quantite_recue
                    recus_mois += quantite_recue

                # Revue périodique le premier jour du mois.
                if jour == 0:
                    stock_en_transit = sum(commandes_en_attente.values())
                    niveau_cible = prevision_journaliere * (
                        delai + jours_revue + jours_securite
                    )
                    position_stock = stock + stock_en_transit
                    quantite = max(0, math.ceil(niveau_cible - position_stock))
                    if quantite:
                        date_arrivee = date_courante + timedelta(days=delai)
                        commandes_en_attente[date_arrivee] += quantite
                        commandes += 1
                        commandes_mois += 1
                        unites_commandees += quantite
                        quantite_commandee_mois += quantite

                # Répartition déterministe de la demande mensuelle sur les jours.
                demande_jour = (
                    math.floor(demande * (jour + 1) / nb_jours)
                    - math.floor(demande * jour / nb_jours)
                )
                servi = min(stock, demande_jour)
                non_servi = demande_jour - servi
                stock -= servi
                ventes_servies += servi
                demande_totale += demande_jour
                ventes_mois += servi
                demande_manquante += non_servi
                stock_journalier_mois += stock
                somme_stock_journalier += stock

            sku_mois += 1
            en_rupture = demande_manquante > 0
            mois_avec_rupture += int(en_rupture)
            couverture_cloture = (
                stock / prevision_journaliere if prevision_journaliere else 0
            )
            somme_couverture_cloture += couverture_cloture

            cle_mois = ligne["Date"]
            if cle_mois not in mensuel:
                mensuel[cle_mois] = {
                    "Date": cle_mois, "Demande": 0, "Ventes_Servies_Scenario": 0,
                    "Demande_Non_Satisfaite": 0, "SKU_Mois": 0,
                    "SKU_Mois_Avec_Rupture": 0, "Commandes": 0,
                    "Unites_Commandees": 0, "Unites_Recues": 0,
                    "Stock_Moyen_Journalier_Total_Sum": 0,
                    "Stock_Cloture_Total_Unites": 0,
                    "Couverture_Fin_Mois_Sum": 0,
                }
            m = mensuel[cle_mois]
            m["Demande"] += demande
            m["Ventes_Servies_Scenario"] += ventes_mois
            m["Demande_Non_Satisfaite"] += demande_manquante
            m["SKU_Mois"] += 1
            m["SKU_Mois_Avec_Rupture"] += int(en_rupture)
            m["Commandes"] += commandes_mois
            m["Unites_Commandees"] += quantite_commandee_mois
            m["Unites_Recues"] += recus_mois
            m["Stock_Moyen_Journalier_Total_Sum"] += stock_journalier_mois
            m["Stock_Cloture_Total_Unites"] += stock
            m["Couverture_Fin_Mois_Sum"] += couverture_cloture

        stock_final_total += stock
        commandes_en_transit += sum(commandes_en_attente.values())

    jours_calendaires = sum(jours_du_mois(x) for x in mensuel)
    couverture_moyenne_journaliere = (
        somme_stock_journalier / demande_totale if demande_totale else 0
    )
    couverture_cloture_moyenne = (
        somme_couverture_cloture / sku_mois if sku_mois else 0
    )
    lignes_mensuelles = []
    for cle in sorted(mensuel):
        m = mensuel[cle]
        nb_jours = jours_du_mois(cle)
        stock_moyen_total = m["Stock_Moyen_Journalier_Total_Sum"] / nb_jours
        demande_journaliere = m["Demande"] / nb_jours
        lignes_mensuelles.append({
            "Date": cle,
            "Demande": m["Demande"],
            "Ventes_Servies_Scenario": m["Ventes_Servies_Scenario"],
            "Demande_Non_Satisfaite": m["Demande_Non_Satisfaite"],
            "Taux_Service_Scenario": round(
                m["Ventes_Servies_Scenario"] / m["Demande"], 6
            ) if m["Demande"] else 0,
            "SKU_Mois_Avec_Rupture": m["SKU_Mois_Avec_Rupture"],
            "Taux_Rupture_Scenario": round(
                m["SKU_Mois_Avec_Rupture"] / m["SKU_Mois"], 6
            ) if m["SKU_Mois"] else 0,
            "Commandes": m["Commandes"],
            "Unites_Commandees": m["Unites_Commandees"],
            "Unites_Recues": m["Unites_Recues"],
            "Stock_Moyen_Total_Unites": round(stock_moyen_total, 2),
            "Stock_Cloture_Total_Unites": m["Stock_Cloture_Total_Unites"],
            "Couverture_Fin_Mois_Moyenne_Jours": round(
                m["Couverture_Fin_Mois_Sum"] / m["SKU_Mois"], 2
            ) if m["SKU_Mois"] else 0,
            "Couverture_Moyenne_Stock_Journalier_Jours": round(
                stock_moyen_total / demande_journaliere, 2
            ) if demande_journaliere else 0,
        })

    return {
        "jours_securite": jours_securite, "jours_revue": jours_revue,
        "demande": demande_totale, "servies": ventes_servies,
        "taux_service": ventes_servies / demande_totale if demande_totale else 0,
        "taux_rupture": mois_avec_rupture / sku_mois if sku_mois else 0,
        "sku_mois_rupture": mois_avec_rupture,
        "demande_non_satisfaite": demande_totale - ventes_servies,
        "couverture_cloture_jours": couverture_cloture_moyenne,
        "couverture_journaliere_jours": couverture_moyenne_journaliere,
        "commandes": commandes, "unites_commandees": unites_commandees,
        "unites_recues": unites_recues, "stock_final": stock_final_total,
        "commandes_en_transit": commandes_en_transit,
        "stock_initial_ajoute": stock_initial_ajoute,
        "lignes_mensuelles": lignes_mensuelles,
    }


def exporter(chemin, lignes):
    with chemin.open("w", encoding="utf-8-sig", newline="") as fichier:
        writer = csv.DictWriter(fichier, fieldnames=list(lignes[0]))
        writer.writeheader()
        writer.writerows(lignes)


def main():
    lignes, groupes = lire_donnees()
    base_demande = sum(int(float(x["Demand_Units"])) for x in lignes)
    base_servies = sum(int(float(x["Units_Sold"])) for x in lignes)
    base_ruptures = sum(int(float(x["Stockout_Flag"])) for x in lignes)
    base_couverture = sum(
        float(x["Stock_Cover_Months"]) * jours_du_mois(x["Date"]) for x in lignes
    ) / len(lignes)

    scenarios = [simuler(groupes, jours) for jours in JOURS_SECURITE_TESTES]
    synthese = [{
        "Scenario": "Historique observé",
        "Jours_Stock_Securite": "",
        "Jours_Revue": "",
        "Taux_Service": round(base_servies / base_demande, 6),
        "Taux_Rupture_SKU_Mois": round(base_ruptures / len(lignes), 6),
        "Demande_Non_Satisfaite": base_demande - base_servies,
        "Couverture_Fin_Mois_Moyenne_Jours": round(base_couverture, 2),
        "Couverture_Moyenne_Stock_Journalier_Jours": "",
        "Commandes": "", "Unites_Commandees": "", "Unites_Recues": "",
        "Stock_Initial_Supplementaire": "",
    }]
    for resultat in scenarios:
        synthese.append({
            "Scenario": f"Stock de securite {resultat['jours_securite']} j",
            "Jours_Stock_Securite": resultat["jours_securite"],
            "Jours_Revue": resultat["jours_revue"],
            "Taux_Service": round(resultat["taux_service"], 6),
            "Taux_Rupture_SKU_Mois": round(resultat["taux_rupture"], 6),
            "Demande_Non_Satisfaite": resultat["demande_non_satisfaite"],
            "Couverture_Fin_Mois_Moyenne_Jours": round(
                resultat["couverture_cloture_jours"], 2
            ),
            "Couverture_Moyenne_Stock_Journalier_Jours": round(
                resultat["couverture_journaliere_jours"], 2
            ),
            "Commandes": resultat["commandes"],
            "Unites_Commandees": resultat["unites_commandees"],
            "Unites_Recues": resultat["unites_recues"],
            "Stock_Initial_Supplementaire": resultat["stock_initial_ajoute"],
        })

    retenu = next(x for x in scenarios if x["jours_securite"] == SCENARIO_RETENU)
    exporter(OUTPUT / "comparaison_scenarios_reappro.csv", synthese)
    exporter(OUTPUT / "synthese_mensuelle_reappro.csv", retenu["lignes_mensuelles"])

    print("SIMULATION DU RÉAPPROVISIONNEMENT")
    print(f"Observations SKU-mois uniques : {len(lignes)}")
    print(f"Taux de service historique : {base_servies / base_demande:.1%}")
    print(f"Taux de service avec {SCENARIO_RETENU} jours de securite : {retenu['taux_service']:.1%}")
    print(f"Taux de rupture SKU-mois historique : {base_ruptures / len(lignes):.1%}")
    print(f"Taux de rupture SKU-mois scenario : {retenu['taux_rupture']:.1%}")
    print(f"Commandes generees : {retenu['commandes']:,}")
    print("Fichiers generes dans outputs/.")


if __name__ == "__main__":
    main()
