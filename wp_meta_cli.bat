@echo off
REM Script batch pour faciliter l'utilisation de WordPress Meta CLI
REM Auteur: William Troillard

setlocal enabledelayedexpansion

REM Configuration par défaut
set PYTHON_CMD=python
set SCRIPT_PATH=wp_meta_cli.py
set LOG_FILE=logs\cline.log

REM Vérification de l'existence du répertoire logs
if not exist logs mkdir logs

REM Affichage du titre
echo ===================================================
echo WordPress Meta CLI - Outil de gestion des metadonnees SEO
echo ===================================================
echo.

REM Vérification des arguments
if "%1"=="" goto :help

REM Exécution de la commande
if "%1"=="export" goto :export
if "%1"=="import" goto :import
if "%1"=="list-types" goto :list_types
if "%1"=="help" goto :help

echo Commande non reconnue: %1
echo Utilisez "help" pour afficher l'aide.
goto :end

:export
echo Exportation des metadonnees SEO en CSV
echo ------------------------------------

REM Vérification des arguments requis
if "%2"=="" (
    echo URL du site WordPress manquante.
    echo Utilisation: wp_meta_cli.bat export [url] [token] [fichier_sortie] [type]
    goto :end
)
if "%3"=="" (
    echo Jeton d'authentification manquant.
    echo Utilisation: wp_meta_cli.bat export [url] [token] [fichier_sortie] [type]
    goto :end
)
if "%4"=="" (
    echo Fichier de sortie manquant.
    echo Utilisation: wp_meta_cli.bat export [url] [token] [fichier_sortie] [type]
    goto :end
)

set URL=%2
set TOKEN=%3
set OUTPUT=%4
set TYPE=%5

REM Construction de la commande
set CMD=%PYTHON_CMD% %SCRIPT_PATH% export --url %URL% --token "%TOKEN%" --output %OUTPUT%
if not "%TYPE%"=="" set CMD=%CMD% --type %TYPE%

echo Execution de la commande: %CMD%
echo.

REM Exécution de la commande
%CMD%

goto :end

:import
echo Importation et mise a jour des metadonnees SEO depuis un CSV
echo --------------------------------------------------------

REM Vérification des arguments requis
if "%2"=="" (
    echo URL du site WordPress manquante.
    echo Utilisation: wp_meta_cli.bat import [url] [token] [fichier_entree] [update]
    goto :end
)
if "%3"=="" (
    echo Jeton d'authentification manquant.
    echo Utilisation: wp_meta_cli.bat import [url] [token] [fichier_entree] [update]
    goto :end
)
if "%4"=="" (
    echo Fichier d'entree manquant.
    echo Utilisation: wp_meta_cli.bat import [url] [token] [fichier_entree] [update]
    goto :end
)

set URL=%2
set TOKEN=%3
set INPUT=%4
set UPDATE=%5

REM Construction de la commande
set CMD=%PYTHON_CMD% %SCRIPT_PATH% import --url %URL% --token "%TOKEN%" --input %INPUT%
if "%UPDATE%"=="update" set CMD=%CMD% --update

echo Execution de la commande: %CMD%
echo.

REM Exécution de la commande
%CMD%

goto :end

:list_types
echo Liste des types de contenu disponibles
echo ----------------------------------

REM Vérification des arguments requis
if "%2"=="" (
    echo URL du site WordPress manquante.
    echo Utilisation: wp_meta_cli.bat list-types [url] [token]
    goto :end
)
if "%3"=="" (
    echo Jeton d'authentification manquant.
    echo Utilisation: wp_meta_cli.bat list-types [url] [token]
    goto :end
)

set URL=%2
set TOKEN=%3

REM Construction de la commande
set CMD=%PYTHON_CMD% %SCRIPT_PATH% list-types --url %URL% --token "%TOKEN%"

echo Execution de la commande: %CMD%
echo.

REM Exécution de la commande
%CMD%

goto :end

:help
echo Aide de WordPress Meta CLI
echo ----------------------
echo.
echo Utilisation:
echo   wp_meta_cli.bat [commande] [arguments]
echo.
echo Commandes disponibles:
echo   export [url] [token] [fichier_sortie] [type]
echo     Exporte les metadonnees SEO en CSV
echo     [type] est optionnel, par defaut tous les types sont exportes
echo.
echo   import [url] [token] [fichier_entree] [update]
echo     Importe les metadonnees SEO depuis un CSV
echo     Ajoutez "update" comme dernier argument pour mettre a jour WordPress
echo.
echo   list-types [url] [token]
echo     Liste les types de contenu disponibles
echo.
echo   help
echo     Affiche cette aide
echo.
echo Exemples:
echo   wp_meta_cli.bat export https://monsite.com mon_token export.csv
echo   wp_meta_cli.bat export https://monsite.com mon_token articles.csv post
echo   wp_meta_cli.bat import https://monsite.com mon_token import.csv
echo   wp_meta_cli.bat import https://monsite.com mon_token import.csv update
echo   wp_meta_cli.bat list-types https://monsite.com mon_token
echo.

:end
echo.
echo Termine!
endlocal
