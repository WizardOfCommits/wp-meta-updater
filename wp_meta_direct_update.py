#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
WordPress Meta Direct Update
Script pour mettre à jour directement les métadonnées SEO dans la base de données WordPress
Contourne les restrictions d'autorisation de l'API REST
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

# Importation conditionnelle de mysql.connector
try:
    import mysql.connector
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False
    print("Module mysql.connector non trouvé. Veuillez l'installer avec 'pip install mysql-connector-python'")

# Configuration du logging
def setup_logging():
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, "direct_update.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8-sig"),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger("wp_meta_direct_update")

class WordPressDirectConnector:
    """Classe pour se connecter directement à la base de données WordPress"""
    
    # Paramètres de traitement par lots pour les mises à jour massives
    BATCH_SIZE = 20       # Nombre d'éléments par lot
    BATCH_DELAY_MS = 200  # Délai entre les lots en millisecondes
    GC_FREQUENCY = 5      # Fréquence d'exécution du garbage collector (tous les X lots)
    
    def __init__(self, logger: logging.Logger):
        """Initialisation du connecteur direct"""
        self.logger = logger
        self.connection = None
        self.cursor = None
        self.db_config = {}
        self.table_prefix = "wp_"
        
        # Vérification de la disponibilité du module MySQL
        if not MYSQL_AVAILABLE:
            self.logger.warning("Module mysql.connector non disponible. Les fonctionnalités MySQL seront désactivées.")
    
    def configure(self, host: str, user: str, password: str, database: str, table_prefix: str = "wp_"):
        """Configure les paramètres de connexion à la base de données"""
        self.db_config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database
        }
        self.table_prefix = table_prefix
        self.logger.info(f"Configuration de la connexion à la base de données {database} sur {host}")
    
    def connect(self) -> bool:
        """Établit la connexion à la base de données"""
        if not MYSQL_AVAILABLE:
            self.logger.error("Impossible de se connecter: module mysql.connector non disponible")
            return False
            
        try:
            self.connection = mysql.connector.connect(**self.db_config)
            self.cursor = self.connection.cursor(dictionary=True)
            self.logger.info("Connexion à la base de données établie")
            return True
        except Exception as e:
            self.logger.error(f"Erreur lors de la connexion à la base de données: {str(e)}")
            return False
    
    def disconnect(self):
        """Ferme la connexion à la base de données"""
        if self.cursor:
            self.cursor.close()
        
        if self.connection:
            self.connection.close()
        
        self.logger.info("Connexion à la base de données fermée")
    
    def get_post(self, post_id: int) -> Optional[Dict[str, Any]]:
        """
        Récupère un article par son ID
        
        Args:
            post_id: ID de l'article
            
        Returns:
            Dictionnaire contenant les informations de l'article, ou None si non trouvé
        """
        if not MYSQL_AVAILABLE or not self.connection:
            self.logger.error("Connexion MySQL non disponible")
            return None
            
        try:
            # Requête pour récupérer l'article
            query = f"""
                SELECT p.*, pm.*
                FROM {self.table_prefix}posts p
                LEFT JOIN {self.table_prefix}postmeta pm ON p.ID = pm.post_id
                WHERE p.ID = %s
            """
            
            self.cursor.execute(query, (post_id,))
            rows = self.cursor.fetchall()
            
            if not rows:
                self.logger.warning(f"Article {post_id} non trouvé")
                return None
            
            # Regroupement des métadonnées
            post_data = rows[0].copy()
            post_data["meta"] = {}
            
            for row in rows:
                if row["meta_key"] and row["meta_value"]:
                    post_data["meta"][row["meta_key"]] = row["meta_value"]
            
            return post_data
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération de l'article {post_id}: {str(e)}")
            return None
    
    def update_seo_metadata(self, post_id: int, seo_title: str, seo_description: str, title: str = None) -> Tuple[bool, str]:
        """
        Met à jour les métadonnées SEO d'un article
        
        Args:
            post_id: ID de l'article
            seo_title: Nouveau titre SEO
            seo_description: Nouvelle description SEO
            title: Nouveau titre H1 (None = pas de changement)
            
        Returns:
            Tuple (succès, message)
        """
        if not MYSQL_AVAILABLE or not self.connection:
            return False, "Connexion MySQL non disponible"
            
        try:
            # Vérification si l'article existe
            post = self.get_post(post_id)
            
            if not post:
                return False, f"Article {post_id} non trouvé"
            
            # Détection du plugin SEO utilisé
            seo_plugin = self.detect_seo_plugin(post)
            
            if not seo_plugin:
                self.logger.warning(f"Aucun plugin SEO détecté pour l'article {post_id}")
                seo_plugin = "generic"
            
            # Mise à jour des métadonnées en fonction du plugin
            if seo_plugin == "yoast":
                # Yoast SEO
                self.update_postmeta(post_id, "_yoast_wpseo_title", seo_title)
                self.update_postmeta(post_id, "_yoast_wpseo_metadesc", seo_description)
            elif seo_plugin == "rank_math":
                # Rank Math
                self.update_postmeta(post_id, "rank_math_title", seo_title)
                self.update_postmeta(post_id, "rank_math_description", seo_description)
            elif seo_plugin == "aioseo":
                # All in One SEO
                self.update_postmeta(post_id, "_aioseo_title", seo_title)
                self.update_postmeta(post_id, "_aioseo_description", seo_description)
            elif seo_plugin == "seopress":
                # SEOPress
                self.update_postmeta(post_id, "_seopress_titles_title", seo_title)
                self.update_postmeta(post_id, "_seopress_titles_desc", seo_description)
            else:
                # Générique
                self.update_postmeta(post_id, "seo_title", seo_title)
                self.update_postmeta(post_id, "seo_description", seo_description)
            
            # Mise à jour du titre H1 si spécifié
            if title:
                query = f"""
                    UPDATE {self.table_prefix}posts
                    SET post_title = %s
                    WHERE ID = %s
                """
                
                self.cursor.execute(query, (title, post_id))
                self.connection.commit()
            
            self.logger.info(f"Métadonnées SEO mises à jour pour l'article {post_id}")
            return True, "Métadonnées SEO mises à jour avec succès"
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la mise à jour des métadonnées SEO de l'article {post_id}: {str(e)}")
            return False, str(e)
    
    def update_postmeta(self, post_id: int, meta_key: str, meta_value: str) -> bool:
        """
        Met à jour une métadonnée d'un article
        
        Args:
            post_id: ID de l'article
            meta_key: Clé de la métadonnée
            meta_value: Valeur de la métadonnée
            
        Returns:
            Succès de la mise à jour
        """
        if not MYSQL_AVAILABLE or not self.connection:
            return False
            
        try:
            # Vérification si la métadonnée existe déjà
            query = f"""
                SELECT meta_id
                FROM {self.table_prefix}postmeta
                WHERE post_id = %s AND meta_key = %s
            """
            
            self.cursor.execute(query, (post_id, meta_key))
            result = self.cursor.fetchone()
            
            if result:
                # Mise à jour de la métadonnée existante
                query = f"""
                    UPDATE {self.table_prefix}postmeta
                    SET meta_value = %s
                    WHERE post_id = %s AND meta_key = %s
                """
                
                self.cursor.execute(query, (meta_value, post_id, meta_key))
            else:
                # Création d'une nouvelle métadonnée
                query = f"""
                    INSERT INTO {self.table_prefix}postmeta (post_id, meta_key, meta_value)
                    VALUES (%s, %s, %s)
                """
                
                self.cursor.execute(query, (post_id, meta_key, meta_value))
            
            self.connection.commit()
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la mise à jour de la métadonnée {meta_key} pour l'article {post_id}: {str(e)}")
            return False
    
    def detect_seo_plugin(self, post: Dict[str, Any]) -> Optional[str]:
        """
        Détecte le plugin SEO utilisé pour un article
        
        Args:
            post: Données de l'article
            
        Returns:
            Nom du plugin SEO détecté, ou None si aucun plugin n'est détecté
        """
        meta = post.get("meta", {})
        
        # Yoast SEO
        if "_yoast_wpseo_title" in meta or "_yoast_wpseo_metadesc" in meta:
            return "yoast"
        
        # Rank Math
        if "rank_math_title" in meta or "rank_math_description" in meta:
            return "rank_math"
        
        # All in One SEO
        if "_aioseo_title" in meta or "_aioseo_description" in meta:
            return "aioseo"
        
        # SEOPress
        if "_seopress_titles_title" in meta or "_seopress_titles_desc" in meta:
            return "seopress"
        
        return None
    
    def bulk_update_metadata(self, items: List[Dict[str, Any]], callback=None) -> Dict[str, Any]:
        """
        Met à jour les métadonnées SEO de plusieurs articles en masse avec traitement par lots
        
        Args:
            items: Liste des articles à mettre à jour
            callback: Fonction de rappel pour suivre la progression
            
        Returns:
            Statistiques de mise à jour
        """
        import gc
        import time
        
        stats = {
            "total": len(items),
            "success": 0,
            "failed": 0,
            "errors": []
        }
        
        if not items:
            return stats
            
        if not MYSQL_AVAILABLE or not self.connection:
            stats["failed"] = len(items)
            stats["errors"].append({
                "id": 0,
                "type": "system",
                "title": "Erreur système",
                "error": "Connexion MySQL non disponible"
            })
            return stats
        
        # Nombre total d'éléments pour le calcul de progression
        total_items = len(items)
        current_progress = 0
        
        # Diviser les éléments en lots
        batches = [items[i:i + self.BATCH_SIZE] for i in range(0, len(items), self.BATCH_SIZE)]
        self.logger.info(f"Traitement de {len(items)} éléments en {len(batches)} lots de {self.BATCH_SIZE} maximum")
        
        # Traitement de chaque lot
        for batch_index, batch in enumerate(batches):
            self.logger.info(f"Traitement du lot {batch_index + 1}/{len(batches)} ({len(batch)} éléments)")
            
            # Exécution du garbage collector périodiquement
            if batch_index % self.GC_FREQUENCY == 0 and batch_index > 0:
                self.logger.info("Exécution du garbage collector")
                collected = gc.collect()
                self.logger.info(f"Objets collectés: {collected}")
            
            # Traitement des éléments du lot
            for item in batch:
                # Vérification si le titre H1 est présent dans l'élément
                title = item.get("title_h1") if "title_h1" in item else None
                
                # Mise à jour des métadonnées
                success, message = self.update_seo_metadata(
                    item["id"],
                    item["seo_title"],
                    item["seo_description"],
                    title
                )
                
                if success:
                    stats["success"] += 1
                else:
                    stats["failed"] += 1
                    stats["errors"].append({
                        "id": item["id"],
                        "type": item.get("type", "post"),
                        "title": item.get("title", ""),
                        "error": message
                    })
                
                # Mise à jour de la progression
                current_progress += 1
                if callback:
                    callback(current_progress, total_items)
            
            # Pause entre les lots pour éviter de surcharger la base de données
            if batch_index < len(batches) - 1:  # Pas de pause après le dernier lot
                self.logger.info(f"Pause de {self.BATCH_DELAY_MS}ms entre les lots")
                time.sleep(self.BATCH_DELAY_MS / 1000)
        
        self.logger.info(f"Mise à jour en masse terminée: {stats['success']} réussies, {stats['failed']} échouées")
        return stats

