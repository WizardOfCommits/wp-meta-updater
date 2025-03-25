# WordPress Meta CLI

Command line minimal version for exporting and importing WordPress SEO metadata.

## Features

- Export SEO metadata to CSV by content type or for all types
- Import and update SEO metadata from a CSV file
- Generate detailed reports in logs
- Support for different SEO plugins (Yoast SEO, Rank Math, All in One SEO, SEOPress)
- Parallel processing for optimal performance

## Prerequisites

- Python 3.8 or higher
- Required Python modules:
  - requests
  - pandas
  - python-dateutil

## Installation

### Installing dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Obtaining a WordPress authentication token

To use this tool, you need to generate an authentication token for the WordPress REST API:

1. Install the [Application Passwords](https://wordpress.org/plugins/application-passwords/) plugin on your WordPress site
2. In your WordPress dashboard, go to Users > Your Profile
3. Scroll down to the "Application Passwords" section
4. Create a new application password named "WP Meta CLI"
5. Copy the generated token and use it in the commands

### Using helper scripts

#### Windows (CMD)

```batch
wp_meta_cli.bat help
```

#### Windows (PowerShell)

In PowerShell, you need to prefix the script name with `.\` to indicate that it is in the current directory:

```powershell
.\wp_meta_cli.bat help
```

#### Linux/macOS

```bash
chmod +x wp_meta_cli.sh
./wp_meta_cli.sh help
```

### Direct use of the Python script

You can also use the Python script directly:

```bash
python wp_meta_cli.py list-types --url https://your-site.com --token "your-token"
```

> **Important**: If your authentication token contains spaces, you must surround it with double quotes so that it is treated as a single argument.

### Export SEO metadata to CSV

To export all SEO metadata to CSV:

```bash
# Windows (CMD)
wp_meta_cli.bat export https://your-site.com "your token with spaces" export.csv

# Windows (PowerShell)
.\wp_meta_cli.bat export https://your-site.com "your token with spaces" export.csv

# Linux/macOS
./wp_meta_cli.sh export https://your-site.com "your token with spaces" export.csv

# Directly with Python
python wp_meta_cli.py export --url https://your-site.com --token "your token with spaces" --output export.csv
```

To export only a specific content type (for example, posts):

```bash
# Windows (CMD)
wp_meta_cli.bat export https://your-site.com "your token with spaces" posts.csv post

# Windows (PowerShell)
.\wp_meta_cli.bat export https://your-site.com "your token with spaces" posts.csv post

# Linux/macOS
./wp_meta_cli.sh export https://your-site.com "your token with spaces" posts.csv post

# Directly with Python
python wp_meta_cli.py export --url https://your-site.com --token "your token with spaces" --output posts.csv --type post
```

### Import and update SEO metadata from a CSV

To import SEO metadata from a CSV file without updating WordPress:

```bash
# Windows (CMD)
wp_meta_cli.bat import https://your-site.com "your token with spaces" import.csv

# Windows (PowerShell)
.\wp_meta_cli.bat import https://your-site.com "your token with spaces" import.csv

# Linux/macOS
./wp_meta_cli.sh import https://your-site.com "your token with spaces" import.csv

# Directly with Python
python wp_meta_cli.py import --url https://your-site.com --token "your token with spaces" --input import.csv
```

To import and update SEO metadata on WordPress:

```bash
# Windows (CMD)
wp_meta_cli.bat import https://your-site.com "your token with spaces" import.csv update

# Windows (PowerShell)
.\wp_meta_cli.bat import https://your-site.com "your token with spaces" import.csv update

# Linux/macOS
./wp_meta_cli.sh import https://your-site.com "your token with spaces" import.csv update

# Directly with Python
python wp_meta_cli.py import --url https://your-site.com --token "your token with spaces" --input import.csv --update
```

## CSV file format

The CSV file must contain at minimum the following columns:

- `id`: WordPress item ID
- `type`: Content type (post, page, etc.)
- `seo_title`: SEO title to update
- `seo_description`: SEO description to update

Example CSV file:

```csv
"id","type","title","url","seo_title","seo_description"
"1","post","My first post","https://your-site.com/my-first-post","New SEO title","New SEO description"
"2","page","About","https://your-site.com/about","About our company","Discover our history and mission"
```

## Logs and reports

Logs are automatically generated in the `logs` directory:

- `cline.log`: General application log
- `update_YYYYMMDD_HHMMSS.json`: Detailed report of each update

Update reports contain detailed information about successfully updated items and any errors.

## Usage examples

### Typical workflow

1. Export current SEO metadata:
   ```bash
   # Windows (PowerShell)
   .\wp_meta_cli.bat export https://your-site.com "your token with spaces" export.csv
   ```

2. Edit the CSV file with a spreadsheet (Excel, LibreOffice Calc, etc.)

3. Import and update the modified metadata:
   ```bash
   # Windows (PowerShell)
   .\wp_meta_cli.bat import https://your-site.com "your token with spaces" export_modified.csv update
   ```

### Automation with a batch script

You can create a batch script to automate export and import:

```batch
@echo off
set SITE_URL=https://your-site.com
set TOKEN=your-token-without-spaces
set EXPORT_FILE=export_%date:~-4,4%%date:~-7,2%%date:~-10,2%.csv
set IMPORT_FILE=import.csv

echo Exporting SEO metadata...
python wp_meta_cli.py export --url %SITE_URL% --token "%TOKEN%" --output %EXPORT_FILE%

echo Importing and updating SEO metadata...
python wp_meta_cli.py import --url %SITE_URL% --token "%TOKEN%" --input %IMPORT_FILE% --update

echo Done!
```

> **Note**: In batch scripts, surround the TOKEN variable with quotes ("%TOKEN%") to handle tokens with spaces.

## Troubleshooting

### Problems with authentication tokens containing spaces

If your authentication token contains spaces, you must surround it with quotes:

```bash
# Incorrect (if the token contains spaces)
python wp_meta_cli.py export --url https://your-site.com --token kFIT w6HU P3vf vmC2 AIxh WqWz --output export.csv

# Correct
python wp_meta_cli.py export --url https://your-site.com --token "kFIT w6HU P3vf vmC2 AIxh WqWz" --output export.csv
```

### Script execution problems

#### In PowerShell

If you get an error like "The term 'wp_meta_cli.bat' is not recognized...", use the following syntax:

```powershell
.\wp_meta_cli.bat [command] [arguments]
```

The `.\` prefix tells PowerShell that the script is in the current directory.

### Connection problems

If you encounter problems connecting to the WordPress API, check:

1. That the site URL is correct and includes the protocol (http:// or https://)
2. That the authentication token is valid
3. That the Application Passwords plugin is correctly installed and activated
4. That the WordPress REST API is not blocked by a firewall or security plugin

### CSV import errors

If CSV import fails, check:

1. That the CSV file is encoded in UTF-8 with BOM
2. That the required columns (id, type) are present
3. That the IDs correspond to existing items on the WordPress site

## License

Copyright © 2025 - All rights reserved

## Author

William Troillard
