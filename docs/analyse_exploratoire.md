# Analyse exploratoire des données

> **Périmètre analysé :** 3 600 observations SKU-mois uniques, de janvier 2024 à décembre 2026. Les 4 enregistrements dupliqués sont exclus des indicateurs de performance. Le fichier brut contient 3 604 lignes. Tous les chiffres sont issus d'une simulation.

## 1. Synthèse exécutive

| Indicateur | Résultat |
|---|---:|
| Chiffre d'affaires cumulé | 23,74 M€ |
| Unités vendues | 456 632 |
| Demande simulée | 499 288 |
| Taux de service | 91,5 % |
| Taux de rupture (SKU-mois) | 37,3 % |
| Précision des prévisions pondérée (1 − WAPE) | 87,3 % |
| WAPE (erreur absolue pondérée) | 12,7 % |
| Biais de prévision | +1,7 % |
| Couverture moyenne | 0,28 mois (environ 8,5 jours) |
| SKU-mois avec couverture inférieure à 0,75 mois | 3 121 (86,7 %) |

**Premier constat :** dans le scénario simulé, la précision des prévisions pondérée atteint 87,3 % (WAPE de 12,7 %). La disponibilité des produits constitue toutefois le principal point de tension : 37,3 % des SKU-mois connaissent une rupture et 86,7 % sont sous le seuil de couverture retenu.

## 2. Évolution annuelle

| Année | Chiffre d'affaires | Évolution | Taux de rupture | Taux de service | WAPE | Couverture moyenne |
|---|---:|---:|---:|---:|---:|---:|
| 2024 | 6,56 M€ | — | 23,5 % | 94,7 % | 13,4 % | 0,47 mois |
| 2025 | 7,43 M€ | +13,3 % | 46,7 % | 89,5 % | 13,2 % | 0,21 mois |
| 2026 | 9,76 M€ | +31,4 % | 41,8 % | 90,9 % | 11,8 % | 0,17 mois |

Le chiffre d'affaires simulé progresse sur les trois années. En parallèle, la couverture moyenne diminue de 0,47 mois en 2024 à 0,17 mois en 2026. Le taux de rupture augmente fortement en 2025, puis recule en 2026 sans retrouver le niveau de 2024.

## 3. Performance par catégorie

| Catégorie | Chiffre d'affaires | Part du CA | Taux de rupture | Taux de service | WAPE | Couverture |
|---|---:|---:|---:|---:|---:|---:|
| Maquillage | 8,99 M€ | 37,9 % | 38,5 % | 91,2 % | 12,4 % | 0,27 mois |
| Soin de la peau | 8,42 M€ | 35,5 % | 36,0 % | 91,6 % | 12,8 % | 0,30 mois |
| Soin capillaire | 6,33 M€ | 26,6 % | 37,5 % | 91,5 % | 12,9 % | 0,28 mois |

Le maquillage apporte la plus grande contribution au chiffre d'affaires simulé et présente aussi le taux de rupture le plus élevé. Les différences entre catégories restent modérées : le risque de disponibilité est transversal dans cette simulation.

## 4. Saisonnalité

Novembre présente le taux de rupture le plus élevé (47,7 %) et une couverture moyenne de 0,20 mois. Les volumes de demande simulée et le chiffre d'affaires sont également élevés en mai, novembre et décembre.

Cette saisonnalité résulte en partie des paramètres utilisés pour générer les données, qui renforcent certains mois promotionnels et la fin d'année. Elle constitue une piste de scénario à tester, pas une preuve de saisonnalité réelle du marché cosmétique.

## 5. SKU à surveiller

| SKU | Marque fictive | Catégorie | Sous-catégorie | Taux de rupture | Couverture |
|---|---|---|---|---:|---:|
| SKU030 | Marque 01 | Soin de la peau | Nettoyant | 69,4 % | 0,14 mois |
| SKU000 | Marque 01 | Soin de la peau | Sérum | 63,9 % | 0,08 mois |
| SKU011 | Marque 02 | Soin capillaire | Traitement | 63,9 % | 0,10 mois |
| SKU064 | Marque 05 | Maquillage | Fond de teint | 63,9 % | 0,07 mois |
| SKU091 | Marque 02 | Maquillage | Fard à joues | 63,9 % | 0,13 mois |

Ces références combinent un taux de rupture élevé et une couverture moyenne faible. Elles constituent des candidates prioritaires pour tester des paramètres de réapprovisionnement différents.

## 6. Qualité des données

| Statut | Lignes |
|---|---:|
| Conforme | 3 558 |
| Valeur manquante | 17 |
| Incohérence de stock | 25 |
| Doublon | 4 |

Ces exceptions ont été injectées volontairement pour démontrer les contrôles. Les indicateurs métier utilisent les 3 600 couples SKU-mois uniques ; l'onglet qualité analyse les 3 604 lignes brutes.

## 7. Recommandations à tester

1. Prioriser les SKU dont le taux de rupture dépasse 50 % et dont la couverture moyenne est faible.
2. Comparer plusieurs niveaux de stock de sécurité en tenant compte de la variabilité de la demande.
3. Tester un pré-positionnement du stock avant les mois de pointe, notamment novembre et décembre.
4. Suivre ensemble le WAPE, le biais de prévision, le taux de service et le taux de rupture.
5. Équilibrer disponibilité et immobilisation du stock avec une définition du surstock adaptée au contexte.

## 8. Limites de l'analyse

- Les ventes, stocks, demandes et prévisions sont simulés et ne représentent aucune entreprise réelle.
- Les marques et fournisseurs sont des libellés fictifs.
- Les réceptions sont simplifiées : les délais fournisseurs sont présents dans le fichier mais ne déterminent pas encore les dates d'arrivée des commandes.
- Le seuil de surstock (125 % du stock cible) ne détecte qu'un seul SKU-mois dans cette version. Ce KPI et les paramètres associés doivent être réexaminés avant toute conclusion.
- Le WAPE agrégé pondère les erreurs par le volume de demande ; il diffère de la moyenne des précisions calculées individuellement par SKU-mois.
- La moyenne simple du champ `Forecast_Accuracy` est de 86,8 %. Elle n'est pas égale à la précision pondérée (87,3 %), car chaque SKU-mois a le même poids dans la moyenne simple, tandis que la précision pondérée tient compte des volumes de demande.

## Reproductibilité

Depuis la racine du dépôt : `python src/analyse_exploratoire.py`. Le script génère trois tableaux CSV dans `outputs/`.
