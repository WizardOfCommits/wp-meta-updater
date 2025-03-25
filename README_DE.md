# WP Meta Updater

Eine Python-Anwendung mit grafischer Benutzeroberfläche zur Aktualisierung von Meta-Titel und -Beschreibung Ihrer WordPress-Website über die REST-API.

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

## Screenshots

*Screenshots werden hier hinzugefügt*

## Voraussetzungen

- Python 3.8 oder höher
- PyQt6
- Requests
- Pandas
- Python-dateutil

## Installation

### Installation der Abhängigkeiten

```bash
pip install -r requirements.txt
```

### Starten der Anwendung

```bash
python wp_meta_updater.py
```

## Konfiguration

### Erhalt eines WordPress-Authentifizierungstokens

Um diese Anwendung zu nutzen, müssen Sie ein Authentifizierungstoken für die WordPress REST API generieren:

1. Installieren Sie das [Application Passwords](https://wordpress.org/plugins/application-passwords/) Plugin auf Ihrer WordPress-Website
2. Gehen Sie in Ihrem WordPress-Dashboard zu Benutzer > Ihr Profil
3. Scrollen Sie nach unten zum Abschnitt "Anwendungspasswörter"
4. Erstellen Sie ein neues Anwendungspasswort mit dem Namen "WP Meta Updater"
5. Kopieren Sie das generierte Token und verwenden Sie es in der Anwendung

## Verwendung

### Verbindung zu WordPress

1. Starten Sie die Anwendung
2. Geben Sie im Tab "Verbindung" die URL Ihrer WordPress-Website und Ihr Authentifizierungstoken ein
3. Klicken Sie auf "Verbindung testen", um zu überprüfen, ob alles korrekt funktioniert

### Metadaten importieren

1. Sobald Sie verbunden sind, klicken Sie auf "Von WordPress importieren", um alle SEO-Metadaten abzurufen
2. Die Anwendung ruft automatisch alle verfügbaren Inhaltstypen ab (Beiträge, Seiten, Produkte usw.)

### Metadaten bearbeiten

1. Im Tab "Metadaten" können Sie nach bestimmten Elementen filtern und suchen
2. Doppelklicken Sie auf ein Element, um dessen SEO-Metadaten zu bearbeiten
3. Geänderte Elemente werden gelb hervorgehoben

### Metadaten aktualisieren

1. Wählen Sie die Elemente aus, die Sie aktualisieren möchten
2. Klicken Sie auf "Ausgewählte aktualisieren" oder "Alle geänderten aktualisieren"
3. Bestätigen Sie die Aktualisierung

### CSV-Export und -Import

1. Um Metadaten zu exportieren, klicken Sie auf "Als CSV exportieren"
2. Um Metadaten aus einer CSV-Datei zu importieren, klicken Sie auf "Aus CSV importieren"

### Updates planen

1. Klicken Sie im Tab "Planung" auf "Update planen"
2. Konfigurieren Sie Datum, Uhrzeit und Wiederholungsoptionen
3. Wählen Sie die zu aktualisierenden Elemente aus
4. Klicken Sie auf "OK", um das Update zu planen

## Projektstruktur

```
wp-update/
├── main.py                  # Haupteinstiegspunkt
├── wp_meta_updater.py       # Startskript
├── wp_connector.py          # WordPress-API-Verbindungsmodul
├── data_manager.py          # Datenverwaltungsmodul
├── update_manager.py        # Update-Verwaltungsmodul
├── requirements.txt         # Python-Abhängigkeiten
├── README.md                # Dokumentation
├── ui/                      # Benutzeroberflächen-Module
│   ├── main_window.py       # Hauptfenster
│   ├── connection_widget.py # Verbindungs-Widget
│   ├── metadata_widget.py   # Metadaten-Verwaltungs-Widget
│   ├── schedule_widget.py   # Planungs-Widget
│   ├── settings_widget.py   # Einstellungs-Widget
│   └── about_dialog.py      # Über-Dialog
├── logs/                    # Anwendungsprotokolle
└── data/                    # Anwendungsdaten
```

## Lizenz

Dieses Projekt ist unter der GNU General Public License v3.0 lizenziert - siehe die [LICENSE](LICENSE)-Datei für Details.

## Autor

William Troillard

## Danksagungen

- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - Grafische Benutzeroberfläche
- [WordPress REST API](https://developer.wordpress.org/rest-api/) - WordPress REST API
- [Requests](https://requests.readthedocs.io/) - HTTP-Bibliothek für Python
- [Pandas](https://pandas.pydata.org/) - Datenanalyse und -manipulation
