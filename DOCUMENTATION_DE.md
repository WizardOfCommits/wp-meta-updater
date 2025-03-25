# WP Meta Updater - Offizielle Dokumentation

## Einführung

WP Meta Updater ist eine umfassende Anwendung zur Verwaltung und Aktualisierung von SEO-Metadaten (Meta-Titel und Meta-Beschreibung) Ihrer WordPress-Website. Diese Tool ist sowohl in einer grafischen Version (GUI) als auch in einer Kommandozeilenversion (CLI) verfügbar und ermöglicht Ihnen, das SEO Ihrer WordPress-Inhalte effizient zu optimieren.

![WP Meta Updater Logo](ui/logo-wp-updater.png)

## Inhaltsverzeichnis

- [Einführung](#einführung)
- [Hauptfunktionen](#hauptfunktionen)
- [Verfügbare Versionen](#verfügbare-versionen)
  - [GUI-Version](#gui-version)
  - [CLI-Version](#cli-version)
- [Voraussetzungen und Installation](#voraussetzungen-und-installation)
  - [Systemkonfiguration](#systemkonfiguration)
  - [Installation der Abhängigkeiten](#installation-der-abhängigkeiten)
  - [Erstellung der ausführbaren Datei](#erstellung-der-ausführbaren-datei)
- [Konfiguration](#konfiguration)
  - [WordPress-Authentifizierung](#wordpress-authentifizierung)
  - [REST-API-Verbindung](#rest-api-verbindung)
  - [Direkte MySQL-Verbindung](#direkte-mysql-verbindung)
- [Verwendung](#verwendung)
  - [Grafische Benutzeroberfläche](#grafische-benutzeroberfläche)
  - [Kommandozeile](#kommandozeile)
  - [CSV-Dateiformat](#csv-dateiformat)
- [Erweiterte Funktionen](#erweiterte-funktionen)
  - [Optimierter CSV-Import](#optimierter-csv-import)
  - [Direkte MySQL-Verbindung](#direkte-mysql-verbindung-1)
  - [Batch-Updates](#batch-updates)
  - [Update-Planung](#update-planung)
- [Rank Math SEO-Erweiterung](#rank-math-seo-erweiterung)
  - [Installation und Konfiguration](#installation-und-konfiguration)
  - [Verwendung mit WordPress Meta Updater](#verwendung-mit-wordpress-meta-updater)
- [Fehlerbehebung](#fehlerbehebung)
  - [Authentifizierungsprobleme](#authentifizierungsprobleme)
  - [CSV-Importprobleme](#csv-importprobleme)
  - [Update-Probleme](#update-probleme)
  - [Probleme mit Skripten](#probleme-mit-skripten)
- [Entwicklung](#entwicklung)
  - [Projektstruktur](#projektstruktur)
  - [Tests](#tests)
- [Lizenz und Credits](#lizenz-und-credits)

## Hauptfunktionen

- **Moderne grafische Benutzeroberfläche**: Intuitive Benutzeroberfläche basierend auf PyQt6
- **Leistungsstarke CLI-Version**: Aufgabenautomatisierung über die Kommandozeile
- **REST-API-Verbindung**: Sichere Kommunikation mit WordPress über die REST-API
- **Direkte MySQL-Verbindung**: Option zur direkten Aktualisierung der Datenbank
- **CSV-Import/Export**: Metadatenverwaltung über CSV-Dateien
- **Massenaktualisierungen**: Optimierte Verarbeitung für umfangreiche Updates
- **Planung**: Programmierung von einmaligen oder wiederkehrenden Updates
- **SEO-Analyse**: Identifizierung nicht optimierter Titel und Beschreibungen
- **Multi-Site-Unterstützung**: Verwaltung mehrerer WordPress-Websites
- **Offline-Modus**: Arbeit mit lokalen Daten mit späterer Synchronisierung
- **Multi-Plugin-SEO-Unterstützung**: Kompatibel mit Yoast SEO, Rank Math, All in One SEO, SEOPress

## Verfügbare Versionen

### GUI-Version

Die Version mit grafischer Benutzeroberfläche bietet eine vollständige und intuitive Benutzererfahrung.

#### GUI-spezifische Funktionen

- Moderne Oberfläche mit automatischem Hell-/Dunkel-Thema
- Filterbare und sortierbare Datentabellen
- Direkte Metadatenbearbeitung
- Visualisierung von SEO-Statistiken
- Assistent für Update-Planung
- Verwaltung von Verbindungsprofilen

#### Starten der GUI-Anwendung

```bash
python wp_meta_updater.py
```

### CLI-Version

Die Kommandozeilenversion ist ideal für Automatisierung und Skripte.

#### CLI-spezifische Funktionen

- Schneller Export von SEO-Metadaten
- Import und Update aus CSV
- Erstellung detaillierter Berichte
- Parallele Verarbeitung für optimale Leistung
- Einfach in Automatisierungsskripte integrierbar

#### Verwendung der CLI-Version

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

## Voraussetzungen und Installation

### Systemkonfiguration

- **Betriebssystem**: Windows, macOS oder Linux
- **Python**: Version 3.8 oder höher
- **Festplattenspeicher**: Mindestens 100 MB
- **Arbeitsspeicher**: Mindestens 512 MB RAM (1 GB empfohlen für große Websites)

### Installation der Abhängigkeiten

1. Klonen oder laden Sie das Repository herunter
2. Installieren Sie die erforderlichen Abhängigkeiten:

```bash
pip install -r requirements.txt
```

**Hauptabhängigkeiten**:
- PyQt6 (nur für die GUI-Version)
- requests
- pandas
- python-dateutil
- darkdetect (nur für die GUI-Version)
- mysql-connector-python (optional, für direkte MySQL-Verbindung)

### Erstellung der ausführbaren Datei

Um eine eigenständige ausführbare Datei zu erstellen (die kein Python erfordert):

```bash
python build_exe.py
```

Die ausführbare Datei wird im Ordner `build/wp_meta_updater/` erstellt.

## Konfiguration

### WordPress-Authentifizierung

Um WP Meta Updater zu verwenden, müssen Sie ein Authentifizierungstoken generieren:

1. Installieren Sie das Plugin [Application Passwords](https://wordpress.org/plugins/application-passwords/) auf Ihrer WordPress-Website
2. Gehen Sie in Ihrem WordPress-Dashboard zu Benutzer > Ihr Profil
3. Scrollen Sie zum Abschnitt "Anwendungspasswörter"
4. Erstellen Sie ein neues Anwendungspasswort mit dem Namen "WP Meta Updater"
5. Kopieren Sie das generierte Token zur Verwendung in der Anwendung

### REST-API-Verbindung

#### In der grafischen Benutzeroberfläche

1. Starten Sie die Anwendung
2. Geben Sie auf der Registerkarte "Verbindung" Folgendes ein:
   - URL Ihrer WordPress-Website (mit https://)
   - Authentifizierungstoken
3. Klicken Sie auf "Verbindung testen"
4. Speichern Sie das Verbindungsprofil, wenn gewünscht

#### In der Kommandozeile

Geben Sie URL und Token im Befehl an:

```bash
python wp_meta_cli.py export --url https://ihre-website.com --token "Ihr Token" --output export.csv
```

### Direkte MySQL-Verbindung

Um die direkte Verbindung zur MySQL-Datenbank zu verwenden (schneller für große Updates):

#### MySQL-Voraussetzungen

- Python-Modul `mysql-connector-python` installiert
- Zugriff auf die MySQL-Datenbank der WordPress-Website
- Ausreichende Berechtigungen zum Ändern der Metadatentabellen

#### Konfiguration in der grafischen Benutzeroberfläche

1. Gehen Sie zur Registerkarte "MySQL-Verbindung"
2. Wenn das MySQL-Modul nicht installiert ist, klicken Sie auf "MySQL-Modul installieren"
3. Konfigurieren Sie die Parameter:
   - Host (z.B. localhost)
   - Benutzer
   - Passwort
   - Datenbankname
   - Tabellenpräfix (Standard: wp_)
4. Klicken Sie auf "Verbindung testen"

#### Konfiguration in der Kommandozeile

```bash
python wp_meta_cli.py import --url https://ihre-website.com --token "Ihr Token" --input daten.csv --update --method mysql --db-host localhost --db-user benutzer --db-password passwort --db-name wordpress --db-prefix wp_
```

## Verwendung

### Grafische Benutzeroberfläche

#### Metadaten importieren

1. Nach der Verbindung klicken Sie auf "Von WordPress importieren"
2. Die Anwendung ruft alle verfügbaren Inhaltstypen ab
3. Die Metadaten werden in der Haupttabelle angezeigt

#### Metadaten ändern

1. Auf der Registerkarte "Metadaten" können Sie Elemente filtern und suchen
2. Doppelklicken Sie auf ein Element, um seine SEO-Metadaten zu bearbeiten
3. Geänderte Elemente werden gelb hervorgehoben

#### Metadaten aktualisieren

1. Wählen Sie die zu aktualisierenden Elemente aus
2. Klicken Sie auf "Ausgewählte aktualisieren" oder "Alle geänderten aktualisieren"
3. Wählen Sie die Aktualisierungsmethode (REST-API oder MySQL)
4. Bestätigen Sie die Aktualisierung

#### CSV-Export und -Import

1. Zum Exportieren klicken Sie auf "Als CSV exportieren"
2. Zum Importieren klicken Sie auf "Aus CSV importieren"
3. Wählen Sie die CSV-Datei aus (UTF-8-kodiert mit BOM)

### Kommandozeile

#### Verfügbare Inhaltstypen auflisten

```bash
python wp_meta_cli.py list-types --url https://ihre-website.com --token "Ihr Token"
```

#### SEO-Metadaten nach CSV exportieren

Für alle Inhaltstypen:

```bash
python wp_meta_cli.py export --url https://ihre-website.com --token "Ihr Token" --output export.csv
```

Für einen bestimmten Typ:

```bash
python wp_meta_cli.py export --url https://ihre-website.com --token "Ihr Token" --output artikel.csv --type post
```

#### Aus CSV importieren und aktualisieren

Import ohne Aktualisierung (Überprüfung):

```bash
python wp_meta_cli.py import --url https://ihre-website.com --token "Ihr Token" --input import.csv
```

Import und Aktualisierung:

```bash
python wp_meta_cli.py import --url https://ihre-website.com --token "Ihr Token" --input import.csv --update
```

Verwendung der direkten MySQL-Verbindung:

```bash
python wp_meta_cli.py import --url https://ihre-website.com --token "Ihr Token" --input import.csv --update --method mysql --db-host localhost --db-user benutzer --db-password passwort --db-name wordpress --db-prefix wp_
```

### CSV-Dateiformat

Die CSV-Datei muss mindestens die folgenden Spalten enthalten:

- `id`: WordPress-Element-ID
- `type`: Inhaltstyp (post, page, etc.)
- `seo_title`: Zu aktualisierender SEO-Titel
- `seo_description`: Zu aktualisierende SEO-Beschreibung

Beispiel für eine CSV-Datei:

```csv
"id","type","title","url","seo_title","seo_description"
"1","post","Mein erster Artikel","https://ihre-website.com/mein-erster-artikel","Neuer SEO-Titel","Neue SEO-Beschreibung"
"2","page","Über uns","https://ihre-website.com/ueber-uns","Über unser Unternehmen","Entdecken Sie unsere Geschichte und Mission"
```

## Erweiterte Funktionen

### Optimierter CSV-Import

Die Anwendung verwendet eine optimierte CSV-Importmethode, um große Dateien effizient zu verarbeiten:

- **Batch-Verarbeitung**: Laden in Batches zur Reduzierung der Speichernutzung
- **Adaptive Batch-Größe**: Automatische Anpassung basierend auf der Dateigröße
- **Reaktionsfähige Oberfläche**: Verarbeitung von UI-Ereignissen während des Imports
- **Intelligente Trennzeichenerkennung**: Unterstützung für Komma, Semikolon, Tabulator
- **Robuste Fehlerbehandlung**: Fortsetzung der Verarbeitung trotz einzelner Fehler

### Direkte MySQL-Verbindung

Die direkte MySQL-Verbindung bietet mehrere Vorteile:

- **Leistung**: Schnellere Updates als mit der REST-API
- **Umgehung von API-Einschränkungen**: Funktioniert auch, wenn die REST-API eingeschränkt ist
- **Effizienz für Massenaktualisierungen**: Ideal für große Websites

**Wichtiger Hinweis**: Die direkte MySQL-Verbindung umgeht WordPress-Hooks und -Filter. Verwenden Sie sie mit Vorsicht und stellen Sie sicher, dass Sie ein Backup Ihrer Datenbank haben.

### Batch-Updates

Um Probleme bei Massenaktualisierungen zu vermeiden, verwendet die Anwendung ein Batch-Verarbeitungssystem:

- **Batch-Verarbeitung**: Elemente werden in Batches von 20 Elementen verarbeitet (konfigurierbar)
- **Verzögerung zwischen Batches**: Standardmäßig 200ms, um den Server nicht zu überlasten
- **Optimierte Speicherverwaltung**: Periodische Ausführung des Garbage Collectors
- **Wiederholungsmechanismus**: Bis zu 2 zusätzliche Versuche im Fehlerfall
- **Detaillierte Protokollierung**: Präzise Verfolgung der Batch-Verarbeitung

Diese Parameter sind in der Klasse `WordPressConnector` konfigurierbar:

```python
# Batch-Verarbeitungsparameter für Massenaktualisierungen
BATCH_SIZE = 20       # Anzahl der Elemente pro Batch
BATCH_DELAY_MS = 200  # Verzögerung zwischen Batches in Millisekunden
MAX_RETRIES = 2       # Maximale Anzahl von Wiederholungsversuchen im Fehlerfall
GC_FREQUENCY = 5      # Häufigkeit der Ausführung des Garbage Collectors (alle X Batches)
```

### Update-Planung

Die grafische Benutzeroberfläche ermöglicht die Planung automatischer Updates:

1. Klicken Sie auf der Registerkarte "Planung" auf "Update planen"
2. Konfigurieren Sie Datum, Uhrzeit und Wiederholungsoptionen
3. Wählen Sie die zu aktualisierenden Elemente aus
4. Klicken Sie auf "OK", um das Update zu planen

Geplante Updates werden auch ausgeführt, wenn die Anwendung geschlossen ist (wenn die Option aktiviert ist).

## Rank Math SEO-Erweiterung

WP Meta Updater ist kompatibel mit der Rank Math SEO API-Erweiterung, die es ermöglicht, Rank Math-Metadaten in der WordPress REST-API verfügbar zu machen.

### Installation und Konfiguration

1. Laden Sie den Ordner `rank-math-seo-api-extension` herunter
2. Laden Sie ihn in das Verzeichnis `/wp-content/plugins/` Ihrer WordPress-Website hoch
3. Aktivieren Sie das Plugin über das Menü "Plugins" in der WordPress-Administration
4. Gehen Sie zu "Einstellungen > Rank Math SEO API" in der WordPress-Administration
5. Aktivieren Sie das Kontrollkästchen "Rank Math SEO in REST-API aktivieren"
6. Klicken Sie auf "Änderungen speichern"

### Verwendung mit WP Meta Updater

Sobald die Erweiterung aktiviert ist, kann WP Meta Updater automatisch:

1. Rank Math SEO-Felder erkennen (`rank_math_title` und `rank_math_description`)
2. Diese Metadaten von WordPress importieren
3. Sie über die Benutzeroberfläche oder CSV-Dateien ändern
4. Sie auf Ihrer WordPress-Website aktualisieren

Um die Erweiterung zu testen:

```bash
python test_rank_math_seo.py --url https://ihre-website.com --token "Ihr Token"
```

## Fehlerbehebung

### Authentifizierungsprobleme

Wenn Sie auf Authentifizierungsprobleme stoßen:

1. Überprüfen Sie, ob das Token korrekt eingegeben wurde (mit Leerzeichen)
2. Stellen Sie sicher, dass das Plugin Application Passwords aktiviert ist
3. Überprüfen Sie, ob der Benutzer ausreichende Rechte hat
4. Testen Sie die API direkt mit einem Tool wie Postman oder cURL

### CSV-Importprobleme

Wenn der CSV-Import fehlschlägt:

1. Überprüfen Sie, ob die Datei in UTF-8 mit BOM kodiert ist
2. Stellen Sie sicher, dass die erforderlichen Spalten vorhanden sind
3. Überprüfen Sie, ob die IDs existierenden Elementen entsprechen
4. Versuchen Sie es mit einer kleineren Datei, um das Problem zu isolieren

### Update-Probleme

Wenn Updates fehlschlagen:

1. Überprüfen Sie die Protokolle im Ordner `logs/`
2. Versuchen Sie, die Anzahl der gleichzeitig aktualisierten Elemente zu reduzieren
3. Testen Sie mit der alternativen Methode (API, wenn Sie MySQL verwenden, oder umgekehrt)
4. Überprüfen Sie, ob der WordPress-Server nicht überlastet ist

### Probleme mit Skripten

#### In PowerShell

Wenn Sie einen Fehler wie "Der Begriff 'wp_meta_cli.bat' wird nicht erkannt..." erhalten, verwenden Sie die folgende Syntax:

```powershell
.\wp_meta_cli.bat [Befehl] [Argumente]
```

Das Präfix `.\` zeigt PowerShell an, dass sich das Skript im aktuellen Verzeichnis befindet.

#### Tokens mit Leerzeichen

Wenn Ihr Authentifizierungstoken Leerzeichen enthält, müssen Sie es in Anführungszeichen setzen:

```bash
# Falsch (wenn das Token Leerzeichen enthält)
python wp_meta_cli.py export --url https://ihre-website.com --token kFIT w6HU P3vf vmC2 AIxh WqWz --output export.csv

# Richtig
python wp_meta_cli.py export --url https://ihre-website.com --token "kFIT w6HU P3vf vmC2 AIxh WqWz" --output export.csv
```

## Entwicklung

### Projektstruktur

```
wp-update/
├── main.py                  # Haupteinstiegspunkt (GUI)
├── wp_meta_updater.py       # Startskript (GUI)
├── wp_meta_cli.py           # Kommandozeilenversion
├── wp_meta_cli.bat          # Batch-Skript für Windows
├── wp_meta_cli.sh           # Shell-Skript für Linux/macOS
├── wp_connector.py          # WordPress-API-Verbindungsmodul
├── wp_meta_direct_update.py # Direktes MySQL-Verbindungsmodul
├── data_manager.py          # Datenverwaltungsmodul
├── update_manager.py        # Update-Verwaltungsmodul
├── build_exe.py             # Skript zur Erstellung der ausführbaren Datei
├── requirements.txt         # Python-Abhängigkeiten
├── ui/                      # Benutzeroberflächen-Module (GUI)
│   ├── main_window.py       # Hauptfenster
│   ├── connection_widget.py # API-Verbindungs-Widget
│   ├── mysql_connection_widget.py # MySQL-Verbindungs-Widget
│   ├── metadata_widget.py   # Metadatenverwaltungs-Widget
│   ├── schedule_widget.py   # Planungs-Widget
│   ├── settings_widget.py   # Einstellungs-Widget
│   ├── about_dialog.py      # Über-Dialog
│   └── on_table_double_clicked.py # Ereignishandler
├── rank-math-seo-api-extension/ # WordPress-Erweiterung für Rank Math SEO
├── logs/                    # Anwendungsprotokolle
├── data/                    # Anwendungsdaten
└── build/                   # Build-Ordner für die ausführbare Datei
```

### Tests

Mehrere Testskripte sind verfügbar, um die ordnungsgemäße Funktion der Anwendung zu überprüfen:

- `test_wp_connector.py`: Testet die Verbindung zur WordPress-API
- `test_wp_post.py`: Testet die Aktualisierung von Metadaten über die API
- `test_wp_create.py`: Testet die Erstellung von Inhalten mit Metadaten
- `test_wp_permissions.py`: Überprüft die Benutzerberechtigungen
- `test_csv_import.py`: Testet den Import von CSV-Dateien
- `test_large_csv_import.py`: Testet den Import großer CSV-Dateien
- `test_batch_update.py`: Testet Batch-Updates
- `test_rank_math_seo.py`: Testet die Integration mit Rank Math SEO

Um einen Test auszuführen:

```bash
python test_wp_connector.py --url https://ihre-website.com --token "Ihr Token"
```

## Lizenz und Credits

### Lizenz

Copyright © 2025 - Alle Rechte vorbehalten

### Autor

William Troillard

### Danksagungen

- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - Grafische Benutzeroberfläche
- [WordPress REST API](https://developer.wordpress.org/rest-api/) - WordPress REST-API
- [Requests](https://requests.readthedocs.io/) - HTTP-Bibliothek für Python
- [Pandas](https://pandas.pydata.org/) - Datenanalyse und -manipulation
- [MySQL Connector/Python](https://dev.mysql.com/doc/connector-python/en/) - MySQL-Verbindung
