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
| Lead_Time_Days | Délai fournisseur simulé en jours |
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
