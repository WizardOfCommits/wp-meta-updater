#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de test pour le connecteur WordPress
Permet de tester la connexion à l'API WordPress et de récupérer les posts
"""

import os
import sys
import logging
import argparse
from wp_connector import WordPressConnector

# Configuration du logging
def setup_logging():
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, "test_connector.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8-sig"),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger("test_wp_connector")

def main():
    # Initialisation du parser d'arguments
    parser = argparse.ArgumentParser(description="Test du connecteur WordPress")
    
    # Arguments
    parser.add_argument("--url", required=True, help="URL du site WordPress")
    parser.add_argument("--token", required=True, help="Jeton d'authentification WordPress")
    parser.add_argument("--type", default="posts", help="Type de contenu à récupérer (par défaut: posts)")
    parser.add_argument("--per-page", type=int, default=10, help="Nombre d'éléments par page (par défaut: 10)")
    parser.add_argument("--page", type=int, default=1, help="Numéro de page (par défaut: 1)")
    
    # Analyse des arguments
    args = parser.parse_args()
    
    # Initialisation du logger
    logger = setup_logging()
    logger.info("Démarrage du test du connecteur WordPress")
    
    # Initialisation du connecteur WordPress
    wp_connector = WordPressConnector(logger)
    
    # Configuration de la connexion WordPress
    wp_connector.configure(args.url, args.token)
    
    # Test de la connexion
    logger.info(f"Test de la connexion à {args.url}")
    success, message = wp_connector.test_connection()
    
    if not success:
        logger.error(f"Échec de la connexion: {message}")
        print(f"Échec de la connexion: {message}")
        return
    
    logger.info(f"Connexion réussie: {message}")
    print(f"Connexion réussie: {message}")
    
    # Récupération des éléments de contenu
    logger.info(f"Récupération des {args.type}s (page {args.page}, {args.per_page} par page)")
    items, total_items, total_pages = wp_connector.fetch_content_items(
        args.type, 
        page=args.page, 
        per_page=args.per_page
    )
    
    # Affichage des résultats
    if items:
        logger.info(f"Récupération réussie: {len(items)} éléments sur {total_items} (page {args.page}/{total_pages})")
        print(f"Récupération réussie: {len(items)} éléments sur {total_items} (page {args.page}/{total_pages})")
        
        # Affichage des éléments récupérés
        print("\nÉléments récupérés:")
        for i, item in enumerate(items, 1):
            title = item.get("title", {}).get("rendered", "Sans titre") if isinstance(item.get("title"), dict) else item.get("title", "Sans titre")
            print(f"{i}. {title} (ID: {item.get('id')})")
            
            # Affichage des métadonnées SEO si disponibles
            metadata = wp_connector.extract_seo_metadata(item)
            if metadata["seo_title"] or metadata["seo_description"]:
                print(f"   - Titre SEO: {metadata['seo_title']}")
                print(f"   - Description SEO: {metadata['seo_description']}")
            
            print("")
    else:
        logger.warning(f"Aucun élément récupéré pour le type {args.type}")
        print(f"Aucun élément récupéré pour le type {args.type}")

if __name__ == "__main__":
    main()
