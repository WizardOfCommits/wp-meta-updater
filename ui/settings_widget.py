#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Widget de paramètres
Permet de configurer les paramètres de l'application
"""

import os
import logging
import json
from typing import Dict, List, Any, Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox,
    QLabel, QLineEdit, QPushButton, QCheckBox, QComboBox,
    QMessageBox, QFileDialog, QProgressBar, QSpacerItem,
    QTabWidget, QSpinBox, QColorDialog, QFontDialog
)
from PyQt6.QtCore import Qt, QSettings, pyqtSignal, pyqtSlot, QSize
from PyQt6.QtGui import QIcon, QFont, QColor

class SettingsWidget(QWidget):
    """Widget de paramètres"""
    
    # Signaux
    settings_changed = pyqtSignal()
    
    def __init__(self, logger: logging.Logger):
        """Initialisation du widget de paramètres"""
        super().__init__()
        
        self.logger = logger
        self.settings = QSettings("WP Meta Tools", "WordPress Meta Updater")
        
        # Configuration de l'interface utilisateur
        self.setup_ui()
        
        # Chargement des paramètres
        self.load_settings()
    
    def setup_ui(self) -> None:
        """Configuration de l'interface utilisateur"""
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Titre
        title_label = QLabel("Paramètres")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)
        
        # Onglets de paramètres
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Onglet Général
        general_tab = QWidget()
        self.tabs.addTab(general_tab, "Général")
        self.setup_general_tab(general_tab)
        
        # Onglet Apparence
        appearance_tab = QWidget()
        self.tabs.addTab(appearance_tab, "Apparence")
        self.setup_appearance_tab(appearance_tab)
        
        # Onglet Avancé
        advanced_tab = QWidget()
        self.tabs.addTab(advanced_tab, "Avancé")
        self.setup_advanced_tab(advanced_tab)
        
        # Boutons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        # Bouton Appliquer
        self.apply_button = QPushButton("Appliquer")
        self.apply_button.clicked.connect(self.on_apply)
        buttons_layout.addWidget(self.apply_button)
        
        # Bouton Réinitialiser
        self.reset_button = QPushButton("Réinitialiser")
        self.reset_button.clicked.connect(self.on_reset)
        buttons_layout.addWidget(self.reset_button)
        
        main_layout.addLayout(buttons_layout)
    
    def setup_general_tab(self, tab: QWidget) -> None:
        """Configuration de l'onglet Général"""
        # Layout principal
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Groupe de paramètres généraux
        general_group = QGroupBox("Paramètres généraux")
        general_layout = QFormLayout(general_group)
        
        # Dossier d'exportation par défaut
        self.export_dir_edit = QLineEdit()
        self.export_dir_edit.setReadOnly(True)
        
        export_dir_layout = QHBoxLayout()
        export_dir_layout.addWidget(self.export_dir_edit)
        
        export_dir_button = QPushButton("Parcourir...")
        export_dir_button.clicked.connect(self.on_browse_export_dir)
        export_dir_layout.addWidget(export_dir_button)
        
        general_layout.addRow("Dossier d'exportation par défaut:", export_dir_layout)
        
        # Nombre maximum de threads
        self.max_threads_spin = QSpinBox()
        self.max_threads_spin.setMinimum(1)
        self.max_threads_spin.setMaximum(20)
        general_layout.addRow("Nombre maximum de threads:", self.max_threads_spin)
        
        # Taille du lot pour les mises à jour
        self.batch_size_spin = QSpinBox()
        self.batch_size_spin.setMinimum(1)
        self.batch_size_spin.setMaximum(100)
        general_layout.addRow("Taille du lot pour les mises à jour:", self.batch_size_spin)
        
        # Délai entre les requêtes API
        self.api_delay_spin = QSpinBox()
        self.api_delay_spin.setMinimum(0)
        self.api_delay_spin.setMaximum(5000)
        self.api_delay_spin.setSuffix(" ms")
        general_layout.addRow("Délai entre les requêtes API:", self.api_delay_spin)
        
        layout.addWidget(general_group)
        
        # Groupe de paramètres d'analyse SEO
        seo_group = QGroupBox("Paramètres d'analyse SEO")
        seo_layout = QFormLayout(seo_group)
        
        # Longueur minimale du titre SEO
        self.min_title_length_spin = QSpinBox()
        self.min_title_length_spin.setMinimum(10)
        self.min_title_length_spin.setMaximum(100)
        seo_layout.addRow("Longueur minimale du titre SEO:", self.min_title_length_spin)
        
        # Longueur maximale du titre SEO
        self.max_title_length_spin = QSpinBox()
        self.max_title_length_spin.setMinimum(10)
        self.max_title_length_spin.setMaximum(100)
        seo_layout.addRow("Longueur maximale du titre SEO:", self.max_title_length_spin)
        
        # Longueur minimale de la description SEO
        self.min_desc_length_spin = QSpinBox()
        self.min_desc_length_spin.setMinimum(50)
        self.min_desc_length_spin.setMaximum(300)
        seo_layout.addRow("Longueur minimale de la description SEO:", self.min_desc_length_spin)
        
        # Longueur maximale de la description SEO
        self.max_desc_length_spin = QSpinBox()
        self.max_desc_length_spin.setMinimum(50)
        self.max_desc_length_spin.setMaximum(300)
        seo_layout.addRow("Longueur maximale de la description SEO:", self.max_desc_length_spin)
        
        layout.addWidget(seo_group)
        
        # Espace flexible
        layout.addStretch(1)
    
    def setup_appearance_tab(self, tab: QWidget) -> None:
        """Configuration de l'onglet Apparence"""
        # Layout principal
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Groupe de paramètres d'interface
        interface_group = QGroupBox("Interface utilisateur")
        interface_layout = QFormLayout(interface_group)
        
        # Thème
        self.theme_combo = QComboBox()
        self.theme_combo.addItem("Clair", "light")
        self.theme_combo.addItem("Sombre", "dark")
        self.theme_combo.addItem("Système", "system")
        interface_layout.addRow("Thème:", self.theme_combo)
        
        # Police
        self.font_edit = QLineEdit()
        self.font_edit.setReadOnly(True)
        
        font_layout = QHBoxLayout()
        font_layout.addWidget(self.font_edit)
        
        font_button = QPushButton("Choisir...")
        font_button.clicked.connect(self.on_choose_font)
        font_layout.addWidget(font_button)
        
        interface_layout.addRow("Police:", font_layout)
        
        # Taille de la police
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setMinimum(8)
        self.font_size_spin.setMaximum(24)
        interface_layout.addRow("Taille de la police:", self.font_size_spin)
        
        layout.addWidget(interface_group)
        
        # Groupe de paramètres de couleurs
        colors_group = QGroupBox("Couleurs")
        colors_layout = QFormLayout(colors_group)
        
        # Couleur des éléments modifiés
        self.modified_color_edit = QLineEdit()
        self.modified_color_edit.setReadOnly(True)
        
        modified_color_layout = QHBoxLayout()
        modified_color_layout.addWidget(self.modified_color_edit)
        
        modified_color_button = QPushButton("Choisir...")
        modified_color_button.clicked.connect(lambda: self.on_choose_color("modified"))
        modified_color_layout.addWidget(modified_color_button)
        
        colors_layout.addRow("Couleur des éléments modifiés:", modified_color_layout)
        
        # Couleur des problèmes SEO
        self.seo_issues_color_edit = QLineEdit()
        self.seo_issues_color_edit.setReadOnly(True)
        
        seo_issues_color_layout = QHBoxLayout()
        seo_issues_color_layout.addWidget(self.seo_issues_color_edit)
        
        seo_issues_color_button = QPushButton("Choisir...")
        seo_issues_color_button.clicked.connect(lambda: self.on_choose_color("seo_issues"))
        seo_issues_color_layout.addWidget(seo_issues_color_button)
        
        colors_layout.addRow("Couleur des problèmes SEO:", seo_issues_color_layout)
        
        layout.addWidget(colors_group)
        
        # Espace flexible
        layout.addStretch(1)
    
    def setup_advanced_tab(self, tab: QWidget) -> None:
        """Configuration de l'onglet Avancé"""
        # Layout principal
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Groupe de paramètres avancés
        advanced_group = QGroupBox("Paramètres avancés")
        advanced_layout = QFormLayout(advanced_group)
        
        # Activer le mode débogage
        self.debug_mode_check = QCheckBox()
        advanced_layout.addRow("Activer le mode débogage:", self.debug_mode_check)
        
        # Activer la journalisation détaillée
        self.verbose_logging_check = QCheckBox()
        advanced_layout.addRow("Activer la journalisation détaillée:", self.verbose_logging_check)
        
        # Niveau de journalisation
        self.log_level_combo = QComboBox()
        self.log_level_combo.addItem("DEBUG", "DEBUG")
        self.log_level_combo.addItem("INFO", "INFO")
        self.log_level_combo.addItem("WARNING", "WARNING")
        self.log_level_combo.addItem("ERROR", "ERROR")
        advanced_layout.addRow("Niveau de journalisation:", self.log_level_combo)
        
        # Dossier des journaux
        self.log_dir_edit = QLineEdit()
        self.log_dir_edit.setReadOnly(True)
        
        log_dir_layout = QHBoxLayout()
        log_dir_layout.addWidget(self.log_dir_edit)
        
        log_dir_button = QPushButton("Parcourir...")
        log_dir_button.clicked.connect(self.on_browse_log_dir)
        log_dir_layout.addWidget(log_dir_button)
        
        advanced_layout.addRow("Dossier des journaux:", log_dir_layout)
        
        # Taille maximale des fichiers journaux
        self.max_log_size_spin = QSpinBox()
        self.max_log_size_spin.setMinimum(1)
        self.max_log_size_spin.setMaximum(100)
        self.max_log_size_spin.setSuffix(" Mo")
        advanced_layout.addRow("Taille maximale des fichiers journaux:", self.max_log_size_spin)
        
        # Nombre maximum de fichiers journaux
        self.max_log_files_spin = QSpinBox()
        self.max_log_files_spin.setMinimum(1)
        self.max_log_files_spin.setMaximum(100)
        advanced_layout.addRow("Nombre maximum de fichiers journaux:", self.max_log_files_spin)
        
        layout.addWidget(advanced_group)
        
        # Groupe de paramètres de cache
        cache_group = QGroupBox("Cache")
        cache_layout = QFormLayout(cache_group)
        
        # Activer le cache
        self.enable_cache_check = QCheckBox()
        cache_layout.addRow("Activer le cache:", self.enable_cache_check)
        
        # Dossier du cache
        self.cache_dir_edit = QLineEdit()
        self.cache_dir_edit.setReadOnly(True)
        
        cache_dir_layout = QHBoxLayout()
        cache_dir_layout.addWidget(self.cache_dir_edit)
        
        cache_dir_button = QPushButton("Parcourir...")
        cache_dir_button.clicked.connect(self.on_browse_cache_dir)
        cache_dir_layout.addWidget(cache_dir_button)
        
        cache_layout.addRow("Dossier du cache:", cache_dir_layout)
        
        # Durée de vie du cache
        self.cache_ttl_spin = QSpinBox()
        self.cache_ttl_spin.setMinimum(1)
        self.cache_ttl_spin.setMaximum(30)
        self.cache_ttl_spin.setSuffix(" jours")
        cache_layout.addRow("Durée de vie du cache:", self.cache_ttl_spin)
        
        # Bouton Vider le cache
        clear_cache_button = QPushButton("Vider le cache")
        clear_cache_button.clicked.connect(self.on_clear_cache)
        cache_layout.addRow("", clear_cache_button)
        
        layout.addWidget(cache_group)
        
        # Espace flexible
        layout.addStretch(1)
    
    def load_settings(self) -> None:
        """Chargement des paramètres"""
        # Paramètres généraux
        self.export_dir_edit.setText(self.settings.value("general/export_dir", os.path.expanduser("~")))
        self.max_threads_spin.setValue(int(self.settings.value("general/max_threads", 5)))
        self.batch_size_spin.setValue(int(self.settings.value("general/batch_size", 10)))
        self.api_delay_spin.setValue(int(self.settings.value("general/api_delay", 500)))
        
        # Paramètres d'analyse SEO
        self.min_title_length_spin.setValue(int(self.settings.value("seo/min_title_length", 30)))
        self.max_title_length_spin.setValue(int(self.settings.value("seo/max_title_length", 60)))
        self.min_desc_length_spin.setValue(int(self.settings.value("seo/min_desc_length", 120)))
        self.max_desc_length_spin.setValue(int(self.settings.value("seo/max_desc_length", 160)))
        
        # Paramètres d'apparence
        theme_index = self.theme_combo.findData(self.settings.value("appearance/theme", "system"))
        self.theme_combo.setCurrentIndex(max(0, theme_index))
        
        font_family = self.settings.value("appearance/font_family", QFont().family())
        self.font_edit.setText(font_family)
        self.font_size_spin.setValue(int(self.settings.value("appearance/font_size", 10)))
        
        self.modified_color_edit.setText(self.settings.value("appearance/modified_color", "#FFFFCC"))
        self.modified_color_edit.setStyleSheet(f"background-color: {self.modified_color_edit.text()}")
        
        self.seo_issues_color_edit.setText(self.settings.value("appearance/seo_issues_color", "#FFCCCC"))
        self.seo_issues_color_edit.setStyleSheet(f"background-color: {self.seo_issues_color_edit.text()}")
        
        # Paramètres avancés
        self.debug_mode_check.setChecked(self.settings.value("advanced/debug_mode", False, type=bool))
        self.verbose_logging_check.setChecked(self.settings.value("advanced/verbose_logging", False, type=bool))
        
        log_level_index = self.log_level_combo.findData(self.settings.value("advanced/log_level", "INFO"))
        self.log_level_combo.setCurrentIndex(max(0, log_level_index))
        
        self.log_dir_edit.setText(self.settings.value("advanced/log_dir", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")))
        self.max_log_size_spin.setValue(int(self.settings.value("advanced/max_log_size", 10)))
        self.max_log_files_spin.setValue(int(self.settings.value("advanced/max_log_files", 5)))
        
        # Paramètres de cache
        self.enable_cache_check.setChecked(self.settings.value("cache/enable_cache", True, type=bool))
        self.cache_dir_edit.setText(self.settings.value("cache/cache_dir", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cache")))
        self.cache_ttl_spin.setValue(int(self.settings.value("cache/cache_ttl", 7)))
    
    def save_settings(self) -> None:
        """Sauvegarde des paramètres"""
        # Paramètres généraux
        self.settings.setValue("general/export_dir", self.export_dir_edit.text())
        self.settings.setValue("general/max_threads", self.max_threads_spin.value())
        self.settings.setValue("general/batch_size", self.batch_size_spin.value())
        self.settings.setValue("general/api_delay", self.api_delay_spin.value())
        
        # Paramètres d'analyse SEO
        self.settings.setValue("seo/min_title_length", self.min_title_length_spin.value())
        self.settings.setValue("seo/max_title_length", self.max_title_length_spin.value())
        self.settings.setValue("seo/min_desc_length", self.min_desc_length_spin.value())
        self.settings.setValue("seo/max_desc_length", self.max_desc_length_spin.value())
        
        # Paramètres d'apparence
        old_theme = self.settings.value("appearance/theme", "system")
        new_theme = self.theme_combo.currentData()
        
        self.settings.setValue("appearance/theme", new_theme)
        self.settings.setValue("appearance/font_family", self.font_edit.text())
        self.settings.setValue("appearance/font_size", self.font_size_spin.value())
        self.settings.setValue("appearance/modified_color", self.modified_color_edit.text())
        self.settings.setValue("appearance/seo_issues_color", self.seo_issues_color_edit.text())
        
        # Paramètres avancés
        self.settings.setValue("advanced/debug_mode", self.debug_mode_check.isChecked())
        self.settings.setValue("advanced/verbose_logging", self.verbose_logging_check.isChecked())
        self.settings.setValue("advanced/log_level", self.log_level_combo.currentData())
        self.settings.setValue("advanced/log_dir", self.log_dir_edit.text())
        self.settings.setValue("advanced/max_log_size", self.max_log_size_spin.value())
        self.settings.setValue("advanced/max_log_files", self.max_log_files_spin.value())
        
        # Paramètres de cache
        self.settings.setValue("cache/enable_cache", self.enable_cache_check.isChecked())
        self.settings.setValue("cache/cache_dir", self.cache_dir_edit.text())
        self.settings.setValue("cache/cache_ttl", self.cache_ttl_spin.value())
        
        # Émission du signal de changement de paramètres
        self.settings_changed.emit()
        
        # Appliquer le thème si changé
        if old_theme != new_theme:
            self.apply_theme(new_theme)
        
        self.logger.info("Paramètres sauvegardés")
    
    def apply_theme(self, theme: str) -> None:
        """
        Applique le thème sélectionné
        
        Args:
            theme: Thème à appliquer (light, dark, system)
        """
        from PyQt6.QtWidgets import QApplication
        
        app = QApplication.instance()
        if not app:
            return
        
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
        
        # Mise à jour de l'interface
        for widget in app.allWidgets():
            widget.update()
        
        self.logger.info(f"Thème appliqué: {theme}")
    
    @pyqtSlot()
    def on_apply(self) -> None:
        """Application des paramètres"""
        self.save_settings()
        
        QMessageBox.information(
            self,
            "Succès",
            "Paramètres appliqués avec succès",
            QMessageBox.StandardButton.Ok
        )
    
    @pyqtSlot()
    def on_reset(self) -> None:
        """Réinitialisation des paramètres"""
        reply = QMessageBox.question(
            self,
            "Confirmation",
            "Voulez-vous vraiment réinitialiser tous les paramètres ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Réinitialisation des paramètres
            self.settings.clear()
            
            # Rechargement des paramètres
            self.load_settings()
            
            QMessageBox.information(
                self,
                "Succès",
                "Paramètres réinitialisés avec succès",
                QMessageBox.StandardButton.Ok
            )
    
    @pyqtSlot()
    def on_browse_export_dir(self) -> None:
        """Sélection du dossier d'exportation par défaut"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Sélectionner le dossier d'exportation par défaut",
            self.export_dir_edit.text()
        )
        
        if directory:
            self.export_dir_edit.setText(directory)
    
    @pyqtSlot()
    def on_browse_log_dir(self) -> None:
        """Sélection du dossier des journaux"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Sélectionner le dossier des journaux",
            self.log_dir_edit.text()
        )
        
        if directory:
            self.log_dir_edit.setText(directory)
    
    @pyqtSlot()
    def on_browse_cache_dir(self) -> None:
        """Sélection du dossier du cache"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Sélectionner le dossier du cache",
            self.cache_dir_edit.text()
        )
        
        if directory:
            self.cache_dir_edit.setText(directory)
    
    @pyqtSlot()
    def on_choose_font(self) -> None:
        """Sélection de la police"""
        current_font = QFont(self.font_edit.text(), self.font_size_spin.value())
        font, ok = QFontDialog.getFont(current_font, self, "Sélectionner la police")
        
        if ok:
            self.font_edit.setText(font.family())
            self.font_size_spin.setValue(font.pointSize())
    
    def on_choose_color(self, color_type: str) -> None:
        """
        Sélection d'une couleur
        
        Args:
            color_type: Type de couleur (modified, seo_issues)
        """
        if color_type == "modified":
            current_color = QColor(self.modified_color_edit.text())
            color = QColorDialog.getColor(current_color, self, "Sélectionner la couleur des éléments modifiés")
            
            if color.isValid():
                self.modified_color_edit.setText(color.name())
                self.modified_color_edit.setStyleSheet(f"background-color: {color.name()}")
        
        elif color_type == "seo_issues":
            current_color = QColor(self.seo_issues_color_edit.text())
            color = QColorDialog.getColor(current_color, self, "Sélectionner la couleur des problèmes SEO")
            
            if color.isValid():
                self.seo_issues_color_edit.setText(color.name())
                self.seo_issues_color_edit.setStyleSheet(f"background-color: {color.name()}")
    
    @pyqtSlot()
    def on_clear_cache(self) -> None:
        """Vidage du cache"""
        reply = QMessageBox.question(
            self,
            "Confirmation",
            "Voulez-vous vraiment vider le cache ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            cache_dir = self.cache_dir_edit.text()
            
            if os.path.exists(cache_dir):
                try:
                    # Suppression des fichiers du cache
                    for filename in os.listdir(cache_dir):
                        file_path = os.path.join(cache_dir, filename)
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    
                    QMessageBox.information(
                        self,
                        "Succès",
                        "Cache vidé avec succès",
                        QMessageBox.StandardButton.Ok
                    )
                    
                    self.logger.info("Cache vidé")
                    
                except Exception as e:
                    QMessageBox.warning(
                        self,
                        "Erreur",
                        f"Erreur lors du vidage du cache: {str(e)}",
                        QMessageBox.StandardButton.Ok
                    )
                    
                    self.logger.error(f"Erreur lors du vidage du cache: {str(e)}")
            else:
                QMessageBox.information(
                    self,
                    "Information",
                    "Le dossier du cache n'existe pas",
                    QMessageBox.StandardButton.Ok
                )
