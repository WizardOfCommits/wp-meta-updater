# WP Meta Updater

Una aplicación Python con interfaz gráfica para actualizar el meta título y la descripción de su sitio WordPress a través de la API REST.

## Características

- Interfaz gráfica de usuario moderna e intuitiva con PyQt6
- Conexión a través de la API REST de WordPress con autenticación por token
- Importación de meta títulos y descripciones actuales del sitio para todos los tipos de contenido (entradas, páginas, productos, etc.)
- Exportación e importación en formato CSV
- Actualización con un clic - actualice todo o solo los elementos seleccionados
- Programación de actualizaciones - programe actualizaciones únicas o recurrentes
- Análisis SEO básico - identifique títulos y descripciones demasiado cortos o largos
- Soporte multi-sitio - gestione múltiples sitios WordPress
- Modo sin conexión - trabaje con datos localmente y sincronice más tarde

## Capturas de pantalla

*Las capturas de pantalla se añadirán aquí*

## Requisitos previos

- Python 3.8 o superior
- PyQt6
- Requests
- Pandas
- Python-dateutil

## Instalación

### Instalación de dependencias

```bash
pip install -r requirements.txt
```

### Lanzamiento de la aplicación

```bash
python wp_meta_updater.py
```

## Configuración

### Obtención de un token de autenticación de WordPress

Para utilizar esta aplicación, necesita generar un token de autenticación para la API REST de WordPress:

1. Instale el plugin [Application Passwords](https://wordpress.org/plugins/application-passwords/) en su sitio WordPress
2. En su panel de WordPress, vaya a Usuarios > Su Perfil
3. Desplácese hacia abajo hasta la sección "Contraseñas de aplicación"
4. Cree una nueva contraseña de aplicación llamada "WP Meta Updater"
5. Copie el token generado y úselo en la aplicación

## Uso

### Conexión a WordPress

1. Inicie la aplicación
2. En la pestaña "Conexión", introduzca la URL de su sitio WordPress y el token de autenticación
3. Haga clic en "Probar conexión" para verificar que todo funciona correctamente

### Importación de metadatos

1. Una vez conectado, haga clic en "Importar desde WordPress" para recuperar todos los metadatos SEO
2. La aplicación recuperará automáticamente todos los tipos de contenido disponibles (entradas, páginas, productos, etc.)

### Edición de metadatos

1. En la pestaña "Metadatos", puede filtrar y buscar elementos específicos
2. Haga doble clic en un elemento para editar sus metadatos SEO
3. Los elementos modificados se resaltan en amarillo

### Actualización de metadatos

1. Seleccione los elementos que desea actualizar
2. Haga clic en "Actualizar seleccionados" o "Actualizar todos los modificados"
3. Confirme la actualización

### Exportación e importación CSV

1. Para exportar metadatos, haga clic en "Exportar a CSV"
2. Para importar metadatos desde un archivo CSV, haga clic en "Importar desde CSV"

### Programación de actualizaciones

1. En la pestaña "Programación", haga clic en "Programar una actualización"
2. Configure la fecha, hora y opciones de recurrencia
3. Seleccione los elementos a actualizar
4. Haga clic en "OK" para programar la actualización

## Estructura del proyecto

```
wp-update/
├── main.py                  # Punto de entrada principal
├── wp_meta_updater.py       # Script de lanzamiento
├── wp_connector.py          # Módulo de conexión a la API de WordPress
├── data_manager.py          # Módulo de gestión de datos
├── update_manager.py        # Módulo de gestión de actualizaciones
├── requirements.txt         # Dependencias Python
├── README.md                # Documentación
├── ui/                      # Módulos de interfaz de usuario
│   ├── main_window.py       # Ventana principal
│   ├── connection_widget.py # Widget de conexión
│   ├── metadata_widget.py   # Widget de gestión de metadatos
│   ├── schedule_widget.py   # Widget de programación
│   ├── settings_widget.py   # Widget de configuración
│   └── about_dialog.py      # Cuadro de diálogo Acerca de
├── logs/                    # Registros de la aplicación
└── data/                    # Datos de la aplicación
```

## Licencia

Este proyecto está licenciado bajo la GNU General Public License v3.0 - consulte el archivo [LICENSE](LICENSE) para más detalles.

## Autor

William Troillard

## Agradecimientos

- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - Interfaz gráfica de usuario
- [WordPress REST API](https://developer.wordpress.org/rest-api/) - API REST de WordPress
- [Requests](https://requests.readthedocs.io/) - Biblioteca HTTP para Python
- [Pandas](https://pandas.pydata.org/) - Análisis y manipulación de datos
