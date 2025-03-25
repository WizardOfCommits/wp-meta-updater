#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de test pour la création d'articles via le connecteur WordPress
Permet de tester la création d'un nouvel article via l'API REST WordPress
"""

import os
import sys
import logging
import argparse
import requests
import json
from datetime import datetime
from wp_connector import WordPressConnector

# Configuration du logging
def setup_logging():
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, "test_create.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8-sig"),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger("test_wp_create")

def main():
    # Initialisation du parser d'arguments
    parser = argparse.ArgumentParser(description="Test de création d'article WordPress")
    
    # Arguments
    parser.add_argument("--url", required=True, help="URL du site WordPress")
    parser.add_argument("--token", required=True, help="Jeton d'authentification WordPress (mot de passe d'application)")
    parser.add_argument("--title", required=True, help="Titre de l'article")
    parser.add_argument("--content", required=True, help="Contenu de l'article")
    parser.add_argument("--excerpt", help="Extrait de l'article (optionnel)")
    parser.add_argument("--status", default="draft", choices=["draft", "publish", "pending", "private"], help="Statut de l'article (par défaut: draft)")
    parser.add_argument("--type", default="post", help="Type de contenu (par défaut: post)")
    parser.add_argument("--seo-title", help="Titre SEO (optionnel)")
    parser.add_argument("--seo-description", help="Description SEO (optionnel)")
    
    # Analyse des arguments
    args = parser.parse_args()
    
    # Initialisation du logger
    logger = setup_logging()
    logger.info("Démarrage du test de création d'article WordPress")
    
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
    
    # Création de l'article
    logger.info("Création d'un nouvel article")
    
    # Préparation des données de l'article
    post_data = {
        "title": args.title,
        "content": args.content,
        "status": args.status
    }
    
    # Ajout de l'extrait si spécifié
    if args.excerpt:
        post_data["excerpt"] = args.excerpt
    
    # Ajout des métadonnées SEO si spécifiées
    if args.seo_title or args.seo_description:
        post_data["meta"] = {}
        
        if args.seo_title:
            # Ajout du titre SEO pour différents plugins
            post_data["meta"]["_yoast_wpseo_title"] = args.seo_title
            post_data["meta"]["rank_math_title"] = args.seo_title
            post_data["meta"]["_aioseo_title"] = args.seo_title
            post_data["meta"]["_seopress_titles_title"] = args.seo_title
        
        if args.seo_description:
            # Ajout de la description SEO pour différents plugins
            post_data["meta"]["_yoast_wpseo_metadesc"] = args.seo_description
            post_data["meta"]["rank_math_description"] = args.seo_description
            post_data["meta"]["_aioseo_description"] = args.seo_description
            post_data["meta"]["_seopress_titles_desc"] = args.seo_description
    
    try:
        # Construction de l'URL pour créer l'article
        site_base_url = wp_connector.site_url
        endpoint = wp_connector.REST_ENDPOINTS.get(args.type, args.type)
        api_url = f"{site_base_url}/wp-json/wp/v2/{endpoint}"
        
        logger.info(f"Requête API: {api_url}")
        logger.debug(f"Données: {json.dumps(post_data, indent=2)}")
        
        # Envoi de la requête
        response = requests.post(
            api_url,
            headers=wp_connector.get_headers(),
            json=post_data,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            # Création réussie
            new_post = response.json()
            logger.info(f"Article créé avec succès (ID: {new_post.get('id')})")
            
            print(f"\nArticle créé avec succès!")
            print(f"ID: {new_post.get('id')}")
            print(f"Titre: {new_post.get('title', {}).get('rendered', '')}")
            print(f"Statut: {new_post.get('status', '')}")
            print(f"URL: {new_post.get('link', '')}")
            
            # Affichage des métadonnées SEO si disponibles
            if "meta" in new_post:
                print("\nMétadonnées SEO:")
                for key, value in new_post["meta"].items():
                    if "title" in key.lower() or "titre" in key.lower():
                        print(f"Titre SEO ({key}): {value}")
                    elif "desc" in key.lower():
                        print(f"Description SEO ({key}): {value}")
        else:
            # Échec de la création
            logger.error(f"Échec de la création: {response.status_code} - {response.text}")
            print(f"\nÉchec de la création: {response.status_code}")
            print(f"Erreur: {response.text}")
    except Exception as e:
        logger.error(f"Erreur lors de la création de l'article: {str(e)}")
        print(f"Erreur lors de la création de l'article: {str(e)}")

if __name__ == "__main__":
    main()
