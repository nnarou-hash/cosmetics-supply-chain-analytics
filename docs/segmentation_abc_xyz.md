# Segmentation ABC/XYZ et politique de stock différenciée

## Objectif

Adapter les paramètres de stock de sécurité à la contribution économique et à la variabilité de la demande de chaque SKU, plutôt que d'appliquer un nombre de jours identique à tous les produits.

## Méthode

### ABC : valeur de demande

Pour chaque SKU, la valeur de demande simulée sur les 36 mois est calculée comme la somme de la demande mensuelle multipliée par le prix unitaire simulé. Les SKU sont triés par valeur décroissante :

- **A :** jusqu'à 80 % de la valeur cumulée ;
- **B :** de 80 % à 95 % ;
- **C :** au-delà de 95 %.

Cette mesure est une valeur de demande au prix de vente simulé, et non une marge ou une valorisation comptable de stock.

### XYZ : variabilité

Pour chaque SKU, le coefficient de variation de la demande mensuelle est calculé sur les 36 mois :

CV = écart-type de population de la demande mensuelle / moyenne de la demande mensuelle.

Les SKU sont triés par CV croissant et répartis en trois terciles empiriques : X = 33 SKU les plus réguliers, Y = 33 SKU intermédiaires et Z = 34 SKU les plus variables. Dans le portefeuille simulé, les seuils sont CV X ≤ 0,2593 et CV Y ≤ 0,3485.

## Répartition

| Classe | SKU | Part de valeur |
|---|---:|---:|
| A | 50 | 79,74 % |
| B | 26 | 15,11 % |
| C | 24 | 5,15 % |

## Politique de stock de sécurité

| Segment | X · stable | Y · intermédiaire | Z · variable |
|---|---:|---:|---:|
| A · forte valeur | 10 jours | 12 jours | 15 jours |
| B · valeur moyenne | 8 jours | 10 jours | 13 jours |
| C · faible valeur | 7 jours | 9 jours | 12 jours |

## Comparaison des politiques

| Scénario | Taux de service | SKU-mois avec rupture | Demande non satisfaite | Couverture fin de mois |
|---|---:|---:|---:|---:|
| Historique de référence | 91,46 % | 37,31 % | 42 656 | 8,6 j |
| Réapprovisionnement uniforme · 10 jours | 98,37 % | 10,08 % | 8 155 | 24,9 j |
| Première matrice ABC/XYZ | 98,34 % | 12,28 % | 8 271 | 24,9 j |
| Politique ABC/XYZ retenue | 98,64 % | 9,56 % | 6 768 | 26,0 j |
| Politique renforcée | 98,79 % | 8,67 % | 6 034 | 26,9 j |

La politique ABC/XYZ retenue améliore le taux de service de 0,28 point par rapport au stock fixe de 10 jours. Elle réduit la demande non satisfaite de 1 387 unités, soit environ 17,0 %, au prix d'une hausse de couverture moyenne de 1,08 jour. Elle n'optimise pas le coût total.

## Résultats par classe ABC

| Classe | SKU | Part de valeur | Service fixe 10 jours | Service ABC/XYZ | Rupture fixe 10 jours | Rupture ABC/XYZ |
|---|---:|---:|---:|---:|---:|---:|
| A | 50 | 79,74 % | 98,55 % | 99,07 % | 9,56 % | 6,50 % |
| B | 26 | 15,11 % | 98,16 % | 98,01 % | 10,15 % | 11,75 % |
| C | 24 | 5,15 % | 97,71 % | 97,38 % | 11,11 % | 13,54 % |

La classe A bénéficie de la priorité, avec un service à 99,07 % contre 98,55 % sous stock fixe. Les classes B et C connaissent un léger recul du service ; le pilotage différencié doit donc être suivi par segment et ajusté aux objectifs opérationnels.

## Fichiers produits

- outputs/segmentation_abc_xyz.csv : classement des 100 SKU.
- outputs/synthese_classes_abc_xyz.csv : résultats par segment.
- outputs/performance_par_classe_abc.csv : comparaison des classes ABC.
- outputs/comparaison_reappro_uniforme_vs_abc_xyz.csv : comparaison des politiques.
- outputs/synthese_mensuelle_abc_xyz.csv : série mensuelle du scénario retenu.
- outputs/politique_stock_securite_abc_xyz.csv : tableau des jours de sécurité.

## Reproduction

Depuis la racine du dépôt : `python src/simuler_politique_abc_xyz.py`.

## Limites

1. Toutes les observations sont synthétiques et pédagogiques.
2. Les classes XYZ sont des terciles relatifs à cet échantillon et non des seuils universels.
3. Les paramètres de sécurité sont fixés par hypothèse ; ils ne proviennent pas d'une optimisation.
4. La demande mensuelle est répartie uniformément au cours du mois et les délais sont déterministes.
5. Le stock d'ouverture est ajusté de 677 unités dans le scénario retenu afin d'éviter un effet de démarrage.
6. Une valorisation indicative des coûts de possession, de passation et de marge perdue est maintenant disponible dans `docs/analyse_couts_reappro.md`. Elle repose sur des hypothèses fictives et ne constitue pas un optimum économique ni un résultat comptable.