def import_from_csv(filepath: str) -> List[Dict[str, Any]]:
    """
    Importe les données depuis un fichier CSV
    
    Args:
        filepath: Chemin du fichier CSV
        
    Returns:
        Liste des éléments importés
    """
    try:
        # Lecture du fichier CSV
        df = pd.read_csv(filepath, encoding="utf-8-sig", sep='\t')
        
        # Vérification des colonnes requises
        required_columns = ["id", "type"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"Colonnes requises manquantes: {', '.join(missing_columns)}")
            return []
        
        # Conversion en liste de dictionnaires
        csv_data = df.to_dict(orient="records")
        
        # Filtrage des éléments avec des métadonnées SEO
        items_to_update = []
        
        for item in csv_data:
            if "seo_title" in item or "seo_description" in item or "title_h1" in item:
                items_to_update.append(item)
        
        return items_to_update
        
    except Exception as e:
        print(f"Erreur lors de l'importation CSV: {str(e)}")
        return []

def main():
    # Vérification de la disponibilité du module MySQL
    if not MYSQL_AVAILABLE:
        print("Erreur: Le module mysql.connector n'est pas installé.")
        print("Veuillez l'installer avec la commande: pip install mysql-connector-python")
        return
        
    # Initialisation du parser d'arguments
    parser = argparse.ArgumentParser(description="WordPress Meta Direct Update - Mise à jour directe des métadonnées SEO dans la base de données WordPress")
    
    # Arguments de connexion à la base de données
    parser.add_argument("--host", required=True, help="Hôte de la base de données MySQL")
    parser.add_argument("--user", required=True, help="Nom d'utilisateur MySQL")
    parser.add_argument("--password", required=True, help="Mot de passe MySQL")
    parser.add_argument("--database", required=True, help="Nom de la base de données WordPress")
    parser.add_argument("--prefix", default="wp_", help="Préfixe des tables WordPress (par défaut: wp_)")
    
    # Arguments d'importation
    parser.add_argument("--input", required=True, help="Chemin du fichier CSV d'entrée")
    
    # Analyse des arguments
    args = parser.parse_args()
    
    # Initialisation du logger
    logger = setup_logging()
    logger.info("Démarrage de l'application de mise à jour directe")
    
    # Initialisation du connecteur direct
    wp_direct = WordPressDirectConnector(logger)
    
    # Configuration de la connexion à la base de données
    wp_direct.configure(args.host, args.user, args.password, args.database, args.prefix)
    
    # Connexion à la base de données
    if not wp_direct.connect():
        print("Échec de la connexion à la base de données")
        return
    
    # Importation des données depuis le CSV
    print(f"Importation des données depuis {args.input}...")
    items_to_update = import_from_csv(args.input)
    
    if not items_to_update:
        print("Aucun élément à mettre à jour")
        wp_direct.disconnect()
        return
    
    # Fonction de callback pour la progression
    def progress_callback(current, total):
        print(f"Progression: {current}/{total}")
    
    # Mise à jour des métadonnées
    print(f"Mise à jour de {len(items_to_update)} éléments...")
    stats = wp_direct.bulk_update_metadata(items_to_update, progress_callback)
    
    # Affichage des résultats
    print(f"Mise à jour terminée: {stats['success']} réussies, {stats['failed']} échouées")
    
    if stats["failed"] > 0:
        print("Erreurs:")
        for error in stats.get("errors", []):
            print(f"  - {error['type']} {error['id']} ({error['title']}): {error['error']}")
    
    # Fermeture de la connexion
    wp_direct.disconnect()

if __name__ == "__main__":
    main()
