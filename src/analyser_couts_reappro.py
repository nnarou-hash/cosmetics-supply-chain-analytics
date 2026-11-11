#!/usr/bin/env python3
"""Analyse de coûts du réapprovisionnement sur le jeu synthétique (36 mois).

Exécution depuis la racine :
    python src/analyser_couts_reappro.py

Les coûts ci-dessous sont des hypothèses pédagogiques, pas des coûts réels.
Dépendance : bibliothèque standard Python uniquement.
"""
from __future__ import annotations

import csv
import math
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

from simuler_politique_abc_xyz import (
    classer_sku,
    lire_donnees,
    POLITIQUE,
    POLITIQUE_RENFORCEE,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs"
OUTPUT.mkdir(exist_ok=True)

# Hypothèses modifiables : elles sont volontairement explicites.
COUT_ACHAT_SUR_PRIX = 0.40
TAUX_ANNUEL_POSSESSION = 0.20
COUT_LIGNE_COMMANDE_EUR = 12.0
TAUX_MARGE_PERDUE = 0.60
JOURS_REVUE = 30
JOURS_ANNEE = 365


def jours_du_mois(date_iso: str) -> int:
    annee, mois, _ = map(int, date_iso.split("-"))
    suivant = date(annee + 1, 1, 1) if mois == 12 else date(annee, mois + 1, 1)
    return (suivant - date(annee, mois, 1)).days


def simuler_couts(profils, politique, hypotheses, nom_scenario):
    """Rejoue le stock quotidien et valorise possession, commandes et marge perdue."""
    demande_totale = ventes_servies = demande_non_satisfaite = 0
    sku_mois = mois_avec_rupture = commandes = unites_commandees = unites_recues = 0
    somme_valeur_stock_jour = somme_unites_stock_jour = 0.0
    achats_commandes = marge_perdue = ventes_perdues = 0.0
    investissement_initial = valeur_stock_final = transit_final = 0.0
    mensuel = {}

    for profil in profils:
        lignes = profil["lignes"]
        premiere = lignes[0]
        securite = politique(profil)
        jours_initiaux = jours_du_mois(premiere["Date"])
        delai_initial = max(1, round(float(premiere["Lead_Time_Days"])))
        stock_ouverture = float(premiere["Opening_Stock"])
        stock_cible_initial = (
            float(premiere["Forecast_Units"]) / jours_initiaux
            * (delai_initial + securite)
        )
        stock = max(stock_ouverture, int(math.ceil(stock_cible_initial)))
        investissement_initial += (
            stock - stock_ouverture
        ) * float(premiere["Price_EUR"]) * hypotheses["cout_achat_sur_prix"]

        transit = defaultdict(int)

        for ligne in lignes:
            date_debut = date.fromisoformat(ligne["Date"])
            nb_jours = jours_du_mois(ligne["Date"])
            demande = int(float(ligne["Demand_Units"]))
            prevision = float(ligne["Forecast_Units"])
            prix = float(ligne["Price_EUR"])
            delai = max(1, round(float(ligne["Lead_Time_Days"])))
            prevision_journaliere = prevision / nb_jours

            servies_mois = non_servies_mois = commandes_mois = unites_commandees_mois = 0
            recus_mois = 0
            valeur_stock_jour_mois = unites_stock_jour_mois = 0.0
            marge_perdue_mois = achats_mois = 0.0

            for jour in range(nb_jours):
                date_courante = date_debut + timedelta(days=jour)

                # Réception avant la demande du jour.
                recu = transit.pop(date_courante, 0)
                if recu:
                    stock += recu
                    unites_recues += recu
                    recus_mois += recu

                # Revue mensuelle : la position de stock inclut les commandes en transit.
                if jour == 0:
                    quantite_en_transit = sum(transit.values())
                    niveau_cible = prevision_journaliere * (
                        delai + JOURS_REVUE + securite
                    )
                    position_stock = stock + quantite_en_transit
                    quantite = max(0, int(math.ceil(niveau_cible - position_stock)))
                    if quantite:
                        transit[date_courante + timedelta(days=delai)] += quantite
                        commandes += 1
                        commandes_mois += 1
                        unites_commandees += quantite
                        unites_commandees_mois += quantite
                        cout_achat = quantite * prix * hypotheses["cout_achat_sur_prix"]
                        achats_commandes += cout_achat
                        achats_mois += cout_achat

                demande_jour = (
                    (demande * (jour + 1)) // nb_jours
                    - (demande * jour) // nb_jours
                )
                servie = min(stock, demande_jour)
                non_servie = demande_jour - servie
                stock -= servie

                demande_totale += demande_jour
                ventes_servies += servie
                demande_non_satisfaite += non_servie
                servies_mois += servie
                non_servies_mois += non_servie

                valeur_stock_jour = stock * prix * hypotheses["cout_achat_sur_prix"]
                somme_valeur_stock_jour += valeur_stock_jour
                somme_unites_stock_jour += stock
                valeur_stock_jour_mois += valeur_stock_jour
                unites_stock_jour_mois += stock

                cout_marge = non_servie * prix * hypotheses["taux_marge_perdue"]
                marge_perdue += cout_marge
                ventes_perdues += non_servie * prix
                marge_perdue_mois += cout_marge

            sku_mois += 1
            rupture = int(non_servies_mois > 0)
            mois_avec_rupture += rupture

            cle = ligne["Date"]
            mensuel.setdefault(cle, {
                "Date": cle, "Demande": 0, "Servies": 0, "Non_Servies": 0,
                "SKU_Mois": 0, "SKU_Mois_Rupture": 0, "Commandes": 0,
                "Unites_Commandees": 0, "Unites_Recues": 0,
                "Valeur_Stock_Jour_Somme": 0.0, "Unites_Stock_Jour_Somme": 0.0,
                "Marge_Perdue": 0.0, "Achats_Commandes": 0.0,
                "Jours": nb_jours,
            })
            m = mensuel[cle]
            m["Demande"] += demande
            m["Servies"] += servies_mois
            m["Non_Servies"] += non_servies_mois
            m["SKU_Mois"] += 1
            m["SKU_Mois_Rupture"] += rupture
            m["Commandes"] += commandes_mois
            m["Unites_Commandees"] += unites_commandees_mois
            m["Unites_Recues"] += recus_mois
            m["Valeur_Stock_Jour_Somme"] += valeur_stock_jour_mois
            m["Unites_Stock_Jour_Somme"] += unites_stock_jour_mois
            m["Marge_Perdue"] += marge_perdue_mois
            m["Achats_Commandes"] += achats_mois

        valeur_stock_final += stock * float(lignes[-1]["Price_EUR"]) * hypotheses["cout_achat_sur_prix"]
        transit_final += sum(transit.values())

    jours_calendaires = sum(jours_du_mois(x) for x in mensuel)
    cout_portage = somme_valeur_stock_jour * hypotheses["taux_annuel_possession"] / JOURS_ANNEE
    cout_commandes = commandes * hypotheses["cout_ligne_commande_eur"]
    cout_total = cout_portage + cout_commandes + marge_perdue

    return {
        "Scenario": nom_scenario,
        "Demande": demande_totale,
        "Ventes_Servies": ventes_servies,
        "Demande_Non_Satisfaite": demande_non_satisfaite,
        "Taux_Service": ventes_servies / demande_totale if demande_totale else 0,
        "Taux_Rupture_SKU_Mois": mois_avec_rupture / sku_mois if sku_mois else 0,
        "Lignes_Commande_Estimees": commandes,
        "Unites_Commandees": unites_commandees,
        "Unites_Recues": unites_recues,
        "Achats_Commandes_EUR": achats_commandes,
        "Stock_Moyen_Portefeuille_EUR": somme_valeur_stock_jour / jours_calendaires,
        "Stock_Moyen_Portefeuille_Unites": somme_unites_stock_jour / jours_calendaires,
        "Cout_Portage_EUR": cout_portage,
        "Cout_Commandes_EUR": cout_commandes,
        "Cout_Marge_Perdue_EUR": marge_perdue,
        "Cout_Total_Pertinent_EUR": cout_total,
        "Valeur_Stock_Final_EUR": valeur_stock_final,
        "Investissement_Stock_Initial_Ajoute_EUR": investissement_initial,
        "Transit_Final_Unites": transit_final,
        "Mensuel": mensuel,
    }


def evaluer_historique(lignes, groupes, hypotheses):
    """Évalue l'historique avec un stock moyen mensuel approximé par (ouverture + clôture)/2."""
    demande = ventes = non_servies = ruptures = lignes_commande = quantite_commandee = recus = 0
    valeur_stock_jour = unites_stock_jour = achats = marge_perdue = 0.0
    jours_par_date = {}
    for x in lignes:
        d = int(float(x["Demand_Units"]))
        s = int(float(x["Units_Sold"]))
        manque = d - s
        prix = float(x["Price_EUR"])
        jours = jours_du_mois(x["Date"])
        stock_moyen = (float(x["Opening_Stock"]) + float(x["Closing_Stock"])) / 2

        demande += d
        ventes += s
        non_servies += manque
        ruptures += int(float(x["Stockout_Flag"]))
        valeur_stock_jour += (
            stock_moyen * prix * hypotheses["cout_achat_sur_prix"] * jours
        )
        unites_stock_jour += stock_moyen * jours

        # Convention d'estimation : une ligne de commande par SKU-mois avec Order_Quantity > 0.
        if float(x["Order_Quantity"]) > 0:
            lignes_commande += 1
            quantite_commandee += int(float(x["Order_Quantity"]))
        q_recu = int(float(x["Receipts"]))
        recus += q_recu
        achats += q_recu * prix * hypotheses["cout_achat_sur_prix"]
        marge_perdue += manque * prix * hypotheses["taux_marge_perdue"]
        jours_par_date[x["Date"]] = jours

    jours_calendaires = sum(jours_par_date.values())
    cout_portage = valeur_stock_jour * hypotheses["taux_annuel_possession"] / JOURS_ANNEE
    cout_commandes = lignes_commande * hypotheses["cout_ligne_commande_eur"]
    cout_total = cout_portage + cout_commandes + marge_perdue
    stock_final = sum(
        float(g[-1]["Closing_Stock"]) * float(g[-1]["Price_EUR"])
        * hypotheses["cout_achat_sur_prix"]
        for g in groupes.values()
    )
    return {
        "Scenario": "Historique estimé (approximation mensuelle)",
        "Demande": demande, "Ventes_Servies": ventes,
        "Demande_Non_Satisfaite": non_servies,
        "Taux_Service": ventes / demande if demande else 0,
        "Taux_Rupture_SKU_Mois": ruptures / len(lignes) if lignes else 0,
        "Lignes_Commande_Estimees": lignes_commande,
        "Unites_Commandees": quantite_commandee, "Unites_Recues": recus,
        "Achats_Commandes_EUR": achats,
        "Stock_Moyen_Portefeuille_EUR": valeur_stock_jour / jours_calendaires if jours_calendaires else 0,
        "Stock_Moyen_Portefeuille_Unites": unites_stock_jour / jours_calendaires if jours_calendaires else 0,
        "Cout_Portage_EUR": cout_portage, "Cout_Commandes_EUR": cout_commandes,
        "Cout_Marge_Perdue_EUR": marge_perdue, "Cout_Total_Pertinent_EUR": cout_total,
        "Valeur_Stock_Final_EUR": stock_final,
        "Investissement_Stock_Initial_Ajoute_EUR": 0,
        "Transit_Final_Unites": 0,
        "Mensuel": {},
    }


def exporter(nom, lignes):
    if not lignes:
        return
    with (OUTPUT / nom).open("w", encoding="utf-8-sig", newline="") as fichier:
        writer = csv.DictWriter(fichier, fieldnames=list(lignes[0]))
        writer.writeheader()
        writer.writerows(lignes)


def arrondir_sortie(resultat):
    return {k: v for k, v in resultat.items() if k != "Mensuel"}


def main():
    lignes, groupes = lire_donnees()
    profils, _, _ = classer_sku(groupes)
    central = {
        "cout_achat_sur_prix": COUT_ACHAT_SUR_PRIX,
        "taux_annuel_possession": TAUX_ANNUEL_POSSESSION,
        "cout_ligne_commande_eur": COUT_LIGNE_COMMANDE_EUR,
        "taux_marge_perdue": TAUX_MARGE_PERDUE,
    }

    def scenarios(h):
        return [
            evaluer_historique(lignes, groupes, h),
            simuler_couts(profils, lambda p: 10, h, "Stock uniforme · 10 jours"),
            simuler_couts(profils, lambda p: POLITIQUE[p["Classe_ABC_XYZ"]], h, "Politique ABC/XYZ"),
            simuler_couts(profils, lambda p: POLITIQUE_RENFORCEE[p["Classe_ABC_XYZ"]], h, "Politique ABC/XYZ renforcée"),
        ]

    resultat_central = scenarios(central)
    total_uniforme = resultat_central[1]["Cout_Total_Pertinent_EUR"]
    comparaison = []
    for r in resultat_central:
        x = arrondir_sortie(r)
        x["Periode_Mois"] = 36
        x["Cout_Annuel_Moyen_EUR"] = x["Cout_Total_Pertinent_EUR"] / 3
        x["Economie_vs_Uniforme_EUR"] = total_uniforme - x["Cout_Total_Pertinent_EUR"]
        x["Economie_vs_Uniforme_Pct"] = (
            (total_uniforme - x["Cout_Total_Pertinent_EUR"]) / total_uniforme
            if total_uniforme else 0
        )
        comparaison.append(x)

    hypotheses = [
        ("Centrale", 0.20, 12.0, 0.60),
        ("Portage faible", 0.10, 12.0, 0.60),
        ("Portage élevé", 0.30, 12.0, 0.60),
        ("Commande faible", 0.20, 6.0, 0.60),
        ("Commande élevée", 0.20, 24.0, 0.60),
        ("Marge perdue faible", 0.20, 12.0, 0.40),
        ("Marge perdue élevée", 0.20, 12.0, 0.70),
    ]
    sensibilite = []
    for nom, taux_portage, cout_commande, marge_perdue in hypotheses:
        h = dict(central)
        h["taux_annuel_possession"] = taux_portage
        h["cout_ligne_commande_eur"] = cout_commande
        h["taux_marge_perdue"] = marge_perdue
        for r in scenarios(h):
            sensibilite.append({
                "Hypothese_Couts": nom, "Scenario": r["Scenario"],
                "Taux_Cout_Stock_Annuel": taux_portage,
                "Cout_Ligne_Commande_EUR": cout_commande,
                "Taux_Marge_Perdue": marge_perdue,
                "Cout_Portage_EUR": r["Cout_Portage_EUR"],
                "Cout_Commandes_EUR": r["Cout_Commandes_EUR"],
                "Cout_Marge_Perdue_EUR": r["Cout_Marge_Perdue_EUR"],
                "Cout_Total_Pertinent_EUR": r["Cout_Total_Pertinent_EUR"],
            })

    couts_mensuels = []
    for r in resultat_central[1:]:
        for cle, m in sorted(r["Mensuel"].items()):
            cout_portage = (
                m["Valeur_Stock_Jour_Somme"]
                * central["taux_annuel_possession"] / JOURS_ANNEE
            )
            cout_commande = m["Commandes"] * central["cout_ligne_commande_eur"]
            couts_mensuels.append({
                "Scenario": r["Scenario"], "Date": cle,
                "Demande_Unites": m["Demande"], "Ventes_Servies": m["Servies"],
                "Demande_Non_Satisfaite": m["Non_Servies"],
                "Taux_Service": m["Servies"] / m["Demande"] if m["Demande"] else 0,
                "Commandes": m["Commandes"], "Unites_Commandees": m["Unites_Commandees"],
                "Unites_Recues": m["Unites_Recues"],
                "Valeur_Moyenne_Stock_Portefeuille_EUR": m["Valeur_Stock_Jour_Somme"] / m["Jours"],
                "Cout_Portage_EUR": cout_portage, "Cout_Commandes_EUR": cout_commande,
                "Cout_Marge_Perdue_EUR": m["Marge_Perdue"],
                "Cout_Total_Pertinent_EUR": cout_portage + cout_commande + m["Marge_Perdue"],
                "Achats_Commandes_EUR": m["Achats_Commandes"],
            })

    parametres = [
        {"Parametre": "Coût d'achat unitaire", "Hypothese_Centrale": "40 % du prix de vente",
         "Sensibilite": "Non varié dans cette analyse", "Utilisation": "Valorisation indicative du stock et des achats"},
        {"Parametre": "Taux annuel de possession", "Hypothese_Centrale": "20 % de la valeur d'achat du stock moyen",
         "Sensibilite": "10 % à 30 %", "Utilisation": "Coût de portage sur 36 mois"},
        {"Parametre": "Coût par ligne de commande", "Hypothese_Centrale": "12 € par ligne SKU",
         "Sensibilite": "6 € à 24 €", "Utilisation": "Coût de passation des commandes"},
        {"Parametre": "Marge perdue sur demande non servie", "Hypothese_Centrale": "60 % du prix de vente",
         "Sensibilite": "40 % à 70 %", "Utilisation": "Coût d'opportunité des ventes perdues"},
        {"Parametre": "Achats", "Hypothese_Centrale": "Quantités commandées × coût d'achat estimé",
         "Sensibilite": "Présentés séparément", "Utilisation": "Besoin d'achat indicatif, exclu du coût pertinent"},
        {"Parametre": "Horizon", "Hypothese_Centrale": "36 mois, janvier 2024 à décembre 2026",
         "Sensibilite": "Sans annualisation des coûts cumulés", "Utilisation": "Comparaison sur un même horizon"},
    ]

    exporter("comparaison_couts_reappro.csv", comparaison)
    exporter("sensibilite_couts_reappro.csv", sensibilite)
    exporter("synthese_mensuelle_couts.csv", couts_mensuels)
    exporter("hypotheses_couts.csv", parametres)

    print("ANALYSE DES COUTS DE REAPPROVISIONNEMENT")
    print(f"Coût total uniforme 10 jours : {resultat_central[1]['Cout_Total_Pertinent_EUR']:,.0f} EUR")
    print(f"Coût total ABC/XYZ : {resultat_central[2]['Cout_Total_Pertinent_EUR']:,.0f} EUR")
    print(f"Coût total ABC/XYZ renforcé : {resultat_central[3]['Cout_Total_Pertinent_EUR']:,.0f} EUR")
    print("Fichiers créés dans outputs/.")


if __name__ == "__main__":
    main()
