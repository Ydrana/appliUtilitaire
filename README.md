Compilation d'utilitaires
======
![Build](https://github.com/Ydrana/appliUtilitaire/workflows/Build/badge.svg)

Cette petite application codée en Python propose des outils d'aide à la récette et au développement.

## Interface

Portail d'accès avec 3 outils:
- incrémenteur/décrémenteur de date pour fichier XML
- l'installation du visualiseur d'offres Obiwan (repo Github privé)
- outil de recherche des clés de MessageUtility non définies/inutilisées dans le code Java
- (à intégrer) générateur de classes Srvice/DAO/hbm d'Alvin
 

## FAQ
- Comment rapidement packager et mettre à jour la release ?

Le script pyinstaller_build.bat permet de packager en .exe standalone ne nécessitant pas d'installer Python ou des librairies. Le script propose par ailleurs d'incrémenter le numéro de version. Si l'on accepte ce dernier évoluera puis un push sera effectué vers le repo Github. Un workflow devrait alors packager et mettre à disposition une nouvelle release.
