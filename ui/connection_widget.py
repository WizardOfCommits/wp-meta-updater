#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Widget de connexion à l'API WordPress
Permet de configurer et tester la connexion à l'API
"""

import os
import logging
import json
from typing import Dict, List, Any, Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox,
    QLabel, QLineEdit, QPushButton, QCheckBox, QComboBox,
    QMessageBox, QFileDialog, QProgressBar, QSpacerItem
)
from PyQt6.QtCore import Qt, QSettings, pyqtSignal, pyqtSlot, QSize
from PyQt6.QtGui import QIcon, QFont

class ConnectionWidget(QWidget):
    """Widget de connexion à l'API WordPress"""
    
    # Signaux
    connection_successful = pyqtSignal(bool, str)
    
    def __init__(self, logger: logging.Logger):
        """Initialisation du widget de connexion"""
        super().__init__()
        
        self.logger = logger
        self.settings = QSettings("WP Meta Tools", "WP Meta Updater")
        self.wp_connector = None
        
        # Configuration de l'interface utilisateur
        self.setup_ui()
        
        # Chargement des paramètres sauvegardés
        self.load_settings()
    
    def setup_ui(self) -> None:
        """Configuration de l'interface utilisateur"""
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Titre
        title_label = QLabel("Connexion à l'API WordPress")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)
        
        # Description
        description_label = QLabel(
            "Configurez la connexion à l'API REST de WordPress pour gérer les métadonnées SEO. "
            "Vous aurez besoin de l'URL de votre site et d'un jeton d'authentification."
        )
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(description_label)
        
        # Groupe de paramètres de connexion
        connection_group = QGroupBox("Paramètres de connexion")
        connection_layout = QFormLayout(connection_group)
        connection_layout.setContentsMargins(20, 20, 20, 20)
        connection_layout.setSpacing(15)
        
        # URL du site
        self.site_url_edit = QLineEdit()
        self.site_url_edit.setPlaceholderText("https://votresite.com")
        connection_layout.addRow("URL du site:", self.site_url_edit)
        
        # Nom d'utilisateur
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Nom d'utilisateur WordPress")
        connection_layout.addRow("Nom d'utilisateur:", self.username_edit)
        
        # Jeton d'authentification
        self.auth_token_edit = QLineEdit()
        self.auth_token_edit.setPlaceholderText("Jeton d'authentification")
        self.auth_token_edit.setEchoMode(QLineEdit.EchoMode.Password)
        connection_layout.addRow("Jeton d'authentification:", self.auth_token_edit)
        
        # Bouton pour afficher/masquer le jeton
        self.show_token_check = QCheckBox("Afficher le jeton")
        self.show_token_check.stateChanged.connect(self.on_show_token_changed)
        connection_layout.addRow("", self.show_token_check)
        
        # Nom du site (optionnel)
        self.site_name_edit = QLineEdit()
        self.site_name_edit.setPlaceholderText("Nom du site (optionnel)")
        connection_layout.addRow("Nom du site:", self.site_name_edit)
        
        # Boutons de connexion
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        # Bouton de test de connexion
        self.test_button = QPushButton("Tester la connexion")
        self.test_button.clicked.connect(self.on_test_connection)
        buttons_layout.addWidget(self.test_button)
        
        # Bouton de sauvegarde
        self.save_button = QPushButton("Sauvegarder")
        self.save_button.clicked.connect(self.on_save_settings)
        buttons_layout.addWidget(self.save_button)
        
        connection_layout.addRow("", buttons_layout)
        
        main_layout.addWidget(connection_group)
        
        # Groupe de gestion des profils
        profiles_group = QGroupBox("Profils de connexion")
        profiles_layout = QFormLayout(profiles_group)
        profiles_layout.setContentsMargins(20, 20, 20, 20)
        profiles_layout.setSpacing(15)
        
        # Sélection du profil
        self.profile_combo = QComboBox()
        self.profile_combo.currentIndexChanged.connect(self.on_profile_changed)
        profiles_layout.addRow("Profil:", self.profile_combo)
        
        # Boutons de gestion des profils
        profile_buttons_layout = QHBoxLayout()
        profile_buttons_layout.setSpacing(10)
        
        # Bouton de sauvegarde du profil
        self.save_profile_button = QPushButton("Sauvegarder le profil")
        self.save_profile_button.clicked.connect(self.on_save_profile)
        profile_buttons_layout.addWidget(self.save_profile_button)
        
        # Bouton de suppression du profil
        self.delete_profile_button = QPushButton("Supprimer le profil")
        self.delete_profile_button.clicked.connect(self.on_delete_profile)
        profile_buttons_layout.addWidget(self.delete_profile_button)
        
        profiles_layout.addRow("", profile_buttons_layout)
        
        main_layout.addWidget(profiles_group)
        
        # Espace flexible
        main_layout.addStretch(1)
        
        # Aide sur l'obtention d'un jeton
        help_label = QLabel(
            "<b>Comment obtenir un jeton d'authentification ?</b><br>"
            "1. Installez le plugin <a href='https://wordpress.org/plugins/application-passwords/'>Application Passwords</a> sur votre site WordPress<br>"
            "2. Dans votre tableau de bord WordPress, allez dans Utilisateurs > Votre profil<br>"
            "3. Faites défiler jusqu'à la section 'Mots de passe d'application'<br>"
            "4. Créez un nouveau mot de passe d'application nommé 'WP Meta Updater'<br>"
            "5. Copiez le jeton généré et collez-le ci-dessus"
        )
        help_label.setWordWrap(True)
        help_label.setOpenExternalLinks(True)
        main_layout.addWidget(help_label)
    
    def set_wp_connector(self, wp_connector) -> None:
        """Définit le connecteur WordPress"""
        self.wp_connector = wp_connector
    
    def load_settings(self) -> None:
        """Chargement des paramètres sauvegardés"""
        # Chargement des paramètres de connexion
        self.site_url_edit.setText(self.settings.value("connection/site_url", ""))
        self.username_edit.setText(self.settings.value("connection/username", ""))
        self.auth_token_edit.setText(self.settings.value("connection/auth_token", ""))
        self.site_name_edit.setText(self.settings.value("connection/site_name", ""))
        
        # Chargement des profils
        self.load_profiles()
    
    def load_profiles(self) -> None:
        """Chargement des profils de connexion"""
        # Déconnexion du signal pour éviter les appels pendant le chargement
        self.profile_combo.currentIndexChanged.disconnect(self.on_profile_changed)
        
        # Effacement des profils existants
        self.profile_combo.clear()
        
        # Ajout du profil par défaut
        self.profile_combo.addItem("Profil par défaut")
        
        # Chargement des profils sauvegardés
        profiles = self.settings.value("connection/profiles", [])
        
        if profiles:
            for profile in profiles:
                self.profile_combo.addItem(profile["name"])
        
        # Sélection du dernier profil utilisé
        last_profile = self.settings.value("connection/last_profile", 0)
        self.profile_combo.setCurrentIndex(int(last_profile))
        
        # Reconnexion du signal
        self.profile_combo.currentIndexChanged.connect(self.on_profile_changed)
    
    def save_settings(self) -> None:
        """Sauvegarde des paramètres de connexion"""
        self.settings.setValue("connection/site_url", self.site_url_edit.text())
        self.settings.setValue("connection/username", self.username_edit.text())
        self.settings.setValue("connection/auth_token", self.auth_token_edit.text())
        self.settings.setValue("connection/site_name", self.site_name_edit.text())
        self.settings.setValue("connection/last_profile", self.profile_combo.currentIndex())
        
        self.logger.info("Paramètres de connexion sauvegardés")
    
    @pyqtSlot(int)
    def on_show_token_changed(self, state: int) -> None:
        """Gestion du changement d'état de la case à cocher pour afficher/masquer le jeton"""
        if state == Qt.CheckState.Checked.value:
            self.auth_token_edit.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.auth_token_edit.setEchoMode(QLineEdit.EchoMode.Password)
    
    @pyqtSlot()
    def on_test_connection(self) -> None:
        """Test de la connexion à l'API WordPress"""
        if not self.wp_connector:
            QMessageBox.warning(
                self,
                "Erreur",
                "Connecteur WordPress non initialisé",
                QMessageBox.StandardButton.Ok
            )
            return
        
        # Récupération des paramètres de connexion
        site_url = self.site_url_edit.text().strip()
        username = self.username_edit.text().strip()
        auth_token = self.auth_token_edit.text().strip()
        site_name = self.site_name_edit.text().strip()
        
        # Vérification des paramètres
        if not site_url:
            QMessageBox.warning(
                self,
                "Erreur",
                "Veuillez saisir l'URL du site",
                QMessageBox.StandardButton.Ok
            )
            return
        
        if not auth_token:
            QMessageBox.warning(
                self,
                "Erreur",
                "Veuillez saisir le jeton d'authentification",
                QMessageBox.StandardButton.Ok
            )
            return
        
        # Configuration du connecteur
        self.wp_connector.configure(site_url, auth_token, site_name, username)
        
        # Désactivation du bouton de test pendant la connexion
        self.test_button.setEnabled(False)
        self.test_button.setText("Connexion en cours...")
        
        # Test de la connexion dans un thread séparé
        import threading
        
        def test_connection_thread():
            try:
                # Test de la connexion dans un thread séparé
                success, message = self.wp_connector.test_connection()
                
                # Traitement du résultat dans le thread principal
                from PyQt6.QtCore import QMetaObject, Qt, Q_ARG
                QMetaObject.invokeMethod(
                    self, 
                    "_handle_connection_result", 
                    Qt.ConnectionType.QueuedConnection,
                    Q_ARG(bool, success),
                    Q_ARG(str, message)
                )
            except Exception as e:
                # Gestion des erreurs
                from PyQt6.QtCore import QMetaObject, Qt, Q_ARG
                QMetaObject.invokeMethod(
                    self, 
                    "_handle_connection_result", 
                    Qt.ConnectionType.QueuedConnection,
                    Q_ARG(bool, False),
                    Q_ARG(str, str(e))
                )
        
        # Lancement du thread
        thread = threading.Thread(target=test_connection_thread)
        thread.daemon = True
        thread.start()
    
    def _handle_connection_result(self, success: bool, message: str) -> None:
        """Gère le résultat du test de connexion"""
        # Réactivation du bouton de test
        self.test_button.setEnabled(True)
        self.test_button.setText("Tester la connexion")
        
        if success:
            QMessageBox.information(
                self,
                "Succès",
                f"Connexion réussie à {self.wp_connector.site_name}",
                QMessageBox.StandardButton.Ok
            )
            
            # Mise à jour du nom du site si nécessaire
            if self.wp_connector.site_name != self.site_name_edit.text():
                self.site_name_edit.setText(self.wp_connector.site_name)
            
            # Sauvegarde automatique des paramètres
            self.save_settings()
            
            # Émission du signal de connexion réussie
            self.connection_successful.emit(True, message)
        else:
            QMessageBox.warning(
                self,
                "Erreur",
                f"Échec de la connexion: {message}",
                QMessageBox.StandardButton.Ok
            )
            
            # Émission du signal de connexion échouée
            self.connection_successful.emit(False, message)
    
    @pyqtSlot()
    def on_save_settings(self) -> None:
        """Sauvegarde des paramètres de connexion"""
        self.save_settings()
        
        QMessageBox.information(
            self,
            "Succès",
            "Paramètres de connexion sauvegardés",
            QMessageBox.StandardButton.Ok
        )
    
    @pyqtSlot(int)
    def on_profile_changed(self, index: int) -> None:
        """Gestion du changement de profil"""
        if index == 0:
            # Profil par défaut
            self.site_url_edit.setText(self.settings.value("connection/site_url", ""))
            self.username_edit.setText(self.settings.value("connection/username", ""))
            self.auth_token_edit.setText(self.settings.value("connection/auth_token", ""))
            self.site_name_edit.setText(self.settings.value("connection/site_name", ""))
        else:
            # Profil sauvegardé
            profiles = self.settings.value("connection/profiles", [])
            
            if profiles and index - 1 < len(profiles):
                profile = profiles[index - 1]
                
                self.site_url_edit.setText(profile.get("site_url", ""))
                self.username_edit.setText(profile.get("username", ""))
                self.auth_token_edit.setText(profile.get("auth_token", ""))
                self.site_name_edit.setText(profile.get("site_name", ""))
        
        # Sauvegarde du dernier profil utilisé
        self.settings.setValue("connection/last_profile", index)
    
    @pyqtSlot()
    def on_save_profile(self) -> None:
        """Sauvegarde du profil de connexion actuel"""
        # Récupération des paramètres de connexion
        site_url = self.site_url_edit.text().strip()
        username = self.username_edit.text().strip()
        auth_token = self.auth_token_edit.text().strip()
        site_name = self.site_name_edit.text().strip()
        
        # Vérification des paramètres
        if not site_url:
            QMessageBox.warning(
                self,
                "Erreur",
                "Veuillez saisir l'URL du site",
                QMessageBox.StandardButton.Ok
            )
            return
        
        if not auth_token:
            QMessageBox.warning(
                self,
                "Erreur",
                "Veuillez saisir le jeton d'authentification",
                QMessageBox.StandardButton.Ok
            )
            return
        
        # Demande du nom du profil
        profile_name = site_name or site_url.replace("https://", "").replace("http://", "").split("/")[0]
        
        # Création du profil
        profile = {
            "name": profile_name,
            "site_url": site_url,
            "username": username,
            "auth_token": auth_token,
            "site_name": site_name
        }
        
        # Récupération des profils existants
        profiles = self.settings.value("connection/profiles", [])
        
        if not profiles:
            profiles = []
        
        # Vérification si le profil existe déjà
        for i, existing_profile in enumerate(profiles):
            if existing_profile["name"] == profile_name:
                # Confirmation de remplacement
                reply = QMessageBox.question(
                    self,
                    "Confirmation",
                    f"Le profil '{profile_name}' existe déjà. Voulez-vous le remplacer ?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )
                
                if reply == QMessageBox.StandardButton.Yes:
                    # Remplacement du profil
                    profiles[i] = profile
                    
                    # Sauvegarde des profils
                    self.settings.setValue("connection/profiles", profiles)
                    
                    # Rechargement des profils
                    self.load_profiles()
                    
                    QMessageBox.information(
                        self,
                        "Succès",
                        f"Profil '{profile_name}' mis à jour",
                        QMessageBox.StandardButton.Ok
                    )
                
                return
        
        # Ajout du nouveau profil
        profiles.append(profile)
        
        # Sauvegarde des profils
        self.settings.setValue("connection/profiles", profiles)
        
        # Rechargement des profils
        self.load_profiles()
        
        # Sélection du nouveau profil
        self.profile_combo.setCurrentText(profile_name)
        
        QMessageBox.information(
            self,
            "Succès",
            f"Profil '{profile_name}' créé",
            QMessageBox.StandardButton.Ok
        )
    
    @pyqtSlot()
    def on_delete_profile(self) -> None:
        """Suppression du profil de connexion actuel"""
        # Vérification si un profil est sélectionné
        index = self.profile_combo.currentIndex()
        
        if index == 0:
            QMessageBox.warning(
                self,
                "Erreur",
                "Impossible de supprimer le profil par défaut",
                QMessageBox.StandardButton.Ok
            )
            return
        
        # Récupération du nom du profil
        profile_name = self.profile_combo.currentText()
        
        # Confirmation de suppression
        reply = QMessageBox.question(
            self,
            "Confirmation",
            f"Voulez-vous vraiment supprimer le profil '{profile_name}' ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.No:
            return
        
        # Récupération des profils existants
        profiles = self.settings.value("connection/profiles", [])
        
        if not profiles:
            return
        
        # Suppression du profil
        profiles.pop(index - 1)
        
        # Sauvegarde des profils
        self.settings.setValue("connection/profiles", profiles)
        
        # Rechargement des profils
        self.load_profiles()
        
        # Sélection du profil par défaut
        self.profile_combo.setCurrentIndex(0)
        
        QMessageBox.information(
            self,
            "Succès",
            f"Profil '{profile_name}' supprimé",
            QMessageBox.StandardButton.Ok
        )
