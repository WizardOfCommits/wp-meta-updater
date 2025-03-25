#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de test pour la mise à jour par lots des métadonnées SEO
Ce script permet de tester la solution implémentée pour résoudre le problème de crash
lors des mises à jour massives de métadonnées SEO.
"""

import os
import sys
import logging
import time
import csv
import random
from typing import List, Dict, Any

# Ajout du répertoire courant au chemin de recherche des modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import des modules nécessaires
from wp_connector import WordPressConnector
from data_manager import DataManager

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/test_batch_update.log", encoding="utf-8-sig"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("test_batch_update")

def load_csv_data(csv_file: str) -> List[Dict[str, Any]]:
    """
    Charge les données depuis un fichier CSV
    
    Args:
        csv_file: Chemin du fichier CSV
        
    Returns:
        Liste des éléments chargés
    """
    items = []
    
    try:
        with open(csv_file, 'r', encoding='utf-8-sig') as f:
            # Détection du délimiteur
            sample = f.read(4096)
            f.seek(0)
            
            if ';' in sample:
                delimiter = ';'
            else:
                delimiter = ','
            
            reader = csv.DictReader(f, delimiter=delimiter)
            
            for row in reader:
                # Conversion des champs
                item = {
                    "id": int(row.get("id", 0)),
                    "type": row.get("type", "post"),
                    "title": row.get("title", ""),
                    "url": row.get("url", ""),
                    "seo_title": row.get("seo_title", ""),
                    "seo_description": row.get("seo_description", ""),
                    "original_seo_title": row.get("seo_title", ""),
                    "original_seo_description": row.get("seo_description", "")
                }
                
                items.append(item)
    
    except Exception as e:
        logger.error(f"Erreur lors du chargement du fichier CSV: {str(e)}")
    
    return items

def modify_items(items: List[Dict[str, Any]], modification_rate: float = 0.5) -> List[Dict[str, Any]]:
    """
    Modifie aléatoirement une partie des éléments pour simuler des changements
    
    Args:
        items: Liste des éléments à modifier
        modification_rate: Taux de modification (0.0 - 1.0)
        
    Returns:
        Liste des éléments modifiés
    """
    modified_items = []
    
    for item in items:
        # Décision aléatoire de modifier l'élément
        if random.random() < modification_rate:
            # Copie de l'élément
            modified_item = item.copy()
            
            # Modification du titre SEO
            modified_item["seo_title"] = f"[TEST] {item['seo_title']}"
            
            # Modification de la description SEO
            modified_item["seo_description"] = f"[TEST] {item['seo_description']}"
            
            modified_items.append(modified_item)
    
    return modified_items

def progress_callback(current: int, total: int) -> None:
    """
    Fonction de rappel pour suivre la progression
    
    Args:
        current: Élément actuel
        total: Nombre total d'éléments
    """
    progress = (current / total) * 100
    logger.info(f"Progression: {current}/{total} ({progress:.1f}%)")

def main():
    """Fonction principale"""
    logger.info("Démarrage du test de mise à jour par lots")
    
    # Paramètres de test
    csv_file = "data/meta-data-1min30.csv"  # Fichier CSV contenant les métadonnées
    api_url = "http://localhost/wordpress"  # URL du site WordPress
    auth_token = "admin password"           # Jeton d'authentification
    modification_rate = 0.5                 # Taux de modification des éléments
    
    # Chargement des données
    logger.info(f"Chargement des données depuis {csv_file}")
    items = load_csv_data(csv_file)
    logger.info(f"{len(items)} éléments chargés")
    
    # Modification des éléments
    logger.info(f"Modification aléatoire des éléments (taux: {modification_rate})")
    modified_items = modify_items(items, modification_rate)
    logger.info(f"{len(modified_items)} éléments modifiés")
    
    # Initialisation du connecteur WordPress
    logger.info("Initialisation du connecteur WordPress")
    wp_connector = WordPressConnector(logger)
    wp_connector.configure(api_url, auth_token)
    
    # Affichage des paramètres de traitement par lots
    logger.info(f"Paramètres de traitement par lots:")
    logger.info(f"- BATCH_SIZE: {wp_connector.BATCH_SIZE}")
    logger.info(f"- BATCH_DELAY_MS: {wp_connector.BATCH_DELAY_MS}")
    logger.info(f"- MAX_RETRIES: {wp_connector.MAX_RETRIES}")
    logger.info(f"- GC_FREQUENCY: {wp_connector.GC_FREQUENCY}")
    logger.info(f"- max_workers: {wp_connector.max_workers}")
    
    # Test de connexion
    logger.info("Test de connexion à WordPress")
    success, message = wp_connector.test_connection()
    
    if not success:
        logger.error(f"Échec de la connexion: {message}")
        return
    
    logger.info(f"Connexion réussie: {message}")
    
    # Mise à jour des métadonnées
    logger.info(f"Début de la mise à jour de {len(modified_items)} éléments")
    start_time = time.time()
    
    stats = wp_connector.bulk_update_metadata(modified_items, progress_callback)
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Affichage des statistiques
    logger.info(f"Mise à jour terminée en {duration:.2f} secondes")
    logger.info(f"Statistiques:")
    logger.info(f"- Total: {stats['total']}")
    logger.info(f"- Réussies: {stats['success']}")
    logger.info(f"- Échouées: {stats['failed']}")
    logger.info(f"- Reprises: {stats.get('retries', 0)}")
    
    # Affichage des erreurs
    if stats['failed'] > 0:
        logger.info(f"Erreurs:")
        for error in stats.get('errors', [])[:10]:  # Afficher les 10 premières erreurs
            logger.info(f"- ID {error['id']} ({error['type']}): {error['error']}")
        
        if len(stats.get('errors', [])) > 10:
            logger.info(f"... et {len(stats.get('errors', [])) - 10} autres erreurs")
    
    logger.info("Test terminé")

if __name__ == "__main__":
    main()
