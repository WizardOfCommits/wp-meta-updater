# WordPress Meta CLI

Versión mínima de línea de comandos para exportar e importar metadatos SEO de WordPress.

## Características

- Exportación de metadatos SEO a CSV por tipo de contenido o para todos los tipos
- Importación y actualización de metadatos SEO desde un archivo CSV
- Generación de informes detallados en logs
- Soporte para diferentes plugins SEO (Yoast SEO, Rank Math, All in One SEO, SEOPress)
- Procesamiento en paralelo para un rendimiento óptimo

## Requisitos previos

- Python 3.8 o superior
- Módulos Python requeridos:
  - requests
  - pandas
  - python-dateutil

## Instalación

### Instalación de dependencias

```bash
pip install -r requirements.txt
```

## Uso

### Obtención de un token de autenticación de WordPress

Para utilizar esta herramienta, necesita generar un token de autenticación para la API REST de WordPress:

1. Instale el plugin [Application Passwords](https://wordpress.org/plugins/application-passwords/) en su sitio WordPress
2. En su panel de WordPress, vaya a Usuarios > Su Perfil
3. Desplácese hacia abajo hasta la sección "Contraseñas de aplicación"
4. Cree una nueva contraseña de aplicación llamada "WP Meta CLI"
5. Copie el token generado y úselo en los comandos

### Uso de scripts de ayuda

#### Windows (CMD)

```batch
wp_meta_cli.bat help
```

#### Windows (PowerShell)

En PowerShell, debe prefijar el nombre del script con `.\` para indicar que se encuentra en el directorio actual:

```powershell
.\wp_meta_cli.bat help
```

#### Linux/macOS

```bash
chmod +x wp_meta_cli.sh
./wp_meta_cli.sh help
```

### Uso directo del script Python

También puede usar directamente el script Python:

```bash
python wp_meta_cli.py list-types --url https://su-sitio.com --token "su-token"
```

> **Importante**: Si su token de autenticación contiene espacios, debe rodearlo con comillas dobles para que sea tratado como un solo argumento.

### Exportar metadatos SEO a CSV

Para exportar todos los metadatos SEO a CSV:

```bash
# Windows (CMD)
wp_meta_cli.bat export https://su-sitio.com "su token con espacios" export.csv

# Windows (PowerShell)
.\wp_meta_cli.bat export https://su-sitio.com "su token con espacios" export.csv

# Linux/macOS
./wp_meta_cli.sh export https://su-sitio.com "su token con espacios" export.csv

# Directamente con Python
python wp_meta_cli.py export --url https://su-sitio.com --token "su token con espacios" --output export.csv
```

Para exportar solo un tipo de contenido específico (por ejemplo, entradas):

```bash
# Windows (CMD)
wp_meta_cli.bat export https://su-sitio.com "su token con espacios" entradas.csv post

# Windows (PowerShell)
.\wp_meta_cli.bat export https://su-sitio.com "su token con espacios" entradas.csv post

# Linux/macOS
./wp_meta_cli.sh export https://su-sitio.com "su token con espacios" entradas.csv post

# Directamente con Python
python wp_meta_cli.py export --url https://su-sitio.com --token "su token con espacios" --output entradas.csv --type post
```

### Importar y actualizar metadatos SEO desde un CSV

Para importar metadatos SEO desde un archivo CSV sin actualizarlos en WordPress:

```bash
# Windows (CMD)
wp_meta_cli.bat import https://su-sitio.com "su token con espacios" import.csv

# Windows (PowerShell)
.\wp_meta_cli.bat import https://su-sitio.com "su token con espacios" import.csv

# Linux/macOS
./wp_meta_cli.sh import https://su-sitio.com "su token con espacios" import.csv

# Directamente con Python
python wp_meta_cli.py import --url https://su-sitio.com --token "su token con espacios" --input import.csv
```

Para importar y actualizar metadatos SEO en WordPress:

```bash
# Windows (CMD)
wp_meta_cli.bat import https://su-sitio.com "su token con espacios" import.csv update

# Windows (PowerShell)
.\wp_meta_cli.bat import https://su-sitio.com "su token con espacios" import.csv update

# Linux/macOS
./wp_meta_cli.sh import https://su-sitio.com "su token con espacios" import.csv update

# Directamente con Python
python wp_meta_cli.py import --url https://su-sitio.com --token "su token con espacios" --input import.csv --update
```

## Formato del archivo CSV

El archivo CSV debe contener como mínimo las siguientes columnas:

- `id`: ID del elemento WordPress
- `type`: Tipo de contenido (post, page, etc.)
- `seo_title`: Título SEO a actualizar
- `seo_description`: Descripción SEO a actualizar

Ejemplo de archivo CSV:

```csv
"id","type","title","url","seo_title","seo_description"
"1","post","Mi primera entrada","https://su-sitio.com/mi-primera-entrada","Nuevo título SEO","Nueva descripción SEO"
"2","page","Acerca de","https://su-sitio.com/acerca-de","Acerca de nuestra empresa","Descubra nuestra historia y misión"
```

## Logs e informes

Los logs se generan automáticamente en el directorio `logs`:

- `cline.log`: Registro general de la aplicación
- `update_YYYYMMDD_HHMMSS.json`: Informe detallado de cada actualización

Los informes de actualización contienen información detallada sobre los elementos actualizados con éxito y cualquier error.

## Ejemplos de uso

### Flujo de trabajo típico

1. Exportar los metadatos SEO actuales:
   ```bash
   # Windows (PowerShell)
   .\wp_meta_cli.bat export https://su-sitio.com "su token con espacios" export.csv
   ```

2. Editar el archivo CSV con una hoja de cálculo (Excel, LibreOffice Calc, etc.)

3. Importar y actualizar los metadatos modificados:
   ```bash
   # Windows (PowerShell)
   .\wp_meta_cli.bat import https://su-sitio.com "su token con espacios" export_modificado.csv update
   ```

### Automatización con un script batch

Puede crear un script batch para automatizar la exportación e importación:

```batch
@echo off
set SITE_URL=https://su-sitio.com
set TOKEN=su-token-sin-espacios
set EXPORT_FILE=export_%date:~-4,4%%date:~-7,2%%date:~-10,2%.csv
set IMPORT_FILE=import.csv

echo Exportando metadatos SEO...
python wp_meta_cli.py export --url %SITE_URL% --token "%TOKEN%" --output %EXPORT_FILE%

echo Importando y actualizando metadatos SEO...
python wp_meta_cli.py import --url %SITE_URL% --token "%TOKEN%" --input %IMPORT_FILE% --update

echo ¡Terminado!
```

> **Nota**: En scripts batch, rodee la variable TOKEN con comillas ("%TOKEN%") para manejar tokens con espacios.

## Solución de problemas

### Problemas con tokens de autenticación que contienen espacios

Si su token de autenticación contiene espacios, debe rodearlo con comillas:

```bash
# Incorrecto (si el token contiene espacios)
python wp_meta_cli.py export --url https://su-sitio.com --token kFIT w6HU P3vf vmC2 AIxh WqWz --output export.csv

# Correcto
python wp_meta_cli.py export --url https://su-sitio.com --token "kFIT w6HU P3vf vmC2 AIxh WqWz" --output export.csv
```

### Problemas de ejecución de scripts

#### En PowerShell

Si obtiene un error como "El término 'wp_meta_cli.bat' no se reconoce...", use la siguiente sintaxis:

```powershell
.\wp_meta_cli.bat [comando] [argumentos]
```

El prefijo `.\` le indica a PowerShell que el script se encuentra en el directorio actual.

### Problemas de conexión

Si encuentra problemas al conectarse a la API de WordPress, verifique:

1. Que la URL del sitio sea correcta e incluya el protocolo (http:// o https://)
2. Que el token de autenticación sea válido
3. Que el plugin Application Passwords esté correctamente instalado y activado
4. Que la API REST de WordPress no esté bloqueada por un firewall o plugin de seguridad

### Errores de importación CSV

Si la importación CSV falla, verifique:

1. Que el archivo CSV esté codificado en UTF-8 con BOM
2. Que las columnas requeridas (id, type) estén presentes
3. Que los IDs correspondan a elementos existentes en el sitio WordPress

## Licencia

Copyright © 2025 - Todos los derechos reservados

## Autor

William Troillard
