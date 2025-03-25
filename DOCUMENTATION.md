# WP Meta Updater - Documentation Officielle

## Introduction

WP Meta Updater est une application complète pour gérer et mettre à jour les métadonnées SEO (meta title et meta description) de votre site WordPress. Disponible en version graphique (GUI) et en ligne de commande (CLI), cet outil vous permet d'optimiser efficacement le référencement de votre contenu WordPress.

![Logo WP Meta Updater](ui/logo-wp-updater.png)

## Table des matières

- [Introduction](#introduction)
- [Fonctionnalités principales](#fonctionnalités-principales)
- [Versions disponibles](#versions-disponibles)
  - [Version GUI](#version-gui)
  - [Version CLI](#version-cli)
- [Prérequis et installation](#prérequis-et-installation)
  - [Configuration système](#configuration-système)
  - [Installation des dépendances](#installation-des-dépendances)
  - [Création de l'exécutable](#création-de-lexécutable)
- [Configuration](#configuration)
  - [Authentification WordPress](#authentification-wordpress)
  - [Connexion à l'API REST](#connexion-à-lapi-rest)
  - [Connexion directe MySQL](#connexion-directe-mysql)
- [Utilisation](#utilisation)
  - [Interface graphique](#interface-graphique)
  - [Ligne de commande](#ligne-de-commande)
  - [Format du fichier CSV](#format-du-fichier-csv)
- [Fonctionnalités avancées](#fonctionnalités-avancées)
  - [Importation CSV optimisée](#importation-csv-optimisée)
  - [Connexion directe MySQL](#connexion-directe-mysql-1)
  - [Mises à jour par lots](#mises-à-jour-par-lots)
  - [Planification des mises à jour](#planification-des-mises-à-jour)
- [Extension Rank Math SEO](#extension-rank-math-seo)
  - [Installation et configuration](#installation-et-configuration)
  - [Utilisation avec WordPress Meta Updater](#utilisation-avec-wordpress-meta-updater)
- [Dépannage](#dépannage)
  - [Problèmes d'authentification](#problèmes-dauthentification)
  - [Problèmes d'importation CSV](#problèmes-dimportation-csv)
  - [Problèmes de mise à jour](#problèmes-de-mise-à-jour)
  - [Problèmes avec les scripts](#problèmes-avec-les-scripts)
- [Développement](#développement)
  - [Structure du projet](#structure-du-projet)
  - [Tests](#tests)
- [Licence et crédits](#licence-et-crédits)

## Fonctionnalités principales

- **Interface graphique moderne** : Interface utilisateur intuitive basée sur PyQt6
- **Version CLI performante** : Automatisation des tâches via ligne de commande
- **Connexion API REST** : Communication sécurisée avec WordPress via l'API REST
- **Connexion directe MySQL** : Option pour mettre à jour directement la base de données
- **Importation/exportation CSV** : Gestion des métadonnées via fichiers CSV
- **Mises à jour en masse** : Traitement optimisé pour les mises à jour volumineuses
- **Planification** : Programmation de mises à jour ponctuelles ou récurrentes
- **Analyse SEO** : Identification des titres et descriptions non optimisés
- **Support multi-sites** : Gestion de plusieurs sites WordPress
- **Mode hors ligne** : Travail sur les données en local avec synchronisation ultérieure
- **Support multi-plugins SEO** : Compatible avec Yoast SEO, Rank Math, All in One SEO, SEOPress

## Versions disponibles

### Version GUI

La version avec interface graphique offre une expérience utilisateur complète et intuitive.

#### Fonctionnalités spécifiques à la GUI

- Interface moderne avec thème clair/sombre automatique
- Tableaux de données filtrables et triables
- Édition directe des métadonnées
- Visualisation des statistiques SEO
- Assistant de planification des mises à jour
- Gestion des profils de connexion

#### Lancement de l'application GUI

```bash
python wp_meta_updater.py
```

### Version CLI

La version en ligne de commande est idéale pour l'automatisation et les scripts.

#### Fonctionnalités spécifiques à la CLI

- Exportation rapide des métadonnées SEO
- Importation et mise à jour depuis CSV
- Génération de rapports détaillés
- Traitement en parallèle pour performances optimales
- Facilement intégrable dans des scripts d'automatisation

#### Utilisation de la version CLI

**Windows (CMD)**:
```batch
wp_meta_cli.bat help
```

**Windows (PowerShell)**:
```powershell
.\wp_meta_cli.bat help
```

**Linux/macOS**:
```bash
chmod +x wp_meta_cli.sh
./wp_meta_cli.sh help
```

## Prérequis et installation

### Configuration système

- **Système d'exploitation** : Windows, macOS ou Linux
- **Python** : Version 3.8 ou supérieure
- **Espace disque** : Minimum 100 MB
- **Mémoire** : Minimum 512 MB RAM (recommandé 1 GB pour les grands sites)

### Installation des dépendances

1. Clonez ou téléchargez le dépôt
2. Installez les dépendances requises :

```bash
pip install -r requirements.txt
```

**Dépendances principales** :
- PyQt6 (uniquement pour la version GUI)
- requests
- pandas
- python-dateutil
- darkdetect (uniquement pour la version GUI)
- mysql-connector-python (optionnel, pour la connexion directe MySQL)

### Création de l'exécutable

Pour créer un exécutable autonome (ne nécessitant pas Python) :

```bash
python build_exe.py
```

L'exécutable sera créé dans le dossier `build/wp_meta_updater/`.

## Configuration

### Authentification WordPress

Pour utiliser WP Meta Updater, vous devez générer un jeton d'authentification :

1. Installez le plugin [Application Passwords](https://wordpress.org/plugins/application-passwords/) sur votre site WordPress
2. Dans votre tableau de bord WordPress, allez dans Utilisateurs > Votre profil
3. Faites défiler jusqu'à la section "Mots de passe d'application"
4. Créez un nouveau mot de passe d'application nommé "WP Meta Updater"
5. Copiez le jeton généré pour l'utiliser dans l'application

### Connexion à l'API REST

#### Dans l'interface graphique

1. Lancez l'application
2. Dans l'onglet "Connexion", entrez :
   - URL de votre site WordPress (avec https://)
   - Jeton d'authentification
3. Cliquez sur "Tester la connexion"
4. Enregistrez le profil de connexion si vous le souhaitez

#### En ligne de commande

Spécifiez l'URL et le jeton dans la commande :

```bash
python wp_meta_cli.py export --url https://votre-site.com --token "votre jeton" --output export.csv
```

### Connexion directe MySQL

Pour utiliser la connexion directe à la base de données MySQL (plus rapide pour les grandes mises à jour) :

#### Prérequis MySQL

- Module Python `mysql-connector-python` installé
- Accès à la base de données MySQL du site WordPress
- Permissions suffisantes pour modifier les tables de métadonnées

#### Configuration dans l'interface graphique

1. Accédez à l'onglet "Connexion MySQL"
2. Si le module MySQL n'est pas installé, cliquez sur "Installer le module MySQL"
3. Configurez les paramètres :
   - Hôte (par exemple: localhost)
   - Utilisateur
   - Mot de passe
   - Nom de la base de données
   - Préfixe des tables (par défaut: wp_)
4. Cliquez sur "Tester la connexion"

#### Configuration en ligne de commande

```bash
python wp_meta_cli.py import --url https://votre-site.com --token "votre jeton" --input donnees.csv --update --method mysql --db-host localhost --db-user utilisateur --db-password motdepasse --db-name wordpress --db-prefix wp_
```

## Utilisation

### Interface graphique

#### Importation des métadonnées

1. Une fois connecté, cliquez sur "Importer depuis WordPress"
2. L'application récupérera tous les types de contenu disponibles
3. Les métadonnées s'afficheront dans le tableau principal

#### Modification des métadonnées

1. Dans l'onglet "Métadonnées", filtrez et recherchez des éléments
2. Double-cliquez sur un élément pour modifier ses métadonnées SEO
3. Les éléments modifiés sont mis en évidence en jaune

#### Mise à jour des métadonnées

1. Sélectionnez les éléments à mettre à jour
2. Cliquez sur "Mettre à jour les sélectionnés" ou "Mettre à jour tous les modifiés"
3. Choisissez la méthode de mise à jour (API REST ou MySQL)
4. Confirmez la mise à jour

#### Exportation et importation CSV

1. Pour exporter, cliquez sur "Exporter en CSV"
2. Pour importer, cliquez sur "Importer depuis CSV"
3. Sélectionnez le fichier CSV (encodé en UTF-8 avec BOM)

### Ligne de commande

#### Lister les types de contenu disponibles

```bash
python wp_meta_cli.py list-types --url https://votre-site.com --token "votre jeton"
```

#### Exporter les métadonnées SEO en CSV

Pour tous les types de contenu :

```bash
python wp_meta_cli.py export --url https://votre-site.com --token "votre jeton" --output export.csv
```

Pour un type spécifique :

```bash
python wp_meta_cli.py export --url https://votre-site.com --token "votre jeton" --output articles.csv --type post
```

#### Importer et mettre à jour depuis un CSV

Importer sans mettre à jour (vérification) :

```bash
python wp_meta_cli.py import --url https://votre-site.com --token "votre jeton" --input import.csv
```

Importer et mettre à jour :

```bash
python wp_meta_cli.py import --url https://votre-site.com --token "votre jeton" --input import.csv --update
```

Utiliser la connexion MySQL directe :

```bash
python wp_meta_cli.py import --url https://votre-site.com --token "votre jeton" --input import.csv --update --method mysql --db-host localhost --db-user utilisateur --db-password motdepasse --db-name wordpress --db-prefix wp_
```

### Format du fichier CSV

Le fichier CSV doit contenir au minimum les colonnes suivantes :

- `id` : ID de l'élément WordPress
- `type` : Type de contenu (post, page, etc.)
- `seo_title` : Titre SEO à mettre à jour
- `seo_description` : Description SEO à mettre à jour

Exemple de fichier CSV :

```csv
"id","type","title","url","seo_title","seo_description"
"1","post","Mon premier article","https://votre-site.com/mon-premier-article","Nouveau titre SEO","Nouvelle description SEO"
"2","page","À propos","https://votre-site.com/a-propos","À propos de notre entreprise","Découvrez notre histoire et notre mission"
```

## Fonctionnalités avancées

### Importation CSV optimisée

L'application utilise une méthode d'importation CSV optimisée pour gérer efficacement les fichiers volumineux :

- **Traitement par lots** : Chargement par lots pour réduire l'utilisation de la mémoire
- **Taille de lot adaptative** : Ajustement automatique selon la taille du fichier
- **Interface réactive** : Traitement des événements UI pendant l'importation
- **Détection intelligente du séparateur** : Support pour virgule, point-virgule, tabulation
- **Gestion robuste des erreurs** : Poursuite du traitement malgré les erreurs individuelles

### Connexion directe MySQL

La connexion directe MySQL offre plusieurs avantages :

- **Performance** : Mises à jour plus rapides qu'avec l'API REST
- **Contournement des limitations API** : Fonctionne même si l'API REST est limitée
- **Efficacité pour les mises à jour massives** : Idéal pour les grands sites

**Note importante** : La connexion directe MySQL contourne les hooks et filtres WordPress. Utilisez-la avec précaution et assurez-vous d'avoir une sauvegarde de votre base de données.

### Mises à jour par lots

Pour éviter les problèmes lors des mises à jour massives, l'application utilise un système de traitement par lots :

- **Traitement par lots** : Les éléments sont traités par lots de 20 items (configurable)
- **Délai entre les lots** : 200ms par défaut pour éviter de surcharger le serveur
- **Gestion optimisée de la mémoire** : Exécution périodique du garbage collector
- **Mécanisme de reprise** : Jusqu'à 2 tentatives supplémentaires en cas d'échec
- **Journalisation détaillée** : Suivi précis du traitement par lots

Ces paramètres sont configurables dans la classe `WordPressConnector` :

```python
# Paramètres de traitement par lots pour les mises à jour massives
BATCH_SIZE = 20       # Nombre d'éléments par lot
BATCH_DELAY_MS = 200  # Délai entre les lots en millisecondes
MAX_RETRIES = 2       # Nombre maximum de tentatives en cas d'échec
GC_FREQUENCY = 5      # Fréquence d'exécution du garbage collector (tous les X lots)
```

### Planification des mises à jour

L'interface graphique permet de planifier des mises à jour automatiques :

1. Dans l'onglet "Planification", cliquez sur "Planifier une mise à jour"
2. Configurez la date, l'heure et les options de récurrence
3. Sélectionnez les éléments à mettre à jour
4. Cliquez sur "OK" pour planifier la mise à jour

Les mises à jour planifiées s'exécuteront même si l'application est fermée (si l'option est activée).

## Extension Rank Math SEO

WP Meta Updater est compatible avec l'extension Rank Math SEO API qui permet d'exposer les métadonnées Rank Math dans l'API REST de WordPress.

### Installation et configuration

1. Téléchargez le dossier `rank-math-seo-api-extension`
2. Uploadez-le dans le répertoire `/wp-content/plugins/` de votre site WordPress
3. Activez le plugin depuis le menu "Extensions" dans l'administration WordPress
4. Accédez à "Réglages > API Rank Math SEO" dans l'administration WordPress
5. Cochez la case "Activer Rank Math SEO dans l'API REST"
6. Cliquez sur "Enregistrer les modifications"

### Utilisation avec WP Meta Updater

Une fois l'extension activée, WP Meta Updater pourra automatiquement :

1. Détecter les champs Rank Math SEO (`rank_math_title` et `rank_math_description`)
2. Importer ces métadonnées depuis WordPress
3. Les modifier via l'interface ou les fichiers CSV
4. Les mettre à jour sur votre site WordPress

Pour tester l'extension :

```bash
python test_rank_math_seo.py --url https://votre-site.com --token "votre jeton"
```

## Dépannage

### Problèmes d'authentification

Si vous rencontrez des problèmes d'authentification :

1. Vérifiez que le jeton est correctement entré (avec les espaces)
2. Assurez-vous que le plugin Application Passwords est activé
3. Vérifiez que l'utilisateur a les droits suffisants
4. Testez l'API directement avec un outil comme Postman ou cURL

### Problèmes d'importation CSV

Si l'importation CSV échoue :

1. Vérifiez que le fichier est encodé en UTF-8 avec BOM
2. Assurez-vous que les colonnes requises sont présentes
3. Vérifiez que les IDs correspondent à des éléments existants
4. Essayez avec un fichier plus petit pour isoler le problème

### Problèmes de mise à jour

Si les mises à jour échouent :

1. Vérifiez les logs dans le dossier `logs/`
2. Essayez de réduire le nombre d'éléments mis à jour simultanément
3. Testez avec la méthode alternative (API si vous utilisez MySQL ou vice versa)
4. Vérifiez que le serveur WordPress n'est pas surchargé

### Problèmes avec les scripts

#### Dans PowerShell

Si vous obtenez une erreur comme "Le terme 'wp_meta_cli.bat' n'est pas reconnu...", utilisez la syntaxe suivante :

```powershell
.\wp_meta_cli.bat [commande] [arguments]
```

Le préfixe `.\` indique à PowerShell que le script se trouve dans le répertoire courant.

#### Jetons avec espaces

Si votre jeton d'authentification contient des espaces, vous devez l'entourer de guillemets :

```bash
# Incorrect (si le jeton contient des espaces)
python wp_meta_cli.py export --url https://votre-site.com --token kFIT w6HU P3vf vmC2 AIxh WqWz --output export.csv

# Correct
python wp_meta_cli.py export --url https://votre-site.com --token "kFIT w6HU P3vf vmC2 AIxh WqWz" --output export.csv
```

## Développement

### Structure du projet

```
wp-update/
├── main.py                  # Point d'entrée principal (GUI)
├── wp_meta_updater.py       # Script de lancement (GUI)
├── wp_meta_cli.py           # Version ligne de commande
├── wp_meta_cli.bat          # Script batch pour Windows
├── wp_meta_cli.sh           # Script shell pour Linux/macOS
├── wp_connector.py          # Module de connexion à l'API WordPress
├── wp_meta_direct_update.py # Module de connexion directe MySQL
├── data_manager.py          # Module de gestion des données
├── update_manager.py        # Module de gestion des mises à jour
├── build_exe.py             # Script de création de l'exécutable
├── requirements.txt         # Dépendances Python
├── ui/                      # Modules d'interface utilisateur (GUI)
│   ├── main_window.py       # Fenêtre principale
│   ├── connection_widget.py # Widget de connexion API
│   ├── mysql_connection_widget.py # Widget de connexion MySQL
│   ├── metadata_widget.py   # Widget de gestion des métadonnées
│   ├── schedule_widget.py   # Widget de planification
│   ├── settings_widget.py   # Widget de paramètres
│   ├── about_dialog.py      # Boîte de dialogue À propos
│   └── on_table_double_clicked.py # Gestionnaire d'événements
├── rank-math-seo-api-extension/ # Extension WordPress pour Rank Math SEO
├── logs/                    # Journaux d'application
├── data/                    # Données de l'application
└── build/                   # Dossier de build pour l'exécutable
```

### Tests

Plusieurs scripts de test sont disponibles pour vérifier le bon fonctionnement de l'application :

- `test_wp_connector.py` : Teste la connexion à l'API WordPress
- `test_wp_post.py` : Teste la mise à jour des métadonnées via l'API
- `test_wp_create.py` : Teste la création de contenu avec métadonnées
- `test_wp_permissions.py` : Vérifie les permissions de l'utilisateur
- `test_csv_import.py` : Teste l'importation de fichiers CSV
- `test_large_csv_import.py` : Teste l'importation de grands fichiers CSV
- `test_batch_update.py` : Teste les mises à jour par lots
- `test_rank_math_seo.py` : Teste l'intégration avec Rank Math SEO

Pour exécuter un test :

```bash
python test_wp_connector.py --url https://votre-site.com --token "votre jeton"
```

## Licence et crédits

### Licence

Copyright © 2025 - Tous droits réservés

### Auteur

William Troillard

### Remerciements

- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - Interface graphique
- [WordPress REST API](https://developer.wordpress.org/rest-api/) - API REST de WordPress
- [Requests](https://requests.readthedocs.io/) - Bibliothèque HTTP pour Python
- [Pandas](https://pandas.pydata.org/) - Analyse et manipulation de données
- [MySQL Connector/Python](https://dev.mysql.com/doc/connector-python/en/) - Connexion MySQL
