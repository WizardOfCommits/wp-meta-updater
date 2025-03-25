# WP Meta Updater - Documentación Oficial

## Introducción

WP Meta Updater es una aplicación completa para gestionar y actualizar metadatos SEO (meta title y meta description) de su sitio WordPress. Disponible en versión gráfica (GUI) y línea de comandos (CLI), esta herramienta le permite optimizar eficientemente el SEO de su contenido WordPress.

![Logo WP Meta Updater](ui/logo-wp-updater.png)

## Tabla de contenidos

- [Introducción](#introducción)
- [Características principales](#características-principales)
- [Versiones disponibles](#versiones-disponibles)
  - [Versión GUI](#versión-gui)
  - [Versión CLI](#versión-cli)
- [Requisitos previos e instalación](#requisitos-previos-e-instalación)
  - [Configuración del sistema](#configuración-del-sistema)
  - [Instalación de dependencias](#instalación-de-dependencias)
  - [Creación del ejecutable](#creación-del-ejecutable)
- [Configuración](#configuración)
  - [Autenticación WordPress](#autenticación-wordpress)
  - [Conexión a la API REST](#conexión-a-la-api-rest)
  - [Conexión directa MySQL](#conexión-directa-mysql)
- [Uso](#uso)
  - [Interfaz gráfica](#interfaz-gráfica)
  - [Línea de comandos](#línea-de-comandos)
  - [Formato del archivo CSV](#formato-del-archivo-csv)
- [Características avanzadas](#características-avanzadas)
  - [Importación CSV optimizada](#importación-csv-optimizada)
  - [Conexión directa MySQL](#conexión-directa-mysql-1)
  - [Actualizaciones por lotes](#actualizaciones-por-lotes)
  - [Programación de actualizaciones](#programación-de-actualizaciones)
- [Extensión Rank Math SEO](#extensión-rank-math-seo)
  - [Instalación y configuración](#instalación-y-configuración)
  - [Uso con WordPress Meta Updater](#uso-con-wordpress-meta-updater)
- [Solución de problemas](#solución-de-problemas)
  - [Problemas de autenticación](#problemas-de-autenticación)
  - [Problemas de importación CSV](#problemas-de-importación-csv)
  - [Problemas de actualización](#problemas-de-actualización)
  - [Problemas con los scripts](#problemas-con-los-scripts)
- [Desarrollo](#desarrollo)
  - [Estructura del proyecto](#estructura-del-proyecto)
  - [Pruebas](#pruebas)
- [Licencia y créditos](#licencia-y-créditos)

## Características principales

- **Interfaz gráfica moderna**: Interfaz de usuario intuitiva basada en PyQt6
- **Versión CLI de alto rendimiento**: Automatización de tareas mediante línea de comandos
- **Conexión API REST**: Comunicación segura con WordPress a través de la API REST
- **Conexión directa MySQL**: Opción para actualizar directamente la base de datos
- **Importación/exportación CSV**: Gestión de metadatos mediante archivos CSV
- **Actualizaciones masivas**: Procesamiento optimizado para actualizaciones a gran escala
- **Programación**: Programación de actualizaciones puntuales o recurrentes
- **Análisis SEO**: Identificación de títulos y descripciones no optimizados
- **Soporte multi-sitio**: Gestión de múltiples sitios WordPress
- **Modo sin conexión**: Trabajo con datos en local con sincronización posterior
- **Soporte multi-plugins SEO**: Compatible con Yoast SEO, Rank Math, All in One SEO, SEOPress

## Versiones disponibles

### Versión GUI

La versión con interfaz gráfica ofrece una experiencia de usuario completa e intuitiva.

#### Características específicas de la GUI

- Interfaz moderna con tema claro/oscuro automático
- Tablas de datos filtrables y ordenables
- Edición directa de metadatos
- Visualización de estadísticas SEO
- Asistente de programación de actualizaciones
- Gestión de perfiles de conexión

#### Lanzamiento de la aplicación GUI

```bash
python wp_meta_updater.py
```

### Versión CLI

La versión de línea de comandos es ideal para automatización y scripts.

#### Características específicas de la CLI

- Exportación rápida de metadatos SEO
- Importación y actualización desde CSV
- Generación de informes detallados
- Procesamiento en paralelo para rendimiento óptimo
- Fácilmente integrable en scripts de automatización

#### Uso de la versión CLI

**Windows (CMD)**:
```batch
wp_meta_cli.bat help
```

**Windows (PowerShell)**:
```powershell
.\wp_meta_cli.bat help
```

**Linux/macOS**:
```bash
chmod +x wp_meta_cli.sh
./wp_meta_cli.sh help
```

## Requisitos previos e instalación

### Configuración del sistema

- **Sistema operativo**: Windows, macOS o Linux
- **Python**: Versión 3.8 o superior
- **Espacio en disco**: Mínimo 100 MB
- **Memoria**: Mínimo 512 MB RAM (recomendado 1 GB para sitios grandes)

### Instalación de dependencias

1. Clone o descargue el repositorio
2. Instale las dependencias requeridas:

```bash
pip install -r requirements.txt
```

**Dependencias principales**:
- PyQt6 (solo para la versión GUI)
- requests
- pandas
- python-dateutil
- darkdetect (solo para la versión GUI)
- mysql-connector-python (opcional, para la conexión directa MySQL)

### Creación del ejecutable

Para crear un ejecutable independiente (que no requiere Python):

```bash
python build_exe.py
```

El ejecutable se creará en la carpeta `build/wp_meta_updater/`.

## Configuración

### Autenticación WordPress

Para utilizar WP Meta Updater, debe generar un token de autenticación:

1. Instale el plugin [Application Passwords](https://wordpress.org/plugins/application-passwords/) en su sitio WordPress
2. En su panel de WordPress, vaya a Usuarios > Su perfil
3. Desplácese hasta la sección "Contraseñas de aplicación"
4. Cree una nueva contraseña de aplicación llamada "WP Meta Updater"
5. Copie el token generado para usarlo en la aplicación

### Conexión a la API REST

#### En la interfaz gráfica

1. Inicie la aplicación
2. En la pestaña "Conexión", introduzca:
   - URL de su sitio WordPress (con https://)
   - Token de autenticación
3. Haga clic en "Probar conexión"
4. Guarde el perfil de conexión si lo desea

#### En línea de comandos

Especifique la URL y el token en el comando:

```bash
python wp_meta_cli.py export --url https://su-sitio.com --token "su token" --output export.csv
```

### Conexión directa MySQL

Para utilizar la conexión directa a la base de datos MySQL (más rápida para actualizaciones grandes):

#### Requisitos previos MySQL

- Módulo Python `mysql-connector-python` instalado
- Acceso a la base de datos MySQL del sitio WordPress
- Permisos suficientes para modificar las tablas de metadatos

#### Configuración en la interfaz gráfica

1. Acceda a la pestaña "Conexión MySQL"
2. Si el módulo MySQL no está instalado, haga clic en "Instalar módulo MySQL"
3. Configure los parámetros:
   - Host (por ejemplo: localhost)
   - Usuario
   - Contraseña
   - Nombre de la base de datos
   - Prefijo de las tablas (por defecto: wp_)
4. Haga clic en "Probar conexión"

#### Configuración en línea de comandos

```bash
python wp_meta_cli.py import --url https://su-sitio.com --token "su token" --input datos.csv --update --method mysql --db-host localhost --db-user usuario --db-password contraseña --db-name wordpress --db-prefix wp_
```

## Uso

### Interfaz gráfica

#### Importación de metadatos

1. Una vez conectado, haga clic en "Importar desde WordPress"
2. La aplicación recuperará todos los tipos de contenido disponibles
3. Los metadatos se mostrarán en la tabla principal

#### Modificación de metadatos

1. En la pestaña "Metadatos", filtre y busque elementos
2. Haga doble clic en un elemento para modificar sus metadatos SEO
3. Los elementos modificados se resaltan en amarillo

#### Actualización de metadatos

1. Seleccione los elementos a actualizar
2. Haga clic en "Actualizar seleccionados" o "Actualizar todos los modificados"
3. Elija el método de actualización (API REST o MySQL)
4. Confirme la actualización

#### Exportación e importación CSV

1. Para exportar, haga clic en "Exportar a CSV"
2. Para importar, haga clic en "Importar desde CSV"
3. Seleccione el archivo CSV (codificado en UTF-8 con BOM)

### Línea de comandos

#### Listar los tipos de contenido disponibles

```bash
python wp_meta_cli.py list-types --url https://su-sitio.com --token "su token"
```

#### Exportar los metadatos SEO a CSV

Para todos los tipos de contenido:

```bash
python wp_meta_cli.py export --url https://su-sitio.com --token "su token" --output export.csv
```

Para un tipo específico:

```bash
python wp_meta_cli.py export --url https://su-sitio.com --token "su token" --output articulos.csv --type post
```

#### Importar y actualizar desde un CSV

Importar sin actualizar (verificación):

```bash
python wp_meta_cli.py import --url https://su-sitio.com --token "su token" --input import.csv
```

Importar y actualizar:

```bash
python wp_meta_cli.py import --url https://su-sitio.com --token "su token" --input import.csv --update
```

Utilizar la conexión MySQL directa:

```bash
python wp_meta_cli.py import --url https://su-sitio.com --token "su token" --input import.csv --update --method mysql --db-host localhost --db-user usuario --db-password contraseña --db-name wordpress --db-prefix wp_
```

### Formato del archivo CSV

El archivo CSV debe contener como mínimo las siguientes columnas:

- `id`: ID del elemento WordPress
- `type`: Tipo de contenido (post, page, etc.)
- `seo_title`: Título SEO a actualizar
- `seo_description`: Descripción SEO a actualizar

Ejemplo de archivo CSV:

```csv
"id","type","title","url","seo_title","seo_description"
"1","post","Mi primer artículo","https://su-sitio.com/mi-primer-articulo","Nuevo título SEO","Nueva descripción SEO"
"2","page","Acerca de","https://su-sitio.com/acerca-de","Acerca de nuestra empresa","Descubra nuestra historia y misión"
```

## Características avanzadas

### Importación CSV optimizada

La aplicación utiliza un método de importación CSV optimizado para manejar eficientemente archivos voluminosos:

- **Procesamiento por lotes**: Carga por lotes para reducir el uso de memoria
- **Tamaño de lote adaptativo**: Ajuste automático según el tamaño del archivo
- **Interfaz receptiva**: Procesamiento de eventos UI durante la importación
- **Detección inteligente del separador**: Soporte para coma, punto y coma, tabulación
- **Gestión robusta de errores**: Continuación del procesamiento a pesar de errores individuales

### Conexión directa MySQL

La conexión directa MySQL ofrece varias ventajas:

- **Rendimiento**: Actualizaciones más rápidas que con la API REST
- **Elusión de limitaciones API**: Funciona incluso si la API REST está limitada
- **Eficiencia para actualizaciones masivas**: Ideal para sitios grandes

**Nota importante**: La conexión directa MySQL evita los hooks y filtros de WordPress. Utilícela con precaución y asegúrese de tener una copia de seguridad de su base de datos.

### Actualizaciones por lotes

Para evitar problemas durante las actualizaciones masivas, la aplicación utiliza un sistema de procesamiento por lotes:

- **Procesamiento por lotes**: Los elementos se procesan por lotes de 20 ítems (configurable)
- **Retraso entre lotes**: 200ms por defecto para evitar sobrecargar el servidor
- **Gestión optimizada de la memoria**: Ejecución periódica del recolector de basura
- **Mecanismo de reintento**: Hasta 2 intentos adicionales en caso de fallo
- **Registro detallado**: Seguimiento preciso del procesamiento por lotes

Estos parámetros son configurables en la clase `WordPressConnector`:

```python
# Parámetros de procesamiento por lotes para actualizaciones masivas
BATCH_SIZE = 20       # Número de elementos por lote
BATCH_DELAY_MS = 200  # Retraso entre lotes en milisegundos
MAX_RETRIES = 2       # Número máximo de intentos en caso de fallo
GC_FREQUENCY = 5      # Frecuencia de ejecución del recolector de basura (cada X lotes)
```

### Programación de actualizaciones

La interfaz gráfica permite programar actualizaciones automáticas:

1. En la pestaña "Programación", haga clic en "Programar una actualización"
2. Configure la fecha, hora y opciones de recurrencia
3. Seleccione los elementos a actualizar
4. Haga clic en "OK" para programar la actualización

Las actualizaciones programadas se ejecutarán incluso si la aplicación está cerrada (si la opción está activada).

## Extensión Rank Math SEO

WP Meta Updater es compatible con la extensión Rank Math SEO API que permite exponer los metadatos de Rank Math en la API REST de WordPress.

### Instalación y configuración

1. Descargue la carpeta `rank-math-seo-api-extension`
2. Súbala al directorio `/wp-content/plugins/` de su sitio WordPress
3. Active el plugin desde el menú "Plugins" en la administración de WordPress
4. Acceda a "Ajustes > API Rank Math SEO" en la administración de WordPress
5. Marque la casilla "Activar Rank Math SEO en la API REST"
6. Haga clic en "Guardar cambios"

### Uso con WP Meta Updater

Una vez activada la extensión, WP Meta Updater podrá automáticamente:

1. Detectar los campos Rank Math SEO (`rank_math_title` y `rank_math_description`)
2. Importar estos metadatos desde WordPress
3. Modificarlos a través de la interfaz o archivos CSV
4. Actualizarlos en su sitio WordPress

Para probar la extensión:

```bash
python test_rank_math_seo.py --url https://su-sitio.com --token "su token"
```

## Solución de problemas

### Problemas de autenticación

Si encuentra problemas de autenticación:

1. Verifique que el token está correctamente introducido (con los espacios)
2. Asegúrese de que el plugin Application Passwords está activado
3. Verifique que el usuario tiene los derechos suficientes
4. Pruebe la API directamente con una herramienta como Postman o cURL

### Problemas de importación CSV

Si la importación CSV falla:

1. Verifique que el archivo está codificado en UTF-8 con BOM
2. Asegúrese de que las columnas requeridas están presentes
3. Verifique que los IDs corresponden a elementos existentes
4. Pruebe con un archivo más pequeño para aislar el problema

### Problemas de actualización

Si las actualizaciones fallan:

1. Verifique los logs en la carpeta `logs/`
2. Intente reducir el número de elementos actualizados simultáneamente
3. Pruebe con el método alternativo (API si está utilizando MySQL o viceversa)
4. Verifique que el servidor WordPress no está sobrecargado

### Problemas con los scripts

#### En PowerShell

Si obtiene un error como "El término 'wp_meta_cli.bat' no se reconoce...", utilice la siguiente sintaxis:

```powershell
.\wp_meta_cli.bat [comando] [argumentos]
```

El prefijo `.\` indica a PowerShell que el script se encuentra en el directorio actual.

#### Tokens con espacios

Si su token de autenticación contiene espacios, debe rodearlo con comillas:

```bash
# Incorrecto (si el token contiene espacios)
python wp_meta_cli.py export --url https://su-sitio.com --token kFIT w6HU P3vf vmC2 AIxh WqWz --output export.csv

# Correcto
python wp_meta_cli.py export --url https://su-sitio.com --token "kFIT w6HU P3vf vmC2 AIxh WqWz" --output export.csv
```

## Desarrollo

### Estructura del proyecto

```
wp-update/
├── main.py                  # Punto de entrada principal (GUI)
├── wp_meta_updater.py       # Script de lanzamiento (GUI)
├── wp_meta_cli.py           # Versión línea de comandos
├── wp_meta_cli.bat          # Script batch para Windows
├── wp_meta_cli.sh           # Script shell para Linux/macOS
├── wp_connector.py          # Módulo de conexión a la API WordPress
├── wp_meta_direct_update.py # Módulo de conexión directa MySQL
├── data_manager.py          # Módulo de gestión de datos
├── update_manager.py        # Módulo de gestión de actualizaciones
├── build_exe.py             # Script de creación del ejecutable
├── requirements.txt         # Dependencias Python
├── ui/                      # Módulos de interfaz de usuario (GUI)
│   ├── main_window.py       # Ventana principal
│   ├── connection_widget.py # Widget de conexión API
│   ├── mysql_connection_widget.py # Widget de conexión MySQL
│   ├── metadata_widget.py   # Widget de gestión de metadatos
│   ├── schedule_widget.py   # Widget de programación
│   ├── settings_widget.py   # Widget de parámetros
│   ├── about_dialog.py      # Cuadro de diálogo Acerca de
│   └── on_table_double_clicked.py # Gestor de eventos
├── rank-math-seo-api-extension/ # Extensión WordPress para Rank Math SEO
├── logs/                    # Registros de aplicación
├── data/                    # Datos de la aplicación
└── build/                   # Carpeta de build para el ejecutable
```

### Pruebas

Varios scripts de prueba están disponibles para verificar el buen funcionamiento de la aplicación:

- `test_wp_connector.py`: Prueba la conexión a la API WordPress
- `test_wp_post.py`: Prueba la actualización de metadatos a través de la API
- `test_wp_create.py`: Prueba la creación de contenido con metadatos
- `test_wp_permissions.py`: Verifica los permisos del usuario
- `test_csv_import.py`: Prueba la importación de archivos CSV
- `test_large_csv_import.py`: Prueba la importación de grandes archivos CSV
- `test_batch_update.py`: Prueba las actualizaciones por lotes
- `test_rank_math_seo.py`: Prueba la integración con Rank Math SEO

Para ejecutar una prueba:

```bash
python test_wp_connector.py --url https://su-sitio.com --token "su token"
```

## Licencia y créditos

### Licencia

Copyright © 2025 - Todos los derechos reservados

### Autor

William Troillard

### Agradecimientos

- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - Interfaz gráfica
- [WordPress REST API](https://developer.wordpress.org/rest-api/) - API REST de WordPress
- [Requests](https://requests.readthedocs.io/) - Biblioteca HTTP para Python
- [Pandas](https://pandas.pydata.org/) - Análisis y manipulación de datos
- [MySQL Connector/Python](https://dev.mysql.com/doc/connector-python/en/) - Conexión MySQL
