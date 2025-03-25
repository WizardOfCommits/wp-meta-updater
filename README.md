# WP Meta Updater

Une application Python avec interface graphique pour mettre à jour les meta title et description de votre site WordPress via l'API REST.

## Fonctionnalités

- Interface graphique utilisateur moderne et intuitive avec PyQt6
- Connexion via l'API REST de WordPress avec authentification par jeton
- Importation des meta title et description actuelles du site pour tous types de contenus (articles, pages, produits, etc.)
- Exportation et importation au format CSV
- Mise à jour en un clic - mettez à jour tout ou seulement les éléments sélectionnés
- Planification des mises à jour - programmez des mises à jour ponctuelles ou récurrentes
- Analyse SEO basique - identifiez les titres et descriptions trop courts ou trop longs
- Support multi-sites - gérez plusieurs sites WordPress
- Mode hors ligne - travaillez sur les données en local et synchronisez ultérieurement

## Captures d'écran

*Des captures d'écran seront ajoutées ici*

## Prérequis

- Python 3.8 ou supérieur
- PyQt6
- Requests
- Pandas
- Python-dateutil

## Installation

### Installation des dépendances

```bash
pip install -r requirements.txt
```

### Lancement de l'application

```bash
python wp_meta_updater.py
```

## Configuration

### Obtention d'un jeton d'authentification WordPress

Pour utiliser cette application, vous devez générer un jeton d'authentification pour l'API REST de WordPress :

1. Installez le plugin [Application Passwords](https://wordpress.org/plugins/application-passwords/) sur votre site WordPress
2. Dans votre tableau de bord WordPress, allez dans Utilisateurs > Votre profil
3. Faites défiler jusqu'à la section "Mots de passe d'application"
4. Créez un nouveau mot de passe d'application nommé "WP Meta Updater"
5. Copiez le jeton généré et utilisez-le dans l'application

## Utilisation

### Connexion à WordPress

1. Lancez l'application
2. Dans l'onglet "Connexion", entrez l'URL de votre site WordPress et votre jeton d'authentification
3. Cliquez sur "Tester la connexion" pour vérifier que tout fonctionne correctement

### Importation des métadonnées

1. Une fois connecté, cliquez sur "Importer depuis WordPress" pour récupérer toutes les métadonnées SEO
2. L'application récupérera automatiquement tous les types de contenu disponibles (articles, pages, produits, etc.)

### Modification des métadonnées

1. Dans l'onglet "Métadonnées", vous pouvez filtrer et rechercher des éléments spécifiques
2. Double-cliquez sur un élément pour modifier ses métadonnées SEO
3. Les éléments modifiés sont mis en évidence en jaune

### Mise à jour des métadonnées

1. Sélectionnez les éléments que vous souhaitez mettre à jour
2. Cliquez sur "Mettre à jour les sélectionnés" ou "Mettre à jour tous les modifiés"
3. Confirmez la mise à jour

### Exportation et importation CSV

1. Pour exporter les métadonnées, cliquez sur "Exporter en CSV"
2. Pour importer des métadonnées depuis un fichier CSV, cliquez sur "Importer depuis CSV"

### Planification des mises à jour

1. Dans l'onglet "Planification", cliquez sur "Planifier une mise à jour"
2. Configurez la date, l'heure et les options de récurrence
3. Sélectionnez les éléments à mettre à jour
4. Cliquez sur "OK" pour planifier la mise à jour

## Développement

### Structure du projet

```
wp-update/
├── main.py                  # Point d'entrée principal
├── wp_meta_updater.py       # Script de lancement
├── wp_connector.py          # Module de connexion à l'API WordPress
├── data_manager.py          # Module de gestion des données
├── update_manager.py        # Module de gestion des mises à jour
├── requirements.txt         # Dépendances Python
├── README.md                # Documentation
├── ui/                      # Modules d'interface utilisateur
│   ├── main_window.py       # Fenêtre principale
│   ├── connection_widget.py # Widget de connexion
│   ├── metadata_widget.py   # Widget de gestion des métadonnées
│   ├── schedule_widget.py   # Widget de planification
│   ├── settings_widget.py   # Widget de paramètres
│   └── about_dialog.py      # Boîte de dialogue À propos
├── logs/                    # Journaux d'application
└── data/                    # Données de l'application
```

## Licence

Copyright © 2025 - Tous droits réservés

## Auteur

William Troillard

## Remerciements

- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - Interface graphique
- [WordPress REST API](https://developer.wordpress.org/rest-api/) - API REST de WordPress
- [Requests](https://requests.readthedocs.io/) - Bibliothèque HTTP pour Python
- [Pandas](https://pandas.pydata.org/) - Analyse et manipulation de données
