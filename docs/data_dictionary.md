# Dictionnaire de données

Le fichier contient 3 604 lignes brutes : 3 600 observations SKU-mois attendues (100 SKU fictifs × 36 mois), auxquelles s'ajoutent 4 lignes volontairement dupliquées. La période couvre janvier 2024 à décembre 2026. Toutes les mesures opérationnelles sont simulées.

| Champ technique | Définition |
|---|---|
| Date | Premier jour du mois |
| SKU | Identifiant fictif du produit |
| Brand | Libellé de marque fictive anonymisée |
| Product_Type | Catégorie : Maquillage, Soin de la peau ou Soin capillaire |
| Subcategory | Sous-catégorie du produit, en français |
| Price_EUR | Prix unitaire simulé en euros |
| Demand_Units | Demande simulée non contrainte par le stock disponible |
| Units_Sold | Quantité servie ; plafonnée par le stock disponible |
| Forecast_Units | Prévision mensuelle de demande |
| Revenue_EUR | Chiffre d'affaires simulé : Units_Sold × Price_EUR |
| Opening_Stock | Stock disponible au début du mois |
| Receipts | Quantité reçue durant le mois |
| Closing_Stock | Stock de clôture : stock initial + réceptions − ventes, sauf sur 25 exceptions injectées |
| Stock_Target | Stock cible simulé |
| Lead_Time_Days | Délai fournisseur simulé en jours ; utilisé pour dater les réceptions du scénario de réapprovisionnement |
| Order_Quantity | Quantité de réapprovisionnement simulée |
| Stockout_Flag | 1 si la demande dépasse le stock disponible |
| Stock_Cover_Months | Stock de clôture / prévision mensuelle |
| Supplier | Libellé de fournisseur fictif ; vide sur 17 lignes de test |
| Data_Quality_Status | Conforme, Valeur manquante, Doublon ou Incohérence de stock |
| Forecast_Variance | Demande simulée − prévision |
| Forecast_Accuracy | 1 − erreur absolue / demande, avec minimum à 0 ; vide si demande nulle |
| Overstock_Flag | 1 si le stock final dépasse 125 % du stock cible |
| Low_Cover_Flag | 1 si la couverture est inférieure à 0,75 mois |
| Stock_Value_EUR | Stock final × prix unitaire |

## Grain et exceptions
Le grain attendu est une ligne par SKU et par mois. Le panel de base comporte 3 600 clés SKU-mois uniques. Quatre copies supplémentaires ont été ajoutées pour tester la détection des doublons. Dix-sept valeurs fournisseur sont volontairement manquantes et 25 bilans de stock sont volontairement incohérents.

## Continuité du stock
Le stock initial du mois suivant reprend le stock de clôture enregistré le mois précédent, y compris lorsqu'une ligne contient une incohérence injectée. Cela isole l'anomalie au mois concerné.

## Interprétation des prévisions
La précision de prévision est calculée par rapport à la demande simulée (Demand_Units), pas seulement par rapport aux ventes servies (Units_Sold). En situation de rupture, les ventes ne représentent pas toute la demande.

## Sorties du modèle de réapprovisionnement

Le script src/simuler_reapprovisionnement.py crée deux fichiers distincts de l'historique de référence :

| Fichier | Contenu |
|---|---|
| outputs/comparaison_scenarios_reappro.csv | Comparaison de l'historique et de cinq niveaux de stock de sécurité (0, 5, 7, 10 et 15 jours) |
| outputs/synthese_mensuelle_reappro.csv | Demande, ventes servies simulées, demande non satisfaite, taux de service, ruptures, commandes, réceptions, stock et couverture du scénario retenu (10 jours) |

Le scénario recalculé n'écrase pas les champs Receipts, Units_Sold et Closing_Stock de l'historique de référence.
 
## Fichiers de segmentation ABC/XYZ

| Fichier | Définition |
|---|---|
| outputs/segmentation_abc_xyz.csv | Classe ABC, classe XYZ, segment, valeur de demande, part cumulée, CV, délai moyen et stock de sécurité par SKU |
| outputs/synthese_classes_abc_xyz.csv | Effectifs, part de valeur, seuils CV, politique de sécurité et performance par segment ABC/XYZ |
| outputs/performance_par_classe_abc.csv | Comparaison des indicateurs par classe ABC entre stock fixe de 10 jours et politique différenciée |
| outputs/comparaison_reappro_uniforme_vs_abc_xyz.csv | Comparaison de l'historique, des politiques uniformes et différenciées |
| outputs/synthese_mensuelle_abc_xyz.csv | Résultats mensuels du scénario ABC/XYZ |
| outputs/politique_stock_securite_abc_xyz.csv | Jours de stock de sécurité par segment |

**CV de demande mensuelle** : écart-type de population de la demande mensuelle / moyenne de la demande mensuelle sur 36 mois. Les classes X, Y et Z sont des terciles empiriques du portefeuille simulé.


## Modèle économique de réapprovisionnement

| Fichier | Contenu |
|---|---|
| outputs/comparaison_couts_reappro.csv | Coûts de portage, de commande, marge perdue, coût pertinent, achats et investissement de démarrage par scénario |
| outputs/sensibilite_couts_reappro.csv | Sensibilité du coût pertinent aux hypothèses de portage, de commande et de marge perdue |
| outputs/synthese_mensuelle_couts.csv | Coûts mensuels des trois politiques simulées, avec achats estimés et service |
| outputs/hypotheses_couts.csv | Hypothèses centrales et intervalles testés |

**Coût pertinent** : somme du coût de portage du stock, du coût de passation des lignes de commande et de la marge estimée perdue sur la demande non satisfaite. Les achats commandés sont exclus de cette somme et présentés à part.
