# Extensión API Rank Math SEO

## Descripción

Esta extensión de WordPress añade los metadatos de Rank Math SEO (meta título y meta descripción) a la API REST de WordPress.

Por defecto, WordPress no expone los campos personalizados utilizados por Rank Math SEO (`rank_math_title` y `rank_math_description`) en su API REST. Este plugin resuelve este problema permitiendo incluir estos datos de manera opcional.

## Requisitos previos

- WordPress 5.0+
- Plugin [Rank Math SEO](https://wordpress.org/plugins/seo-by-rank-math/) instalado y configurado

## Instalación

1. Descargue la carpeta `rank-math-seo-api-extension`
2. Súbala al directorio `/wp-content/plugins/` de su sitio WordPress
3. Active el plugin desde el menú "Plugins" en el administrador de WordPress

## Configuración

1. Vaya a "Ajustes > API Rank Math SEO" en el administrador de WordPress
2. Marque la casilla "Habilitar Rank Math SEO en la API REST"
3. Haga clic en "Guardar cambios"

## Uso

Una vez activada, la extensión añadirá automáticamente los campos `rank_math_title` y `rank_math_description` a las respuestas de la API REST para entradas y páginas.

### Ejemplo de solicitud

```
GET /wp-json/wp/v2/posts/{ID_ENTRADA}
```

### Ejemplo de respuesta (con la extensión activada)

```json
{
  "id": 123,
  "title": {
    "rendered": "Título de la entrada"
  },
  "content": {
    "rendered": "<p>Contenido de la entrada...</p>"
  },
  "rank_math_title": "Título SEO optimizado para esta entrada | Nombre del sitio",
  "rank_math_description": "Aquí hay una meta descripción optimizada para SEO que describe con precisión el contenido de esta entrada."
}
```

## Prueba y verificación

Para verificar que la extensión está funcionando correctamente:

1. Asegúrese de que los datos estén correctamente rellenados en Rank Math (compruebe la pestaña "Edit Snippet" en el editor de entradas)
2. Acceda a `https://su-sitio.com/wp-json/wp/v2/posts/123` (reemplace 123 con el ID de una entrada)
3. Verifique que los campos `rank_math_title` y `rank_math_description` estén presentes en la respuesta JSON

También puede hacer una prueba con y sin la opción activada para confirmar que los campos solo aparecen cuando la opción está activada.

## Solución de problemas

### Los campos de Rank Math no aparecen en la API REST

1. Compruebe que la opción esté habilitada en "Ajustes > API Rank Math SEO"
2. Asegúrese de que Rank Math SEO esté correctamente instalado y los campos estén rellenados
3. Verifique que ningún plugin de seguridad o firewall esté bloqueando la API REST de WordPress

### Permisos de acceso

Por defecto, los metadatos solo son visibles para usuarios con derechos de edición (`edit_posts`). Si necesita modificar esta restricción, puede ajustar el `permission_callback` en la función `register_rank_math_meta()`.

## Soporte para tipos de contenido personalizados

La extensión admite entradas (`post`) y páginas (`page`) por defecto. Si necesita añadir soporte para otros tipos de contenido personalizados, puede agregar filtros adicionales en su archivo `functions.php`:

```php
// Ejemplo para un tipo de contenido personalizado 'product'
add_filter('rest_prepare_product', 'expose_rank_math_meta_to_rest', 10, 3);
