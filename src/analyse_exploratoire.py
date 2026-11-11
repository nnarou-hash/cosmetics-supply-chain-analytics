#!/usr/bin/env python3
"""Analyse exploratoire du jeu de données cosmétique simulé.

Exécution : python src/analyse_exploratoire.py
Dépendance : bibliothèque standard Python uniquement.
"""
from __future__ import annotations
import csv
from collections import defaultdict
from pathlib import Path

RACINE=Path(__file__).resolve().parents[1]
SOURCE=RACINE/"data"/"cosmetics_supply_chain_36m.csv"
SORTIE=RACINE/"outputs"
SORTIE.mkdir(exist_ok=True)

def lire():
    with SOURCE.open(encoding="utf-8-sig", newline="") as f:
        brutes=list(csv.DictReader(f))
    vues=set(); uniques=[]
    for r in brutes:
        cle=(r["SKU"],r["Date"])
        if cle not in vues:
            vues.add(cle); uniques.append(r)
    return brutes,uniques

def n(r,champ):
    return float(r[champ]) if r.get(champ) not in ("",None) else 0.0

def indicateurs(groupe):
    demande=sum(n(r,"Demand_Units") for r in groupe)
    ventes=sum(n(r,"Units_Sold") for r in groupe)
    previsions=sum(n(r,"Forecast_Units") for r in groupe)
    erreur=sum(abs(n(r,"Demand_Units")-n(r,"Forecast_Units")) for r in groupe)
    return {
      "observations":len(groupe),
      "ca":sum(n(r,"Revenue_EUR") for r in groupe),
      "ventes":ventes,"demande":demande,"previsions":previsions,
      "taux_rupture":sum(n(r,"Stockout_Flag") for r in groupe)/len(groupe),
      "taux_service":ventes/demande if demande else 0,
      "wape":erreur/demande if demande else 0,
      "biais":(demande-previsions)/demande if demande else 0,
      "couverture":sum(n(r,"Stock_Cover_Months") for r in groupe)/len(groupe),
    }

def groupes(lignes,cle):
    resultat=defaultdict(list)
    for r in lignes: resultat[cle(r)].append(r)
    return resultat

def exporter(nom,lignes):
    if not lignes: return
    with (SORTIE/nom).open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(lignes[0]))
        w.writeheader(); w.writerows(lignes)

def main():
    brutes,uniques=lire()
    mensuel=[]
    for mois,g in sorted(groupes(uniques,lambda r:r["Date"][:7]).items()):
        m=indicateurs(g)
        mensuel.append({"Mois":mois,"Chiffre_Affaires_EUR":round(m["ca"],2),
          "Unites_Vendues":int(m["ventes"]),"Demande":int(m["demande"]),
          "Previsions":int(m["previsions"]),"Taux_Rupture":round(m["taux_rupture"],4),
          "Taux_Service":round(m["taux_service"],4),"WAPE":round(m["wape"],4),
          "Biais_Previsions":round(m["biais"],4),"Couverture_Moyenne_Mois":round(m["couverture"],4)})
    exporter("synthese_mensuelle.csv",mensuel)

    total=indicateurs(uniques); categories=[]
    for categorie,g in sorted(groupes(uniques,lambda r:r["Product_Type"]).items()):
        m=indicateurs(g)
        categories.append({"Categorie":categorie,"Chiffre_Affaires_EUR":round(m["ca"],2),
          "Part_CA":round(m["ca"]/total["ca"],4),"Taux_Rupture":round(m["taux_rupture"],4),
          "Taux_Service":round(m["taux_service"],4),"WAPE":round(m["wape"],4),
          "Couverture_Moyenne_Mois":round(m["couverture"],4)})
    exporter("synthese_categories.csv",categories)

    risques=[]
    for sku,g in groupes(uniques,lambda r:r["SKU"]).items():
        m=indicateurs(g); risques.append({"SKU":sku,"Marque_Fictive":g[0]["Brand"],
          "Categorie":g[0]["Product_Type"],"Sous_Categorie":g[0]["Subcategory"],
          "Chiffre_Affaires_EUR":round(m["ca"],2),"Taux_Rupture":round(m["taux_rupture"],4),
          "Taux_Service":round(m["taux_service"],4),"WAPE":round(m["wape"],4),
          "Couverture_Moyenne_Mois":round(m["couverture"],4)})
    risques.sort(key=lambda x:(-x["Taux_Rupture"],x["Couverture_Moyenne_Mois"]))
    exporter("liste_sku_a_risque.csv",risques[:20])

    print("Analyse exploratoire terminée.")
    print(f"Lignes brutes : {len(brutes):,}")
    print(f"Observations uniques : {len(uniques):,}")
    print(f"Chiffre d'affaires : {total['ca']:,.2f} €")
    print(f"Taux de service : {total['taux_service']:.1%}")
    print(f"Taux de rupture : {total['taux_rupture']:.1%}")
    print(f"WAPE : {total['wape']:.1%}")
    print("Tableaux enregistrés dans le dossier outputs/.")

if __name__=="__main__":
    main()
