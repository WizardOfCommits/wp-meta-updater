# Rank Math SEO API Erweiterung

## Beschreibung

Diese WordPress-Erweiterung fügt Rank Math SEO-Metadaten (Meta-Titel und Meta-Beschreibung) zur WordPress REST API hinzu.

Standardmäßig stellt WordPress die von Rank Math SEO verwendeten benutzerdefinierten Felder (`rank_math_title` und `rank_math_description`) nicht in seiner REST API zur Verfügung. Dieses Plugin löst dieses Problem, indem es ermöglicht, diese Daten optional einzubeziehen.

## Voraussetzungen

- WordPress 5.0+
- [Rank Math SEO](https://wordpress.org/plugins/seo-by-rank-math/) Plugin installiert und konfiguriert

## Installation

1. Laden Sie den Ordner `rank-math-seo-api-extension` herunter
2. Laden Sie ihn in das Verzeichnis `/wp-content/plugins/` Ihrer WordPress-Website hoch
3. Aktivieren Sie das Plugin über das Menü "Plugins" in der WordPress-Administration

## Konfiguration

1. Gehen Sie zu "Einstellungen > Rank Math SEO API" in der WordPress-Administration
2. Aktivieren Sie das Kontrollkästchen "Rank Math SEO in REST API aktivieren"
3. Klicken Sie auf "Änderungen speichern"

## Verwendung

Nach der Aktivierung fügt die Erweiterung automatisch die Felder `rank_math_title` und `rank_math_description` zu den REST API-Antworten für Beiträge und Seiten hinzu.

### Anfrage-Beispiel

```
GET /wp-json/wp/v2/posts/{BEITRAGS_ID}
```

### Antwort-Beispiel (mit aktivierter Erweiterung)

```json
{
  "id": 123,
  "title": {
    "rendered": "Beitragstitel"
  },
  "content": {
    "rendered": "<p>Beitragsinhalt...</p>"
  },
  "rank_math_title": "SEO-optimierter Titel für diesen Beitrag | Website-Name",
  "rank_math_description": "Hier ist eine SEO-optimierte Meta-Beschreibung, die den Inhalt dieses Beitrags genau beschreibt."
}
```

## Test und Überprüfung

Um zu überprüfen, ob die Erweiterung korrekt funktioniert:

1. Stellen Sie sicher, dass die Daten in Rank Math korrekt ausgefüllt sind (überprüfen Sie die Registerkarte "Edit Snippet" im Beitragseditor)
2. Rufen Sie `https://ihre-website.com/wp-json/wp/v2/posts/123` auf (ersetzen Sie 123 durch eine Beitrags-ID)
3. Überprüfen Sie, ob die Felder `rank_math_title` und `rank_math_description` in der JSON-Antwort vorhanden sind

Sie können auch mit und ohne aktivierte Option testen, um zu bestätigen, dass die Felder nur erscheinen, wenn die Option aktiviert ist.

## Fehlerbehebung

### Rank Math-Felder erscheinen nicht in der REST API

1. Überprüfen Sie, ob die Option in "Einstellungen > Rank Math SEO API" aktiviert ist
2. Stellen Sie sicher, dass Rank Math SEO korrekt installiert ist und die Felder ausgefüllt sind
3. Überprüfen Sie, dass kein Sicherheits-Plugin oder Firewall die WordPress REST API blockiert

### Zugriffsberechtigungen

Standardmäßig sind Metadaten nur für Benutzer mit Bearbeitungsrechten (`edit_posts`) sichtbar. Wenn Sie diese Einschränkung ändern müssen, können Sie den `permission_callback` in der Funktion `register_rank_math_meta()` anpassen.

## Unterstützung für benutzerdefinierte Inhaltstypen

Die Erweiterung unterstützt standardmäßig Beiträge (`post`) und Seiten (`page`). Wenn Sie Unterstützung für andere benutzerdefinierte Inhaltstypen hinzufügen müssen, können Sie zusätzliche Filter in Ihrer `functions.php`-Datei hinzufügen:

```php
// Beispiel für einen benutzerdefinierten Inhaltstyp 'product'
add_filter('rest_prepare_product', 'expose_rank_math_meta_to_rest', 10, 3);
