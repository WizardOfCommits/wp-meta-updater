# Solution au problème de crash lors des mises à jour massives

## Problème identifié

Lors de la mise à jour d'un grand nombre de métadonnées SEO (plusieurs centaines) via l'interface graphique, l'application crashe. Ce problème est particulièrement visible lorsque :

- Le nombre d'éléments à mettre à jour dépasse 100-150 items
- Les mises à jour sont lancées simultanément
- La connexion réseau ou le serveur WordPress est lent

## Cause du problème

Après analyse du code, plusieurs causes ont été identifiées :

1. **Surcharge de threads** : La méthode `bulk_update_metadata()` dans `wp_connector.py` lançait toutes les requêtes en parallèle sans contrôle de lot, créant potentiellement des centaines de threads simultanés.

2. **Consommation excessive de mémoire** : Chaque requête API consomme de la mémoire pour stocker les données de requête/réponse, et sans libération périodique, cela peut conduire à une saturation de la mémoire.

3. **Surcharge du serveur WordPress** : L'envoi simultané de centaines de requêtes peut surcharger le serveur WordPress, entraînant des timeouts ou des rejets de connexion.

4. **Absence de mécanisme de reprise** : En cas d'échec d'une requête, aucune tentative de reprise n'était effectuée.

## Solution implémentée

La solution mise en œuvre comprend les améliorations suivantes :

1. **Traitement par lots (batch processing)** :
   - Les éléments sont désormais traités par lots de 20 items (configurable via `BATCH_SIZE`)
   - Un délai de 200ms est ajouté entre chaque lot pour éviter de surcharger le serveur

2. **Gestion de la mémoire** :
   - Exécution périodique du garbage collector pour libérer la mémoire non utilisée
   - Limitation du nombre de threads simultanés (max_workers=5)

3. **Mécanisme de reprise** :
   - En cas d'échec, jusqu'à 2 tentatives supplémentaires sont effectuées (configurable via `MAX_RETRIES`)
   - Délai entre les tentatives pour permettre au serveur de récupérer

4. **Amélioration du suivi et des logs** :
   - Journalisation détaillée du traitement par lots
   - Statistiques sur les reprises et les erreurs

## Paramètres configurables

Les paramètres suivants peuvent être ajustés dans la classe `WordPressConnector` :

```python
# Paramètres de traitement par lots pour les mises à jour massives
BATCH_SIZE = 20       # Nombre d'éléments par lot
BATCH_DELAY_MS = 200  # Délai entre les lots en millisecondes
MAX_RETRIES = 2       # Nombre maximum de tentatives en cas d'échec
GC_FREQUENCY = 5      # Fréquence d'exécution du garbage collector (tous les X lots)
```

## Comment tester la solution

Pour vérifier que la solution résout le problème :

1. Importez un fichier CSV contenant un grand nombre d'éléments (200+)
2. Modifiez plusieurs métadonnées SEO
3. Lancez la mise à jour via l'interface graphique

Vous devriez observer :
- Un traitement progressif par lots dans les logs
- Aucun crash même avec un grand nombre d'éléments
- Une utilisation mémoire stable

## Performances

Avec les paramètres par défaut :
- Un lot de 20 éléments prend environ 5-10 secondes à traiter
- Le délai entre les lots est de 200ms
- Pour 500 éléments (25 lots), le temps total estimé est d'environ 2-4 minutes

Ces paramètres offrent un bon équilibre entre performance et stabilité, mais peuvent être ajustés en fonction des besoins spécifiques et des capacités du serveur WordPress.
