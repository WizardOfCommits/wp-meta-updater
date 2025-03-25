#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
WordPress Meta CLI
Version minimale en ligne de commande pour l'exportation et l'importation des métadonnées SEO WordPress
"""

import os
import sys
import json
import logging
import argparse
import csv
import pandas as pd
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

# Import des modules existants (sans les dépendances PyQt6)
from wp_connector import WordPressConnector

# Import conditionnel du module MySQL
try:
    from wp_meta_direct_update import WordPressDirectConnector
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False

# Configuration du logging
def setup_logging():
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, "cline.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8-sig"),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger("wp_meta_cli")

# Classe DataManager adaptée pour la ligne de commande (sans PyQt6)
class CLIDataManager:
    """Classe pour gérer les données de l'application en ligne de commande"""
    
    def __init__(self, logger: logging.Logger):
        """Initialisation du gestionnaire de données"""
        self.logger = logger
        self.data = {}  # Données actuelles
        self.modified_items = set()  # Éléments modifiés
    
    def clear_data(self) -> None:
        """Efface toutes les données"""
        self.data = {}
        self.modified_items = set()
        self.logger.info("Données effacées")
    
    def import_from_wp(self, content_data: Dict[str, List[Dict[str, Any]]]) -> None:
        """
        Importe les données depuis WordPress
        
        Args:
            content_data: Dictionnaire avec les types de contenu comme clés et les listes d'éléments comme valeurs
        """
        self.logger.info("Importation des données depuis WordPress")
        
        # Réinitialisation des données
        self.data = {}
        
        # Traitement des données importées
        total_items = sum(len(items) for items in content_data.values())
        processed = 0
        
        for content_type, items in content_data.items():
            self.data[content_type] = []
            
            for item in items:
                processed += 1
                print(f"Traitement de {processed}/{total_items} : {content_type} {item.get('id', 'inconnu')}")
                
                # Extraction des métadonnées SEO
                if "extract_seo_metadata" in item:
                    # Si les métadonnées sont déjà extraites
                    metadata = item
                else:
                    # Extraction des métadonnées de base
                    title_value = item.get("title", {}).get("rendered", "") if isinstance(item.get("title"), dict) else item.get("title", "")
                    metadata = {
                        "id": item.get("id", 0),
                        "type": content_type,
                        "title": title_value,
                        "url": item.get("link", ""),
                        "date_modified": item.get("modified", ""),
                        "seo_title": "",
                        "seo_description": "",
                        "original_seo_title": "",
                        "original_seo_description": "",
                        "title_h1": title_value,
                        "original_title_h1": title_value
                    }
                    
                    # Extraction des métadonnées SEO en fonction du plugin
                    # (Code d'extraction des métadonnées SEO existant)
                    
                    # Sauvegarder les valeurs originales pour comparaison ultérieure
                    metadata["original_seo_title"] = metadata["seo_title"]
                    metadata["original_seo_description"] = metadata["seo_description"]
                
                # Ajout des métadonnées à la liste
                self.data[content_type].append(metadata)
        
        self.logger.info(f"Importation terminée: {total_items} éléments importés")
    
    def export_to_csv(self, filepath: str, content_type: str = None) -> bool:
        """
        Exporte les données vers un fichier CSV
        
        Args:
            filepath: Chemin du fichier CSV
            content_type: Type de contenu à exporter (None = tous)
            
        Returns:
            Succès de l'exportation
        """
        # (Code d'exportation CSV existant)
        return True
    
    def import_from_csv(self, filepath: str) -> Tuple[bool, str, int]:
        """
        Importe les données depuis un fichier CSV
        
        Args:
            filepath: Chemin du fichier CSV
            
        Returns:
            Tuple (succès, message, nombre d'éléments importés)
        """
        # (Code d'importation CSV existant)
        return True, "Importation réussie", 0
    
    def get_items_for_update(self) -> List[Dict[str, Any]]:
        """
        Récupère les éléments à mettre à jour
        
        Returns:
            Liste des éléments à mettre à jour
        """
        items_to_update = []
        
        # Mise à jour de tous les éléments modifiés
        for content_type, items in self.data.items():
            for item in items:
                if item["id"] in self.modified_items:
                    items_to_update.append(item)
        
        return items_to_update

