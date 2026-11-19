# Data Ameli · Explorer les professions de santé et les prescriptions

Data Ameli est une application web qui permet d’explorer les données agrégées de l’Assurance Maladie. L’utilisateur peut consulter les effectifs des professions de santé sur une carte des régions, comparer les montants des prescriptions entre régions et visualiser leur répartition par poste pour une année donnée.

## Aperçu du site

### Prescriptions par région

[![Montants des prescriptions dans les quatre régions de l’extrait en 2023](docs/prescriptions-regions-2023.png)](docs/prescriptions-regions-2023.png)

Comparaison des montants totaux des prescriptions en 2023, exprimés en millions d’euros. L’extrait fourni couvre l’Île-de-France, Auvergne-Rhône-Alpes, les Hauts-de-France et La Réunion. Le sélecteur d’année permet de comparer 2022 et 2023.

### Effectifs des professions de santé

[![Aperçu illustré des effectifs et modes d’exercice des médecins en Île-de-France en 2023](docs/filtre-professions-ameli.png)](docs/filtre-professions-ameli.png)

Illustration des données consultables après la sélection d’une région : profession, effectif et mode d’exercice libéral. Ce visuel reprend les résultats de l’extrait SQLite ; il s’agit d’une présentation illustrée, et non d’une capture de l’interface.

## Lancer la démonstration en local

Préparer **Python 3.12**, version utilisée pour vérifier le projet. Télécharger ou cloner le dépôt, puis ouvrir un terminal à sa racine, dans le dossier `site-amelie`.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m flask --app app run
```

### macOS ou Linux

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m flask --app app run
```

Ouvrir [localhost:5000](http://127.0.0.1:5000). Aucun compte n’est nécessaire. Le site utilise SQLite et ne nécessite pas de serveur de base de données.

La démonstration démarre avec `demo/amelie-demo.sqlite`, un **extrait des données réelles agrégées** : prescriptions de 2022 et 2023, effectifs de 2023 pour quatre régions et agrégats nationaux nécessaires au graphique par poste. Le script `demo/creer_extrait.py` sert à reconstruire cet extrait à partir de la base complète ; il n’est pas nécessaire au lancement.

## Fonctionnalités

- **Professions de santé** : choisir une région sur la carte, puis cocher ou décocher les professions à afficher. Le tableau présente les effectifs et les modes d’exercice pour la dernière année disponible. Dans la démonstration, un message indique les régions absentes de l’extrait.
- **Prescriptions par région** : sélectionner une année et comparer les montants totaux régionaux pour l’ensemble des médecins.
- **Montants moyens par poste** : consulter un graphique national par catégorie de prescription pour l’année choisie.
- **Aperçu des prescriptions** : rechercher dans un tableau limité à 200 lignes au maximum. Cette limite concerne l’aperçu ; les graphiques interrogent les agrégats de la base.

## Utiliser la base complète

Arrêter le serveur avec `Ctrl+C`, puis préparer les données et relancer le site.

### Windows PowerShell

```powershell
.\.venv\Scripts\python.exe prepare_data.py
.\.venv\Scripts\python.exe -m flask --app app run
```

### macOS ou Linux

Avec l’environnement virtuel activé :

```sh
python prepare_data.py
python -m flask --app app run
```

Le script extrait la base de `site-amelie.zip` vers `model/data/debase_db.sqllite3` (environ 278 Mo). Au redémarrage, le site utilise ce fichier en priorité. Les prescriptions couvrent alors **2010 à 2023**, avec **18 régions** dans le graphique régional de 2023. Les effectifs affichés restent ceux de la dernière année disponible.

## Organisation du code

Flask reçoit les demandes de l’utilisateur, pandas prépare les résultats des requêtes SQLite et Matplotlib produit les graphiques. Les pages utilisent HTML, CSS et JavaScript.

- `app.py` : routes, formulaires et transmission des résultats aux pages.
- `model/db.py` : connexion SQLite et requêtes sur les effectifs et les prescriptions.
- `utils/graphiques.py` : génération des graphiques.
- `templates/` et `static/` : pages, carte et interactions de l’interface.
- `demo/` : extrait SQLite et script de reconstruction.
- `prepare_data.py` : extraction de la base complète fournie dans l’archive.

Pour la conception et l’exploration SQL, consulter le [dépôt consacré à la base de données](https://github.com/Kajan94/database-amelie).

## Données

Les graphiques régionaux utilisent le poste **total**, l’agrégat **Ensemble des médecins** et le code départemental **999**. Les résultats nationaux utilisent le code région **99**. Ces sélections permettent de comparer un même périmètre sans additionner les totaux nationaux, régionaux et départementaux.

Données agrégées de la Cnam, sous [Open Database License 1.0](https://opendatacommons.org/licenses/odbl/1-0/). [Prescriptions](https://data.ameli.fr/explore/assets/prescriptions/) · [Effectifs par mode d’exercice](https://data.ameli.fr/explore/dataset/demographie-exercices-liberaux/) · [Conditions de réutilisation](https://data.ameli.fr/terms/terms-and-conditions/)

[Projet dans le portfolio](https://kajan94.github.io/Portefolio/#ameli)

## Travail en équipe

Projet universitaire réalisé en groupe en BUT Informatique à l’IUT de Créteil-Vitry (UPEC). Le travail a porté sur l’interrogation des données de santé et leur restitution dans une application web avec une carte, des tableaux et des graphiques.
