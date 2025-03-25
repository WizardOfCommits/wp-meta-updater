#!/bin/bash
# Script shell pour faciliter l'utilisation de WordPress Meta CLI
# Auteur: William Troillard

# Configuration par défaut
PYTHON_CMD="python3"
SCRIPT_PATH="wp_meta_cli.py"
LOG_FILE="logs/cline.log"

# Vérification de l'existence du répertoire logs
mkdir -p logs

# Affichage du titre
echo "==================================================="
echo "WordPress Meta CLI - Outil de gestion des métadonnées SEO"
echo "==================================================="
echo ""

# Fonction d'aide
show_help() {
    echo "Aide de WordPress Meta CLI"
    echo "----------------------"
    echo ""
    echo "Utilisation:"
    echo "  ./wp_meta_cli.sh [commande] [arguments]"
    echo ""
    echo "Commandes disponibles:"
    echo "  export [url] [token] [fichier_sortie] [type]"
    echo "    Exporte les métadonnées SEO en CSV"
    echo "    [type] est optionnel, par défaut tous les types sont exportés"
    echo ""
    echo "  import [url] [token] [fichier_entrée] [update]"
    echo "    Importe les métadonnées SEO depuis un CSV"
    echo "    Ajoutez \"update\" comme dernier argument pour mettre à jour WordPress"
    echo ""
    echo "  list-types [url] [token]"
    echo "    Liste les types de contenu disponibles"
    echo ""
    echo "  help"
    echo "    Affiche cette aide"
    echo ""
    echo "Exemples:"
    echo "  ./wp_meta_cli.sh export https://monsite.com mon_token export.csv"
    echo "  ./wp_meta_cli.sh export https://monsite.com mon_token articles.csv post"
    echo "  ./wp_meta_cli.sh import https://monsite.com mon_token import.csv"
    echo "  ./wp_meta_cli.sh import https://monsite.com mon_token import.csv update"
    echo "  ./wp_meta_cli.sh list-types https://monsite.com mon_token"
    echo ""
}

# Vérification des arguments
if [ $# -eq 0 ]; then
    show_help
    exit 0
fi

# Exécution de la commande
case "$1" in
    export)
        echo "Exportation des métadonnées SEO en CSV"
        echo "------------------------------------"
        echo ""
        
        # Vérification des arguments requis
        if [ -z "$2" ]; then
            echo "URL du site WordPress manquante."
            echo "Utilisation: ./wp_meta_cli.sh export [url] [token] [fichier_sortie] [type]"
            exit 1
        fi
        if [ -z "$3" ]; then
            echo "Jeton d'authentification manquant."
            echo "Utilisation: ./wp_meta_cli.sh export [url] [token] [fichier_sortie] [type]"
            exit 1
        fi
        if [ -z "$4" ]; then
            echo "Fichier de sortie manquant."
            echo "Utilisation: ./wp_meta_cli.sh export [url] [token] [fichier_sortie] [type]"
            exit 1
        fi
        
        URL="$2"
        TOKEN="$3"
        OUTPUT="$4"
        TYPE="$5"
        
        # Construction de la commande
        CMD="$PYTHON_CMD $SCRIPT_PATH export --url $URL --token \"$TOKEN\" --output $OUTPUT"
        if [ ! -z "$TYPE" ]; then
            CMD="$CMD --type $TYPE"
        fi
        
        echo "Exécution de la commande: $CMD"
        echo ""
        
        # Exécution de la commande
        $CMD
        ;;
        
    import)
        echo "Importation et mise à jour des métadonnées SEO depuis un CSV"
        echo "--------------------------------------------------------"
        echo ""
        
        # Vérification des arguments requis
        if [ -z "$2" ]; then
            echo "URL du site WordPress manquante."
            echo "Utilisation: ./wp_meta_cli.sh import [url] [token] [fichier_entrée] [update]"
            exit 1
        fi
        if [ -z "$3" ]; then
            echo "Jeton d'authentification manquant."
            echo "Utilisation: ./wp_meta_cli.sh import [url] [token] [fichier_entrée] [update]"
            exit 1
        fi
        if [ -z "$4" ]; then
            echo "Fichier d'entrée manquant."
            echo "Utilisation: ./wp_meta_cli.sh import [url] [token] [fichier_entrée] [update]"
            exit 1
        fi
        
        URL="$2"
        TOKEN="$3"
        INPUT="$4"
        UPDATE="$5"
        
        # Construction de la commande
        CMD="$PYTHON_CMD $SCRIPT_PATH import --url $URL --token \"$TOKEN\" --input $INPUT"
        if [ "$UPDATE" = "update" ]; then
            CMD="$CMD --update"
        fi
        
        echo "Exécution de la commande: $CMD"
        echo ""
        
        # Exécution de la commande
        $CMD
        ;;
        
    list-types)
        echo "Liste des types de contenu disponibles"
        echo "----------------------------------"
        echo ""
        
        # Vérification des arguments requis
        if [ -z "$2" ]; then
            echo "URL du site WordPress manquante."
            echo "Utilisation: ./wp_meta_cli.sh list-types [url] [token]"
            exit 1
        fi
        if [ -z "$3" ]; then
            echo "Jeton d'authentification manquant."
            echo "Utilisation: ./wp_meta_cli.sh list-types [url] [token]"
            exit 1
        fi
        
        URL="$2"
        TOKEN="$3"
        
        # Construction de la commande
        CMD="$PYTHON_CMD $SCRIPT_PATH list-types --url $URL --token \"$TOKEN\""
        
        echo "Exécution de la commande: $CMD"
        echo ""
        
        # Exécution de la commande
        $CMD
        ;;
        
    help)
        show_help
        ;;
        
    *)
        echo "Commande non reconnue: $1"
        echo "Utilisez \"help\" pour afficher l'aide."
        exit 1
        ;;
esac

echo ""
echo "Terminé!"
exit 0
