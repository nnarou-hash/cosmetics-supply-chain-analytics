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
- Dans l'historique de référence, les réceptions sont simplifiées : les délais fournisseurs n'y déterminent pas les dates d'arrivée. Une simulation distincte utilise ces délais pour planifier les réceptions recalculées.
- Le seuil de surstock (125 % du stock cible) ne détecte qu'un seul SKU-mois dans cette version. Ce KPI et les paramètres associés doivent être réexaminés avant toute conclusion.
- Le WAPE agrégé pondère les erreurs par le volume de demande ; il diffère de la moyenne des précisions calculées individuellement par SKU-mois.
- La moyenne simple du champ `Forecast_Accuracy` est de 86,8 %. Elle n'est pas égale à la précision pondérée (87,3 %), car chaque SKU-mois a le même poids dans la moyenne simple, tandis que la précision pondérée tient compte des volumes de demande.

## 9. Scénario de réapprovisionnement

Une simulation séparée teste une politique de revue mensuelle. Au premier jour de chaque mois, le niveau cible est calculé à partir de la prévision journalière du SKU, de son délai fournisseur, de 30 jours de période de revue et du stock de sécurité choisi. La quantité commandée tient compte du stock disponible et des commandes déjà en transit. Chaque réception est enregistrée à la date de commande + délai fournisseur. La demande mensuelle est répartie sur les jours du mois.

### Comparaison de référence

| Indicateur | Historique de référence | Scénario retenu (10 jours) |
|---|---:|---:|
| Taux de service | 91,5 % | 98,4 % |
| SKU-mois avec rupture | 37,3 % | 10,1 % |
| Demande non satisfaite | 42 656 unités | 8 155 unités |
| Couverture moyenne fin de mois | 8,6 jours | 24,9 jours |
| Commandes générées | — | 3 596 |

Le scénario réduit les ruptures et la demande non satisfaite, mais augmente la couverture moyenne de fin de mois. Ce résultat illustre un arbitrage de stock et de disponibilité ; il ne démontre pas une réduction du coût total, car les coûts de stockage, de commande, de transport et de rupture ne sont pas valorisés.

### Sensibilité au stock de sécurité

| Stock de sécurité | Taux de service | SKU-mois avec rupture | Demande non satisfaite | Couverture fin de mois |
|---:|---:|---:|---:|---:|
| 0 jour | 92,5 % | 43,5 % | 37 597 | 16,7 jours |
| 5 jours | 96,4 % | 22,5 % | 18 097 | 20,5 jours |
| 7 jours | 97,4 % | 17,4 % | 13 175 | 22,2 jours |
| 10 jours | 98,4 % | 10,1 % | 8 155 | 24,9 jours |
| 15 jours | 99,2 % | 4,8 % | 4 054 | 29,6 jours |

Le scénario à 10 jours est retenu comme compromis illustratif, pas comme optimum universel. Les hypothèses et les limites de la méthode figurent dans le document consacré au modèle.

### Limites spécifiques

- Le modèle suppose une revue le premier jour de chaque mois et une demande répartie uniformément au cours du mois.
- Les commandes sont supposées livrées intégralement après le délai fournisseur simulé ; retards aléatoires, capacités, lots minimums et calendriers de livraison ne sont pas modélisés.
- Le stock initial est ajusté pour éviter un artefact de démarrage : 536 unités sont ajoutées au stock d'ouverture agrégé dans le scénario à 10 jours.
- Le scénario reprend les demandes et prévisions simulées connues du jeu ; il ne constitue pas un test prédictif en conditions réelles.
- Les coûts de possession, passation, transport, obsolescence et rupture ne sont pas valorisés.

## 10. Segmentation ABC/XYZ et stock de sécurité différencié

### Méthode de classement

- **ABC :** valeur de demande sur 36 mois = somme de la demande mensuelle multipliée par le prix unitaire simulé. Les SKU sont triés par valeur décroissante ; A couvre jusqu'à 80 % de la valeur cumulée, B jusqu'à 95 %, C le solde.
- **XYZ :** coefficient de variation (écart-type de population / moyenne) de la demande mensuelle par SKU sur 36 mois. Le portefeuille est réparti en trois terciles empiriques : X (33 SKU, CV ≤ 0,2593), Y (33 SKU, 0,2593 < CV ≤ 0,3485), Z (34 SKU, CV > 0,3485).
- Les seuils XYZ sont relatifs à ce jeu simulé ; ils ne doivent pas être interprétés comme des seuils universels.

### Répartition

| Classe ABC | SKU | Part de valeur de demande |
|---|---:|---:|
| A | 50 | 79,74 % |
| B | 26 | 15,11 % |
| C | 24 | 5,15 % |

### Politique de stock de sécurité retenue

| Segment | X · stable | Y · intermédiaire | Z · variable |
|---|---:|---:|---:|
| A · forte valeur | 10 j | 12 j | 15 j |
| B · valeur moyenne | 8 j | 10 j | 13 j |
| C · faible valeur | 7 j | 9 j | 12 j |

### Résultats globaux

| Indicateur | Réapprovisionnement uniforme (10 j) | Politique ABC/XYZ |
|---|---:|---:|
| Taux de service | 98,37 % | 98,64 % |
| SKU-mois avec rupture | 10,08 % | 9,56 % |
| Demande non satisfaite | 8 155 | 6 768 |
| Couverture de fin de mois moyenne | 24,88 j | 25,96 j |
| Commandes générées | 3 596 | 3 596 |
| Unités commandées | 496 517 | 499 406 |

La politique différenciée apporte +0,28 point de taux de service et réduit la demande non satisfaite de 1 387 unités (environ 17,0 %) par rapport au scénario uniforme. La couverture moyenne augmente d'environ 1,08 jour.

