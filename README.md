# WP Meta Updater

A Python application with a graphical user interface to update meta title and description of your WordPress site via the REST API.

*Une application Python avec interface graphique pour mettre à jour les meta title et description de votre site WordPress via l'API REST.*

*Eine Python-Anwendung mit grafischer Benutzeroberfläche zur Aktualisierung von Meta-Titel und -Beschreibung Ihrer WordPress-Website über die REST-API.*

*Una aplicación Python con interfaz gráfica para actualizar el meta título y la descripción de su sitio WordPress a través de la API REST.*

## Features

- Modern and intuitive graphical user interface with PyQt6
- Connection via WordPress REST API with token authentication
- Import current meta title and description from the site for all content types (posts, pages, products, etc.)
- Export and import in CSV format
- One-click update - update all or only selected items
- Update scheduling - schedule one-time or recurring updates
- Basic SEO analysis - identify titles and descriptions that are too short or too long
- Multi-site support - manage multiple WordPress sites
- Offline mode - work on data locally and synchronize later

## Screenshots

*Screenshots will be added here*

## Prerequisites

- Python 3.8 or higher
- PyQt6
- Requests
- Pandas
- Python-dateutil

## Installation

### Installing dependencies

```bash
pip install -r requirements.txt
```

### Launching the application

```bash
python wp_meta_updater.py
```

## Configuration

### Obtaining a WordPress authentication token

To use this application, you need to generate an authentication token for the WordPress REST API:

1. Install the [Application Passwords](https://wordpress.org/plugins/application-passwords/) plugin on your WordPress site
2. In your WordPress dashboard, go to Users > Your Profile
3. Scroll down to the "Application Passwords" section
4. Create a new application password named "WP Meta Updater"
5. Copy the generated token and use it in the application

## Usage

### Connecting to WordPress

1. Launch the application
2. In the "Connection" tab, enter your WordPress site URL and authentication token
3. Click on "Test Connection" to verify that everything is working correctly

### Importing metadata

1. Once connected, click on "Import from WordPress" to retrieve all SEO metadata
2. The application will automatically retrieve all available content types (posts, pages, products, etc.)

### Editing metadata

1. In the "Metadata" tab, you can filter and search for specific items
2. Double-click on an item to edit its SEO metadata
3. Modified items are highlighted in yellow

### Updating metadata

1. Select the items you want to update
2. Click on "Update Selected" or "Update All Modified"
3. Confirm the update

### CSV export and import

1. To export metadata, click on "Export to CSV"
2. To import metadata from a CSV file, click on "Import from CSV"

### Scheduling updates

1. In the "Scheduling" tab, click on "Schedule an Update"
2. Configure the date, time, and recurrence options
3. Select the items to update
4. Click "OK" to schedule the update

## Development

### Project structure

```
wp-update/
├── main.py                  # Main entry point
├── wp_meta_updater.py       # Launch script
├── wp_connector.py          # WordPress API connection module
├── data_manager.py          # Data management module
├── update_manager.py        # Update management module
├── requirements.txt         # Python dependencies
├── README.md                # Documentation
├── ui/                      # User interface modules
│   ├── main_window.py       # Main window
│   ├── connection_widget.py # Connection widget
│   ├── metadata_widget.py   # Metadata management widget
│   ├── schedule_widget.py   # Scheduling widget
│   ├── settings_widget.py   # Settings widget
│   └── about_dialog.py      # About dialog box
├── logs/                    # Application logs
└── data/                    # Application data
```

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Author

William Troillard

## Acknowledgments

- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - Graphical user interface
- [WordPress REST API](https://developer.wordpress.org/rest-api/) - WordPress REST API
- [Requests](https://requests.readthedocs.io/) - HTTP library for Python
- [Pandas](https://pandas.pydata.org/) - Data analysis and manipulation

---

# Documentation en Français

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

## Licence

Ce projet est sous licence GNU General Public License v3.0 - voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

# Dokumentation auf Deutsch

## Funktionen

- Moderne und intuitive grafische Benutzeroberfläche mit PyQt6
- Verbindung über WordPress REST API mit Token-Authentifizierung
- Import aktueller Meta-Titel und -Beschreibungen von der Website für alle Inhaltstypen (Beiträge, Seiten, Produkte usw.)
- Export und Import im CSV-Format
- Ein-Klick-Update - Aktualisieren Sie alle oder nur ausgewählte Elemente
- Update-Planung - Planen Sie einmalige oder wiederkehrende Updates
- Grundlegende SEO-Analyse - Identifizieren Sie zu kurze oder zu lange Titel und Beschreibungen
- Multi-Site-Unterstützung - Verwalten Sie mehrere WordPress-Websites
- Offline-Modus - Arbeiten Sie lokal an Daten und synchronisieren Sie später

## Lizenz

Dieses Projekt ist unter der GNU General Public License v3.0 lizenziert - siehe die [LICENSE](LICENSE)-Datei für Details.

---

# Documentación en Español

## Características

- Interfaz gráfica de usuario moderna e intuitiva con PyQt6
- Conexión a través de la API REST de WordPress con autenticación por token
- Importación de meta títulos y descripciones actuales del sitio para todos los tipos de contenido (entradas, páginas, productos, etc.)
- Exportación e importación en formato CSV
- Actualización con un clic - actualice todo o solo los elementos seleccionados
- Programación de actualizaciones - programe actualizaciones únicas o recurrentes
- Análisis SEO básico - identifique títulos y descripciones demasiado cortos o largos
- Soporte multi-sitio - gestione múltiples sitios WordPress
- Modo sin conexión - trabaje con datos localmente y sincronice más tarde

## Licencia

Este proyecto está licenciado bajo la GNU General Public License v3.0 - consulte el archivo [LICENSE](LICENSE) para más detalles.
