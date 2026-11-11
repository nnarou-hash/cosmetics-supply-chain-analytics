# Modèle de simulation du réapprovisionnement

## Objectif

Tester l'effet de paramètres de réapprovisionnement sur la disponibilité des produits, en utilisant les demandes, prévisions et délais fournisseurs simulés dans le jeu de données. Ce scénario est séparé de l'historique initial : il recalcule les commandes, les arrivées, les stocks et les ventes servies.

## Politique testée

- **Périmètre :** 100 SKU et 36 mois, de janvier 2024 à décembre 2026 ; 3 600 clés SKU-mois uniques. Les doublons sont écartés.
- **Fréquence de revue :** une revue au premier jour de chaque mois, soit une période de revue de 30 jours dans la formule de niveau cible.
- **Délai fournisseur :** champ Lead_Time_Days propre à chaque SKU et mois ; la réception est programmée à la date de commande + délai en jours.
- **Demande :** le total mensuel Demand_Units est réparti uniformément sur les jours du mois, avec arrondi entier déterministe.
- **Approvisionnement :** au jour de revue, la position de stock correspond au stock disponible + commandes en transit. La quantité à commander complète cette position jusqu'au niveau cible.
- **Stock de sécurité :** valeur testée de 0, 5, 7, 10 ou 15 jours de demande prévisionnelle.
- **Niveau cible :** prévision journalière × (délai fournisseur + période de revue + stock de sécurité).
- **Réception :** livraison intégrale à la date prévue ; la réception est ajoutée au stock avant la demande du jour.
- **Rupture :** la demande non couverte par le stock disponible est comptée comme non satisfaite, sans report sur les jours suivants.

## Démarrage du scénario

Pour éviter de pénaliser artificiellement le premier mois parce qu'aucune commande n'a été passée avant janvier 2024, le stock d'ouverture de chaque SKU est ajusté au minimum au niveau correspondant à sa prévision journalière initiale × (délai fournisseur initial + stock de sécurité). Dans le scénario retenu (10 jours), l'ajustement agrégé est de 536 unités. Cet ajustement est une hypothèse de simulation et non une réception observée.

## Résultats

| Indicateur | Historique de référence | Réapprovisionnement, 10 jours |
|---|---:|---:|
| Taux de service | 91,5 % | 98,4 % |
| SKU-mois avec rupture | 37,3 % | 10,1 % |
| Demande non satisfaite | 42 656 | 8 155 |
| Couverture de fin de mois moyenne | 8,6 jours | 24,9 jours |
| Commandes | Non disponible dans l'historique | 3 596 |

Le taux de service s'améliore de 6,9 points. Le taux de rupture diminue de 27,2 points. La demande non satisfaite baisse d'environ 80,9 %. En contrepartie, la couverture moyenne de fin de mois passe de 8,6 à 24,9 jours.

## Sensibilité au stock de sécurité

| Stock de sécurité | Taux de service | SKU-mois avec rupture | Demande non satisfaite | Couverture fin de mois |
|---:|---:|---:|---:|---:|
| 0 jour | 92,5 % | 43,5 % | 37 597 | 16,7 jours |
| 5 jours | 96,4 % | 22,5 % | 18 097 | 20,5 jours |
| 7 jours | 97,4 % | 17,4 % | 13 175 | 22,2 jours |
| 10 jours | 98,4 % | 10,1 % | 8 155 | 24,9 jours |
| 15 jours | 99,2 % | 4,8 % | 4 054 | 29,6 jours |

Le stock de sécurité de 10 jours est retenu pour l'illustration du tableau de bord. Il ne s'agit pas d'un optimum démontré : le choix dépendrait du coût de possession, du coût des ruptures et du niveau de service cible.

## Fichiers générés

- outputs/comparaison_scenarios_reappro.csv : comparaison historique et sensibilité.
- outputs/synthese_mensuelle_reappro.csv : série mensuelle du scénario à 10 jours.
- dashboard/cosmetics_supply_chain_dashboard.html : onglet « Simulation de réapprovisionnement ».

## Limites et précautions

1. La demande du mois est répartie uniformément sur les jours, alors que la vraie demande peut être irrégulière.
2. Les délais sont supposés déterministes à partir de la valeur du champ ; aucune variabilité ou fiabilité fournisseur n'est modélisée.
3. Les quantités sont livrées intégralement à la date prévue ; pas de contrainte de capacité, de quantité minimale, de multiple de colis ou de calendrier ouvré.
4. La revue se fait au premier jour de chaque mois ; un contrôle plus fréquent pourrait changer les résultats.
5. L'horizon commence avec un stock ajusté pour neutraliser le démarrage ; l'ajustement doit être pris en compte dans toute comparaison de stock.
6. Une estimation pédagogique des coûts de portage, de commande et de marge perdue est désormais disponible dans `docs/analyse_couts_reappro.md`. Elle dépend d'hypothèses non observées et ne constitue pas un coût complet ; elle n'inclut pas notamment tous les frais de transport, d'obsolescence et les coûts indirects de rupture.
7. Les demandes, prévisions, stocks et délais sont tous synthétiques. Les résultats sont des illustrations pédagogiques, pas des estimations de performance réelle.

## Reproduire

Depuis la racine du dépôt :

```bash
python src/simuler_reapprovisionnement.py
```

Dépendance : bibliothèque standard Python uniquement.

## Extension : segmentation ABC/XYZ

La simulation complémentaire classe les SKU sur deux axes :

- ABC selon la valeur de demande sur 36 mois (demande × prix unitaire simulé), avec seuils cumulatifs de 80 % et 95 %.
- XYZ selon le coefficient de variation de la demande mensuelle sur 36 mois. Les 100 SKU sont répartis en terciles empiriques (33 X, 33 Y, 34 Z ; CV X ≤ 0,2593 et CV Y ≤ 0,3485).

### Politique retenue

| Segment | X | Y | Z |
|---|---:|---:|---:|
| A | 10 jours | 12 jours | 15 jours |
| B | 8 jours | 10 jours | 13 jours |
| C | 7 jours | 9 jours | 12 jours |

### Comparaison des scénarios

| Scénario | Taux de service | SKU-mois avec rupture | Demande non satisfaite | Couverture moyenne fin de mois |
|---|---:|---:|---:|---:|
| Historique de référence | 91,46 % | 37,31 % | 42 656 | 8,6 j |
| Réapprovisionnement uniforme · 10 jours | 98,37 % | 10,08 % | 8 155 | 24,9 j |
| Première matrice ABC/XYZ | 98,34 % | 12,28 % | 8 271 | 24,9 j |
| Politique ABC/XYZ retenue | 98,64 % | 9,56 % | 6 768 | 26,0 j |
| Politique renforcée | 98,79 % | 8,67 % | 6 034 | 26,9 j |

Face au stock fixe de 10 jours, la politique différenciée atteint 98,64 % de taux de service contre 98,37 %, réduit la demande non satisfaite de 8 155 à 6 768 unités et augmente la couverture fin de mois de 24,88 à 25,96 jours. Pour la classe A, le service passe de 98,55 % à 99,07 %. Les classes B et C peuvent être un peu moins bien servies que sous le scénario uniforme.

Le stock initial est augmenté de 677 unités dans le scénario retenu pour éviter un effet de démarrage. Les coûts de stockage et de rupture ne sont pas intégrés : ce résultat ne démontre pas un optimum économique.
