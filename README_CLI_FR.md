# WordPress Meta CLI

Version minimale en ligne de commande pour l'exportation et l'importation des métadonnées SEO WordPress.

## Fonctionnalités

- Exportation des métadonnées SEO en CSV par type de contenu ou pour tous les types
- Importation et mise à jour des métadonnées SEO depuis un fichier CSV
- Génération de rapports détaillés dans des logs
- Support de différents plugins SEO (Yoast SEO, Rank Math, All in One SEO, SEOPress)
- Traitement en parallèle pour des performances optimales

## Prérequis

- Python 3.8 ou supérieur
- Modules Python requis :
  - requests
  - pandas
  - python-dateutil

## Installation

### Installation des dépendances

```bash
pip install -r requirements.txt
```

## Utilisation

### Obtention d'un jeton d'authentification WordPress

Pour utiliser cet outil, vous devez générer un jeton d'authentification pour l'API REST de WordPress :

1. Installez le plugin [Application Passwords](https://wordpress.org/plugins/application-passwords/) sur votre site WordPress
2. Dans votre tableau de bord WordPress, allez dans Utilisateurs > Votre profil
3. Faites défiler jusqu'à la section "Mots de passe d'application"
4. Créez un nouveau mot de passe d'application nommé "WP Meta CLI"
5. Copiez le jeton généré et utilisez-le dans les commandes

### Utilisation des scripts d'aide

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

### Utilisation directe du script Python

Vous pouvez également utiliser directement le script Python :

```bash
python wp_meta_cli.py list-types --url https://votre-site.com --token "votre-jeton"
```

> **Important** : Si votre jeton d'authentification contient des espaces, vous devez l'entourer de guillemets doubles pour qu'il soit traité comme un seul argument.

### Exporter les métadonnées SEO en CSV

Pour exporter toutes les métadonnées SEO en CSV :

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

Pour exporter uniquement un type de contenu spécifique (par exemple, les articles) :

```bash
# Windows (CMD)
wp_meta_cli.bat export https://votre-site.com "votre jeton avec espaces" articles.csv post

# Windows (PowerShell)
.\wp_meta_cli.bat export https://votre-site.com "votre jeton avec espaces" articles.csv post

# Linux/macOS
./wp_meta_cli.sh export https://votre-site.com "votre jeton avec espaces" articles.csv post

# Directement avec Python
python wp_meta_cli.py export --url https://votre-site.com --token "votre jeton avec espaces" --output articles.csv --type post
```

### Importer et mettre à jour les métadonnées SEO depuis un CSV

Pour importer des métadonnées SEO depuis un fichier CSV sans les mettre à jour sur WordPress :

```bash
# Windows (CMD)
wp_meta_cli.bat import https://votre-site.com "votre jeton avec espaces" import.csv

# Windows (PowerShell)
.\wp_meta_cli.bat import https://votre-site.com "votre jeton avec espaces" import.csv

# Linux/macOS
./wp_meta_cli.sh import https://votre-site.com "votre jeton avec espaces" import.csv

# Directement avec Python
python wp_meta_cli.py import --url https://votre-site.com --token "votre jeton avec espaces" --input import.csv
```

Pour importer et mettre à jour les métadonnées SEO sur WordPress :

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

## Format du fichier CSV

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

## Logs et rapports

Les logs sont générés automatiquement dans le répertoire `logs` :

- `cline.log` : Journal général de l'application
- `update_YYYYMMDD_HHMMSS.json` : Rapport détaillé de chaque mise à jour

Les rapports de mise à jour contiennent des informations détaillées sur les éléments mis à jour avec succès et les erreurs éventuelles.

## Exemples d'utilisation

### Workflow typique

1. Exporter les métadonnées SEO actuelles :
   ```bash
   # Windows (PowerShell)
   .\wp_meta_cli.bat export https://votre-site.com "votre jeton avec espaces" export.csv
   ```

2. Modifier le fichier CSV avec un tableur (Excel, LibreOffice Calc, etc.)

3. Importer et mettre à jour les métadonnées modifiées :
   ```bash
   # Windows (PowerShell)
   .\wp_meta_cli.bat import https://votre-site.com "votre jeton avec espaces" export_modifie.csv update
   ```

### Automatisation avec un script batch

Vous pouvez créer un script batch pour automatiser l'exportation et l'importation :

```batch
@echo off
set SITE_URL=https://votre-site.com
set TOKEN=votre-jeton-sans-espaces
set EXPORT_FILE=export_%date:~-4,4%%date:~-7,2%%date:~-10,2%.csv
set IMPORT_FILE=import.csv

echo Exportation des métadonnées SEO...
python wp_meta_cli.py export --url %SITE_URL% --token "%TOKEN%" --output %EXPORT_FILE%

echo Importation et mise à jour des métadonnées SEO...
python wp_meta_cli.py import --url %SITE_URL% --token "%TOKEN%" --input %IMPORT_FILE% --update

echo Terminé!
```

> **Note** : Dans les scripts batch, entourez la variable TOKEN de guillemets ("%TOKEN%") pour gérer les jetons avec espaces.

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

### Problèmes de connexion

Si vous rencontrez des problèmes de connexion à l'API WordPress, vérifiez :

1. Que l'URL du site est correcte et inclut le protocole (http:// ou https://)
2. Que le jeton d'authentification est valide
3. Que le plugin Application Passwords est correctement installé et activé
4. Que l'API REST de WordPress n'est pas bloquée par un pare-feu ou un plugin de sécurité

### Erreurs d'importation CSV

Si l'importation CSV échoue, vérifiez :

1. Que le fichier CSV est encodé en UTF-8 avec BOM
2. Que les colonnes requises (id, type) sont présentes
3. Que les IDs correspondent à des éléments existants sur le site WordPress

## Licence

Copyright © 2025 - Tous droits réservés

## Auteur

William Troillard
