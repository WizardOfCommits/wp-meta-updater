# Ajout de la connexion directe MySQL pour WordPress Meta Updater

Ce document explique les modifications apportées au projet pour permettre la connexion directe à la base de données MySQL de WordPress, tant en version UI qu'en CLI.

## Modifications apportées

### 1. Interface utilisateur (UI)

1. **Nouveau widget de connexion MySQL** (`ui/mysql_connection_widget.py`)
   - Permet de configurer et tester la connexion directe à la base de données MySQL
   - Gère les profils de connexion MySQL
   - Vérifie la disponibilité du module `mysql-connector-python`
   - Propose une fonctionnalité d'installation du module MySQL directement depuis l'interface

2. **Intégration dans la fenêtre principale** (`ui/main_window.py`)
   - Ajout d'un nouvel onglet "Connexion MySQL" dans l'interface
   - Modification du gestionnaire de mise à jour pour prendre en compte la méthode MySQL
   - Ajout d'une boîte de dialogue pour choisir la méthode de mise à jour (API ou MySQL)
   - Gestion de l'absence du module MySQL avec un message d'erreur explicite

3. **Mise à jour du gestionnaire de mises à jour** (`update_manager.py`)
   - Ajout du paramètre `method` pour spécifier la méthode de mise à jour
   - Gestion de la connexion MySQL pour les mises à jour directes
   - Journalisation de la méthode utilisée dans les logs

### 2. Interface en ligne de commande (CLI)

1. **Mise à jour de l'outil CLI** (`wp_meta_cli.py`)
   - Ajout de l'option `--method` pour spécifier la méthode de mise à jour (api ou mysql)
   - Ajout des options de connexion MySQL (`--db-host`, `--db-user`, `--db-password`, `--db-name`, `--db-prefix`)
   - Vérification de la disponibilité du module MySQL

### 3. Connecteur direct MySQL (`wp_meta_direct_update.py`)

1. **Importation conditionnelle du module MySQL**
   - Vérification de la disponibilité du module `mysql-connector-python`
   - Gestion des erreurs en cas d'absence du module
   - Affichage d'un message d'erreur explicite

2. **Classe `WordPressDirectConnector`**
   - Connexion directe à la base de données MySQL de WordPress
   - Détection automatique du plugin SEO utilisé
   - Mise à jour des métadonnées SEO en fonction du plugin détecté
   - Gestion des erreurs de connexion et de mise à jour

## Utilisation

### Interface utilisateur (UI)

1. Ouvrez l'application et accédez à l'onglet "Connexion MySQL"
2. Si le module MySQL n'est pas installé, cliquez sur le bouton "Installer le module MySQL"
3. Configurez les paramètres de connexion MySQL:
   - Hôte (par exemple: localhost)
   - Utilisateur
   - Mot de passe
   - Nom de la base de données
   - Préfixe des tables (par défaut: wp_)
4. Cliquez sur "Tester la connexion" pour vérifier que les paramètres sont corrects
5. Lors de la mise à jour des métadonnées, vous pourrez choisir entre la méthode API REST standard ou la méthode MySQL directe

### Interface en ligne de commande (CLI)

Pour utiliser la connexion MySQL directe en ligne de commande:

```bash
python wp_meta_cli.py import --url https://votre-site.com --token votre-token --input donnees.csv --update --method mysql --db-host localhost --db-user utilisateur --db-password motdepasse --db-name wordpress --db-prefix wp_
```

## Installation du module MySQL

Le module `mysql-connector-python` est requis pour utiliser la fonctionnalité de connexion directe MySQL. Vous pouvez l'installer de plusieurs façons:

### 1. Via l'interface utilisateur

1. Ouvrez l'application et accédez à l'onglet "Connexion MySQL"
2. Cliquez sur le bouton "Installer le module MySQL"
3. Confirmez l'installation
4. Redémarrez l'application après l'installation

### 2. Via la ligne de commande

```bash
pip install mysql-connector-python
```

ou

```bash
python -m pip install mysql-connector-python
```

## Avantages de la connexion MySQL directe

1. **Performance**: Les mises à jour directes en base de données sont généralement plus rapides que les appels API REST
2. **Contournement des limitations API**: Permet de mettre à jour les métadonnées même si l'API REST est limitée ou indisponible
3. **Mises à jour en masse**: Plus efficace pour les mises à jour de nombreux éléments

## Prérequis

- Module Python `mysql-connector-python` installé
- Accès à la base de données MySQL du site WordPress
- Permissions suffisantes pour modifier les tables de métadonnées

## Notes importantes

- La connexion directe MySQL contourne les hooks et filtres WordPress, utilisez-la avec précaution
- Assurez-vous de disposer d'une sauvegarde de la base de données avant d'effectuer des mises à jour en masse
- Les mises à jour directes ne déclenchent pas les actions WordPress habituelles (comme la purge du cache)
- Si le module MySQL n'est pas disponible, l'application affichera un message d'erreur explicite et désactivera les fonctionnalités MySQL
