# WP Meta Updater - Official Documentation

## Introduction

WP Meta Updater is a comprehensive application for managing and updating SEO metadata (meta title and meta description) of your WordPress site. Available in both graphical (GUI) and command line (CLI) versions, this tool allows you to efficiently optimize the SEO of your WordPress content.

![WP Meta Updater Logo](ui/logo-wp-updater.png)

## Table of Contents

- [Introduction](#introduction)
- [Main Features](#main-features)
- [Available Versions](#available-versions)
  - [GUI Version](#gui-version)
  - [CLI Version](#cli-version)
- [Prerequisites and Installation](#prerequisites-and-installation)
  - [System Configuration](#system-configuration)
  - [Installing Dependencies](#installing-dependencies)
  - [Creating the Executable](#creating-the-executable)
- [Configuration](#configuration)
  - [WordPress Authentication](#wordpress-authentication)
  - [REST API Connection](#rest-api-connection)
  - [Direct MySQL Connection](#direct-mysql-connection)
- [Usage](#usage)
  - [Graphical Interface](#graphical-interface)
  - [Command Line](#command-line)
  - [CSV File Format](#csv-file-format)
- [Advanced Features](#advanced-features)
  - [Optimized CSV Import](#optimized-csv-import)
  - [Direct MySQL Connection](#direct-mysql-connection-1)
  - [Batch Updates](#batch-updates)
  - [Update Scheduling](#update-scheduling)
- [Rank Math SEO Extension](#rank-math-seo-extension)
  - [Installation and Configuration](#installation-and-configuration)
  - [Using with WordPress Meta Updater](#using-with-wordpress-meta-updater)
- [Troubleshooting](#troubleshooting)
  - [Authentication Issues](#authentication-issues)
  - [CSV Import Issues](#csv-import-issues)
  - [Update Issues](#update-issues)
  - [Script Issues](#script-issues)
- [Development](#development)
  - [Project Structure](#project-structure)
  - [Tests](#tests)
- [License and Credits](#license-and-credits)

## Main Features

- **Modern Graphical Interface**: Intuitive user interface based on PyQt6
- **High-Performance CLI Version**: Task automation via command line
- **REST API Connection**: Secure communication with WordPress via REST API
- **Direct MySQL Connection**: Option to directly update the database
- **CSV Import/Export**: Metadata management via CSV files
- **Bulk Updates**: Optimized processing for large-scale updates
- **Scheduling**: Programming of one-time or recurring updates
- **SEO Analysis**: Identification of non-optimized titles and descriptions
- **Multi-site Support**: Management of multiple WordPress sites
- **Offline Mode**: Work on data locally with later synchronization
- **Multi-plugin SEO Support**: Compatible with Yoast SEO, Rank Math, All in One SEO, SEOPress

## Available Versions

### GUI Version

The graphical interface version offers a complete and intuitive user experience.

#### GUI-Specific Features

- Modern interface with automatic light/dark theme
- Filterable and sortable data tables
- Direct metadata editing
- SEO statistics visualization
- Update scheduling assistant
- Connection profile management

#### Launching the GUI Application

```bash
python wp_meta_updater.py
```

### CLI Version

The command line version is ideal for automation and scripts.

#### CLI-Specific Features

- Fast export of SEO metadata
- Import and update from CSV
- Detailed report generation
- Parallel processing for optimal performance
- Easily integrable into automation scripts

#### Using the CLI Version

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

## Prerequisites and Installation

### System Configuration

- **Operating System**: Windows, macOS, or Linux
- **Python**: Version 3.8 or higher
- **Disk Space**: Minimum 100 MB
- **Memory**: Minimum 512 MB RAM (1 GB recommended for large sites)

### Installing Dependencies

1. Clone or download the repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

**Main Dependencies**:
- PyQt6 (only for GUI version)
- requests
- pandas
- python-dateutil
- darkdetect (only for GUI version)
- mysql-connector-python (optional, for direct MySQL connection)

### Creating the Executable

To create a standalone executable (not requiring Python):

```bash
python build_exe.py
```

The executable will be created in the `build/wp_meta_updater/` folder.

## Configuration

### WordPress Authentication

To use WP Meta Updater, you need to generate an authentication token:

1. Install the [Application Passwords](https://wordpress.org/plugins/application-passwords/) plugin on your WordPress site
2. In your WordPress dashboard, go to Users > Your Profile
3. Scroll down to the "Application Passwords" section
4. Create a new application password named "WP Meta Updater"
5. Copy the generated token to use in the application

### REST API Connection

#### In the Graphical Interface

1. Launch the application
2. In the "Connection" tab, enter:
   - URL of your WordPress site (with https://)
   - Authentication token
3. Click on "Test Connection"
4. Save the connection profile if desired

#### In Command Line

Specify the URL and token in the command:

```bash
python wp_meta_cli.py export --url https://your-site.com --token "your token" --output export.csv
```

### Direct MySQL Connection

To use the direct connection to the MySQL database (faster for large updates):

#### MySQL Prerequisites

- Python module `mysql-connector-python` installed
- Access to the MySQL database of the WordPress site
- Sufficient permissions to modify metadata tables

#### Configuration in the Graphical Interface

1. Go to the "MySQL Connection" tab
2. If the MySQL module is not installed, click on "Install MySQL Module"
3. Configure the parameters:
   - Host (e.g., localhost)
   - User
   - Password
   - Database name
   - Table prefix (default: wp_)
4. Click on "Test Connection"

#### Configuration in Command Line

```bash
python wp_meta_cli.py import --url https://your-site.com --token "your token" --input data.csv --update --method mysql --db-host localhost --db-user user --db-password password --db-name wordpress --db-prefix wp_
```

## Usage

### Graphical Interface

#### Importing Metadata

1. Once connected, click on "Import from WordPress"
2. The application will retrieve all available content types
3. Metadata will be displayed in the main table

#### Modifying Metadata

1. In the "Metadata" tab, filter and search for items
2. Double-click on an item to edit its SEO metadata
3. Modified items are highlighted in yellow

#### Updating Metadata

1. Select the items to update
2. Click on "Update Selected" or "Update All Modified"
3. Choose the update method (REST API or MySQL)
4. Confirm the update

#### CSV Export and Import

1. To export, click on "Export to CSV"
2. To import, click on "Import from CSV"
3. Select the CSV file (UTF-8 encoded with BOM)

### Command Line

#### Listing Available Content Types

```bash
python wp_meta_cli.py list-types --url https://your-site.com --token "your token"
```

#### Exporting SEO Metadata to CSV

For all content types:

```bash
python wp_meta_cli.py export --url https://your-site.com --token "your token" --output export.csv
```

For a specific type:

```bash
python wp_meta_cli.py export --url https://your-site.com --token "your token" --output articles.csv --type post
```

#### Importing and Updating from CSV

Import without updating (verification):

```bash
python wp_meta_cli.py import --url https://your-site.com --token "your token" --input import.csv
```

Import and update:

```bash
python wp_meta_cli.py import --url https://your-site.com --token "your token" --input import.csv --update
```

Using direct MySQL connection:

```bash
python wp_meta_cli.py import --url https://your-site.com --token "your token" --input import.csv --update --method mysql --db-host localhost --db-user user --db-password password --db-name wordpress --db-prefix wp_
```

### CSV File Format

The CSV file must contain at minimum the following columns:

- `id`: WordPress item ID
- `type`: Content type (post, page, etc.)
- `seo_title`: SEO title to update
- `seo_description`: SEO description to update

Example CSV file:

```csv
"id","type","title","url","seo_title","seo_description"
"1","post","My first article","https://your-site.com/my-first-article","New SEO title","New SEO description"
"2","page","About","https://your-site.com/about","About our company","Discover our history and mission"
```

## Advanced Features

### Optimized CSV Import

The application uses an optimized CSV import method to efficiently handle large files:

- **Batch Processing**: Loading in batches to reduce memory usage
- **Adaptive Batch Size**: Automatic adjustment based on file size
- **Responsive Interface**: Processing UI events during import
- **Intelligent Separator Detection**: Support for comma, semicolon, tab
- **Robust Error Handling**: Continuing processing despite individual errors

### Direct MySQL Connection

The direct MySQL connection offers several advantages:

- **Performance**: Faster updates than with the REST API
- **API Limitation Bypass**: Works even if the REST API is limited
- **Efficiency for Mass Updates**: Ideal for large sites

**Important Note**: The direct MySQL connection bypasses WordPress hooks and filters. Use it with caution and make sure you have a backup of your database.

### Batch Updates

To avoid issues during mass updates, the application uses a batch processing system:

- **Batch Processing**: Items are processed in batches of 20 items (configurable)
- **Delay Between Batches**: 200ms by default to avoid overloading the server
- **Optimized Memory Management**: Periodic execution of the garbage collector
- **Retry Mechanism**: Up to 2 additional attempts in case of failure
- **Detailed Logging**: Precise tracking of batch processing

These parameters are configurable in the `WordPressConnector` class:

```python
# Batch processing parameters for mass updates
BATCH_SIZE = 20       # Number of items per batch
BATCH_DELAY_MS = 200  # Delay between batches in milliseconds
MAX_RETRIES = 2       # Maximum number of retry attempts in case of failure
GC_FREQUENCY = 5      # Garbage collector execution frequency (every X batches)
```

### Update Scheduling

The graphical interface allows scheduling automatic updates:

1. In the "Scheduling" tab, click on "Schedule an Update"
2. Configure the date, time, and recurrence options
3. Select the items to update
4. Click "OK" to schedule the update

Scheduled updates will run even if the application is closed (if the option is enabled).

## Rank Math SEO Extension

WP Meta Updater is compatible with the Rank Math SEO API extension which allows exposing Rank Math metadata in the WordPress REST API.

### Installation and Configuration

1. Download the `rank-math-seo-api-extension` folder
2. Upload it to the `/wp-content/plugins/` directory of your WordPress site
3. Activate the plugin from the "Plugins" menu in the WordPress administration
4. Go to "Settings > Rank Math SEO API" in the WordPress administration
5. Check the "Enable Rank Math SEO in REST API" box
6. Click on "Save Changes"

### Using with WP Meta Updater

Once the extension is activated, WP Meta Updater will automatically:

1. Detect Rank Math SEO fields (`rank_math_title` and `rank_math_description`)
2. Import these metadata from WordPress
3. Modify them via the interface or CSV files
4. Update them on your WordPress site

To test the extension:

```bash
python test_rank_math_seo.py --url https://your-site.com --token "your token"
```

## Troubleshooting

### Authentication Issues

If you encounter authentication problems:

1. Verify that the token is correctly entered (with spaces)
2. Make sure the Application Passwords plugin is activated
3. Check that the user has sufficient rights
4. Test the API directly with a tool like Postman or cURL

### CSV Import Issues

If CSV import fails:

1. Check that the file is encoded in UTF-8 with BOM
2. Make sure the required columns are present
3. Verify that the IDs correspond to existing items
4. Try with a smaller file to isolate the problem

### Update Issues

If updates fail:

1. Check the logs in the `logs/` folder
2. Try reducing the number of items updated simultaneously
3. Test with the alternative method (API if you're using MySQL or vice versa)
4. Check that the WordPress server is not overloaded

### Script Issues

#### In PowerShell

If you get an error like "The term 'wp_meta_cli.bat' is not recognized...", use the following syntax:

```powershell
.\wp_meta_cli.bat [command] [arguments]
```

The `.\` prefix indicates to PowerShell that the script is in the current directory.

#### Tokens with Spaces

If your authentication token contains spaces, you must surround it with quotes:

```bash
# Incorrect (if the token contains spaces)
python wp_meta_cli.py export --url https://your-site.com --token kFIT w6HU P3vf vmC2 AIxh WqWz --output export.csv

# Correct
python wp_meta_cli.py export --url https://your-site.com --token "kFIT w6HU P3vf vmC2 AIxh WqWz" --output export.csv
```

## Development

### Project Structure

```
wp-update/
├── main.py                  # Main entry point (GUI)
├── wp_meta_updater.py       # Launch script (GUI)
├── wp_meta_cli.py           # Command line version
├── wp_meta_cli.bat          # Batch script for Windows
├── wp_meta_cli.sh           # Shell script for Linux/macOS
├── wp_connector.py          # WordPress API connection module
├── wp_meta_direct_update.py # Direct MySQL connection module
├── data_manager.py          # Data management module
├── update_manager.py        # Update management module
├── build_exe.py             # Executable creation script
├── requirements.txt         # Python dependencies
├── ui/                      # User interface modules (GUI)
│   ├── main_window.py       # Main window
│   ├── connection_widget.py # API connection widget
│   ├── mysql_connection_widget.py # MySQL connection widget
│   ├── metadata_widget.py   # Metadata management widget
│   ├── schedule_widget.py   # Scheduling widget
│   ├── settings_widget.py   # Settings widget
│   ├── about_dialog.py      # About dialog box
│   └── on_table_double_clicked.py # Event handler
├── rank-math-seo-api-extension/ # WordPress extension for Rank Math SEO
├── logs/                    # Application logs
├── data/                    # Application data
└── build/                   # Build folder for the executable
```

### Tests

Several test scripts are available to verify the proper functioning of the application:

- `test_wp_connector.py`: Tests the connection to the WordPress API
- `test_wp_post.py`: Tests metadata update via the API
- `test_wp_create.py`: Tests content creation with metadata
- `test_wp_permissions.py`: Checks user permissions
- `test_csv_import.py`: Tests CSV file import
- `test_large_csv_import.py`: Tests large CSV file import
- `test_batch_update.py`: Tests batch updates
- `test_rank_math_seo.py`: Tests integration with Rank Math SEO

To run a test:

```bash
python test_wp_connector.py --url https://your-site.com --token "your token"
```

## License and Credits

### License

Copyright © 2025 - All rights reserved

### Author

William Troillard

### Acknowledgements

- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - Graphical interface
- [WordPress REST API](https://developer.wordpress.org/rest-api/) - WordPress REST API
- [Requests](https://requests.readthedocs.io/) - HTTP library for Python
- [Pandas](https://pandas.pydata.org/) - Data analysis and manipulation
- [MySQL Connector/Python](https://dev.mysql.com/doc/connector-python/en/) - MySQL connection
