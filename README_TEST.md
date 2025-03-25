# Test du Connecteur WordPress

Ce dossier contient des scripts pour tester la connexion à l'API WordPress et récupérer des contenus.

## Modifications Apportées

Le fichier `wp_connector.py` a été modifié pour résoudre les problèmes d'accès à l'API WordPress. Les principales modifications sont :

1. **Construction cohérente des URLs de l'API** : Toutes les méthodes utilisent maintenant la même approche pour construire les URLs de l'API WordPress, en utilisant directement l'URL du site avec le chemin standard `/wp-json/wp/v2/`.

2. **Journalisation améliorée** : Des messages de log détaillés ont été ajoutés pour faciliter le débogage, incluant les URLs complètes des requêtes API.

3. **Gestion plus robuste des erreurs** : Les erreurs sont mieux capturées et journalisées pour faciliter l'identification des problèmes.

## Scripts de Test

### `test_wp_connector.py`

Script Python principal pour tester la connexion à l'API WordPress et récupérer des contenus.

#### Utilisation

```bash
python test_wp_connector.py --url https://www.votresite.com --token votre_token [--type post] [--per-page 10] [--page 1]
```

#### Options

- `--url` : URL du site WordPress (obligatoire)
- `--token` : Jeton d'authentification WordPress (obligatoire)
- `--type` : Type de contenu à récupérer (par défaut: post)
- `--per-page` : Nombre d'éléments par page (par défaut: 10)
- `--page` : Numéro de page (par défaut: 1)

### `test_wp_connector.bat`

Script batch pour Windows qui exécute `test_wp_connector.py`.

#### Utilisation

```bash
test_wp_connector.bat --url https://www.votresite.com --token votre_token [--type post] [--per-page 10] [--page 1]
```

### `test_wp_connector.sh`

Script shell pour Linux/macOS qui exécute `test_wp_connector.py`.

#### Utilisation

```bash
./test_wp_connector.sh --url https://www.votresite.com --token votre_token [--type post] [--per-page 10] [--page 1]
```

## Obtention d'un Jeton d'Authentification

Pour utiliser l'API WordPress avec authentification, vous avez besoin d'un jeton d'accès. Voici comment en obtenir un :

### Méthode 1 : Plugin JWT Authentication

1. Installez le plugin "JWT Authentication for WP REST API"
2. Configurez le plugin selon les instructions
3. Obtenez un jeton en envoyant une requête POST à `/wp-json/jwt-auth/v1/token` avec vos identifiants

### Méthode 2 : Application Passwords (WordPress 5.6+)

1. Dans l'administration WordPress, allez dans "Profil" > "Mots de passe d'application"
2. Créez un nouveau mot de passe d'application
3. Utilisez ce mot de passe avec votre nom d'utilisateur pour l'authentification Basic

## Résolution des Problèmes

Si vous rencontrez toujours des problèmes d'accès à l'API WordPress, vérifiez les points suivants :

1. **Vérifiez que l'API REST est activée** : Certains plugins de sécurité peuvent la désactiver.

2. **Vérifiez les permissions** : Assurez-vous que l'utilisateur associé au jeton a les permissions nécessaires.

3. **Vérifiez les logs** : Consultez les logs dans le dossier `logs/` pour plus de détails sur les erreurs.

4. **Testez directement l'API** : Utilisez un outil comme Postman ou cURL pour tester directement l'API :

   ```bash
   curl -X GET https://www.votresite.com/wp-json/wp/v2/posts -H "Authorization: Bearer votre_token"
   ```

5. **Vérifiez les plugins de sécurité** : Désactivez temporairement les plugins de sécurité pour voir s'ils bloquent l'accès à l'API.
