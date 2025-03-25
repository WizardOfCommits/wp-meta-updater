@echo off
REM Script batch pour exécuter le test du connecteur WordPress
REM Utilisation: test_wp_connector.bat --url https://www.votresite.com --token votre_token [--type post] [--per-page 10] [--page 1]

echo Test du connecteur WordPress
echo ===========================

python test_wp_connector.py %*

echo.
echo Test terminé.
pause
