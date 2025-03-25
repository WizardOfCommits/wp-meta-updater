#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Boîte de dialogue À propos
Affiche des informations sur l'application
"""

import os
import sys
import platform
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTabWidget, QTextEdit, QDialogButtonBox, QWidget
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPixmap, QIcon

class AboutDialog(QDialog):
    """Boîte de dialogue À propos"""
    
    def __init__(self, parent=None):
        """Initialisation de la boîte de dialogue"""
        super().__init__(parent)
        
        self.setWindowTitle("À propos de WP Meta Updater")
        self.setMinimumSize(600, 400)
        
        # Configuration de l'interface utilisateur
        self.setup_ui()
    
    def setup_ui(self) -> None:
        """Configuration de l'interface utilisateur"""
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # En-tête
        header_layout = QHBoxLayout()
        
        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap("ui/logo-wp-updater.png")
        logo_pixmap = logo_pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setFixedSize(64, 64)
        header_layout.addWidget(logo_label)
        
        # Titre et version
        title_layout = QVBoxLayout()
        
        title_label = QLabel("WP Meta Updater")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_layout.addWidget(title_label)
        
        version_label = QLabel("Version 1.0.0")
        version_font = QFont()
        version_font.setPointSize(10)
        version_label.setFont(version_font)
        title_layout.addWidget(version_label)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch(1)
        
        layout.addLayout(header_layout)
        
        # Description
        description_label = QLabel(
            "WP Meta Updater est un outil professionnel pour gérer efficacement "
            "les métadonnées SEO de votre site WordPress via l'API REST."
        )
        description_label.setWordWrap(True)
        layout.addWidget(description_label)
        
        # Onglets
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # Onglet À propos
        about_tab = QWidget()
        about_layout = QVBoxLayout(about_tab)
        
        about_text = QTextEdit()
        about_text.setReadOnly(True)
        about_text.setHtml("""
            <h3>Fonctionnalités</h3>
            <ul>
                <li>Connexion à l'API REST de WordPress</li>
                <li>Importation des métadonnées SEO existantes</li>
                <li>Exportation et importation au format CSV</li>
                <li>Mise à jour en un clic</li>
                <li>Planification des mises à jour</li>
                <li>Analyse SEO basique</li>
                <li>Support multi-sites</li>
            </ul>
            
            <h3>Développé par</h3>
            <p>Cette application a été développée par <strong>William Troillard</strong>.<br>
            Site web: <a href="https://qontent.fr">Qontent.fr</a></p>
            
            <h3>Licence</h3>
            <p>Copyright © 2025 William Troillard - Tous droits réservés</p>
            <p>Ce logiciel est la propriété intellectuelle de William Troillard. Il est disponible gratuitement pour un usage privé.</p>
            
            <h3>Soutenir le développement</h3>
            <p>Si vous trouvez cette application utile, vous pouvez soutenir son développement en faisant un don.
            Cela contribuera à l'amélioration continue et à la maintenance de cet outil.</p>
        """)
        
        about_layout.addWidget(about_text)
        tabs.addTab(about_tab, "À propos")
        
        # Onglet Système
        system_tab = QWidget()
        system_layout = QVBoxLayout(system_tab)
        
        system_text = QTextEdit()
        system_text.setReadOnly(True)
        
        # Informations système
        python_version = platform.python_version()
        qt_version = "6.5.0"  # À remplacer par la version réelle si disponible
        os_name = platform.system()
        os_version = platform.version()
        
        system_text.setHtml(f"""
            <h3>Informations système</h3>
            <ul>
                <li><b>Système d'exploitation:</b> {os_name} {os_version}</li>
                <li><b>Python:</b> {python_version}</li>
                <li><b>PyQt:</b> {qt_version}</li>
                <li><b>Architecture:</b> {platform.architecture()[0]}</li>
                <li><b>Processeur:</b> {platform.processor()}</li>
            </ul>
            
            <h3>Dépendances</h3>
            <ul>
                <li><b>PyQt6:</b> Interface graphique</li>
                <li><b>requests:</b> Appels API REST</li>
                <li><b>pandas:</b> Manipulation des données CSV</li>
                <li><b>python-dateutil:</b> Manipulation des dates</li>
            </ul>
        """)
        
        system_layout.addWidget(system_text)
        tabs.addTab(system_tab, "Système")
        
        # Onglet Crédits
        credits_tab = QWidget()
        credits_layout = QVBoxLayout(credits_tab)
        
        credits_text = QTextEdit()
        credits_text.setReadOnly(True)
        credits_text.setHtml("""
            <h3>Crédits</h3>
            <p>WP Meta Updater utilise les bibliothèques et ressources suivantes:</p>
            
            <h4>Bibliothèques</h4>
            <ul>
                <li><b>PyQt6:</b> <a href="https://www.riverbankcomputing.com/software/pyqt/">https://www.riverbankcomputing.com/software/pyqt/</a></li>
                <li><b>requests:</b> <a href="https://requests.readthedocs.io/">https://requests.readthedocs.io/</a></li>
                <li><b>pandas:</b> <a href="https://pandas.pydata.org/">https://pandas.pydata.org/</a></li>
                <li><b>python-dateutil:</b> <a href="https://dateutil.readthedocs.io/">https://dateutil.readthedocs.io/</a></li>
            </ul>
            
            <h4>API</h4>
            <ul>
                <li><b>WordPress REST API:</b> <a href="https://developer.wordpress.org/rest-api/">https://developer.wordpress.org/rest-api/</a></li>
            </ul>
        """)
        
        credits_layout.addWidget(credits_text)
        tabs.addTab(credits_tab, "Crédits")
        
        # Boutons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)
