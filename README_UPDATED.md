# WP Meta Updater

Une application pour mettre à jour les meta title et description de votre site WordPress via l'API REST.

## Versions disponibles

Ce projet est disponible en deux versions :

1. **Version GUI** - Application graphique complète avec interface PyQt6
2. **Version CLI** - Version minimale en ligne de commande

## Version GUI

### Fonctionnalités

- Interface graphique utilisateur moderne et intuitive avec PyQt6
- Connexion via l'API REST de WordPress avec authentification par jeton
- Importation des meta title et description actuelles du site pour tous types de contenus (articles, pages, produits, etc.)
- Exportation et importation au format CSV
- Mise à jour en un clic - mettez à jour tout ou seulement les éléments sélectionnés
- Planification des mises à jour - programmez des mises à jour ponctuelles ou récurrentes
- Analyse SEO basique - identifiez les titres et descriptions trop courts ou trop longs
- Support multi-sites - gérez plusieurs sites WordPress
- Mode hors ligne - travaillez sur les données en local et synchronisez ultérieurement

### Lancement de l'application GUI

```bash
python wp_meta_updater.py
```

## Version CLI

### Fonctionnalités

- Exportation des métadonnées SEO en CSV par type de contenu ou pour tous les types
- Importation et mise à jour des métadonnées SEO depuis un fichier CSV
- Génération de rapports détaillés dans des logs
- Support de différents plugins SEO (Yoast SEO, Rank Math, All in One SEO, SEOPress)
- Traitement en parallèle pour des performances optimales

### Utilisation de la version CLI

#### Windows (CMD)

```batch
wp_meta_cli.bat help
```

#### Windows (PowerShell)

Dans PowerShell, vous devez préfixer le nom du script avec `.\` pour indiquer qu'il se trouve dans le répertoire courant :

```powershell
.\wp_meta_cli.bat help
```

#### Linux/macOS

```bash
chmod +x wp_meta_cli.sh
./wp_meta_cli.sh help
```

#### Exemples d'utilisation

> **Important** : Si votre jeton d'authentification contient des espaces, vous devez l'entourer de guillemets doubles pour qu'il soit traité comme un seul argument.

Exporter tous les contenus en CSV :

```bash
# Windows (CMD)
wp_meta_cli.bat export https://votre-site.com "votre jeton avec espaces" export.csv

# Windows (PowerShell)
.\wp_meta_cli.bat export https://votre-site.com "votre jeton avec espaces" export.csv

# Linux/macOS
./wp_meta_cli.sh export https://votre-site.com "votre jeton avec espaces" export.csv

# Directement avec Python
python wp_meta_cli.py export --url https://votre-site.com --token "votre jeton avec espaces" --output export.csv
```

Importer et mettre à jour depuis un CSV :

```bash
# Windows (CMD)
wp_meta_cli.bat import https://votre-site.com "votre jeton avec espaces" import.csv update

# Windows (PowerShell)
.\wp_meta_cli.bat import https://votre-site.com "votre jeton avec espaces" import.csv update

# Linux/macOS
./wp_meta_cli.sh import https://votre-site.com "votre jeton avec espaces" import.csv update

# Directement avec Python
python wp_meta_cli.py import --url https://votre-site.com --token "votre jeton avec espaces" --input import.csv --update
```

Pour plus de détails sur la version CLI, consultez le fichier [README_CLI.md](README_CLI.md).

## Prérequis

- Python 3.8 ou supérieur
- Modules Python requis :
  - PyQt6 (uniquement pour la version GUI)
  - requests
  - pandas
  - python-dateutil
  - darkdetect (uniquement pour la version GUI)

### Installation des dépendances

```bash
pip install -r requirements.txt
```

## Configuration

### Obtention d'un jeton d'authentification WordPress

Pour utiliser cette application, vous devez générer un jeton d'authentification pour l'API REST de WordPress :

1. Installez le plugin [Application Passwords](https://wordpress.org/plugins/application-passwords/) sur votre site WordPress
2. Dans votre tableau de bord WordPress, allez dans Utilisateurs > Votre profil
3. Faites défiler jusqu'à la section "Mots de passe d'application"
4. Créez un nouveau mot de passe d'application nommé "WP Meta Updater"
5. Copiez le jeton généré et utilisez-le dans l'application

## Structure du projet

```
wp-update/
├── main.py                  # Point d'entrée principal (GUI)
├── wp_meta_updater.py       # Script de lancement (GUI)
├── wp_meta_cli.py           # Version ligne de commande
├── wp_meta_cli.bat          # Script batch pour Windows
├── wp_meta_cli.sh           # Script shell pour Linux/macOS
├── wp_connector.py          # Module de connexion à l'API WordPress
├── data_manager.py          # Module de gestion des données
├── update_manager.py        # Module de gestion des mises à jour
├── requirements.txt         # Dépendances Python
├── README.md                # Documentation principale
├── README_CLI.md            # Documentation de la version CLI
├── ui/                      # Modules d'interface utilisateur (GUI)
│   ├── main_window.py       # Fenêtre principale
│   ├── connection_widget.py # Widget de connexion
│   ├── metadata_widget.py   # Widget de gestion des métadonnées
│   ├── schedule_widget.py   # Widget de planification
│   ├── settings_widget.py   # Widget de paramètres
│   └── about_dialog.py      # Boîte de dialogue À propos
├── logs/                    # Journaux d'application
└── data/                    # Données de l'application
```

## Dépannage

### Problèmes avec les jetons d'authentification contenant des espaces

Si votre jeton d'authentification contient des espaces, vous devez l'entourer de guillemets :

```bash
# Incorrect (si le jeton contient des espaces)
python wp_meta_cli.py export --url https://votre-site.com --token kFIT w6HU P3vf vmC2 AIxh WqWz --output export.csv

# Correct
python wp_meta_cli.py export --url https://votre-site.com --token "kFIT w6HU P3vf vmC2 AIxh WqWz" --output export.csv
```

### Problèmes d'exécution des scripts

#### Dans PowerShell

Si vous obtenez une erreur comme "Le terme 'wp_meta_cli.bat' n'est pas reconnu...", utilisez la syntaxe suivante :

```powershell
.\wp_meta_cli.bat [commande] [arguments]
```

Le préfixe `.\` indique à PowerShell que le script se trouve dans le répertoire courant.

## Licence

Copyright © 2025 - Tous droits réservés

## Auteur

William Troillard

## Remerciements

- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - Interface graphique
- [WordPress REST API](https://developer.wordpress.org/rest-api/) - API REST de WordPress
- [Requests](https://requests.readthedocs.io/) - Bibliothèque HTTP pour Python
- [Pandas](https://pandas.pydata.org/) - Analyse et manipulation de données
