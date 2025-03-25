#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module de connexion à l'API WordPress
Gère toutes les interactions avec l'API REST de WordPress
"""

import logging
import requests
import json
import time
import gc
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

class WordPressConnector:
    """Classe pour gérer les connexions à l'API WordPress"""
    
    # Paramètres de traitement par lots pour les mises à jour massives
    BATCH_SIZE = 5        # Nombre d'éléments par lot (réduit de 10 à 5)
    BATCH_DELAY_MS = 2000 # Délai entre les lots en millisecondes (augmenté de 1000 à 2000)
    MAX_RETRIES = 5       # Nombre maximum de tentatives en cas d'échec (augmenté de 3 à 5)
    RETRY_DELAY_MS = 1000 # Délai initial entre les tentatives en millisecondes
    RETRY_BACKOFF = 2     # Facteur multiplicatif pour le délai exponentiel
    GC_FREQUENCY = 3      # Fréquence d'exécution du garbage collector (tous les X lots)
    
    # Types de contenu WordPress supportés
    CONTENT_TYPES = {
        "post": "Articles",
        "page": "Pages",
        "product": "Produits",
        "attachment": "Médias",
        "custom": "Types personnalisés"
    }
    
    # Correspondance entre les types de contenu et les endpoints REST API
    REST_ENDPOINTS = {
        "post": "posts",
        "page": "pages",
        "product": "products",
        "attachment": "media",
        # Les types personnalisés seront ajoutés dynamiquement
    }
    
    def __init__(self, logger: logging.Logger):
        """Initialisation du connecteur WordPress"""
        self.logger = logger
        self.api_url = ""
        self.auth_token = ""
        self.site_name = ""
        self.max_workers = 5  # Nombre maximum de threads pour les requêtes parallèles
        self.custom_types = []  # Types de contenu personnalisés
    
    def configure(self, site_url: str, auth_token: str, site_name: str = "", username: str = "") -> None:
        """Configure les paramètres de connexion à l'API"""
        # Normalisation de l'URL du site
        if site_url.endswith('/'):
            site_url = site_url[:-1]
        
        # Stockage de l'URL de base sans le chemin API pour une utilisation ultérieure
        self.site_url = site_url
        self.api_url = f"{site_url}/wp-json/wp/v2"
        self.auth_token = auth_token
        self.username = username
        self.site_name = site_name or site_url.replace('https://', '').replace('http://', '').split('/')[0]
        self.logger.info(f"Configuration de la connexion à {self.site_name}")
    
    def get_headers(self) -> Dict[str, str]:
        """Retourne les en-têtes HTTP pour les requêtes API"""
        import base64
        import random
        import socket
        
        # En-têtes de base pour toutes les requêtes
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": f"WP-Meta-Updater/1.0 (Python/{socket.gethostname()})",
            "X-WP-Nonce": f"{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache"
        }
        
        # Journalisation du jeton d'authentification (masqué pour la sécurité)
        token_preview = self.auth_token[:4] + "..." + self.auth_token[-4:] if len(self.auth_token) > 8 else "***"
        self.logger.info(f"Génération des en-têtes d'authentification pour le jeton: {token_preview}")
        
        # Détermination du nom d'utilisateur et du mot de passe
        # Utiliser le nom d'utilisateur spécifié s'il existe
        if hasattr(self, 'username') and self.username:
            username = self.username
            password = self.auth_token
            self.logger.info(f"Utilisation du nom d'utilisateur personnalisé: {username}")
        else:
            # Comportement de secours - essayer de déterminer le nom d'utilisateur à partir du token
            # Format spécifique pour Application Passwords WordPress
            # Les Application Passwords WordPress sont généralement au format:
            # XXXX XXXX XXXX XXXX XXXX XXXX (plusieurs groupes de 4 caractères séparés par des espaces)
            
            # Vérification du format avec des espaces (Application Password typique)
            if ' ' in self.auth_token and len(self.auth_token.split()) > 1:
                # Pour le format Application Password WordPress, nous devons extraire le nom d'utilisateur
                # Format typique: soit "username password" soit juste le password (avec nom d'utilisateur implicite)
                
                # Si le premier segment est le nom d'utilisateur
                parts = self.auth_token.split()
                if len(parts) >= 2 and len(parts[0]) == 4 and all(len(part) == 4 for part in parts[1:]):
                    # C'est probablement un mot de passe d'application complet
                    username = "admin"  # Nom d'utilisateur par défaut
                    password = self.auth_token
                    self.logger.info(f"Détection d'un Application Password WordPress (format complet)")
                else:
                    # Format "username password"
                    username, password = self.auth_token.split(' ', 1)
                    self.logger.info(f"Détection du format username password: {username}")
            else:
                # Si pas d'espace, on utilise un nom d'utilisateur par défaut
                username = "admin"  # Nom d'utilisateur par défaut
                password = self.auth_token
                self.logger.info(f"Utilisation du format simple token avec nom d'utilisateur par défaut: {username}")
        
        self.logger.info(f"Utilisation de l'authentification Basic pour '{username}'")
        
        # Création de la chaîne d'authentification au format username:password
        auth_string = f"{username}:{password}"
        
        # Encodage en base64 pour l'authentification Basic
        auth_encoded = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
        headers["Authorization"] = f"Basic {auth_encoded}"
        
        # Journalisation des en-têtes générés (masqués pour la sécurité)
        headers_log = headers.copy()
        if "Authorization" in headers_log:
            auth_value = headers_log["Authorization"]
            if auth_value.startswith("Basic "):
                headers_log["Authorization"] = "Basic ****"
            elif auth_value.startswith("Bearer "):
                headers_log["Authorization"] = "Bearer ****"
        
        self.logger.info(f"En-têtes générés: {headers_log}")
        
        return headers
    
    def test_connection(self) -> Tuple[bool, str]:
        """Teste la connexion à l'API WordPress"""
        if not self.api_url or not self.auth_token:
            return False, "URL du site ou jeton d'authentification non configuré"
        
        # Initialisation des variables pour le mécanisme de reprise
        retry_count = 0
        current_delay = self.RETRY_DELAY_MS / 1000  # Conversion en secondes
        
        while retry_count <= self.MAX_RETRIES:
            try:
                # Tentative de récupération des informations du site
                # Utiliser l'URL du site directement
                site_base_url = getattr(self, 'site_url', self.api_url.split('/wp-json')[0])
                api_url = f"{site_base_url}/wp-json"
                
                self.logger.info(f"Test de connexion à: {api_url}")
                
                response = requests.get(
                    api_url,
                    headers=self.get_headers(),
                    timeout=15  # Augmentation du timeout
                )
                
                # Gestion des erreurs 403 (Forbidden) - Limitation de taux probable
                if response.status_code == 403:
                    retry_count += 1
                    if retry_count > self.MAX_RETRIES:
                        error_msg = f"Échec de la connexion après {self.MAX_RETRIES} tentatives: 403 Forbidden - Le serveur a probablement bloqué les requêtes en raison d'une limitation de taux"
                        self.logger.error(error_msg)
                        return False, error_msg
                    
                    # Délai exponentiel plus long pour les erreurs 403
                    wait_time = current_delay * 2  # Délai plus long pour les erreurs 403
                    self.logger.warning(f"Erreur 403 Forbidden. Attente de {wait_time:.1f}s avant nouvelle tentative ({retry_count}/{self.MAX_RETRIES})")
                    time.sleep(wait_time)
                    current_delay *= self.RETRY_BACKOFF
                    continue
                
                # Gestion des erreurs 502/503
                if response.status_code in [502, 503]:
                    retry_count += 1
                    if retry_count > self.MAX_RETRIES:
                        error_msg = f"Échec de la connexion après {self.MAX_RETRIES} tentatives: {response.status_code}"
                        self.logger.error(error_msg)
                        return False, error_msg
                    
                    self.logger.warning(f"Erreur {response.status_code}. Attente de {current_delay:.1f}s avant nouvelle tentative ({retry_count}/{self.MAX_RETRIES})")
                    time.sleep(current_delay)
                    current_delay *= self.RETRY_BACKOFF
                    continue
                
                # Succès
                if response.status_code == 200:
                    data = response.json()
                    site_name = data.get('name', self.site_name)
                    self.site_name = site_name
                    self.logger.info(f"Connexion réussie à {site_name}")
                    
                    # Récupération des types de contenu personnalisés
                    self._fetch_custom_types()
                    
                    return True, f"Connexion réussie à {site_name}"
                else:
                    # Autres erreurs
                    error_msg = f"Échec de la connexion: {response.status_code} - {response.text}"
                    self.logger.error(error_msg)
                    return False, error_msg
                    
            except requests.exceptions.Timeout:
                # Gestion des timeouts
                retry_count += 1
                if retry_count > self.MAX_RETRIES:
                    error_msg = f"Timeout lors du test de connexion après {self.MAX_RETRIES} tentatives"
                    self.logger.error(error_msg)
                    return False, error_msg
                
                self.logger.warning(f"Timeout lors du test de connexion. Attente de {current_delay:.1f}s avant nouvelle tentative ({retry_count}/{self.MAX_RETRIES})")
                time.sleep(current_delay)
                current_delay *= self.RETRY_BACKOFF
                
            except Exception as e:
                # Autres exceptions
                error_msg = f"Erreur lors du test de connexion: {str(e)}"
                self.logger.error(error_msg)
                return False, error_msg
        
        # Si on arrive ici, c'est que toutes les tentatives ont échoué
        return False, f"Échec du test de connexion après {self.MAX_RETRIES} tentatives"
    
    def _fetch_custom_types(self) -> None:
        """Récupère les types de contenu personnalisés"""
        try:
            # Utiliser directement l'URL du site avec le chemin standard de l'API WordPress
            site_base_url = getattr(self, 'site_url', self.api_url.split('/wp-json')[0])
            api_url = f"{site_base_url}/wp-json/wp/v2/types"
            
            self.logger.info(f"Récupération des types de contenu: {api_url}")
            
            response = requests.get(
                api_url,
                headers=self.get_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                types = response.json()
                # Filtrer les types de contenu standard
                standard_types = set(["post", "page", "attachment", "wp_block", "wp_template", "wp_navigation"])
                self.custom_types = [
                    type_info for type_name, type_info in types.items()
                    if type_name not in standard_types and type_info.get('rest_base')
                ]
                
                # Ajouter les types personnalisés aux dictionnaires CONTENT_TYPES et REST_ENDPOINTS
                for custom_type in self.custom_types:
                    type_name = custom_type.get('rest_base')
                    type_label = custom_type.get('name', type_name)
                    if type_name:
                        self.CONTENT_TYPES[type_name] = type_label
                        # Ajouter également au dictionnaire des endpoints REST
                        self.REST_ENDPOINTS[type_name] = type_name
                
                self.logger.info(f"Types de contenu personnalisés récupérés: {len(self.custom_types)}")
            else:
                self.logger.warning(f"Impossible de récupérer les types personnalisés: {response.status_code}")
                
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération des types personnalisés: {str(e)}")
    
    def fetch_content_items(self, content_type: str, page: int = 1, per_page: int = 100, category: str = None) -> Tuple[List[Dict[str, Any]], int, int]:
        """
        Récupère les éléments de contenu d'un type spécifique
        
        Args:
            content_type: Type de contenu (post, page, etc.)
            page: Numéro de page pour la pagination
            per_page: Nombre d'éléments par page
            category: Catégorie à filtrer (optionnel)
            
        Returns:
            Tuple contenant:
            - Liste des éléments de contenu
            - Nombre total d'éléments
            - Nombre total de pages
        """
        if not self.api_url or not self.auth_token:
            self.logger.error("API non configurée")
            return [], 0, 0
        
        try:
            # Construction de l'URL en fonction du type de contenu
            # Utiliser l'endpoint REST correspondant au type de contenu
            endpoint = self.REST_ENDPOINTS.get(content_type, content_type)
            
            # Paramètres de requête
            params = {
                "page": page,
                "per_page": per_page,
                "_embed": "true",  # Pour récupérer les données liées (auteur, catégories, etc.)
            }
            
            # Ajout du filtre par catégorie si spécifié
            if category:
                if content_type == "post":
                    params["categories"] = category
                elif content_type == "product":
                    params["product_cat"] = category
            
            # Utiliser directement l'URL du site avec le chemin standard de l'API WordPress
            site_base_url = getattr(self, 'site_url', self.api_url.split('/wp-json')[0])
            api_url = f"{site_base_url}/wp-json/wp/v2/{endpoint}"
            
            self.logger.info(f"Requête API: {api_url} avec params={params}")
            
            response = requests.get(
                api_url,
                headers=self.get_headers(),
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                items = response.json()
                
                # Extraction des informations des en-têtes pour la pagination
                total_items = int(response.headers.get('X-WP-Total', 0))
                total_pages = int(response.headers.get('X-WP-TotalPages', 0))
                
                self.logger.info(f"Récupération de {len(items)} {content_type}s (page {page}/{total_pages})")
                return items, total_items, total_pages
            else:
                self.logger.error(f"Échec de la récupération des {content_type}s: {response.status_code} - {response.text}")
                return [], 0, 0
                
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération des {content_type}s: {str(e)}")
            return [], 0, 0
    
    def fetch_all_content(self, content_types: List[str] = None, category: str = None) -> Dict[str, List[Dict[str, Any]]]:
        """
        Récupère tout le contenu des types spécifiés
        
        Args:
            content_types: Liste des types de contenu à récupérer (None = tous)
            category: Catégorie à filtrer (optionnel)
            
        Returns:
            Dictionnaire avec les types de contenu comme clés et les listes d'éléments comme valeurs
        """
        if content_types is None:
            content_types = list(self.CONTENT_TYPES.keys())
        
        result = {}
        
        for content_type in content_types:
            items = []
            page = 1
            total_pages = 1
            
            # Récupération de la première page pour obtenir le nombre total de pages
            first_page_items, _, total_pages = self.fetch_content_items(content_type, page=1, category=category)
            items.extend(first_page_items)
            
            # Récupération des pages restantes en parallèle si nécessaire
            if total_pages > 1:
                with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                    future_to_page = {
                        executor.submit(self.fetch_content_items, content_type, p, 100, category): p
                        for p in range(2, total_pages + 1)
                    }
                    
                    for future in future_to_page:
                        page_items, _, _ = future.result()
                        items.extend(page_items)
            
            result[content_type] = items
            self.logger.info(f"Total de {len(items)} {content_type}s récupérés")
        
        return result
    
    def extract_seo_metadata(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extrait les métadonnées SEO d'un élément de contenu
        Supporte différents plugins SEO (Yoast, Rank Math, All in One SEO, etc.)
        
        Args:
            item: Élément de contenu WordPress
            
        Returns:
            Dictionnaire contenant les métadonnées SEO extraites
        """
        metadata = {
            "id": item.get("id", 0),
            "type": item.get("type", "unknown"),
            "title": item.get("title", {}).get("rendered", ""),
            "url": item.get("link", ""),
            "date_modified": item.get("modified", ""),
            "seo_title": "",
            "seo_description": "",
            "original_seo_title": "",
            "original_seo_description": ""
        }
        
        # Journalisation détaillée pour le débogage
        self.logger.debug(f"Extraction des métadonnées SEO pour {metadata['type']} {metadata['id']}")
        
        # Extraction des métadonnées en fonction du plugin SEO
        
        # 1. Rank Math - Vérification prioritaire
        if ("rank_math_title" in item or "rank_math_description" in item or 
            "rank_math_title" in item.get("meta", {}) or "rank_math_description" in item.get("meta", {})):
            
            self.logger.debug(f"Plugin détecté: Rank Math SEO")
            
            # Vérifier d'abord les champs directement à la racine de l'élément (ajoutés par l'extension Rank Math SEO API)
            if "rank_math_title" in item:
                metadata["seo_title"] = item.get("rank_math_title", "")
                self.logger.debug(f"Titre Rank Math trouvé à la racine: {metadata['seo_title']}")
            elif "rank_math_title" in item.get("meta", {}):
                metadata["seo_title"] = item["meta"].get("rank_math_title", "")
                self.logger.debug(f"Titre Rank Math trouvé dans meta: {metadata['seo_title']}")
                
            if "rank_math_description" in item:
                metadata["seo_description"] = item.get("rank_math_description", "")
                self.logger.debug(f"Description Rank Math trouvée à la racine: {metadata['seo_description']}")
            elif "rank_math_description" in item.get("meta", {}):
                metadata["seo_description"] = item["meta"].get("rank_math_description", "")
                self.logger.debug(f"Description Rank Math trouvée dans meta: {metadata['seo_description']}")
            
            # Vérification des métadonnées alternatives si nécessaire
            if not metadata["seo_description"]:
                if "rank_math_og_description" in item.get("meta", {}):
                    metadata["seo_description"] = item["meta"]["rank_math_og_description"]
                    self.logger.debug(f"Description Rank Math OG utilisée: {metadata['seo_description']}")
                elif "rank_math_twitter_description" in item.get("meta", {}):
                    metadata["seo_description"] = item["meta"]["rank_math_twitter_description"]
                    self.logger.debug(f"Description Rank Math Twitter utilisée: {metadata['seo_description']}")
                    
            # Afficher le contenu complet de l'élément pour le débogage
            self.logger.debug(f"Contenu de l'élément pour l'ID {item.get('id')}: {json.dumps(item)[:500]}...")
            
        # 2. Yoast SEO - Vérifié seulement si Rank Math n'est pas trouvé
        elif "yoast_head_json" in item:
            yoast_data = item["yoast_head_json"]
            self.logger.debug(f"Plugin détecté: Yoast SEO")
            
            # Extraction du titre SEO
            metadata["seo_title"] = yoast_data.get("title", "")
            
            # Extraction de la description SEO - plusieurs emplacements possibles
            if "description" in yoast_data:
                metadata["seo_description"] = yoast_data["description"]
            elif "og_description" in yoast_data:
                metadata["seo_description"] = yoast_data["og_description"]
            elif "twitter_description" in yoast_data:
                metadata["seo_description"] = yoast_data["twitter_description"]
            
            # Vérification des métadonnées OpenGraph
            if "og_description" in yoast_data and not metadata["seo_description"]:
                metadata["seo_description"] = yoast_data["og_description"]
            
            # Vérification des métadonnées Twitter
            if "twitter_description" in yoast_data and not metadata["seo_description"]:
                metadata["seo_description"] = yoast_data["twitter_description"]
            
            # Vérification des métadonnées dans l'objet meta
            if not metadata["seo_description"] and "meta" in item:
                metadata["seo_description"] = item["meta"].get("_yoast_wpseo_metadesc", "")
        
        # All in One SEO
        elif "_aioseo_title" in item.get("meta", {}) or "_aioseo_description" in item.get("meta", {}):
            self.logger.debug(f"Plugin détecté: All in One SEO")
            metadata["seo_title"] = item["meta"].get("_aioseo_title", "")
            metadata["seo_description"] = item["meta"].get("_aioseo_description", "")
            
            # Vérification des métadonnées alternatives
            if not metadata["seo_description"]:
                if "_aioseo_og_description" in item.get("meta", {}):
                    metadata["seo_description"] = item["meta"]["_aioseo_og_description"]
                elif "_aioseo_twitter_description" in item.get("meta", {}):
                    metadata["seo_description"] = item["meta"]["_aioseo_twitter_description"]
        
        # SEOPress
        elif "_seopress_titles_title" in item.get("meta", {}) or "_seopress_titles_desc" in item.get("meta", {}):
            self.logger.debug(f"Plugin détecté: SEOPress")
            metadata["seo_title"] = item["meta"].get("_seopress_titles_title", "")
            metadata["seo_description"] = item["meta"].get("_seopress_titles_desc", "")
            
            # Vérification des métadonnées alternatives
            if not metadata["seo_description"]:
                if "_seopress_social_fb_desc" in item.get("meta", {}):
                    metadata["seo_description"] = item["meta"]["_seopress_social_fb_desc"]
                elif "_seopress_social_twitter_desc" in item.get("meta", {}):
                    metadata["seo_description"] = item["meta"]["_seopress_social_twitter_desc"]
        
        # Vérification des métadonnées génériques
        if not metadata["seo_title"] and not metadata["seo_description"]:
            self.logger.debug(f"Aucun plugin SEO spécifique détecté, recherche de métadonnées génériques")
            
            # Vérification des métadonnées dans l'objet meta
            if "meta" in item:
                # Parcourir toutes les clés meta pour trouver des métadonnées SEO
                for key, value in item["meta"].items():
                    # Recherche de clés contenant "title" ou "titre"
                    if ("title" in key.lower() or "titre" in key.lower()) and not metadata["seo_title"]:
                        metadata["seo_title"] = value
                        self.logger.debug(f"Titre SEO trouvé dans meta[{key}]")
                    
                    # Recherche de clés contenant "desc"
                    if "desc" in key.lower() and not metadata["seo_description"]:
                        metadata["seo_description"] = value
                        self.logger.debug(f"Description SEO trouvée dans meta[{key}]")
            
            # Vérification des métadonnées OpenGraph dans l'en-tête
            if "_links" in item and "https://api.w.org/featuredmedia" in item.get("_links", {}):
                self.logger.debug(f"Recherche de métadonnées dans les médias associés")
                # Les métadonnées peuvent être dans les médias associés
                # Cette partie nécessiterait une requête supplémentaire
            
            # Vérification des extraits
            if "excerpt" in item and isinstance(item["excerpt"], dict) and "rendered" in item["excerpt"]:
                # Si aucune description n'est trouvée, utiliser l'extrait comme fallback
                if not metadata["seo_description"]:
                    # Nettoyer l'extrait des balises HTML
                    import re
                    excerpt = re.sub(r'<[^>]+>', '', item["excerpt"]["rendered"])
                    excerpt = excerpt.strip()
                    if excerpt:
                        metadata["seo_description"] = excerpt
                        self.logger.debug(f"Description SEO extraite de l'extrait")
        
        # Si aucun plugin SEO n'est détecté, utiliser le titre par défaut
        if not metadata["seo_title"]:
            metadata["seo_title"] = metadata["title"]
            self.logger.debug(f"Aucun titre SEO trouvé, utilisation du titre par défaut")
        
        # Vérification des métadonnées dans l'objet _embedded
        if not metadata["seo_description"] and "_embedded" in item:
            self.logger.debug(f"Recherche de métadonnées dans _embedded")
            # Les métadonnées peuvent être dans les objets embarqués
            if "wp:featuredmedia" in item["_embedded"] and item["_embedded"]["wp:featuredmedia"]:
                featured_media = item["_embedded"]["wp:featuredmedia"][0]
                if "alt_text" in featured_media and featured_media["alt_text"]:
                    metadata["seo_description"] = featured_media["alt_text"]
                    self.logger.debug(f"Description SEO extraite du texte alternatif du média")
        
        # Journalisation des résultats
        self.logger.debug(f"Métadonnées extraites: titre='{metadata['seo_title']}', description='{metadata['seo_description']}'")
        
        # Sauvegarder les valeurs originales pour comparaison ultérieure
        metadata["original_seo_title"] = metadata["seo_title"]
        metadata["original_seo_description"] = metadata["seo_description"]
        
        return metadata
    
    def update_seo_metadata(self, item_id: int, content_type: str, seo_title: str, seo_description: str, title: str = None) -> Tuple[bool, str]:
        """
        Met à jour les métadonnées SEO d'un élément de contenu
        
        Args:
            item_id: ID de l'élément
            content_type: Type de contenu (post, page, etc.)
            seo_title: Nouveau titre SEO
            seo_description: Nouvelle description SEO
            title: Nouveau titre H1 (None = pas de changement)
            
        Returns:
            Tuple (succès, message)
        """
        if not self.api_url or not self.auth_token:
            return False, "API non configurée"
        
        # Initialisation des variables pour le mécanisme de reprise
        retry_count = 0
        current_delay = self.RETRY_DELAY_MS / 1000  # Conversion en secondes
        
        while retry_count <= self.MAX_RETRIES:
            try:
                # Utiliser directement l'URL du site avec le chemin standard de l'API WordPress
                site_base_url = getattr(self, 'site_url', self.api_url.split('/wp-json')[0])
                # Utiliser l'endpoint REST correspondant au type de contenu
                endpoint = self.REST_ENDPOINTS.get(content_type, content_type)
                api_url = f"{site_base_url}/wp-json/wp/v2/{endpoint}/{item_id}"
                
                self.logger.info(f"Récupération de l'élément: {api_url}")
                
                # Récupération de l'élément pour déterminer le plugin SEO utilisé
                response = requests.get(
                    api_url,
                    headers=self.get_headers(),
                    timeout=15  # Augmentation du timeout
                )
                
                # Gestion des erreurs 502/503 lors de la récupération
                if response.status_code in [502, 503]:
                    retry_count += 1
                    if retry_count > self.MAX_RETRIES:
                        return False, f"Échec de la récupération de l'élément: {response.status_code}"
                    
                    self.logger.warning(f"Erreur {response.status_code} lors de la récupération de l'élément {item_id}. Tentative {retry_count}/{self.MAX_RETRIES} dans {current_delay:.1f}s")
                    time.sleep(current_delay)
                    current_delay *= self.RETRY_BACKOFF  # Délai exponentiel
                    continue
                
                # Autres erreurs lors de la récupération
                if response.status_code != 200:
                    return False, f"Échec de la récupération de l'élément: {response.status_code}"
                
                item = response.json()
                update_data = {"meta": {}}
                
                # Détermination du plugin SEO et préparation des données de mise à jour
                
                # Vérification de Rank Math SEO API
                has_rank_math_api = "rank_math_title" in item or "rank_math_description" in item
                has_rank_math_meta = "rank_math_title" in item.get("meta", {}) or "rank_math_description" in item.get("meta", {})
                
                # Rank Math - Vérification prioritaire
                if has_rank_math_api or has_rank_math_meta:
                    self.logger.info(f"Mise à jour des métadonnées pour Rank Math SEO")
                    
                    # Si l'extension Rank Math SEO API est utilisée, le plugin supporte les champs directs
                    if has_rank_math_api:
                        self.logger.info("Utilisation des champs Rank Math directs (API Extension activée)")
                        update_data["rank_math_title"] = seo_title
                        update_data["rank_math_description"] = seo_description
                    
                    # Toujours mettre à jour les champs meta également pour être sûr
                    update_data["meta"]["rank_math_title"] = seo_title
                    update_data["meta"]["rank_math_description"] = seo_description
                    
                    # Mise à jour des métadonnées OpenGraph et Twitter pour Rank Math
                    update_data["meta"]["rank_math_og_title"] = seo_title
                    update_data["meta"]["rank_math_og_description"] = seo_description
                    update_data["meta"]["rank_math_twitter_title"] = seo_title
                    update_data["meta"]["rank_math_twitter_description"] = seo_description
                
                # Yoast SEO
                elif "yoast_head_json" in item:
                    self.logger.info(f"Mise à jour des métadonnées pour Yoast SEO")
                    update_data["meta"]["_yoast_wpseo_title"] = seo_title
                    update_data["meta"]["_yoast_wpseo_metadesc"] = seo_description
                
                # All in One SEO
                elif "_aioseo_title" in item.get("meta", {}):
                    update_data["meta"]["_aioseo_title"] = seo_title
                    update_data["meta"]["_aioseo_description"] = seo_description
                
                # SEOPress
                elif "_seopress_titles_title" in item.get("meta", {}):
                    update_data["meta"]["_seopress_titles_title"] = seo_title
                    update_data["meta"]["_seopress_titles_desc"] = seo_description
                
                # Si aucun plugin SEO n'est détecté, utiliser les champs génériques
                else:
                    update_data["meta"]["seo_title"] = seo_title
                    update_data["meta"]["seo_description"] = seo_description
                
                # Mise à jour du titre H1 si spécifié
                if title is not None:
                    update_data["title"] = title
                
                # Envoi de la mise à jour
                # Utiliser l'endpoint REST correspondant au type de contenu
                endpoint = self.REST_ENDPOINTS.get(content_type, content_type)
                update_url = f"{site_base_url}/wp-json/wp/v2/{endpoint}/{item_id}"
                self.logger.info(f"Mise à jour de l'élément: {update_url}")
                
                # Journalisation des données de mise à jour
                self.logger.info(f"Données de mise à jour: {json.dumps(update_data, indent=2)}")
                
                update_response = requests.post(
                    update_url,
                    headers=self.get_headers(),
                    json=update_data,
                    timeout=15  # Augmentation du timeout
                )
                
                # Gestion des erreurs 502/503 lors de la mise à jour
                if update_response.status_code in [502, 503]:
                    retry_count += 1
                    if retry_count > self.MAX_RETRIES:
                        error_msg = f"Échec de la mise à jour: {update_response.status_code} - {update_response.text}"
                        self.logger.error(error_msg)
                        return False, error_msg
                    
                    self.logger.warning(f"Erreur {update_response.status_code} lors de la mise à jour de l'élément {item_id}. Tentative {retry_count}/{self.MAX_RETRIES} dans {current_delay:.1f}s")
                    time.sleep(current_delay)
                    current_delay *= self.RETRY_BACKOFF  # Délai exponentiel
                    continue
                
                # Succès de la mise à jour
                if update_response.status_code in [200, 201]:
                    self.logger.info(f"Métadonnées mises à jour pour {content_type} {item_id}")
                    return True, f"Métadonnées mises à jour avec succès"
                else:
                    # Autres erreurs lors de la mise à jour
                    error_msg = f"Échec de la mise à jour: {update_response.status_code} - {update_response.text}"
                    self.logger.error(error_msg)
                    return False, error_msg
                    
            except requests.exceptions.Timeout:
                # Gestion des timeouts
                retry_count += 1
                if retry_count > self.MAX_RETRIES:
                    error_msg = f"Timeout lors de la mise à jour des métadonnées après {self.MAX_RETRIES} tentatives"
                    self.logger.error(error_msg)
                    return False, error_msg
                
                self.logger.warning(f"Timeout lors de la mise à jour de l'élément {item_id}. Tentative {retry_count}/{self.MAX_RETRIES} dans {current_delay:.1f}s")
                time.sleep(current_delay)
                current_delay *= self.RETRY_BACKOFF  # Délai exponentiel
                
            except Exception as e:
                # Autres exceptions
                error_msg = f"Erreur lors de la mise à jour des métadonnées: {str(e)}"
                self.logger.error(error_msg)
                return False, error_msg
        
        # Si on arrive ici, c'est que toutes les tentatives ont échoué
        return False, f"Échec après {self.MAX_RETRIES} tentatives"
    
    def bulk_update_metadata(self, items: List[Dict[str, Any]], callback=None) -> Dict[str, Any]:
        """
        Met à jour les métadonnées SEO de plusieurs éléments en utilisant un traitement par lots
        
        Args:
            items: Liste des éléments à mettre à jour
            callback: Fonction de rappel pour suivre la progression
            
        Returns:
            Statistiques de mise à jour
        """
        stats = {
            "total": len(items),
            "success": 0,
            "failed": 0,
            "errors": [],
            "retries": 0
        }
        
        if not items:
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
            
            # Traitement du lot avec un pool de threads
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                future_to_item = {}
                
                # Soumission des tâches au pool de threads
                for item in batch:
                    # Vérification si le titre H1 est présent dans l'élément
                    title = item.get("title_h1") if "title_h1" in item else None
                    
                    # Soumission de la tâche avec mécanisme de reprise
                    retry_count = 0
                    while retry_count <= self.MAX_RETRIES:
                        try:
                            future = executor.submit(
                                self.update_seo_metadata,
                                item["id"],
                                item["type"],
                                item["seo_title"],
                                item["seo_description"],
                                title
                            )
                            future_to_item[future] = item
                            break
                        except Exception as e:
                            retry_count += 1
                            stats["retries"] += 1
                            if retry_count > self.MAX_RETRIES:
                                self.logger.error(f"Échec après {self.MAX_RETRIES} tentatives pour l'élément {item['id']}: {str(e)}")
                                stats["failed"] += 1
                                stats["errors"].append({
                                    "id": item["id"],
                                    "type": item["type"],
                                    "title": item["title"],
                                    "error": f"Échec après {self.MAX_RETRIES} tentatives: {str(e)}"
                                })
                            else:
                                self.logger.warning(f"Tentative {retry_count}/{self.MAX_RETRIES} pour l'élément {item['id']}: {str(e)}")
                                time.sleep(0.5)  # Attente avant nouvelle tentative
                
                # Récupération des résultats
                for i, future in enumerate(future_to_item):
                    item = future_to_item[future]
                    try:
                        success, message = future.result()
                        
                        if success:
                            stats["success"] += 1
                        else:
                            stats["failed"] += 1
                            stats["errors"].append({
                                "id": item["id"],
                                "type": item["type"],
                                "title": item["title"],
                                "error": message
                            })
                            
                    except Exception as e:
                        stats["failed"] += 1
                        stats["errors"].append({
                            "id": item["id"],
                            "type": item["type"],
                            "title": item["title"],
                            "error": str(e)
                        })
                    
                    # Mise à jour de la progression
                    current_progress += 1
                    if callback:
                        callback(current_progress, total_items)
            
            # Pause entre les lots pour éviter de surcharger le serveur
            if batch_index < len(batches) - 1:  # Pas de pause après le dernier lot
                self.logger.info(f"Pause de {self.BATCH_DELAY_MS}ms entre les lots")
                time.sleep(self.BATCH_DELAY_MS / 1000)
        
        self.logger.info(f"Mise à jour en masse terminée: {stats['success']} réussies, {stats['failed']} échouées, {stats['retries']} reprises")
        return stats
