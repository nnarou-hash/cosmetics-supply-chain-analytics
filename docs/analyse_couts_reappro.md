# Analyse économique du réapprovisionnement

## Objectif et périmètre

Comparer sur 36 mois (janvier 2024 à décembre 2026) trois politiques recalculées à partir de la même demande synthétique : stock uniforme de 10 jours, politique ABC/XYZ retenue et politique ABC/XYZ renforcée. L'historique initial est ajouté comme point de repère, mais son estimation des stocks et des commandes est moins précise que la simulation quotidienne.

## Hypothèses centrales

| Paramètre | Hypothèse centrale | Sensibilité testée |
|---|---:|---:|
| Coût d'achat unitaire | 40 % du prix de vente simulé | Maintenu constant |
| Taux annuel de possession | 20 % de la valeur d'achat du stock moyen | 10 % et 30 % |
| Coût par ligne de commande | 12 € par ligne SKU | 6 € et 24 € |
| Marge perdue sur demande non servie | 60 % du prix de vente | 40 % et 70 % |

Ces paramètres sont fictifs et servent uniquement à illustrer la méthode. Ils ne sont pas issus d'une facture, d'un ERP, d'une comptabilité analytique ou d'un benchmark fournisseur.

## Construction du coût pertinent

Le modèle calcule :

- **Coût de portage** = somme quotidienne de la valeur d'achat du stock disponible × taux annuel de possession / 365.
- **Coût de commande** = nombre de lignes de commande estimées × coût unitaire d'une ligne.
- **Marge perdue estimée** = unités de demande non servies × prix de vente simulé × taux de marge supposé.
- **Coût total pertinent** = coût de portage + coût de commande + marge perdue estimée.

Les achats de marchandises et la valeur du stock final sont affichés séparément. Les achats ne sont pas intégrés au coût pertinent, afin de ne pas assimiler un achat destiné à constituer du stock à une charge consommée sur la période.

## Résultats centraux

| Politique | Portage | Commandes | Marge perdue | Coût pertinent 36 mois | Moyenne annuelle |
|---|---:|---:|---:|---:|---:|
| Stock uniforme · 10 jours | 135 522 € | 43 152 € | 229 793 € | **408 467 €** | 136 156 € |
| Politique ABC/XYZ | 148 088 € | 43 152 € | 173 761 € | **365 000 €** | 121 667 € |
| ABC/XYZ renforcée | 156 557 € | 43 152 € | 146 068 € | **345 778 €** | 115 259 € |

Par rapport au stock uniforme :

- La politique ABC/XYZ réduit le coût pertinent estimé de **43 467 € (10,64 %)**.
- La politique renforcée le réduit de **62 689 € (15,35 %)**.

Le mécanisme est visible : le coût de portage augmente avec le stock moyen, mais la marge perdue estimée diminue plus fortement. Le coût de commande est presque inchangé, car le nombre de lignes de commande est proche entre les simulations.

## Besoin d'achat et stock

| Politique | Achats commandés estimés | Valeur moyenne du stock | Investissement initial de stock ajouté |
|---|---:|---:|---:|
| Stock uniforme · 10 jours | 10 307 376 € | 225 663 € | 10 920 € |
| Politique ABC/XYZ | 10 380 558 € | 246 587 € | 14 264 € |
| ABC/XYZ renforcée | 10 417 425 € | 260 691 € | 18 062 € |

Le besoin d'achat est présenté comme un flux distinct ; il ne faut pas le lire comme une économie ou une dépense nette, car la valeur du stock restant à la fin de la période demeure à l'actif dans ce modèle simplifié.

## Sensibilité aux hypothèses

Chaque variante modifie un seul paramètre à la fois. Le tableau ci-dessous présente le coût pertinent sur 36 mois.

| Hypothèse | Stock uniforme · 10 j | ABC/XYZ | ABC/XYZ renforcée |
|---|---:|---:|---:|
| Centrale | 408 467 € | 365 000 € | 345 778 € |
| Portage faible | 340 706 € | 290 957 € | 267 499 € |
| Portage élevé | 476 228 € | 439 044 € | 424 056 € |
| Commande faible | 386 891 € | 343 424 € | 324 202 € |
| Commande élevée | 451 619 € | 408 152 € | 388 930 € |
| Marge perdue faible | 331 869 € | 307 080 € | 297 088 € |
| Marge perdue élevée | 446 766 € | 393 961 € | 370 122 € |

Le classement reste identique dans les sept variantes testées. Cela rend la conclusion moins dépendante du choix d'une seule hypothèse, mais ne remplace pas une calibration sur les coûts réels ni une analyse combinant simultanément tous les paramètres.

## Précaution sur l'historique

L'historique est évalué à partir de la moyenne mensuelle approchée du stock : (stock d'ouverture + stock de clôture) / 2. Le nombre de lignes de commande est estimé à une ligne par SKU-mois avec quantité de commande positive. Les simulations, elles, recalculent le stock au jour le jour, la passation et les réceptions selon le délai fournisseur. Le total historique n'est donc pas strictement comparable aux trois politiques simulées et ne doit pas être utilisé pour annoncer une économie attribuable au nouveau modèle.

## Limites

1. Tous les prix, volumes, coûts et délais sont synthétiques.
2. Le coût d'achat de 40 % du prix de vente est une hypothèse ; les coûts réels de fabrication, d'approvisionnement et de transport peuvent être très différents.
3. Le taux de possession agrège stockage, financement, assurance, manutention et obsolescence sous un taux unique.
4. Le coût de commande est appliqué par ligne SKU, sans distinguer commandes fournisseur multi-SKU, frais fixes, minimums ou coûts administratifs.
5. La marge perdue ne tient pas compte des substitutions, reports de demande, élasticité, fidélisation ou coût de rupture indirect.
6. Le stock initial ajouté pour neutraliser le démarrage est affiché séparément ; il ne constitue ni une réception historique ni une économie.
7. Le coût pertinent n'est pas un résultat comptable, un EBITDA, un cash-flow net ou un coût total de possession complet.

## Reproduction

Depuis la racine du dépôt :

```bash
python src/analyser_couts_reappro.py
```

Le script génère les fichiers suivants :

- `outputs/comparaison_couts_reappro.csv`
- `outputs/sensibilite_couts_reappro.csv`
- `outputs/synthese_mensuelle_couts.csv`
- `outputs/hypotheses_couts.csv`
