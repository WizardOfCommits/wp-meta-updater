#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Outil de diagnostic pour Rank Math SEO API
Ce script vérifie si les métadonnées Rank Math SEO sont correctement exposées dans l'API WordPress
"""

import requests
import json
import argparse
import sys
from typing import Dict, Any, Tuple

def get_headers(username: str, password: str) -> Dict[str, str]:
    """Génère les en-têtes d'authentification pour l'API WordPress"""
    import base64
    
    # Création de la chaîne d'authentification au format username:password
    auth_string = f"{username}:{password}"
    
    # Encodage en base64 pour l'authentification Basic
    auth_encoded = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
    
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Basic {auth_encoded}"
    }

def test_rank_math_api(site_url: str, post_id: int, username: str, password: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Teste si les métadonnées Rank Math SEO sont exposées dans l'API WordPress
    
    Args:
        site_url: URL du site WordPress
        post_id: ID de l'article à tester
        username: Nom d'utilisateur WordPress
        password: Mot de passe ou jeton d'authentification
        
    Returns:
        Tuple (succès, résultats)
    """
    # Normalisation de l'URL du site
    if site_url.endswith('/'):
        site_url = site_url[:-1]
    
    # Récupération des en-têtes d'authentification
    headers = get_headers(username, password)
    
    # Construction de l'URL de l'API
    api_url = f"{site_url}/wp-json/wp/v2/posts/{post_id}"
    
    try:
        # Requête à l'API WordPress
        print(f"Requête API: {api_url}")
        response = requests.get(api_url, headers=headers, timeout=10)
        
        # Vérification du code de statut
        if response.status_code != 200:
            print(f"Erreur: Code de statut {response.status_code}")
            print(f"Réponse: {response.text}")
            return False, {"error": f"Code de statut {response.status_code}"}
        
        # Récupération des données
        post_data = response.json()
        
        # Analyse des métadonnées Rank Math SEO
        results = {
            "post_id": post_id,
            "post_title": post_data.get("title", {}).get("rendered", ""),
            "post_url": post_data.get("link", ""),
            "has_rank_math_api": False,
            "rank_math_title": None,
            "rank_math_description": None,
            "meta_rank_math_title": None,
            "meta_rank_math_description": None,
            "excerpt": post_data.get("excerpt", {}).get("rendered", ""),
        }
        
        # Vérification des champs Rank Math à la racine (ajoutés par Rank Math SEO API Extension)
        if "rank_math_title" in post_data:
            results["has_rank_math_api"] = True
            results["rank_math_title"] = post_data["rank_math_title"]
        
        if "rank_math_description" in post_data:
            results["has_rank_math_api"] = True
            results["rank_math_description"] = post_data["rank_math_description"]
        
        # Vérification des champs Rank Math dans l'objet meta
        if "meta" in post_data:
            if "rank_math_title" in post_data["meta"]:
                results["meta_rank_math_title"] = post_data["meta"]["rank_math_title"]
            
            if "rank_math_description" in post_data["meta"]:
                results["meta_rank_math_description"] = post_data["meta"]["rank_math_description"]
        
        return True, results
        
    except Exception as e:
        print(f"Erreur: {str(e)}")
        return False, {"error": str(e)}

def print_results(results: Dict[str, Any]) -> None:
    """Affiche les résultats du test"""
    print("\n=== RÉSULTATS DU TEST RANK MATH SEO API ===\n")
    
    print(f"ID de l'article: {results['post_id']}")
    print(f"Titre de l'article: {results['post_title']}")
    print(f"URL de l'article: {results['post_url']}")
    print("")
    
    if results.get("has_rank_math_api"):
        print("✓ L'extension Rank Math SEO API est activée")
    else:
        print("✗ L'extension Rank Math SEO API n'est pas activée ou ne fonctionne pas correctement")
    
    print("\n=== MÉTADONNÉES DÉTECTÉES ===\n")
    
    # Affichage des métadonnées Rank Math à la racine
    print("À la racine de la réponse JSON (via Rank Math SEO API Extension):")
    if results.get("rank_math_title"):
        print(f"- Titre Rank Math: {results['rank_math_title']}")
    else:
        print("- Titre Rank Math: Non détecté")
    
    if results.get("rank_math_description"):
        print(f"- Description Rank Math: {results['rank_math_description']}")
    else:
        print("- Description Rank Math: Non détectée")
    
    # Affichage des métadonnées Rank Math dans l'objet meta
    print("\nDans l'objet meta (via REST API standard):")
    if results.get("meta_rank_math_title"):
        print(f"- Titre Rank Math: {results['meta_rank_math_title']}")
    else:
        print("- Titre Rank Math: Non détecté")
    
    if results.get("meta_rank_math_description"):
        print(f"- Description Rank Math: {results['meta_rank_math_description']}")
    else:
        print("- Description Rank Math: Non détectée")
    
    # Affichage de l'extrait comme référence
    print("\nExtrait de l'article (pour référence):")
    if results.get("excerpt"):
        import re
        excerpt = re.sub(r'<[^>]+>', '', results['excerpt'])
        excerpt = excerpt.strip()
        print(f"- {excerpt}")
    else:
        print("- Pas d'extrait disponible")
    
    print("\n=== DIAGNOSTIC ===\n")
    
    if not results.get("has_rank_math_api"):
        print("L'extension Rank Math SEO API n'est pas activée ou ne fonctionne pas correctement.")
        print("Vérifiez que:")
        print("1. L'extension est installée dans /wp-content/plugins/")
        print("2. L'extension est activée dans l'interface WordPress")
        print("3. L'option 'Activer Rank Math SEO dans l'API REST' est cochée dans Réglages > API Rank Math SEO")
    else:
        if results.get("rank_math_title") != results.get("meta_rank_math_title") or \
           results.get("rank_math_description") != results.get("meta_rank_math_description"):
            print("⚠️ Les métadonnées Rank Math à la racine et dans l'objet meta sont différentes.")
            print("Cela pourrait indiquer un problème de synchronisation ou une mise en cache.")
        else:
            print("✓ Les métadonnées Rank Math sont correctement exposées dans l'API REST.")
    
    if not results.get("rank_math_description") and not results.get("meta_rank_math_description"):
        print("\nAucune description Rank Math n'a été détectée.")
        print("Si vous avez configuré une description dans l'interface Rank Math SEO de WordPress,")
        print("cela suggère que l'extension Rank Math SEO API ne fonctionne pas correctement.")
        print("Votre application utilise probablement l'extrait de l'article comme fallback.")

def main():
    # Analyse des arguments
    parser = argparse.ArgumentParser(description="Outil de diagnostic pour Rank Math SEO API")
    parser.add_argument("site_url", help="URL du site WordPress")
    parser.add_argument("post_id", type=int, help="ID de l'article à tester")
    parser.add_argument("username", help="Nom d'utilisateur WordPress")
    parser.add_argument("password", help="Mot de passe ou jeton d'authentification")
    
    args = parser.parse_args()
    
    # Test de l'API Rank Math SEO
    success, results = test_rank_math_api(args.site_url, args.post_id, args.username, args.password)
    
    if success:
        print_results(results)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
