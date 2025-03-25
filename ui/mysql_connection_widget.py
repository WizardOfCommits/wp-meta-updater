#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Widget de connexion MySQL
Gère la connexion directe à la base de données MySQL de WordPress
"""

import os
import sys
import logging
from typing import Dict, List, Any, Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox,
    QLabel, QLineEdit, QPushButton, QComboBox, QCheckBox,
    QMessageBox, QFileDialog, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt, QSettings, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QIcon, QFont

class MySQLConnectionWidget(QWidget):
    """Widget de connexion MySQL"""
    
    # Signal émis lors de la connexion réussie
    connection_successful = pyqtSignal(bool, str)
    
    def __init__(self, logger: logging.Logger):
        """Initialisation du widget de connexion MySQL"""
        super().__init__()
        
        self.logger = logger
        self.settings = QSettings("WP Meta Tools", "WordPress Meta Updater")
        self.wp_direct_connector = None
        
        # Configuration de l'interface utilisateur
        self.setup_ui()
        
        # Chargement des paramètres sauvegardés
        self.load_settings()
    
    def setup_ui(self) -> None:
        """Configuration de l'interface utilisateur"""
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Groupe de paramètres de connexion
        connection_group = QGroupBox("Paramètres de connexion MySQL")
        connection_layout = QFormLayout(connection_group)
        connection_layout.setContentsMargins(10, 20, 10, 10)
        connection_layout.setSpacing(10)
        
        # Champ Hôte
        self.host_input = QLineEdit()
        self.host_input.setPlaceholderText("localhost")
        connection_layout.addRow("Hôte:", self.host_input)
        
        # Champ Utilisateur
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("root")
        connection_layout.addRow("Utilisateur:", self.user_input)
        
        # Champ Mot de passe
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        connection_layout.addRow("Mot de passe:", self.password_input)
        
        # Champ Base de données
        self.database_input = QLineEdit()
        self.database_input.setPlaceholderText("wordpress")
        connection_layout.addRow("Base de données:", self.database_input)
        
        # Champ Préfixe des tables
        self.prefix_input = QLineEdit()
        self.prefix_input.setPlaceholderText("wp_")
        connection_layout.addRow("Préfixe des tables:", self.prefix_input)
        
        # Boutons de connexion
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 10, 0, 0)
        button_layout.setSpacing(10)
        
        # Bouton Tester la connexion
        self.test_button = QPushButton("Tester la connexion")
        self.test_button.clicked.connect(self.on_test_connection)
        button_layout.addWidget(self.test_button)
        
        # Bouton Sauvegarder
        self.save_button = QPushButton("Sauvegarder")
        self.save_button.clicked.connect(self.on_save_settings)
        button_layout.addWidget(self.save_button)
        
        # Ajout des boutons au groupe de connexion
        connection_layout.addRow("", button_layout)
        
        # Groupe de profils de connexion
        profiles_group = QGroupBox("Profils de connexion")
        profiles_layout = QHBoxLayout(profiles_group)
        profiles_layout.setContentsMargins(10, 20, 10, 10)
        profiles_layout.setSpacing(10)
        
        # Liste des profils
        self.profiles_combo = QComboBox()
        self.profiles_combo.currentIndexChanged.connect(self.on_profile_changed)
        profiles_layout.addWidget(self.profiles_combo)
        
        # Bouton Charger
        self.load_button = QPushButton("Charger")
        self.load_button.clicked.connect(self.on_load_profile)
        profiles_layout.addWidget(self.load_button)
        
        # Bouton Supprimer
        self.delete_button = QPushButton("Supprimer")
        self.delete_button.clicked.connect(self.on_delete_profile)
        profiles_layout.addWidget(self.delete_button)
        
        # Zone d'information
        info_group = QGroupBox("Informations")
        info_layout = QVBoxLayout(info_group)
        info_layout.setContentsMargins(10, 20, 10, 10)
        info_layout.setSpacing(10)
        
        # Label d'information
        self.info_label = QLabel(
            "Cette fonctionnalité permet de se connecter directement à la base de données MySQL "
            "de WordPress pour mettre à jour les métadonnées SEO sans passer par l'API REST.\n\n"
            "Avantages:\n"
            "- Plus rapide pour les mises à jour en masse\n"
            "- Contourne les limitations de l'API REST\n"
            "- Fonctionne même si l'API REST est désactivée\n\n"
            "Prérequis:\n"
            "- Accès à la base de données MySQL du site WordPress\n"
            "- Module Python 'mysql-connector-python' installé\n"
            "- Permissions suffisantes pour modifier les tables de métadonnées"
        )
        self.info_label.setWordWrap(True)
        info_layout.addWidget(self.info_label)
        
        # Bouton d'installation du module MySQL
        self.install_button = QPushButton("Installer le module MySQL")
        self.install_button.clicked.connect(self.on_install_mysql)
        info_layout.addWidget(self.install_button)
        
        # Ajout des groupes au layout principal
        main_layout.addWidget(connection_group)
        main_layout.addWidget(profiles_group)
        main_layout.addWidget(info_group)
        main_layout.addStretch(1)
        
        # Message d'erreur MySQL
        self.mysql_error_label = QLabel()
        self.mysql_error_label.setStyleSheet("color: red; font-weight: bold;")
        self.mysql_error_label.setWordWrap(True)
        self.mysql_error_label.setVisible(False)
        main_layout.addWidget(self.mysql_error_label)
    
    def load_settings(self) -> None:
        """Chargement des paramètres sauvegardés"""
        # Chargement des paramètres de connexion
        self.host_input.setText(self.settings.value("mysql/host", ""))
        self.user_input.setText(self.settings.value("mysql/user", ""))
        self.password_input.setText(self.settings.value("mysql/password", ""))
        self.database_input.setText(self.settings.value("mysql/database", ""))
        self.prefix_input.setText(self.settings.value("mysql/prefix", "wp_"))
        
        # Chargement des profils de connexion
        self.load_profiles()
    
    def load_profiles(self) -> None:
        """Chargement des profils de connexion"""
        # Récupération des profils
        profiles = self.settings.value("mysql/profiles", [])
        
        # Mise à jour de la liste des profils
        self.profiles_combo.clear()
        self.profiles_combo.addItem("-- Sélectionner un profil --")
        
        if profiles:
            for profile in profiles:
                self.profiles_combo.addItem(profile)
    
    def save_settings(self) -> None:
        """Sauvegarde des paramètres"""
        # Sauvegarde des paramètres de connexion
        self.settings.setValue("mysql/host", self.host_input.text())
        self.settings.setValue("mysql/user", self.user_input.text())
        self.settings.setValue("mysql/password", self.password_input.text())
        self.settings.setValue("mysql/database", self.database_input.text())
        self.settings.setValue("mysql/prefix", self.prefix_input.text())
    
    def set_wp_direct_connector(self, wp_direct_connector) -> None:
        """Définit le connecteur direct WordPress"""
        self.wp_direct_connector = wp_direct_connector
    
    def show_mysql_not_available(self) -> None:
        """Affiche un message d'erreur lorsque le module MySQL n'est pas disponible"""
        self.mysql_error_label.setText(
            "Le module MySQL n'est pas disponible. Veuillez installer le module 'mysql-connector-python' "
            "pour utiliser cette fonctionnalité.\n\n"
            "Vous pouvez l'installer en cliquant sur le bouton 'Installer le module MySQL' ci-dessus."
        )
        self.mysql_error_label.setVisible(True)
        
        # Désactivation des champs de saisie
        self.host_input.setEnabled(False)
        self.user_input.setEnabled(False)
        self.password_input.setEnabled(False)
        self.database_input.setEnabled(False)
        self.prefix_input.setEnabled(False)
        self.test_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.profiles_combo.setEnabled(False)
        self.load_button.setEnabled(False)
        self.delete_button.setEnabled(False)
    
    @pyqtSlot()
    def on_test_connection(self) -> None:
        """Test de la connexion à la base de données"""
        if not self.wp_direct_connector:
            QMessageBox.warning(
                self,
                "Erreur",
                "Connecteur direct non initialisé",
                QMessageBox.StandardButton.Ok
            )
            return
        
        # Récupération des paramètres de connexion
        host = self.host_input.text()
        user = self.user_input.text()
        password = self.password_input.text()
        database = self.database_input.text()
        prefix = self.prefix_input.text()
        
        # Vérification des paramètres
        if not host or not user or not database:
            QMessageBox.warning(
                self,
                "Erreur",
                "Veuillez remplir tous les champs obligatoires",
                QMessageBox.StandardButton.Ok
            )
            return
        
        # Configuration du connecteur
        self.wp_direct_connector.configure(host, user, password, database, prefix)
        
        # Test de la connexion
        if self.wp_direct_connector.connect():
            QMessageBox.information(
                self,
                "Succès",
                "Connexion à la base de données établie avec succès",
                QMessageBox.StandardButton.Ok
            )
            
            # Fermeture de la connexion
            self.wp_direct_connector.disconnect()
            
            # Émission du signal de connexion réussie
            self.connection_successful.emit(True, "Connexion MySQL établie avec succès")
        else:
            QMessageBox.warning(
                self,
                "Erreur",
                "Impossible de se connecter à la base de données",
                QMessageBox.StandardButton.Ok
            )
            
            # Émission du signal de connexion échouée
            self.connection_successful.emit(False, "Échec de la connexion MySQL")
    
    @pyqtSlot()
    def on_save_settings(self) -> None:
        """Sauvegarde des paramètres"""
        # Sauvegarde des paramètres
        self.save_settings()
        
        # Demande de création d'un profil
        profile_name, ok = QMessageBox.question(
            self,
            "Sauvegarde",
            "Paramètres sauvegardés. Voulez-vous créer un profil de connexion ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if profile_name == QMessageBox.StandardButton.Yes:
            self.on_create_profile()
    
    @pyqtSlot()
    def on_create_profile(self) -> None:
        """Création d'un profil de connexion"""
        # Demande du nom du profil
        profile_name, ok = QInputDialog.getText(
            self,
            "Création de profil",
            "Nom du profil:"
        )
        
        if ok and profile_name:
            # Récupération des profils existants
            profiles = self.settings.value("mysql/profiles", [])
            
            # Ajout du nouveau profil
            if profile_name not in profiles:
                profiles.append(profile_name)
                
                # Sauvegarde des profils
                self.settings.setValue("mysql/profiles", profiles)
                
                # Sauvegarde des paramètres du profil
                self.settings.setValue(f"mysql/profile/{profile_name}/host", self.host_input.text())
                self.settings.setValue(f"mysql/profile/{profile_name}/user", self.user_input.text())
                self.settings.setValue(f"mysql/profile/{profile_name}/password", self.password_input.text())
                self.settings.setValue(f"mysql/profile/{profile_name}/database", self.database_input.text())
                self.settings.setValue(f"mysql/profile/{profile_name}/prefix", self.prefix_input.text())
                
                # Mise à jour de la liste des profils
                self.load_profiles()
                
                # Sélection du nouveau profil
                index = self.profiles_combo.findText(profile_name)
                if index >= 0:
                    self.profiles_combo.setCurrentIndex(index)
            else:
                QMessageBox.warning(
                    self,
                    "Erreur",
                    "Un profil avec ce nom existe déjà",
                    QMessageBox.StandardButton.Ok
                )
    
    @pyqtSlot(int)
    def on_profile_changed(self, index: int) -> None:
        """Gestion du changement de profil"""
        # Ne rien faire si c'est l'élément par défaut
        if index <= 0:
            return
        
        # Récupération du nom du profil
        profile_name = self.profiles_combo.currentText()
        
        # Chargement des paramètres du profil
        self.host_input.setText(self.settings.value(f"mysql/profile/{profile_name}/host", ""))
        self.user_input.setText(self.settings.value(f"mysql/profile/{profile_name}/user", ""))
        self.password_input.setText(self.settings.value(f"mysql/profile/{profile_name}/password", ""))
        self.database_input.setText(self.settings.value(f"mysql/profile/{profile_name}/database", ""))
        self.prefix_input.setText(self.settings.value(f"mysql/profile/{profile_name}/prefix", "wp_"))
    
    @pyqtSlot()
    def on_load_profile(self) -> None:
        """Chargement d'un profil de connexion"""
        # Vérification qu'un profil est sélectionné
        if self.profiles_combo.currentIndex() <= 0:
            QMessageBox.warning(
                self,
                "Erreur",
                "Veuillez sélectionner un profil",
                QMessageBox.StandardButton.Ok
            )
            return
        
        # Récupération du nom du profil
        profile_name = self.profiles_combo.currentText()
        
        # Chargement des paramètres du profil
        self.host_input.setText(self.settings.value(f"mysql/profile/{profile_name}/host", ""))
        self.user_input.setText(self.settings.value(f"mysql/profile/{profile_name}/user", ""))
        self.password_input.setText(self.settings.value(f"mysql/profile/{profile_name}/password", ""))
        self.database_input.setText(self.settings.value(f"mysql/profile/{profile_name}/database", ""))
        self.prefix_input.setText(self.settings.value(f"mysql/profile/{profile_name}/prefix", "wp_"))
        
        # Sauvegarde des paramètres
        self.save_settings()
        
        QMessageBox.information(
            self,
            "Succès",
            f"Profil '{profile_name}' chargé avec succès",
            QMessageBox.StandardButton.Ok
        )
    
    @pyqtSlot()
    def on_delete_profile(self) -> None:
        """Suppression d'un profil de connexion"""
        # Vérification qu'un profil est sélectionné
        if self.profiles_combo.currentIndex() <= 0:
            QMessageBox.warning(
                self,
                "Erreur",
                "Veuillez sélectionner un profil",
                QMessageBox.StandardButton.Ok
            )
            return
        
        # Récupération du nom du profil
        profile_name = self.profiles_combo.currentText()
        
        # Confirmation de la suppression
        reply = QMessageBox.question(
            self,
            "Confirmation",
            f"Voulez-vous vraiment supprimer le profil '{profile_name}' ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Récupération des profils existants
            profiles = self.settings.value("mysql/profiles", [])
            
            # Suppression du profil
            if profile_name in profiles:
                profiles.remove(profile_name)
                
                # Sauvegarde des profils
                self.settings.setValue("mysql/profiles", profiles)
                
                # Suppression des paramètres du profil
                self.settings.remove(f"mysql/profile/{profile_name}")
                
                # Mise à jour de la liste des profils
                self.load_profiles()
                
                QMessageBox.information(
                    self,
                    "Succès",
                    f"Profil '{profile_name}' supprimé avec succès",
                    QMessageBox.StandardButton.Ok
                )
    
    @pyqtSlot()
    def on_install_mysql(self) -> None:
        """Installation du module MySQL"""
        # Confirmation de l'installation
        reply = QMessageBox.question(
            self,
            "Installation",
            "Voulez-vous installer le module MySQL ?\n\n"
            "Cette opération nécessite une connexion Internet et peut prendre quelques instants.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Commande d'installation
            try:
                import subprocess
                
                # Exécution de la commande d'installation
                process = subprocess.Popen(
                    [sys.executable, "-m", "pip", "install", "mysql-connector-python"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
                
                # Récupération de la sortie
                stdout, stderr = process.communicate()
                
                if process.returncode == 0:
                    QMessageBox.information(
                        self,
                        "Succès",
                        "Module MySQL installé avec succès.\n\n"
                        "Veuillez redémarrer l'application pour utiliser la fonctionnalité MySQL.",
                        QMessageBox.StandardButton.Ok
                    )
                else:
                    QMessageBox.warning(
                        self,
                        "Erreur",
                        f"Erreur lors de l'installation du module MySQL:\n\n{stderr}",
                        QMessageBox.StandardButton.Ok
                    )
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Erreur",
                    f"Erreur lors de l'installation du module MySQL:\n\n{str(e)}",
                    QMessageBox.StandardButton.Ok
                )

# Import conditionnel de QInputDialog
try:
    from PyQt6.QtWidgets import QInputDialog
except ImportError:
    # Classe de remplacement pour QInputDialog
    class QInputDialog:
        @staticmethod
        def getText(parent, title, label):
            # Utilisation de QMessageBox comme alternative
            text, ok = "", False
            
            # Boîte de dialogue personnalisée
            dialog = QMessageBox(parent)
            dialog.setWindowTitle(title)
            dialog.setText(label)
            
            # Champ de texte
            text_edit = QLineEdit(dialog)
            
            # Layout pour le champ de texte
            layout = QVBoxLayout()
            layout.addWidget(text_edit)
            
            # Ajout du layout au contenu de la boîte de dialogue
            content = dialog.layout()
            content.addLayout(layout, 1, 0, 1, content.columnCount())
            
            # Boutons
            dialog.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            
            # Exécution de la boîte de dialogue
            result = dialog.exec()
            
            # Récupération du résultat
            if result == QMessageBox.StandardButton.Ok:
                text = text_edit.text()
                ok = True
            
            return text, ok