### Résultats par classe ABC

| Classe | SKU | Part de valeur | Service fixe 10 j | Service ABC/XYZ | Rupture fixe 10 j | Rupture ABC/XYZ |
|---|---:|---:|---:|---:|---:|---:|
| A | 50 | 79,74 % | 98,55 % | 99,07 % | 9,56 % | 6,50 % |
| B | 26 | 15,11 % | 98,16 % | 98,01 % | 10,15 % | 11,75 % |
| C | 24 | 5,15 % | 97,71 % | 97,38 % | 11,11 % | 13,54 % |

La classe A, qui pèse près de 80 % de la valeur de demande, bénéficie de la priorité : son taux de service passe de 98,55 % à 99,07 %. Le service des classes B et C recule légèrement par rapport au scénario uniforme. La politique rend donc visible un arbitrage de priorité, et pas une amélioration identique pour tous les produits.

### Détail de la matrice ABC/XYZ

| Segment | SKU | Part de valeur | Stock de sécurité | Service simulé | SKU-mois avec rupture |
|---|---:|---:|---:|---:|---:|
| AX | 16 | 20,35 % | 10 j | 99,27 % | 7,12 % |
| AY | 10 | 14,87 % | 12 j | 98,42 % | 8,89 % |
| AZ | 24 | 44,52 % | 15 j | 99,19 % | 5,09 % |
| BX | 11 | 7,24 % | 8 j | 97,74 % | 15,66 % |
| BY | 11 | 5,80 % | 10 j | 98,72 % | 8,33 % |
| BZ | 4 | 2,07 % | 13 j | 97,02 % | 10,42 % |
| CX | 6 | 1,37 % | 7 j | 97,15 % | 19,44 % |
| CY | 12 | 2,42 % | 9 j | 97,28 % | 13,66 % |
| CZ | 6 | 1,36 % | 12 j | 97,79 % | 7,41 % |

### Scénarios comparés

| Scénario | Taux de service | SKU-mois avec rupture | Demande non satisfaite | Couverture fin de mois |
|---|---:|---:|---:|---:|
| Historique de référence | 91,46 % | 37,31 % | 42 656 | 8,6 j |
| Réapprovisionnement uniforme · 10 jours | 98,37 % | 10,08 % | 8 155 | 24,9 j |
| Première matrice ABC/XYZ | 98,34 % | 12,28 % | 8 271 | 24,9 j |
| Politique ABC/XYZ retenue | 98,64 % | 9,56 % | 6 768 | 26,0 j |
| Politique renforcée | 98,79 % | 8,67 % | 6 034 | 26,9 j |

### Limites

- Les données, prix, demandes, délais et stocks sont fictifs. La valeur ABC est une valeur de demande au prix simulé, pas une marge ou une valorisation comptable du stock.
- Les classes XYZ sont des terciles calculés dans cet échantillon de 100 SKU, et les limites CV varient avec la composition du portefeuille.
- Les jours de stock de sécurité ont été choisis par scénario et testés ; ils ne résultent pas d'une optimisation de coût total ou d'un niveau de service imposé.
- La revue reste mensuelle, les délais sont déterministes et la demande intra-mensuelle est répartie uniformément.
- Le stock initial du scénario ABC/XYZ est ajusté de 677 unités pour neutraliser l'effet de démarrage. Cet ajustement n'est pas une réception observée.
- Les coûts de possession, de commande, de transport, d'obsolescence et de rupture ne sont pas valorisés.

## 11. Analyse économique du réapprovisionnement

Une valorisation indicative compare le stock uniforme de 10 jours, la politique ABC/XYZ et une politique ABC/XYZ renforcée. Les hypothèses centrales sont : coût d'achat à 40 % du prix de vente simulé, taux annuel de possession de 20 %, 12 € par ligne de commande et marge perdue égale à 60 % du prix de vente sur les unités non servies.

| Politique | Coût pertinent sur 36 mois | Moyenne annuelle | Écart vs uniforme |
|---|---:|---:|---:|
| Stock uniforme · 10 jours | 408 467 € | 136 156 € | — |
| Politique ABC/XYZ | 365 000 € | 121 667 € | −43 467 € (−10,6 %) |
| ABC/XYZ renforcée | 345 778 € | 115 259 € | −62 689 € (−15,3 %) |

Le coût pertinent additionne le portage du stock, la passation des commandes et la marge estimée perdue. Les achats de marchandises sont exclus et présentés séparément. La politique ABC/XYZ accroît le coût de portage par rapport au stock uniforme, mais réduit davantage la marge perdue estimée.

Les sept variantes testées (portage faible/élevé, coût de commande faible/élevé, marge perdue faible/élevée, plus le scénario central) conservent le même classement des politiques. Ce test univarié ne remplace pas la calibration de coûts réels ni une variation simultanée des paramètres.

**Limites de comparabilité :** l'historique utilise un stock moyen mensuel approché par (stock d'ouverture + stock de clôture) / 2 et une ligne de commande estimée par SKU-mois positif. Les simulations recalculent les stocks au jour le jour. Le coût historique est donc un repère approximatif, non strictement comparable aux scénarios.

Les coûts, prix, taux et délais sont fictifs. Le résultat ne correspond ni à un coût comptable complet ni à une économie constatée.

Voir [l'analyse économique détaillée](analyse_couts_reappro.md).

## Reproductibilité

Depuis la racine du dépôt :

- `python src/analyse_exploratoire.py` génère les synthèses historiques et la liste des SKU à risque.
- `python src/simuler_reapprovisionnement.py` génère la comparaison des scénarios de stock de sécurité et la synthèse mensuelle du scénario retenu.
