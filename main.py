#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Application de mise à jour des méta-données SEO WordPress
Point d'entrée principal de l'application
"""

import sys
import os
import logging
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTranslator, QLocale
from ui.main_window import MainWindow

# Configuration du logging
def setup_logging():
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, "cline.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8-sig"),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger("wp_meta_updater")

def apply_theme(app, theme: str = None) -> None:
    """
    Applique le thème sélectionné
    
    Args:
        app: Instance de QApplication
        theme: Thème à appliquer (light, dark, system)
    """
    from PyQt6.QtCore import QSettings
    
    # Si aucun thème n'est spécifié, utiliser celui des paramètres
    if theme is None:
        settings = QSettings("WP Meta Tools", "WP Meta Updater")
        theme = settings.value("appearance/theme", "system")
    
    # Détermination du thème à appliquer
    if theme == "system":
        # Utilisation du thème du système
        import darkdetect
        system_theme = darkdetect.theme()
        theme = "dark" if system_theme and system_theme.lower() == "dark" else "light"
    
    # Application du thème
    if theme == "dark":
        # Thème sombre
        app.setStyleSheet("""
            QWidget {
                background-color: #2D2D30;
                color: #FFFFFF;
            }
            QMenuBar, QMenu {
                background-color: #1E1E1E;
                color: #FFFFFF;
            }
            QMenuBar::item:selected, QMenu::item:selected {
                background-color: #3E3E40;
            }
            QTableView {
                background-color: #252526;
                alternate-background-color: #2D2D30;
                color: #FFFFFF;
                gridline-color: #3E3E40;
            }
            QTableView::item:selected {
                background-color: #3399FF;
                color: #FFFFFF;
            }
            QHeaderView::section {
                background-color: #1E1E1E;
                color: #FFFFFF;
                border: 1px solid #3E3E40;
            }
            QPushButton {
                background-color: #3E3E40;
                color: #FFFFFF;
                border: 1px solid #555555;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            QPushButton:pressed {
                background-color: #3399FF;
            }
            QLineEdit, QTextEdit, QComboBox, QSpinBox {
                background-color: #333333;
                color: #FFFFFF;
                border: 1px solid #555555;
                padding: 3px;
                border-radius: 2px;
            }
            QTabWidget::pane {
                border: 1px solid #3E3E40;
            }
            QTabBar::tab {
                background-color: #2D2D30;
                color: #FFFFFF;
                padding: 5px 10px;
                border: 1px solid #3E3E40;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #3E3E40;
            }
            QGroupBox {
                border: 1px solid #3E3E40;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
            }
            QCheckBox {
                color: #FFFFFF;
            }
            QCheckBox::indicator {
                width: 13px;
                height: 13px;
            }
            QCheckBox::indicator:unchecked {
                border: 1px solid #555555;
                background-color: #333333;
            }
            QCheckBox::indicator:checked {
                border: 1px solid #3399FF;
                background-color: #3399FF;
            }
            QProgressBar {
                border: 1px solid #555555;
                border-radius: 3px;
                background-color: #333333;
                text-align: center;
                color: #FFFFFF;
            }
            QProgressBar::chunk {
                background-color: #3399FF;
                width: 10px;
            }
            QScrollBar:vertical {
                border: none;
                background-color: #2D2D30;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #3E3E40;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar:horizontal {
                border: none;
                background-color: #2D2D30;
                height: 10px;
                margin: 0px;
            }
            QScrollBar::handle:horizontal {
                background-color: #3E3E40;
                min-width: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
        """)
    else:
        # Thème clair (par défaut)
        app.setStyleSheet("")

def main():
    # Initialisation du logger
    logger = setup_logging()
    logger.info("Démarrage de l'application")
    
    # Création de l'application Qt
    app = QApplication(sys.argv)
    app.setApplicationName("WP Meta Updater")
    app.setOrganizationName("WP Meta Tools")
    app.setOrganizationDomain("wpmetatools.com")
    
    # Définition de l'icône de l'application
    from PyQt6.QtGui import QIcon
    app_icon = QIcon("ui/logo-wp-updater.png")
    app.setWindowIcon(app_icon)
    
    # Support de la traduction (pour l'internationalisation future)
    translator = QTranslator()
    translator.load(QLocale.system(), "translations", "_", ".")
    app.installTranslator(translator)
    
    # Application du thème
    apply_theme(app)
    
    # Création et affichage de la fenêtre principale
    main_window = MainWindow(logger)
    main_window.show()
    
    # Exécution de l'application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
