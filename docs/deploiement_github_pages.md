# Publication du dashboard avec GitHub Pages

## Adresse publique

[Ouvrir le dashboard](<https://nnarou-hash.github.io/cosmetics-supply-chain-analytics/>)

## Activation initiale

Dans le dépôt GitHub, ouvrir **Settings → Pages** puis, dans **Build and deployment**, sélectionner **GitHub Actions** comme source. Cette configuration initiale est à faire une seule fois si Pages n'est pas déjà activé.

## Déploiement automatique

Le workflow `.github/workflows/deploy-pages.yml` s'exécute lorsqu'un commit modifie `dashboard/cosmetics_supply_chain_dashboard.html` sur la branche `main`, ou lorsqu'il est lancé manuellement depuis l'onglet Actions.

Le workflow copie le dashboard vers `_site/index.html`, téléverse le site statique et le publie avec GitHub Pages. Les mises à jour futures du HTML seront donc republiées automatiquement.

## Suivre le déploiement

Consulter l'onglet **Actions**, ouvrir le workflow **Déployer le dashboard sur GitHub Pages**, puis vérifier que le job de publication se termine avec succès. Après le premier déploiement, l'adresse publique est indiquée dans les paramètres **Settings → Pages**.

## Dépannage

Si le workflow échoue parce que Pages n'est pas activé, définir la source sur **GitHub Actions** dans **Settings → Pages**, puis relancer le workflow depuis l'onglet Actions.
