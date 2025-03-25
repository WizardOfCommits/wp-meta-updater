#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de test pour l'importation CSV avec différents séparateurs
"""

import logging
import sys
from data_manager import DataManager

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("test_csv_import")

def main():
    """Fonction principale de test"""
    # Création du gestionnaire de données
    data_manager = DataManager(logger)
    
    # Initialisation avec des données fictives pour simuler une importation WordPress
    content_data = {
        "post": [
            {
                "id": 1,
                "title": "Original Post",
                "link": "https://example.com/post/1",
                "modified": "2025-03-24T12:00:00",
                "seo_title": "Original SEO Title",
                "seo_description": "Original SEO Description"
            },
            {
                "id": 3,
                "title": "Original Another Post",
                "link": "https://example.com/post/3",
                "modified": "2025-03-24T12:00:00",
                "seo_title": "Original Another SEO Title",
                "seo_description": "Original Another SEO Description"
            }
        ],
        "page": [
            {
                "id": 2,
                "title": "Original Page",
                "link": "https://example.com/page/2",
                "modified": "2025-03-24T12:00:00",
                "seo_title": "Original Page SEO Title",
                "seo_description": "Original Page SEO Description"
            },
            {
                "id": 4,
                "title": "Original Another Page",
                "link": "https://example.com/page/4",
                "modified": "2025-03-24T12:00:00",
                "seo_title": "Original Another Page SEO Title",
                "seo_description": "Original Another Page SEO Description"
            }
        ]
    }
    
    # Importation des données WordPress
    data_manager.import_from_wp(content_data)
    
    # Test d'importation avec séparateur point-virgule
    logger.info("=== Test d'importation avec séparateur point-virgule ===")
    success, message, count = data_manager.import_from_csv("import-test-semicolon.csv")
    logger.info(f"Résultat: {success}, {message}, {count} éléments importés")
    
    # Test d'importation avec séparateur virgule
    logger.info("=== Test d'importation avec séparateur virgule ===")
    success, message, count = data_manager.import_from_csv("import-test-comma.csv")
    logger.info(f"Résultat: {success}, {message}, {count} éléments importés")
    
    # Affichage des données mises à jour
    logger.info("=== Données après importation ===")
    for content_type, items in data_manager.data.items():
        for item in items:
            logger.info(f"ID: {item['id']}, Type: {item['type']}, Titre: {item['title']}, Titre SEO: {item['seo_title']}, Description SEO: {item['seo_description']}")

if __name__ == "__main__":
    main()
