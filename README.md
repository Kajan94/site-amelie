# Data Ameli · Explorer les professions de santé et les prescriptions

Data Ameli est une application web qui permet d’explorer les données agrégées de l’Assurance Maladie. L’utilisateur peut consulter les effectifs des professions de santé sur une carte des régions, comparer les montants des prescriptions entre régions et visualiser leur répartition par poste pour une année donnée.

## Lancer en local

Préparer **Python 3.12** avec pip, version utilisée pour vérifier le projet. Télécharger ou cloner le dépôt, puis ouvrir un terminal à sa racine, dans le dossier `site-amelie`.

Installer les bibliothèques et lancer l’application :

```sh
python -m pip install -r requirements.txt
python -m flask --app app run
```

Sur macOS ou Linux, utiliser `python3` à la place de `python` si nécessaire.

Ouvrir [localhost:5000](http://127.0.0.1:5000). Aucun compte n’est nécessaire. Le site utilise SQLite et ne nécessite pas de serveur de base de données.

Au premier lancement, l’application extrait automatiquement la **base complète déjà remplie** depuis `site-amelie.zip` vers `model/data/debase_db.sqllite3` (environ 278 Mo). Il faut conserver cette archive à la racine du dépôt et prévoir l’espace disque nécessaire. Aucun import CSV ni génération de données n’est à exécuter. Les lancements suivants réutilisent le fichier extrait.

Les données réelles agrégées couvrent **2010 à 2023**. La carte permet de consulter les effectifs des **18 régions**, et les deux graphiques utilisent la base complète dès le premier lancement.

## Fonctionnalités

- **Professions de santé** : choisir une région sur la carte, puis cocher ou décocher les professions à afficher. Le tableau présente les effectifs et les modes d’exercice pour la dernière année disponible.
- **Prescriptions par région** : sélectionner une année et consulter deux graphiques en anneaux, l’un pour les régions métropolitaines et l’autre pour l’outre-mer. Chaque graphique présente la répartition des montants au sein de son groupe, pour l’ensemble des médecins.
- **Montants moyens par poste** : consulter un histogramme vertical national par catégorie de prescription pour l’année choisie, exprimé en milliers d’euros.
- **Aperçu des prescriptions** : rechercher dans un tableau limité à 200 lignes au maximum. Cette limite concerne l’aperçu ; les graphiques interrogent les agrégats de la base.

## Organisation du code

Flask reçoit les demandes de l’utilisateur, pandas prépare les résultats des requêtes SQLite et Matplotlib produit les graphiques. Les pages utilisent HTML, CSS et JavaScript.

- `app.py` : routes, formulaires et transmission des résultats aux pages.
- `model/db.py` : connexion SQLite et requêtes sur les effectifs et les prescriptions.
- `utils/graphiques.py` : génération des graphiques.
- `templates/` et `static/` : pages, carte et interactions de l’interface.
- `prepare_data.py` : extraction automatique de la base complète fournie dans l’archive.
- `model/data/debase_db.sqllite3` : fichier SQLite complet utilisé par le site après extraction.

Pour la conception et l’exploration SQL, consulter le [dépôt consacré à la base de données](https://github.com/Kajan94/database-amelie).

## Travail en équipe

Projet universitaire réalisé en groupe en **première année de BUT Informatique** à l’IUT de Créteil-Vitry (UPEC). Le travail a porté sur l’interrogation des données de santé et leur restitution dans une application web avec une carte, des tableaux et des graphiques.
