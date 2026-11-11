# Audit de qualité des données

## Profil
- Lignes brutes : 3 604
- Clés SKU-mois uniques : 3 600
- SKU : 100
- Périodes mensuelles : 36
- Doublons supplémentaires : 4
- Fournisseurs manquants : 17
- Incohérences de bilan de stock : 25

## Contrôles
| Contrôle | Résultat attendu |
|---|---:|
| Nombre de lignes brutes | 3 604 |
| Clés SKU-mois uniques | 3 600 |
| Doublons supplémentaires | 4 |
| Fournisseurs manquants | 17 |
| Incohérences de bilan de stock | 25 (injectées) |
| Chiffre d'affaires = ventes × prix | 0 erreur |
| Ventes ≤ stock initial + réceptions | 0 erreur |
| Indicateur de rupture correctement calculé | 0 erreur |
| Écart de prévision correctement calculé | 0 erreur |
| Précision de prévision correctement calculée | 0 erreur |
| Couverture correctement calculée | 0 erreur |
| Continuité du stock entre mois | 0 erreur sur les lignes uniques |

## Méthode
Les indicateurs métier et l'analyse exploratoire écartent les doublons en conservant la première occurrence de chaque couple SKU + Date. L'onglet Qualité des données travaille sur les 3 604 lignes brutes afin de rendre les doublons visibles.

Les valeurs manquantes, doublons et incohérences sont des cas de test simulés, pas des défauts de données réelles.

## Reproduire les contrôles
Depuis la racine du dépôt : `python src/validate_data.py`.
