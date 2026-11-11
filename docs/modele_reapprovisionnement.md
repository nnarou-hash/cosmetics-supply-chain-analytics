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
6. Les coûts de stock, de commande, de transport, d'obsolescence et de rupture ne sont pas modélisés. Un taux de service supérieur n'implique donc pas automatiquement un profit ou un coût total meilleur.
7. Les demandes, prévisions, stocks et délais sont tous synthétiques. Les résultats sont des illustrations pédagogiques, pas des estimations de performance réelle.

## Reproduire

Depuis la racine du dépôt :

```bash
python src/simuler_reapprovisionnement.py
```

Dépendance : bibliothèque standard Python uniquement.