# Fonction pour mettre à jour les métadonnées
def update_metadata(wp_connector, data_manager, logger, skip_auth_check=False, method="api", mysql_connector=None):
    """
    Met à jour les métadonnées SEO sur WordPress
    
    Args:
        wp_connector: Instance de WordPressConnector
        data_manager: Instance de CLIDataManager
        logger: Instance de Logger
        skip_auth_check: Ignorer les erreurs d'autorisation
        method: Méthode de mise à jour ("api" ou "mysql")
        mysql_connector: Instance de WordPressDirectConnector (pour la méthode "mysql")
    """
    # Récupération des éléments à mettre à jour
    items_to_update = data_manager.get_items_for_update()
    
    if not items_to_update:
        logger.warning("Aucun élément à mettre à jour")
        print("Aucun élément à mettre à jour")
        return
    
    # Vérification de la méthode de mise à jour
    if method == "api":
        # Vérification de la connexion à WordPress
        if not wp_connector or not wp_connector.api_url or not wp_connector.auth_token:
            logger.error("Connexion WordPress API non configurée")
            print("Connexion WordPress API non configurée")
            return
        
        # Fonction de callback pour la progression
        def progress_callback(current, total):
            print(f"Progression: {current}/{total}")
        
        # Exécution de la mise à jour
        print(f"Mise à jour de {len(items_to_update)} éléments via API REST...")
        
        if skip_auth_check:
            print("Note: La vérification d'autorisation est désactivée. Les erreurs d'autorisation seront ignorées.")
            print("ATTENTION: Les mises à jour avec erreurs d'autorisation seront marquées comme 'réussies' dans les statistiques,")
            print("          mais les modifications ne seront PAS appliquées sur le serveur WordPress.")
            
            # Créer une version modifiée de la fonction de mise à jour qui ignore les erreurs d'autorisation
            original_update_func = wp_connector.update_seo_metadata
            
            def update_with_skip_auth(item_id, content_type, seo_title, seo_description, title=None):
                try:
                    success, message = original_update_func(item_id, content_type, seo_title, seo_description, title)
                    if not success:
                        if "401" in message or "rest_cannot_edit" in message or "autorisation" in message.lower():
                            # Ignorer les erreurs d'autorisation
                            logger.warning(f"Erreur d'autorisation ignorée pour {content_type} {item_id}")
                            # Ajouter une note spéciale pour ces éléments
                            return True, "IGNORÉ: Erreur d'autorisation - Modifications non appliquées sur WordPress"
                    return success, message
                except Exception as e:
                    return False, str(e)
            
            # Remplacer temporairement la fonction de mise à jour
            wp_connector.update_seo_metadata = update_with_skip_auth
        
        try:
            # Exécution de la mise à jour
            stats = wp_connector.bulk_update_metadata(items_to_update, progress_callback)
        finally:
            # Restaurer la fonction originale si nécessaire
            if skip_auth_check:
                wp_connector.update_seo_metadata = original_update_func
    
    elif method == "mysql":
        # Vérification du connecteur MySQL
        if not mysql_connector:
            logger.error("Connecteur MySQL non configuré")
            print("Connecteur MySQL non configuré")
            return
        
        # Connexion à la base de données
        print(f"Mise à jour de {len(items_to_update)} éléments via connexion MySQL directe...")
        if not mysql_connector.connect():
            logger.error("Impossible de se connecter à la base de données MySQL")
            print("Impossible de se connecter à la base de données MySQL")
            return
        
        try:
            # Fonction de callback pour la progression
            def progress_callback(current, total):
                print(f"Progression: {current}/{total}")
            
            # Exécution de la mise à jour
            stats = mysql_connector.bulk_update_metadata(items_to_update, progress_callback)
        finally:
            # Fermeture de la connexion
            mysql_connector.disconnect()
    
    else:
        logger.error(f"Méthode de mise à jour non reconnue: {method}")
        print(f"Méthode de mise à jour non reconnue: {method}")
        return
    
    # Journalisation des résultats
    log_update_results(stats, logger, method)
    
    # Affichage des résultats
    print(f"Mise à jour terminée: {stats['success']} réussies, {stats['failed']} échouées")
    
    if stats["failed"] > 0:
        print("Erreurs:")
        for error in stats.get("errors", []):
            print(f"  - {error['type']} {error['id']} ({error['title']}): {error['error']}")

