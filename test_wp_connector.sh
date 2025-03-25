#!/bin/bash
# Script shell pour exécuter le test du connecteur WordPress
# Utilisation: ./test_wp_connector.sh --url https://www.votresite.com --token votre_token [--type post] [--per-page 10] [--page 1]

echo "Test du connecteur WordPress"
echo "==========================="

python3 test_wp_connector.py "$@"

echo ""
echo "Test terminé."
read -p "Appuyez sur Entrée pour continuer..."

# Rendre le script exécutable
chmod +x test_wp_connector.sh
