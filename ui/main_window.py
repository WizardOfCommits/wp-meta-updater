#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fenêtre principale de l'application
Gère l'interface utilisateur principale
"""

import os
import sys
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QLabel, QPushButton, QStatusBar, QMessageBox, QFileDialog,
    QSplitter, QApplication
)
from PyQt6.QtCore import Qt, QSize, QSettings, pyqtSlot, QTimer
from PyQt6.QtGui import QIcon, QAction, QPixmap, QFont

from ui.connection_widget import ConnectionWidget
# Importation du widget MySQL retirée de l'interface graphique mais conservée pour la ligne de commande
# from ui.mysql_connection_widget import MySQLConnectionWidget
from ui.metadata_widget import MetadataWidget
from ui.settings_widget import SettingsWidget
from ui.schedule_widget import ScheduleWidget
from ui.about_dialog import AboutDialog

class MainWindow(QMainWindow):
    """Fenêtre principale de l'application"""
    
    def __init__(self, logger: logging.Logger):
        """Initialisation de la fenêtre principale"""
        super().__init__()
        
        self.logger = logger
        self.settings = QSettings("WP Meta Tools", "WP Meta Updater")
        
        # Initialisation des composants
        self.wp_connector = None
        self.wp_direct_connector = None
        self.data_manager = None
        self.update_manager = None
        
        # Configuration de la fenêtre
        self.setWindowTitle("WP Meta Updater")
        self.setMinimumSize(1200, 800)
        
        # Définition de l'icône de la fenêtre
        self.setWindowIcon(QIcon("ui/logo-wp-updater.png"))
        
        # Restauration de la taille et position de la fenêtre
        self.restore_window_state()
        
        # Création des widgets
        self.setup_ui()
        
        # Connexion des signaux
        self.connect_signals()
        
        # Initialisation des gestionnaires
        self.init_managers()
        
        # Restauration de la session précédente
        self.restore_previous_session()
        
        self.logger.info("Fenêtre principale initialisée")
    
    def setup_ui(self) -> None:
        """Configuration de l'interface utilisateur"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Onglets principaux
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Onglet de connexion API
        self.connection_widget = ConnectionWidget(self.logger)
        self.tabs.addTab(self.connection_widget, "Connexion API")
        
        # Onglet de gestion des métadonnées
        self.metadata_widget = MetadataWidget(self.logger)
        self.tabs.addTab(self.metadata_widget, "Métadonnées")
        
        # Onglet de planification
        self.schedule_widget = ScheduleWidget(self.logger)
        self.tabs.addTab(self.schedule_widget, "Planification")
        
        # Onglet de paramètres
        self.settings_widget = SettingsWidget(self.logger)
        self.tabs.addTab(self.settings_widget, "Paramètres")
        
        # Barre d'état
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Affichage du message de bienvenue
        self.status_bar.showMessage("Bienvenue dans WP Meta Updater")
        
        # Création du menu
        self.create_menu()
    
    def create_menu(self) -> None:
        """Création du menu de l'application"""
        # Menu Fichier
        file_menu = self.menuBar().addMenu("Fichier")
        
        # Action Importer depuis WordPress
        import_wp_action = QAction("Importer depuis WordPress", self)
        import_wp_action.setShortcut("Ctrl+I")
        import_wp_action.triggered.connect(self.on_import_from_wp)
        file_menu.addAction(import_wp_action)
        
        # Action Exporter en CSV
        export_csv_action = QAction("Exporter en CSV", self)
        export_csv_action.setShortcut("Ctrl+E")
        export_csv_action.triggered.connect(self.on_export_to_csv)
        file_menu.addAction(export_csv_action)
        
        # Action Importer depuis CSV
        import_csv_action = QAction("Importer depuis CSV", self)
        import_csv_action.setShortcut("Ctrl+Shift+I")
        import_csv_action.triggered.connect(self.on_import_from_csv)
        file_menu.addAction(import_csv_action)
        
        file_menu.addSeparator()
        
        # Action Quitter
        quit_action = QAction("Quitter", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        # Menu Édition
        edit_menu = self.menuBar().addMenu("Édition")
        
        # Action Sélectionner tout
        select_all_action = QAction("Sélectionner tout", self)
        select_all_action.setShortcut("Ctrl+A")
        select_all_action.triggered.connect(self.on_select_all)
        edit_menu.addAction(select_all_action)
        
        # Action Désélectionner tout
        deselect_all_action = QAction("Désélectionner tout", self)
        deselect_all_action.setShortcut("Ctrl+D")
        deselect_all_action.triggered.connect(self.on_deselect_all)
        edit_menu.addAction(deselect_all_action)
        
        edit_menu.addSeparator()
        
        # Action Annuler
        undo_action = QAction("Annuler", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.on_undo)
        edit_menu.addAction(undo_action)
        
        # Menu Mise à jour
        update_menu = self.menuBar().addMenu("Mise à jour")
        
        # Action Mettre à jour les sélectionnés
        update_selected_action = QAction("Mettre à jour les sélectionnés", self)
        update_selected_action.setShortcut("Ctrl+U")
        update_selected_action.triggered.connect(self.on_update_selected)
        update_menu.addAction(update_selected_action)
        
        # Action Mettre à jour tous les modifiés
        update_all_action = QAction("Mettre à jour tous les modifiés", self)
        update_all_action.setShortcut("Ctrl+Shift+U")
        update_all_action.triggered.connect(self.on_update_all_modified)
        update_menu.addAction(update_all_action)
        
        update_menu.addSeparator()
        
        # Action Planifier une mise à jour
        schedule_action = QAction("Planifier une mise à jour", self)
        schedule_action.triggered.connect(self.on_schedule_update)
        update_menu.addAction(schedule_action)
        
        # Menu Aide
        help_menu = self.menuBar().addMenu("Aide")
        
        # Action À propos
        about_action = QAction("À propos", self)
        about_action.triggered.connect(self.on_about)
        help_menu.addAction(about_action)
    
    def init_managers(self) -> None:
        """Initialisation des gestionnaires"""
        from wp_connector import WordPressConnector
        from data_manager import DataManager
        from update_manager import UpdateManager
        
        # Création des gestionnaires
        self.wp_connector = WordPressConnector(self.logger)
        self.data_manager = DataManager(self.logger)
        
        # Importation conditionnelle du connecteur MySQL (conservé pour la ligne de commande)
        try:
            from wp_meta_direct_update import WordPressDirectConnector, MYSQL_AVAILABLE
            if MYSQL_AVAILABLE:
                self.wp_direct_connector = WordPressDirectConnector(self.logger)
                self.logger.info("Module MySQL disponible, connecteur direct initialisé pour la ligne de commande")
            else:
                self.wp_direct_connector = None
                self.logger.warning("Module MySQL non disponible, connecteur direct désactivé")
        except ImportError:
            self.wp_direct_connector = None
            self.logger.warning("Module wp_meta_direct_update non disponible, connecteur direct désactivé")
        
        # Initialisation du gestionnaire de mise à jour
        self.update_manager = UpdateManager(self.logger, self.wp_connector, self.data_manager, self.wp_direct_connector)
        
        # Transmission des gestionnaires aux widgets
        self.connection_widget.set_wp_connector(self.wp_connector)
        self.metadata_widget.set_data_manager(self.data_manager)
        self.metadata_widget.set_wp_connector(self.wp_connector)
        self.metadata_widget.set_update_manager(self.update_manager)
        self.schedule_widget.set_update_manager(self.update_manager)
        self.schedule_widget.set_data_manager(self.data_manager)
    
    def connect_signals(self) -> None:
        """Connexion des signaux"""
        # Connexion des signaux du widget de connexion API
        self.connection_widget.connection_successful.connect(self.on_connection_successful)
        
        # Connexion des signaux du widget de métadonnées
        self.metadata_widget.status_message.connect(self.status_bar.showMessage)
        
        # Connexion des signaux du widget de planification
        self.schedule_widget.status_message.connect(self.status_bar.showMessage)
    
    def restore_window_state(self) -> None:
        """Restauration de l'état de la fenêtre"""
        # Restauration de la géométrie de la fenêtre
        if self.settings.contains("geometry"):
            self.restoreGeometry(self.settings.value("geometry"))
        else:
            # Position par défaut
            screen_geometry = QApplication.primaryScreen().availableGeometry()
            window_geometry = self.geometry()
            x = (screen_geometry.width() - window_geometry.width()) / 2
            y = (screen_geometry.height() - window_geometry.height()) / 2
            self.move(int(x), int(y))
        
        # Restauration de l'état de la fenêtre
        if self.settings.contains("windowState"):
            self.restoreState(self.settings.value("windowState"))
    
    def save_window_state(self) -> None:
        """Sauvegarde de l'état de la fenêtre"""
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
    
    def closeEvent(self, event) -> None:
        """Gestion de l'événement de fermeture de la fenêtre"""
        # Sauvegarde de l'état de la fenêtre
        self.save_window_state()
        
        # Sauvegarde de la session si des données sont présentes
        if self.data_manager and self.data_manager.data:
            # Sauvegarde automatique de la session
            self.data_manager.save_session_data()
            self.logger.info("Session sauvegardée automatiquement à la fermeture")
            
            # Confirmation de fermeture si des modifications sont en cours
            if self.data_manager.modified_items:
                reply = QMessageBox.question(
                    self,
                    "Confirmation",
                    "Des modifications n'ont pas été enregistrées. Voulez-vous vraiment quitter ?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )
                
                if reply == QMessageBox.StandardButton.No:
                    event.ignore()
                    return
        
        # Arrêt du planificateur de mises à jour
        if self.update_manager:
            self.update_manager._stop_scheduler()
        
        # Acceptation de l'événement de fermeture
        event.accept()
    
    @pyqtSlot()
    def on_import_from_wp(self) -> None:
        """Importation des données depuis WordPress"""
        if not self.wp_connector or not self.wp_connector.api_url:
            QMessageBox.warning(
                self,
                "Erreur",
                "Veuillez d'abord configurer la connexion à WordPress",
                QMessageBox.StandardButton.Ok
            )
            return
        
        # Passage à l'onglet de métadonnées
        self.tabs.setCurrentWidget(self.metadata_widget)
        
        # Lancement de l'importation
        self.metadata_widget.import_from_wp()
    
    @pyqtSlot()
    def on_export_to_csv(self) -> None:
        """Exportation des données vers un fichier CSV"""
        if not self.data_manager or not self.data_manager.data:
            QMessageBox.warning(
                self,
                "Erreur",
                "Aucune donnée à exporter",
                QMessageBox.StandardButton.Ok
            )
            return
        
        # Sélection du fichier de destination
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter en CSV",
            os.path.join(os.path.expanduser("~"), "export_wp_meta.csv"),
            "Fichiers CSV (*.csv)"
        )
        
        if not file_path:
            return
        
        # Confirmation pour exporter tout ou seulement les sélectionnés
        export_all = True
        
        if self.data_manager.selected_items:
            reply = QMessageBox.question(
                self,
                "Confirmation",
                "Voulez-vous exporter toutes les données ou seulement les éléments sélectionnés ?",
                "Tout", "Sélectionnés", "Annuler"
            )
            
            if reply == 2:  # Annuler
                return
            
            export_all = (reply == 0)  # Tout
        
        # Exportation des données
        success = self.data_manager.export_to_csv(file_path, export_all)
        
        if success:
            QMessageBox.information(
                self,
                "Succès",
                f"Données exportées avec succès vers {file_path}",
                QMessageBox.StandardButton.Ok
            )
            
            self.status_bar.showMessage(f"Données exportées vers {file_path}")
        else:
            QMessageBox.warning(
                self,
                "Erreur",
                "Erreur lors de l'exportation des données",
                QMessageBox.StandardButton.Ok
            )
    
    @pyqtSlot()
    def on_import_from_csv(self) -> None:
        """Importation des données depuis un fichier CSV"""
        if not self.data_manager:
            QMessageBox.warning(
                self,
                "Erreur",
                "Gestionnaire de données non initialisé",
                QMessageBox.StandardButton.Ok
            )
            return
        
        # Sélection du fichier source
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Importer depuis CSV",
            os.path.join(os.path.expanduser("~")),
            "Fichiers CSV (*.csv)"
        )
        
        if not file_path:
            return
        
        # Importation des données
        success, message, count = self.data_manager.import_from_csv(file_path)
        
        if success:
            QMessageBox.information(
                self,
                "Succès",
                f"{message}",
                QMessageBox.StandardButton.Ok
            )
            
            self.status_bar.showMessage(f"Données importées depuis {file_path}")
            
            # Passage à l'onglet de métadonnées
            self.tabs.setCurrentWidget(self.metadata_widget)
        else:
            QMessageBox.warning(
                self,
                "Erreur",
                f"Erreur lors de l'importation des données: {message}",
                QMessageBox.StandardButton.Ok
            )
    
    @pyqtSlot()
    def on_select_all(self) -> None:
        """Sélection de tous les éléments"""
        if self.data_manager:
            self.data_manager.select_all(True)
            self.status_bar.showMessage("Tous les éléments sélectionnés")
    
    @pyqtSlot()
    def on_deselect_all(self) -> None:
        """Désélection de tous les éléments"""
        if self.data_manager:
            self.data_manager.select_all(False)
            self.status_bar.showMessage("Tous les éléments désélectionnés")
    
    @pyqtSlot()
    def on_undo(self) -> None:
        """Annulation de la dernière modification"""
        if self.data_manager:
            success = self.data_manager.restore_from_history()
            
            if success:
                self.status_bar.showMessage("Dernière modification annulée")
            else:
                self.status_bar.showMessage("Impossible d'annuler")
    
    @pyqtSlot()
    def on_update_selected(self) -> None:
        """Mise à jour des éléments sélectionnés"""
        if not self.data_manager or not self.update_manager:
            return
        
        # Récupération des éléments sélectionnés
        items = self.data_manager.get_items_for_update(selected_only=True)
        
        if not items:
            QMessageBox.warning(
                self,
                "Erreur",
                "Aucun élément sélectionné à mettre à jour",
                QMessageBox.StandardButton.Ok
            )
            return
        
        # Choix de la méthode de mise à jour
        method = self._choose_update_method()
        if method is None:
            return
        
        # Confirmation de la mise à jour
        reply = QMessageBox.question(
            self,
            "Confirmation",
            f"Voulez-vous mettre à jour {len(items)} éléments sélectionnés ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.No:
            return
        
        # Lancement de la mise à jour
        self.update_manager.update_metadata(items, selected_only=True, method=method)
        
        # Passage à l'onglet de métadonnées
        self.tabs.setCurrentWidget(self.metadata_widget)
    
    @pyqtSlot()
    def on_update_all_modified(self) -> None:
        """Mise à jour de tous les éléments modifiés"""
        if not self.data_manager or not self.update_manager:
            return
        
        # Récupération des éléments modifiés
        items = self.data_manager.get_items_for_update(selected_only=False)
        
        if not items:
            QMessageBox.warning(
                self,
                "Erreur",
                "Aucun élément modifié à mettre à jour",
                QMessageBox.StandardButton.Ok
            )
            return
        
        # Choix de la méthode de mise à jour
        method = self._choose_update_method()
        if method is None:
            return
        
        # Confirmation de la mise à jour
        reply = QMessageBox.question(
            self,
            "Confirmation",
            f"Voulez-vous mettre à jour tous les {len(items)} éléments modifiés ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.No:
            return
        
        # Lancement de la mise à jour
        self.update_manager.update_metadata(items, selected_only=False, method=method)
        
        # Passage à l'onglet de métadonnées
        self.tabs.setCurrentWidget(self.metadata_widget)
    
    def _choose_update_method(self) -> Optional[str]:
        """
        Demande à l'utilisateur de choisir la méthode de mise à jour
        
        Returns:
            Méthode choisie ("api" ou "mysql") ou None si annulé
        """
        # Vérification des connexions disponibles
        api_available = self.wp_connector and self.wp_connector.api_url and self.wp_connector.auth_token
        mysql_available = self.wp_direct_connector is not None and hasattr(self.wp_direct_connector, "connect") and self.settings.contains("mysql/host")
        
        # Si une seule méthode est disponible, l'utiliser automatiquement
        if api_available and not mysql_available:
            return "api"
        elif mysql_available and not api_available:
            return "mysql"
        elif not api_available and not mysql_available:
            QMessageBox.warning(
                self,
                "Erreur",
                "Aucune connexion n'est configurée. Veuillez configurer la connexion API ou MySQL.",
                QMessageBox.StandardButton.Ok
            )
            return None
        
        # Si les deux méthodes sont disponibles, demander à l'utilisateur
        reply = QMessageBox.question(
            self,
            "Méthode de mise à jour",
            "Quelle méthode de mise à jour souhaitez-vous utiliser ?",
            "API REST (standard)", "MySQL (direct)", "Annuler"
        )
        
        if reply == 0:
            return "api"
        elif reply == 1:
            return "mysql"
        else:
            return None
    
    @pyqtSlot()
    def on_schedule_update(self) -> None:
        """Planification d'une mise à jour"""
        # Passage à l'onglet de planification
        self.tabs.setCurrentWidget(self.schedule_widget)
        
        # Ouverture de la boîte de dialogue de planification
        self.schedule_widget.show_schedule_dialog()
    
    @pyqtSlot()
    def on_about(self) -> None:
        """Affichage de la boîte de dialogue À propos"""
        about_dialog = AboutDialog(self)
        about_dialog.exec()
        
    def restore_previous_session(self) -> None:
        """Restauration de la session précédente"""
        if not self.data_manager:
            return
            
        # Vérification si une session précédente existe
        session_file = self.data_manager.session_file
        if not os.path.exists(session_file):
            self.logger.info("Aucune session précédente trouvée")
            return
            
        # Demande à l'utilisateur s'il souhaite restaurer la session précédente
        reply = QMessageBox.question(
            self,
            "Restauration de session",
            "Une session précédente a été trouvée. Souhaitez-vous la restaurer ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Restauration de la session
            success = self.data_manager.restore_session()
            
            if success:
                # Passage à l'onglet de métadonnées
                self.tabs.setCurrentWidget(self.metadata_widget)
                
                # Mise à jour du statut
                total_items = sum(len(items) for items in self.data_manager.data.values())
                self.status_bar.showMessage(f"Session restaurée: {total_items} éléments chargés")
                
                # Mise à jour des types de contenu dans le widget de métadonnées
                self.metadata_widget.update_content_types()
            else:
                self.status_bar.showMessage("Impossible de restaurer la session précédente")
    
    @pyqtSlot(bool, str)
    def on_connection_successful(self, success: bool, message: str) -> None:
        """Gestion de la connexion API réussie"""
        if success:
            # Passage à l'onglet de métadonnées
            self.tabs.setCurrentWidget(self.metadata_widget)
            
            # Affichage du message de succès
            self.status_bar.showMessage(message)
            
            # Proposition d'importation des données
            reply = QMessageBox.question(
                self,
                "Connexion réussie",
                "Voulez-vous importer les métadonnées depuis WordPress maintenant ?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.on_import_from_wp()
        else:
            # Affichage du message d'erreur
            self.status_bar.showMessage(message)
    
    @pyqtSlot(bool, str)
    def on_mysql_connection_successful(self, success: bool, message: str) -> None:
        """Gestion de la connexion MySQL réussie (conservée pour compatibilité)"""
        if success:
            # Affichage du message de succès
            self.status_bar.showMessage(message)
            
            # Mise à jour du gestionnaire de mise à jour
            if self.update_manager:
                self.update_manager.set_mysql_connection_available(True)
        else:
            # Affichage du message d'erreur
            self.status_bar.showMessage(message)
            
            # Mise à jour du gestionnaire de mise à jour
            if self.update_manager:
                self.update_manager.set_mysql_connection_available(False)
