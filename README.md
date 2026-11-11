# Analyse de la chaîne d'approvisionnement cosmétique

**Projet portfolio | Business & Data Analyst | Stocks | Prévisions | Qualité des données**

## Objectif métier
Analyser la performance des stocks et de la demande dans un portefeuille de produits cosmétiques, depuis la fiabilisation des données jusqu'à l'identification des risques de rupture et de surstock.

## Tableau de bord
Le [tableau de bord en trois onglets](dashboard/cosmetics_supply_chain_dashboard.html) est un fichier HTML autonome. Télécharge-le puis ouvre-le dans un navigateur.

1. **Vue d'ensemble** : chiffre d'affaires, ventes, précision des prévisions, taux de service et performance annuelle.
2. **Stocks et prévisions** : couverture, ruptures, demande vs prévisions et SKU à surveiller.
3. **Qualité des données** : valeurs manquantes, doublons, incohérences et contrôles.

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
- couverture moyenne : 0,28 mois.

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

## Structure du dépôt
```text
.
├── README.md
├── data/
│   └── cosmetics_supply_chain_36m.csv
├── dashboard/
│   └── cosmetics_supply_chain_dashboard.html
├── docs/
│   ├── data_dictionary.md
│   ├── data_quality_audit.md
│   └── analyse_exploratoire.md
├── outputs/
│   ├── synthese_mensuelle.csv
│   ├── synthese_categories.csv
│   └── liste_sku_a_risque.csv
└── src/
    ├── validate_data.py
    └── analyse_exploratoire.py
```

## Reproduire les analyses
`python src/validate_data.py`  
`python src/analyse_exploratoire.py`

---
*Projet pédagogique. Tous les résultats sont simulés et illustratifs.*
