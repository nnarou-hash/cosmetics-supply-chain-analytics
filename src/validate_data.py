#!/usr/bin/env python3
"""Valide le jeu de données cosmétique simulé. Exécuter : python src/validate_data.py"""
from __future__ import annotations
import csv,sys
from collections import Counter,defaultdict
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FICHIER=ROOT/"data"/"cosmetics_supply_chain_36m.csv"
def i(r,k): return int(float(r[k]))
def f(r,k): return float(r[k])
def main():
    with FICHIER.open(encoding="utf-8-sig",newline="") as h: lignes=list(csv.DictReader(h))
    vues=set(); uniques=[]; doublons=0
    for r in lignes:
        cle=(r["SKU"],r["Date"])
        if cle in vues: doublons+=1
        else: vues.add(cle); uniques.append(r)
    controles=[
      ("lignes brutes",len(lignes),3604),("couples SKU-mois uniques",len(uniques),3600),
      ("SKU distincts",len({r["SKU"] for r in lignes}),100),
      ("périodes mensuelles",len({r["Date"] for r in lignes}),36),
      ("doublons supplémentaires",doublons,4),
      ("fournisseurs manquants",sum(not r["Supplier"].strip() for r in lignes),17)]
    bilan=ca=ventes=ruptures=ecarts=precision=couverture=negatifs=0
    for r in lignes:
        disponible=i(r,"Opening_Stock")+i(r,"Receipts")
        vendu=i(r,"Units_Sold"); demande=i(r,"Demand_Units"); prevision=i(r,"Forecast_Units")
        stock=i(r,"Closing_Stock"); ecart=demande-prevision
        bilan+=int(disponible-vendu!=stock)
        ca+=int(abs(f(r,"Revenue_EUR")-vendu*f(r,"Price_EUR"))>0.011)
        ventes+=int(vendu>disponible)
        ruptures+=int(i(r,"Stockout_Flag")!=int(demande>disponible))
        ecarts+=int(i(r,"Forecast_Variance")!=ecart)
        attendu=max(0,1-abs(ecart)/demande) if demande else None
        valeur=r["Forecast_Accuracy"].strip()
        precision+=int((attendu is None and bool(valeur)) or (attendu is not None and (not valeur or abs(float(valeur)-attendu)>1e-6)))
        couverture+=int(abs(f(r,"Stock_Cover_Months")-round(stock/max(prevision,1),2))>0.011)
        negatifs+=sum(int(f(r,k)<0) for k in ("Price_EUR","Demand_Units","Units_Sold","Forecast_Units","Opening_Stock","Receipts","Closing_Stock","Revenue_EUR"))
    controles += [("incohérences de bilan de stock",bilan,25),("erreurs de calcul du CA",ca,0),
      ("ventes supérieures au stock disponible",ventes,0),("erreurs de calcul des ruptures",ruptures,0),
      ("erreurs d'écart de prévision",ecarts,0),("erreurs de précision de prévision",precision,0),
      ("erreurs de couverture",couverture,0),("valeurs négatives",negatifs,0)]
    par_sku=defaultdict(list)
    for r in uniques: par_sku[r["SKU"]].append(r)
    continuite=0
    for g in par_sku.values():
        g.sort(key=lambda r:datetime.strptime(r["Date"],"%Y-%m-%d"))
        for a,b in zip(g,g[1:]): continuite+=int(i(b,"Opening_Stock")!=i(a,"Closing_Stock"))
    controles.append(("ruptures de continuité",continuite,0))
    statuts=Counter(r["Data_Quality_Status"] for r in lignes)
    for statut,attendu in {"Conforme":3558,"Valeur manquante":17,"Doublon":4,"Incohérence de stock":25}.items():
        controles.append((f"statut « {statut} »",statuts.get(statut,0),attendu))
    echec=False
    print("VALIDATION DES DONNÉES — PROJET COSMÉTIQUE")
    print("-"*58)
    for nom,obtenu,attendu in controles:
        ok=obtenu==attendu; echec|=not ok
        print(f"[{'OK' if ok else 'ÉCHEC'}] {nom} : {obtenu} (attendu : {attendu})")
    if echec: print("La validation a échoué.",file=sys.stderr); return 1
    print("Tous les contrôles ont le résultat attendu."); return 0
if __name__=="__main__": raise SystemExit(main())
