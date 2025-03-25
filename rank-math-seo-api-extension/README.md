# Rank Math SEO API Extension

## Description

Cette extension WordPress ajoute les métadonnées Rank Math SEO (meta title et meta description) à l'API REST de WordPress. 

Par défaut, WordPress n'expose pas les champs personnalisés utilisés par Rank Math SEO (`rank_math_title` et `rank_math_description`) dans son API REST. Ce plugin résout ce problème en permettant d'inclure ces données de manière optionnelle.

## Prérequis

- WordPress 5.0+
- Plugin [Rank Math SEO](https://wordpress.org/plugins/seo-by-rank-math/) installé et configuré

## Installation

1. Téléchargez le dossier `rank-math-seo-api-extension`
2. Uploadez-le dans le répertoire `/wp-content/plugins/` de votre site WordPress
3. Activez le plugin depuis le menu "Extensions" dans l'administration WordPress

## Configuration

1. Accédez à "Réglages > API Rank Math SEO" dans l'administration WordPress
2. Cochez la case "Activer Rank Math SEO dans l'API REST"
3. Cliquez sur "Enregistrer les modifications"

## Utilisation

Une fois activée, l'extension ajoutera automatiquement les champs `rank_math_title` et `rank_math_description` aux réponses de l'API REST pour les articles et les pages.

### Exemple de requête

```
GET /wp-json/wp/v2/posts/{ID_POST}
```

### Exemple de réponse (avec l'extension activée)

```json
{
  "id": 123,
  "title": {
    "rendered": "Titre de l'article"
  },
  "content": {
    "rendered": "<p>Contenu de l'article...</p>"
  },
  "rank_math_title": "Titre SEO optimisé pour cet article | Nom du site",
  "rank_math_description": "Voici une méta description optimisée pour les moteurs de recherche qui décrit précisément le contenu de cet article."
}
```

## Test et vérification

Pour vérifier que l'extension fonctionne correctement :

1. Assurez-vous que les données sont bien renseignées dans Rank Math (vérifiez l'onglet "Edit Snippet" dans l'éditeur d'articles)
2. Accédez à `https://votre-site.com/wp-json/wp/v2/posts/123` (remplacez 123 par l'ID d'un article)
3. Vérifiez que les champs `rank_math_title` et `rank_math_description` sont présents dans la réponse JSON

Vous pouvez également faire un test avec et sans l'option activée pour confirmer que les champs n'apparaissent que lorsque l'option est activée.

## Dépannage

### Les champs Rank Math n'apparaissent pas dans l'API REST

1. Vérifiez que l'option est bien activée dans "Réglages > API Rank Math SEO"
2. Assurez-vous que Rank Math SEO est correctement installé et que les champs sont bien remplis
3. Vérifiez qu'aucun plugin de sécurité ou pare-feu ne bloque l'API REST de WordPress

### Permissions d'accès

Par défaut, les métadonnées ne sont visibles que pour les utilisateurs ayant les droits d'édition (`edit_posts`). Si vous avez besoin de modifier cette restriction, vous pouvez ajuster le `permission_callback` dans la fonction `register_rank_math_meta()`.

## Support des types de contenu personnalisés

L'extension prend en charge par défaut les articles (`post`) et les pages (`page`). Si vous avez besoin d'ajouter le support pour d'autres types de contenu personnalisés, vous pouvez ajouter des filtres supplémentaires dans votre fichier `functions.php` :

```php
// Exemple pour un type de contenu personnalisé 'product'
add_filter('rest_prepare_product', 'expose_rank_math_meta_to_rest', 10, 3);