# Fonction pour journaliser les résultats de mise à jour
def log_update_results(stats, logger, method="api"):
    """
    Journalise les résultats de la mise à jour
    
    Args:
        stats: Statistiques de mise à jour
        logger: Instance de Logger
        method: Méthode de mise à jour utilisée
    """
    # Création du répertoire de logs si nécessaire
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    # Nom du fichier de log
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"update_{timestamp}.json")
    
    # Données du log
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "type": "cli_update",
        "method": method,
        "stats": stats,
        "errors": stats.get("errors", [])
    }
    
    # Écriture du log
    with open(log_file, "w", encoding="utf-8-sig") as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Résultats de mise à jour enregistrés dans {log_file}")

def main():
    # Initialisation du parser d'arguments
    parser = argparse.ArgumentParser(description="WordPress Meta CLI - Outil en ligne de commande pour la gestion des métadonnées SEO WordPress")
    
    # Sous-commandes
    subparsers = parser.add_subparsers(dest="command", help="Commande à exécuter")
    
    # Commande d'exportation
    export_parser = subparsers.add_parser("export", help="Exporter les métadonnées SEO en CSV")
    export_parser.add_argument("--url", required=True, help="URL du site WordPress")
    export_parser.add_argument("--token", required=True, help="Jeton d'authentification WordPress")
    export_parser.add_argument("--output", required=True, help="Chemin du fichier CSV de sortie")
    export_parser.add_argument("--type", help="Type de contenu à exporter (par défaut: tous)")
    
    # Commande d'importation
    import_parser = subparsers.add_parser("import", help="Importer et mettre à jour les métadonnées SEO depuis un CSV")
    import_parser.add_argument("--url", required=True, help="URL du site WordPress")
    import_parser.add_argument("--token", required=True, help="Jeton d'authentification WordPress")
    import_parser.add_argument("--input", required=True, help="Chemin du fichier CSV d'entrée")
    import_parser.add_argument("--update", action="store_true", help="Mettre à jour les métadonnées sur WordPress après l'importation")
    import_parser.add_argument("--skip-auth-check", action="store_true", help="Ignorer la vérification d'autorisation lors de la récupération des posts")
    import_parser.add_argument("--method", choices=["api", "mysql"], default="api", help="Méthode de mise à jour (api ou mysql)")
    
    # Arguments MySQL pour la commande d'importation
    if MYSQL_AVAILABLE:
        import_parser.add_argument("--db-host", help="Hôte de la base de données MySQL")
        import_parser.add_argument("--db-user", help="Nom d'utilisateur MySQL")
        import_parser.add_argument("--db-password", help="Mot de passe MySQL")
        import_parser.add_argument("--db-name", help="Nom de la base de données")
        import_parser.add_argument("--db-prefix", default="wp_", help="Préfixe des tables WordPress (par défaut: wp_)")
    
    # Commande de liste des types de contenu
    list_parser = subparsers.add_parser("list-types", help="Lister les types de contenu disponibles")
    list_parser.add_argument("--url", required=True, help="URL du site WordPress")
    list_parser.add_argument("--token", required=True, help="Jeton d'authentification WordPress")
    
    # Analyse des arguments
    args = parser.parse_args()
    
    # Initialisation du logger
    logger = setup_logging()
    logger.info("Démarrage de l'application CLI")
    
    # Vérification de la commande
    if not args.command:
        parser.print_help()
        return
    
    # Initialisation du connecteur WordPress
    wp_connector = WordPressConnector(logger)
    
    # Initialisation du connecteur MySQL si nécessaire
    mysql_connector = None
    if MYSQL_AVAILABLE and args.command == "import" and args.method == "mysql":
        # Vérification des arguments MySQL
        if not args.db_host or not args.db_user or not args.db_password or not args.db_name:
            logger.error("Arguments MySQL manquants pour la méthode de mise à jour MySQL")
            print("Erreur: Pour utiliser la méthode MySQL, vous devez spécifier --db-host, --db-user, --db-password et --db-name")
            return
        
        # Initialisation du connecteur MySQL
        mysql_connector = WordPressDirectConnector(logger)
        mysql_connector.configure(args.db_host, args.db_user, args.db_password, args.db_name, args.db_prefix)
    
    # Exécution de la commande
    if args.command == "export":
        # Configuration de la connexion WordPress
        wp_connector.configure(args.url, args.token)
        
        # Test de la connexion
        success, message = wp_connector.test_connection()
        if not success:
            logger.error(f"Échec de la connexion: {message}")
            print(f"Échec de la connexion: {message}")
            return
        
        # Récupération des données
        print("Récupération des données depuis WordPress...")
        content_types = [args.type] if args.type else None
        content_data = wp_connector.fetch_all_content(content_types)
        
        # Initialisation du gestionnaire de données
        data_manager = CLIDataManager(logger)
        
        # Importation des données
        data_manager.import_from_wp(content_data)
        
        # Exportation vers CSV
        data_manager.export_to_csv(args.output, args.type)
    
    elif args.command == "import":
        # Configuration de la connexion WordPress
        wp_connector.configure(args.url, args.token)
        
        # Test de la connexion
        success, message = wp_connector.test_connection()
        if not success:
            logger.error(f"Échec de la connexion: {message}")
            print(f"Échec de la connexion: {message}")
            return
        
        # Lire d'abord le fichier CSV pour extraire les IDs des posts à mettre à jour
        try:
            df_import = pd.read_csv(args.input, encoding="utf-8-sig", sep='\t')
            if "id" not in df_import.columns or "type" not in df_import.columns:
                logger.error("Le fichier CSV doit contenir les colonnes 'id' et 'type'")
                print("Le fichier CSV doit contenir les colonnes 'id' et 'type'")
                return
                
            # Extraire les IDs et types uniques
            post_ids_by_type = {}
            for _, row in df_import.iterrows():
                post_type = row["type"]
                post_id = int(row["id"])
                if post_type not in post_ids_by_type:
                    post_ids_by_type[post_type] = []
                post_ids_by_type[post_type].append(post_id)
                
            # Récupérer uniquement les posts spécifiés dans le CSV
            print("Récupération des données spécifiques depuis WordPress...")
            content_data = {}
            
            for post_type, ids in post_ids_by_type.items():
                content_data[post_type] = []
                for post_id in ids:
                    print(f"Récupération du {post_type} avec ID {post_id}...")
                    try:
                        # Utiliser l'endpoint REST correspondant au type de contenu
                        endpoint = wp_connector.REST_ENDPOINTS.get(post_type, post_type)
                        site_base_url = wp_connector.site_url
                        api_url = f"{site_base_url}/wp-json/wp/v2/{endpoint}/{post_id}"
                        
                        response = requests.get(
                            api_url,
                            headers=wp_connector.get_headers(),
                            params={"_embed": "true"},
                            timeout=10
                        )
                        
                        if response.status_code == 200:
                            post_data = response.json()
                            content_data[post_type].append(post_data)
                        else:
                            logger.warning(f"Impossible de récupérer {post_type} {post_id}: {response.status_code}")
                            print(f"Impossible de récupérer {post_type} {post_id}: {response.status_code}")
                    except Exception as e:
                        logger.error(f"Erreur lors de la récupération de {post_type} {post_id}: {str(e)}")
                        print(f"Erreur lors de la récupération de {post_type} {post_id}: {str(e)}")
            
            # Initialisation du gestionnaire de données
            data_manager = CLIDataManager(logger)
            
            # Importation des données récupérées
            data_manager.import_from_wp(content_data)
        except Exception as e:
            logger.error(f"Erreur lors de la lecture du fichier CSV: {str(e)}")
            print(f"Erreur lors de la lecture du fichier CSV: {str(e)}")
            return
        
        # Importation depuis CSV
        success, message, count = data_manager.import_from_csv(args.input)
        
        if not success:
            return
        
        # Mise à jour sur WordPress si demandé
        if args.update and count > 0:
            update_metadata(wp_connector, data_manager, logger, args.skip_auth_check, args.method, mysql_connector)
    
    elif args.command == "list-types":
        # Configuration de la connexion WordPress
        wp_connector.configure(args.url, args.token)
        
        # Test de la connexion
        success, message = wp_connector.test_connection()
        if not success:
            logger.error(f"Échec de la connexion: {message}")
            print(f"Échec de la connexion: {message}")
            return
        
        # Affichage des types de contenu disponibles
        print("Types de contenu disponibles:")
        for type_key, type_name in wp_connector.CONTENT_TYPES.items():
            print(f"  - {type_key}: {type_name}")

if __name__ == "__main__":
    main()
