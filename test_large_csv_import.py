#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de test pour l'importation de fichiers CSV volumineux
"""

import os
import sys
import logging
import time
import pandas as pd
from data_manager import DataManager

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/test_large_csv_import.log", mode="w")
    ]
)
logger = logging.getLogger("test_large_csv_import")

def generate_large_csv(filename, num_rows=10000, existing_ids=[1, 2]):
    """
    Génère un fichier CSV volumineux pour les tests
    
    Args:
        filename: Nom du fichier CSV à générer
        num_rows: Nombre de lignes à générer
        existing_ids: Liste des IDs existants à inclure dans le CSV
    """
    logger.info(f"Génération d'un fichier CSV volumineux avec {num_rows} lignes...")
    
    # Création des données
    data = []
    
    # D'abord, inclure les IDs existants pour tester la mise à jour
    for id_value in existing_ids:
        data.append({
            "id": id_value,
            "type": "post" if id_value == 1 else "page",
            "title": f"Updated Title {id_value}",
            "url": f"https://example.com/test-{id_value}",
            "date_modified": "2025-03-24T12:00:00",
            "seo_title": f"Updated SEO Title {id_value} - Optimized for Search Engines",
            "seo_description": f"This is an updated SEO description {id_value} that tests the performance of the import function with existing IDs."
        })
    
    # Ensuite, ajouter des lignes supplémentaires avec de nouveaux IDs
    start_id = max(existing_ids) + 1 if existing_ids else 1
    for i in range(start_id, start_id + num_rows - len(existing_ids)):
        data.append({
            "id": i,
            "type": "post" if i % 2 == 0 else "page",
            "title": f"Test Title {i}",
            "url": f"https://example.com/test-{i}",
            "date_modified": "2025-03-24T12:00:00",
            "seo_title": f"Test SEO Title {i} - Optimized for Search Engines with Keywords",
            "seo_description": f"This is a test SEO description {i} that is designed to be long enough to test the performance of the import function with a large dataset. It includes various keywords and phrases that might be used in real SEO descriptions."
        })
    
    # Création du DataFrame
    df = pd.DataFrame(data)
    
    # Exportation vers CSV
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    
    file_size_mb = os.path.getsize(filename) / (1024 * 1024)
    logger.info(f"Fichier CSV généré: {filename} ({file_size_mb:.2f} MB)")
    
    return filename

def test_import_performance(csv_file, separator=","):
    """
    Teste les performances de l'importation CSV
    
    Args:
        csv_file: Chemin du fichier CSV à importer
        separator: Séparateur CSV
    """
    logger.info(f"Test d'importation du fichier {csv_file}...")
    
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
            }
        ]
    }
    
    # Importation des données WordPress
    data_manager.import_from_wp(content_data)
    
    # Connexion du signal de progression
    def on_import_progress(current, total, message):
        logger.info(f"Progression: {current}/{total} - {message}")
    
    data_manager.import_progress.connect(on_import_progress)
    
    # Mesure du temps d'importation
    start_time = time.time()
    
    # Importation du fichier CSV
    success, message, count = data_manager.import_from_csv(csv_file, separator)
    
    # Calcul du temps écoulé
    elapsed_time = time.time() - start_time
    
    # Affichage des résultats
    logger.info(f"Résultat: {success}, {message}")
    logger.info(f"Temps d'importation: {elapsed_time:.2f} secondes")
    logger.info(f"Vitesse: {count / elapsed_time:.2f} éléments/seconde")
    
    # Affichage des statistiques de mémoire
    import psutil
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    logger.info(f"Utilisation mémoire: {memory_info.rss / (1024 * 1024):.2f} MB")
    
    return success, count, elapsed_time

def main():
    """Fonction principale de test"""
    logger.info("=== Test d'importation de fichiers CSV volumineux ===")
    
    # Test avec différentes tailles de fichiers
    test_sizes = [100, 1000, 5000]
    
    for size in test_sizes:
        logger.info(f"\n=== Test avec {size} lignes ===")
        
        # Génération d'un fichier CSV volumineux
        csv_file = f"test_large_import_{size}.csv"
        generate_large_csv(csv_file, num_rows=size, existing_ids=[1, 2])
        
        # Test d'importation
        success, count, elapsed_time = test_import_performance(csv_file)
        
        # Nettoyage
        if os.path.exists(csv_file) and success:
            os.remove(csv_file)
            logger.info(f"Fichier de test {csv_file} supprimé")

if __name__ == "__main__":
    main()
