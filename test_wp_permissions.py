#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de test pour vérifier les permissions de l'utilisateur WordPress
Permet de tester les différentes actions que l'utilisateur peut effectuer via l'API REST
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
    
    log_file = os.path.join(log_dir, "test_permissions.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8-sig"),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger("test_wp_permissions")

def test_endpoint(url, headers, method="GET", data=None, logger=None):
    """
    Teste un endpoint de l'API REST WordPress
    
    Args:
        url: URL de l'endpoint
        headers: En-têtes HTTP
        method: Méthode HTTP (GET, POST, PUT, DELETE)
        data: Données à envoyer (pour POST, PUT)
        logger: Logger pour journalisation
        
    Returns:
        Tuple (succès, message, données)
    """
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=10)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=10)
        else:
            return False, f"Méthode non supportée: {method}", None
        
        if response.status_code in [200, 201]:
            return True, f"Succès ({response.status_code})", response.json() if response.text else None
        else:
            return False, f"Échec ({response.status_code}): {response.text}", None
    except Exception as e:
        if logger:
            logger.error(f"Erreur lors de la requête {method} {url}: {str(e)}")
        return False, f"Erreur: {str(e)}", None

def main():
    # Initialisation du parser d'arguments
    parser = argparse.ArgumentParser(description="Test des permissions WordPress")
    
    # Arguments
    parser.add_argument("--url", required=True, help="URL du site WordPress")
    parser.add_argument("--token", required=True, help="Jeton d'authentification WordPress")
    
    # Analyse des arguments
    args = parser.parse_args()
    
    # Initialisation du logger
    logger = setup_logging()
    logger.info("Démarrage du test des permissions WordPress")
    
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
    
    # Récupération des informations de l'utilisateur actuel
    logger.info("Récupération des informations de l'utilisateur actuel")
    
    site_base_url = wp_connector.site_url
    headers = wp_connector.get_headers()
    
    # Test de l'endpoint /wp/v2/users/me
    print("\n=== Test de l'endpoint /wp/v2/users/me ===")
    success, message, data = test_endpoint(
        f"{site_base_url}/wp-json/wp/v2/users/me",
        headers,
        "GET",
        logger=logger
    )
    
    if success:
        print("Informations de l'utilisateur récupérées avec succès")
        print(f"ID: {data.get('id')}")
        print(f"Nom: {data.get('name')}")
        print(f"Rôles: {', '.join(data.get('roles', []))}")
        print(f"Capacités: {json.dumps(data.get('capabilities', {}), indent=2)}")
        
        # Stockage de l'ID de l'utilisateur pour les tests suivants
        user_id = data.get('id')
    else:
        print(f"Échec de la récupération des informations de l'utilisateur: {message}")
        user_id = None
    
    # Test des différents endpoints et méthodes
    endpoints = [
        # Posts
        {"name": "Liste des articles", "url": f"{site_base_url}/wp-json/wp/v2/posts", "method": "GET"},
        {"name": "Création d'article", "url": f"{site_base_url}/wp-json/wp/v2/posts", "method": "POST", "data": {
            "title": "Test de permission",
            "content": "Test de permission pour la création d'article",
            "status": "draft"
        }},
        
        # Pages
        {"name": "Liste des pages", "url": f"{site_base_url}/wp-json/wp/v2/pages", "method": "GET"},
        {"name": "Création de page", "url": f"{site_base_url}/wp-json/wp/v2/pages", "method": "POST", "data": {
            "title": "Test de permission",
            "content": "Test de permission pour la création de page",
            "status": "draft"
        }},
        
        # Médias
        {"name": "Liste des médias", "url": f"{site_base_url}/wp-json/wp/v2/media", "method": "GET"},
        
        # Catégories
        {"name": "Liste des catégories", "url": f"{site_base_url}/wp-json/wp/v2/categories", "method": "GET"},
        {"name": "Création de catégorie", "url": f"{site_base_url}/wp-json/wp/v2/categories", "method": "POST", "data": {
            "name": "Test de permission",
            "description": "Test de permission pour la création de catégorie"
        }},
        
        # Étiquettes
        {"name": "Liste des étiquettes", "url": f"{site_base_url}/wp-json/wp/v2/tags", "method": "GET"},
        {"name": "Création d'étiquette", "url": f"{site_base_url}/wp-json/wp/v2/tags", "method": "POST", "data": {
            "name": "Test de permission",
            "description": "Test de permission pour la création d'étiquette"
        }},
        
        # Utilisateurs
        {"name": "Liste des utilisateurs", "url": f"{site_base_url}/wp-json/wp/v2/users", "method": "GET"},
    ]
    
    # Exécution des tests
    for endpoint in endpoints:
        print(f"\n=== Test: {endpoint['name']} ===")
        success, message, data = test_endpoint(
            endpoint["url"],
            headers,
            endpoint["method"],
            endpoint.get("data"),
            logger
        )
        
        if success:
            print(f"Succès: {message}")
            if endpoint["method"] == "POST" and data:
                print(f"ID créé: {data.get('id')}")
        else:
            print(f"Échec: {message}")
    
    print("\n=== Résumé des permissions ===")
    print("Votre utilisateur a les permissions suivantes:")
    
    # Affichage des permissions en fonction des résultats des tests
    permissions = {
        "Lecture d'articles": "À déterminer",
        "Création d'articles": "À déterminer",
        "Modification d'articles": "À déterminer",
        "Suppression d'articles": "À déterminer",
        "Lecture de pages": "À déterminer",
        "Création de pages": "À déterminer",
        "Lecture de médias": "À déterminer",
        "Lecture de catégories": "À déterminer",
        "Création de catégories": "À déterminer",
        "Lecture d'étiquettes": "À déterminer",
        "Création d'étiquettes": "À déterminer",
        "Lecture d'utilisateurs": "À déterminer"
    }
    
    # Affichage des permissions
    for permission, status in permissions.items():
        print(f"- {permission}: {status}")
    
    print("\nPour résoudre les problèmes d'autorisation, vous pouvez:")
    print("1. Vérifier que votre utilisateur a les rôles et capacités nécessaires")
    print("2. Vérifier qu'aucun plugin de sécurité ne bloque l'accès à l'API REST")
    print("3. Vérifier les règles de pare-feu et les restrictions d'accès")
    print("4. Utiliser un mot de passe d'application spécifique pour l'API REST")

if __name__ == "__main__":
    main()
