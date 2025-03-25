#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de test pour la publication via le connecteur WordPress
Permet de tester la mise à jour des métadonnées SEO d'un article existant
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
    
    log_file = os.path.join(log_dir, "test_post.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8-sig"),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger("test_wp_post")

def main():
    # Initialisation du parser d'arguments
    parser = argparse.ArgumentParser(description="Test de publication WordPress")
    
    # Arguments
    parser.add_argument("--url", required=True, help="URL du site WordPress")
    parser.add_argument("--token", required=True, help="Jeton d'authentification WordPress (mot de passe d'application)")
    parser.add_argument("--id", type=int, required=True, help="ID de l'article à mettre à jour")
    parser.add_argument("--type", default="post", help="Type de contenu (par défaut: post)")
    parser.add_argument("--title", help="Nouveau titre SEO (optionnel)")
    parser.add_argument("--description", help="Nouvelle description SEO (optionnel)")
    parser.add_argument("--h1", help="Nouveau titre H1 (optionnel)")
    
    # Analyse des arguments
    args = parser.parse_args()
    
    # Initialisation du logger
    logger = setup_logging()
    logger.info("Démarrage du test de publication WordPress")
    
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
    
    # Récupération directe de l'article par son ID
    logger.info(f"Récupération directe de l'article {args.id}")
    try:
        # Construction de l'URL pour récupérer l'article spécifique
        site_base_url = wp_connector.site_url
        endpoint = wp_connector.REST_ENDPOINTS.get(args.type, args.type)
        api_url = f"{site_base_url}/wp-json/wp/v2/{endpoint}/{args.id}"
        
        logger.info(f"Requête API: {api_url}")
        
        import requests
        response = requests.get(
            api_url,
            headers=wp_connector.get_headers(),
            params={"_embed": "true"},
            timeout=10
        )
        
        if response.status_code == 200:
            item = response.json()
            metadata = wp_connector.extract_seo_metadata(item)
            
            # Affichage des métadonnées actuelles
            print("\nMétadonnées actuelles:")
            print(f"Titre SEO: {metadata['seo_title']}")
            print(f"Description SEO: {metadata['seo_description']}")
            print(f"Titre H1: {item.get('title', {}).get('rendered', '')}")
            
            # Utilisation des valeurs actuelles si non spécifiées
            seo_title = args.title if args.title else metadata['seo_title']
            seo_description = args.description if args.description else metadata['seo_description']
            title_h1 = args.h1 if args.h1 else None
            
            # Mise à jour des métadonnées
            logger.info(f"Mise à jour des métadonnées de l'article {args.id}")
            success, message = wp_connector.update_seo_metadata(
                args.id,
                args.type,
                seo_title,
                seo_description,
                title_h1
            )
            
            if success:
                logger.info(f"Mise à jour réussie: {message}")
                print(f"\nMise à jour réussie: {message}")
                print("\nNouvelles métadonnées:")
                print(f"Titre SEO: {seo_title}")
                print(f"Description SEO: {seo_description}")
                if title_h1:
                    print(f"Titre H1: {title_h1}")
            else:
                logger.error(f"Échec de la mise à jour: {message}")
                print(f"\nÉchec de la mise à jour: {message}")
                
                # Affichage des détails de l'erreur
                print("\nDétails de l'erreur:")
                print(message)
        else:
            logger.error(f"Échec de la récupération de l'article: {response.status_code} - {response.text}")
            print(f"Échec de la récupération de l'article: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'article: {str(e)}")
        print(f"Erreur lors de la récupération de l'article: {str(e)}")

if __name__ == "__main__":
    main()
