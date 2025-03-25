# WordPress Meta CLI

Minimale Kommandozeilenversion zum Exportieren und Importieren von WordPress SEO-Metadaten.

## Funktionen

- Export von SEO-Metadaten in CSV nach Inhaltstyp oder für alle Typen
- Import und Aktualisierung von SEO-Metadaten aus einer CSV-Datei
- Erstellung detaillierter Berichte in Protokollen
- Unterstützung verschiedener SEO-Plugins (Yoast SEO, Rank Math, All in One SEO, SEOPress)
- Parallele Verarbeitung für optimale Leistung

## Voraussetzungen

- Python 3.8 oder höher
- Erforderliche Python-Module:
  - requests
  - pandas
  - python-dateutil

## Installation

### Installation der Abhängigkeiten

```bash
pip install -r requirements.txt
```

## Verwendung

### Erhalt eines WordPress-Authentifizierungstokens

Um dieses Tool zu nutzen, müssen Sie ein Authentifizierungstoken für die WordPress REST API generieren:

1. Installieren Sie das [Application Passwords](https://wordpress.org/plugins/application-passwords/) Plugin auf Ihrer WordPress-Website
2. Gehen Sie in Ihrem WordPress-Dashboard zu Benutzer > Ihr Profil
3. Scrollen Sie nach unten zum Abschnitt "Anwendungspasswörter"
4. Erstellen Sie ein neues Anwendungspasswort mit dem Namen "WP Meta CLI"
5. Kopieren Sie das generierte Token und verwenden Sie es in den Befehlen

### Verwendung der Hilfsskripte

#### Windows (CMD)

```batch
wp_meta_cli.bat help
```

#### Windows (PowerShell)

In PowerShell müssen Sie den Skriptnamen mit `.\` präfixieren, um anzuzeigen, dass es sich im aktuellen Verzeichnis befindet:

```powershell
.\wp_meta_cli.bat help
```

#### Linux/macOS

```bash
chmod +x wp_meta_cli.sh
./wp_meta_cli.sh help
```

### Direkte Verwendung des Python-Skripts

Sie können das Python-Skript auch direkt verwenden:

```bash
python wp_meta_cli.py list-types --url https://ihre-website.com --token "ihr-token"
```

> **Wichtig**: Wenn Ihr Authentifizierungstoken Leerzeichen enthält, müssen Sie es mit doppelten Anführungszeichen umgeben, damit es als ein einzelnes Argument behandelt wird.

### Export von SEO-Metadaten in CSV

Um alle SEO-Metadaten in CSV zu exportieren:

```bash
# Windows (CMD)
wp_meta_cli.bat export https://ihre-website.com "ihr token mit leerzeichen" export.csv

# Windows (PowerShell)
.\wp_meta_cli.bat export https://ihre-website.com "ihr token mit leerzeichen" export.csv

# Linux/macOS
./wp_meta_cli.sh export https://ihre-website.com "ihr token mit leerzeichen" export.csv

# Direkt mit Python
python wp_meta_cli.py export --url https://ihre-website.com --token "ihr token mit leerzeichen" --output export.csv
```

Um nur einen bestimmten Inhaltstyp zu exportieren (zum Beispiel Beiträge):

```bash
# Windows (CMD)
wp_meta_cli.bat export https://ihre-website.com "ihr token mit leerzeichen" beitraege.csv post

# Windows (PowerShell)
.\wp_meta_cli.bat export https://ihre-website.com "ihr token mit leerzeichen" beitraege.csv post

# Linux/macOS
./wp_meta_cli.sh export https://ihre-website.com "ihr token mit leerzeichen" beitraege.csv post

# Direkt mit Python
python wp_meta_cli.py export --url https://ihre-website.com --token "ihr token mit leerzeichen" --output beitraege.csv --type post
```

### Import und Aktualisierung von SEO-Metadaten aus einer CSV-Datei

Um SEO-Metadaten aus einer CSV-Datei zu importieren, ohne sie in WordPress zu aktualisieren:

```bash
# Windows (CMD)
wp_meta_cli.bat import https://ihre-website.com "ihr token mit leerzeichen" import.csv

# Windows (PowerShell)
.\wp_meta_cli.bat import https://ihre-website.com "ihr token mit leerzeichen" import.csv

# Linux/macOS
./wp_meta_cli.sh import https://ihre-website.com "ihr token mit leerzeichen" import.csv

# Direkt mit Python
python wp_meta_cli.py import --url https://ihre-website.com --token "ihr token mit leerzeichen" --input import.csv
```

Um SEO-Metadaten zu importieren und in WordPress zu aktualisieren:

```bash
# Windows (CMD)
wp_meta_cli.bat import https://ihre-website.com "ihr token mit leerzeichen" import.csv update

# Windows (PowerShell)
.\wp_meta_cli.bat import https://ihre-website.com "ihr token mit leerzeichen" import.csv update

# Linux/macOS
./wp_meta_cli.sh import https://ihre-website.com "ihr token mit leerzeichen" import.csv update

# Direkt mit Python
python wp_meta_cli.py import --url https://ihre-website.com --token "ihr token mit leerzeichen" --input import.csv --update
```

## CSV-Dateiformat

Die CSV-Datei muss mindestens die folgenden Spalten enthalten:

- `id`: WordPress-Element-ID
- `type`: Inhaltstyp (post, page, etc.)
- `seo_title`: Zu aktualisierender SEO-Titel
- `seo_description`: Zu aktualisierende SEO-Beschreibung

Beispiel einer CSV-Datei:

```csv
"id","type","title","url","seo_title","seo_description"
"1","post","Mein erster Beitrag","https://ihre-website.com/mein-erster-beitrag","Neuer SEO-Titel","Neue SEO-Beschreibung"
"2","page","Über uns","https://ihre-website.com/ueber-uns","Über unser Unternehmen","Entdecken Sie unsere Geschichte und Mission"
```

## Protokolle und Berichte

Protokolle werden automatisch im Verzeichnis `logs` generiert:

- `cline.log`: Allgemeines Anwendungsprotokoll
- `update_YYYYMMDD_HHMMSS.json`: Detaillierter Bericht jeder Aktualisierung

Aktualisierungsberichte enthalten detaillierte Informationen über erfolgreich aktualisierte Elemente und eventuelle Fehler.

## Verwendungsbeispiele

### Typischer Arbeitsablauf

1. Exportieren Sie die aktuellen SEO-Metadaten:
   ```bash
   # Windows (PowerShell)
   .\wp_meta_cli.bat export https://ihre-website.com "ihr token mit leerzeichen" export.csv
   ```

2. Bearbeiten Sie die CSV-Datei mit einer Tabellenkalkulation (Excel, LibreOffice Calc, etc.)

3. Importieren und aktualisieren Sie die modifizierten Metadaten:
   ```bash
   # Windows (PowerShell)
   .\wp_meta_cli.bat import https://ihre-website.com "ihr token mit leerzeichen" export_modifiziert.csv update
   ```

### Automatisierung mit einem Batch-Skript

Sie können ein Batch-Skript erstellen, um Export und Import zu automatisieren:

```batch
@echo off
set SITE_URL=https://ihre-website.com
set TOKEN=ihr-token-ohne-leerzeichen
set EXPORT_FILE=export_%date:~-4,4%%date:~-7,2%%date:~-10,2%.csv
set IMPORT_FILE=import.csv

echo Exportiere SEO-Metadaten...
python wp_meta_cli.py export --url %SITE_URL% --token "%TOKEN%" --output %EXPORT_FILE%

echo Importiere und aktualisiere SEO-Metadaten...
python wp_meta_cli.py import --url %SITE_URL% --token "%TOKEN%" --input %IMPORT_FILE% --update

echo Fertig!
```

> **Hinweis**: In Batch-Skripten umgeben Sie die TOKEN-Variable mit Anführungszeichen ("%TOKEN%"), um Tokens mit Leerzeichen zu verarbeiten.

## Fehlerbehebung

### Probleme mit Authentifizierungstokens, die Leerzeichen enthalten

Wenn Ihr Authentifizierungstoken Leerzeichen enthält, müssen Sie es mit Anführungszeichen umgeben:

```bash
# Falsch (wenn das Token Leerzeichen enthält)
python wp_meta_cli.py export --url https://ihre-website.com --token kFIT w6HU P3vf vmC2 AIxh WqWz --output export.csv

# Richtig
python wp_meta_cli.py export --url https://ihre-website.com --token "kFIT w6HU P3vf vmC2 AIxh WqWz" --output export.csv
```

### Probleme bei der Skriptausführung

#### In PowerShell

Wenn Sie einen Fehler wie "Der Begriff 'wp_meta_cli.bat' wird nicht erkannt..." erhalten, verwenden Sie die folgende Syntax:

```powershell
.\wp_meta_cli.bat [Befehl] [Argumente]
```

Das Präfix `.\` teilt PowerShell mit, dass sich das Skript im aktuellen Verzeichnis befindet.

### Verbindungsprobleme

Wenn Sie Probleme bei der Verbindung zur WordPress-API haben, überprüfen Sie:

1. Dass die Website-URL korrekt ist und das Protokoll enthält (http:// oder https://)
2. Dass das Authentifizierungstoken gültig ist
3. Dass das Application Passwords Plugin korrekt installiert und aktiviert ist
4. Dass die WordPress REST API nicht durch eine Firewall oder ein Sicherheits-Plugin blockiert wird

### CSV-Importfehler

Wenn der CSV-Import fehlschlägt, überprüfen Sie:

1. Dass die CSV-Datei in UTF-8 mit BOM kodiert ist
2. Dass die erforderlichen Spalten (id, type) vorhanden sind
3. Dass die IDs mit existierenden Elementen auf der WordPress-Website übereinstimmen

## Lizenz

Copyright © 2025 - Alle Rechte vorbehalten

## Autor

William Troillard
