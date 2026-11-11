# Analyse de la chaîne d'approvisionnement cosmétique

**Projet portfolio | Business & Data Analyst | Stocks | Prévisions | Qualité des données**


## Dashboard en ligne

Le dashboard interactif est hébergé sur le portfolio :

**[Ouvrir le dashboard live](https://nnarou-hash.github.io/cosmetics-supply-chain-analytics/)**

Le code source du dashboard est disponible dans `dashboard/cosmetics_supply_chain_dashboard.html`.

## Objectif métier
Analyser la performance des stocks et de la demande dans un portefeuille de produits cosmétiques, depuis la fiabilisation des données jusqu'à l'identification des risques de rupture et de surstock.

## Tableau de bord
Le [tableau de bord en trois onglets](dashboard/cosmetics_supply_chain_dashboard.html) est un fichier HTML autonome. Télécharge-le puis ouvre-le dans un navigateur.

1. **Vue d'ensemble** : chiffre d'affaires, ventes, précision des prévisions, taux de service et performance annuelle.
2. **Stocks et prévisions** : couverture, ruptures, demande vs prévisions et SKU à surveiller.
3. **Qualité des données** : valeurs manquantes, doublons, incohérences et contrôles.
4. **Simulation de réapprovisionnement** : impact du stock de sécurité et des délais fournisseurs sur le taux de service et les ruptures.
5. **Segmentation ABC/XYZ** : segmentation de la valeur de demande et de la variabilité, puis test de stocks de sécurité différenciés.

## Jeu de données
- 3 604 lignes brutes, dont 4 doublons volontairement ajoutés ;
- 3 600 clés SKU-mois uniques attendues ;
- 100 SKU fictifs répartis entre Maquillage, Soin de la peau et Soin capillaire ;
- 36 mois, de janvier 2024 à décembre 2026.

**Transparence :** l'historique des ventes, demandes, stocks et prévisions est entièrement simulé. Les marques et fournisseurs sont des libellés fictifs anonymisés. La structure métier s'inspire du dépôt public [Supply-Chain-Dataset_Excel](https://github.com/Indu-nb/Supply-Chain-Dataset_Excel), mais les 36 mois d'historique de ce projet ne proviennent pas d'une entreprise réelle.

## Résultats de l'analyse exploratoire
- Chiffre d'affaires simulé : 23,74 M€ ;
- taux de service : 91,5 % ;
- taux de rupture : 37,3 % des SKU-mois ;
- précision des prévisions pondérée : 87,3 % ;
- WAPE : 12,7 % (erreur absolue pondérée) ;
- couverture moyenne historique : 0,28 mois.

### Analyse économique du réapprovisionnement
Sous des hypothèses pédagogiques explicites (coût d'achat de 40 % du prix de vente, portage annuel de 20 %, 12 € par ligne de commande et marge perdue de 60 %), le coût pertinent estimé sur 36 mois est de **408 467 €** pour le stock uniforme, **365 000 €** pour ABC/XYZ et **345 778 €** pour la variante renforcée. Ces valeurs ne sont pas des coûts réels : les achats sont affichés séparément, et les hypothèses sont testées en sensibilité. Voir `docs/analyse_couts_reappro.md`.

### Segmentation ABC/XYZ
La segmentation classe les 100 SKU selon leur valeur de demande (A : 79,7 % de la valeur ; B : 15,1 % ; C : 5,2 %) et leur variabilité mensuelle (X : 33 SKU ; Y : 33 ; Z : 34). La politique de sécurité différenciée atteint un taux de service simulé de **98,6 %**, contre 98,4 % avec 10 jours uniformes. Elle réduit la demande non satisfaite de 8 155 à 6 768 unités, avec une couverture moyenne de fin de mois de 26,0 jours. Voir `docs/segmentation_abc_xyz.md`.

### Scénario de réapprovisionnement
Une simulation distincte applique une revue mensuelle et les délais fournisseurs de chaque SKU. Avec 10 jours de stock de sécurité, le taux de service simulé atteint **98,4 %**, contre 91,5 % dans l'historique de référence ; le taux de rupture passe de **37,3 % à 10,1 %** des SKU-mois. La couverture moyenne de fin de mois augmente à **24,9 jours**. Il s'agit d'un arbitrage disponibilité / immobilisation, pas d'une économie financière démontrée.

Voir le [rapport d'analyse exploratoire](docs/analyse_exploratoire.md).

## Définitions des indicateurs
- **Taux de rupture** : part des SKU-mois où la demande dépasse le stock disponible.
- **Taux de service** : unités servies / demande simulée.
- **Couverture** : stock de clôture / prévision mensuelle.
- **WAPE** : somme des erreurs absolues / somme de la demande.
- **Précision des prévisions pondérée** : 1 − WAPE. Elle vaut 87,3 % dans le scénario simulé.
- **Précision moyenne par SKU-mois** : moyenne simple du champ Forecast_Accuracy ; elle vaut 86,8 %. Elle diffère de la précision pondérée car les SKU-mois n'ont pas tous le même poids en volume.
- **Biais de prévision** : (demande − prévision) / demande ; un biais positif signifie une sous-prévision.
- **Sous-couverture** : couverture inférieure à 0,75 mois.
- **Surstock** : stock de clôture supérieur à 125 % du stock cible.
- **Stock de sécurité** : jours de demande prévisionnelle ajoutés au délai fournisseur et à la période de revue pour déterminer le niveau cible.

## Structure du dépôt
```text
.
├── README.md
├── data/
│   └── cosmetics_supply_chain_36m.csv
├── dashboard/
│   └── cosmetics_supply_chain_dashboard.html
├── docs/
│   ├── modele_reapprovisionnement.md
│   ├── segmentation_abc_xyz.md
│   ├── data_dictionary.md
│   ├── data_quality_audit.md
│   └── analyse_exploratoire.md
├── outputs/
│   ├── synthese_mensuelle.csv
│   ├── synthese_categories.csv
│   ├── liste_sku_a_risque.csv
│   ├── comparaison_scenarios_reappro.csv
│   ├── synthese_mensuelle_reappro.csv
│   ├── segmentation_abc_xyz.csv
│   ├── synthese_classes_abc_xyz.csv
│   ├── performance_par_classe_abc.csv
│   ├── comparaison_reappro_uniforme_vs_abc_xyz.csv
│   ├── synthese_mensuelle_abc_xyz.csv
│   ├── politique_stock_securite_abc_xyz.csv
│   ├── sensibilite_politique_abc_xyz.csv
│   ├── comparaison_couts_reappro.csv
│   ├── sensibilite_couts_reappro.csv
│   ├── synthese_mensuelle_couts.csv
│   └── hypotheses_couts.csv
└── src/
    ├── validate_data.py
    ├── analyse_exploratoire.py
    ├── simuler_reapprovisionnement.py
    ├── simuler_politique_abc_xyz.py
    └── analyser_couts_reappro.py
```

## Reproduire les analyses
`python src/validate_data.py`  
`python src/analyse_exploratoire.py`  
`python src/simuler_reapprovisionnement.py`  
`python src/simuler_politique_abc_xyz.py`  
`python src/analyser_couts_reappro.py`

---
*Projet pédagogique. Tous les résultats sont simulés et illustratifs.*
