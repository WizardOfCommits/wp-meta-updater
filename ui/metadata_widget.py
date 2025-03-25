#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Widget de gestion des métadonnées
Permet de visualiser, filtrer et modifier les métadonnées SEO
"""

import os
import logging
import csv
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox,
    QLabel, QLineEdit, QPushButton, QCheckBox, QComboBox,
    QMessageBox, QFileDialog, QProgressBar, QSpacerItem,
    QTableView, QHeaderView, QAbstractItemView, QSplitter,
    QTextEdit, QToolBar, QStatusBar, QDialog, QDialogButtonBox,
    QApplication
)
from PyQt6.QtCore import (
    Qt, QSettings, pyqtSignal, pyqtSlot, QSize, QTimer,
    QAbstractTableModel, QModelIndex, QSortFilterProxyModel
)
from PyQt6.QtGui import QIcon, QFont, QColor, QAction

class MetadataTableModel(QAbstractTableModel):
    """Modèle de données pour le tableau des métadonnées"""
    
    def __init__(self, data_manager=None, parent=None):
        """Initialisation du modèle de données"""
        super().__init__(parent)
        self.data_manager = data_manager
        self.headers = [
            "ID", "Type", "Titre", "URL", 
            "Titre SEO", "Description SEO", 
            "Modifié"
        ]
    
    def rowCount(self, parent=QModelIndex()) -> int:
        """Retourne le nombre de lignes"""
        if parent.isValid() or not self.data_manager:
            return 0
        
        return len(self.data_manager.filtered_data)
    
    def columnCount(self, parent=QModelIndex()) -> int:
        """Retourne le nombre de colonnes"""
        return len(self.headers)
    
    def data(self, index: QModelIndex, role=Qt.ItemDataRole.DisplayRole) -> Any:
        """Retourne les données pour un index donné"""
        if not index.isValid() or not self.data_manager:
            return None
        
        if index.row() >= len(self.data_manager.filtered_data) or index.row() < 0:
            return None
        
        item = self.data_manager.filtered_data[index.row()]
        column = index.column()
        
        if role == Qt.ItemDataRole.DisplayRole:
            # Données à afficher
            if column == 0:
                return str(item["id"])
            elif column == 1:
                return item["type"]
            elif column == 2:
                # Ajout d'un indicateur Rank Math au titre si applicable
                is_rank_math = "rank_math_title" in item or "rank_math_description" in item or item.get("seo_source") == "rank_math"
                if is_rank_math:
                    return f"{item['title']} [RM]"
                return item["title"]
            elif column == 3:
                return item["url"]
            elif column == 4:
                # Indication de la source pour le titre SEO
                if "rank_math_title" in item or item.get("seo_title_source") == "rank_math":
                    return f"{item['seo_title']} [RM]"
                return item["seo_title"]
            elif column == 5:
                # Indication de la source pour la description SEO
                if "rank_math_description" in item or item.get("seo_description_source") == "rank_math":
                    return f"{item['seo_description']} [RM]"
                return item["seo_description"]
            elif column == 6:
                return "Oui" if item["id"] in self.data_manager.modified_items else "Non"
        
        elif role == Qt.ItemDataRole.BackgroundRole:
            # Couleur de fond
            if item["id"] in self.data_manager.modified_items:
                # Élément modifié
                return QColor(255, 255, 200)  # Jaune clair
            
            # Vérification si c'est Rank Math SEO
            is_rank_math = "rank_math_title" in item or "rank_math_description" in item or item.get("seo_source") == "rank_math"
            
            # Couleur de fond légèrement verte pour les éléments Rank Math dans les colonnes 4 et 5
            if is_rank_math and column in [4, 5]:
                return QColor(240, 255, 240)  # Vert très clair
            
            # Analyse SEO
            if column == 4:  # Titre SEO
                title_length = len(item["seo_title"])
                min_length = 40 if is_rank_math else 30
                max_length = 60
                if title_length < min_length or title_length > max_length:
                    return QColor(255, 200, 200)  # Rouge clair
            
            elif column == 5:  # Description SEO
                desc_length = len(item["seo_description"])
                min_length = 120
                max_length = 160
                if desc_length < min_length or desc_length > max_length:
                    return QColor(255, 200, 200)  # Rouge clair
        
        elif role == Qt.ItemDataRole.CheckStateRole:
            # Case à cocher pour la sélection
            if column == 0:
                return Qt.CheckState.Checked if item["id"] in self.data_manager.selected_items else Qt.CheckState.Unchecked
        
        elif role == Qt.ItemDataRole.ToolTipRole:
            # Infobulle
            # Vérification si c'est Rank Math SEO
            is_rank_math = "rank_math_title" in item or "rank_math_description" in item or item.get("seo_source") == "rank_math"
            
            if column == 2 and is_rank_math:  # Titre avec RM
                return "Métadonnées gérées par Rank Math SEO"
                
            elif column == 4:  # Titre SEO
                title_length = len(item["seo_title"])
                # Ajustement des limites en fonction de la source
                min_length = 40 if is_rank_math else 30
                max_length = 60
                
                tooltip = ""
                if is_rank_math:
                    tooltip = "Titre Rank Math SEO: "
                else:
                    tooltip = "Titre SEO: "
                
                if title_length < min_length:
                    tooltip += f"Trop court ({title_length} caractères, min. recommandé: {min_length})"
                elif title_length > max_length:
                    tooltip += f"Trop long ({title_length} caractères, max. recommandé: {max_length})"
                else:
                    tooltip += f"Longueur optimale ({title_length} caractères)"
                
                return tooltip
            
            elif column == 5:  # Description SEO
                desc_length = len(item["seo_description"])
                # Limites standard pour Rank Math et autres
                min_length = 120
                max_length = 160
                
                tooltip = ""
                if is_rank_math:
                    tooltip = "Description Rank Math SEO: "
                else:
                    tooltip = "Description SEO: "
                
                if desc_length < min_length:
                    tooltip += f"Trop courte ({desc_length} caractères, min. recommandé: {min_length})"
                elif desc_length > max_length:
                    tooltip += f"Trop longue ({desc_length} caractères, max. recommandé: {max_length})"
                else:
                    tooltip += f"Longueur optimale ({desc_length} caractères)"
                
                return tooltip
        
        return None
    
    def headerData(self, section: int, orientation: Qt.Orientation, role=Qt.ItemDataRole.DisplayRole) -> Any:
        """Retourne les données d'en-tête"""
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.headers[section]
        
        return None
    
    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        """Retourne les drapeaux pour un index donné"""
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        
        flags = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        
        # Case à cocher pour la sélection
        if index.column() == 0:
            flags |= Qt.ItemFlag.ItemIsUserCheckable
        
        # Édition des colonnes de métadonnées SEO
        if index.column() in [4, 5]:
            flags |= Qt.ItemFlag.ItemIsEditable
        
        return flags
    
    def setData(self, index: QModelIndex, value: Any, role=Qt.ItemDataRole.EditRole) -> bool:
        """Définit les données pour un index donné"""
        if not index.isValid() or not self.data_manager:
            return False
        
        if index.row() >= len(self.data_manager.filtered_data) or index.row() < 0:
            return False
        
        item = self.data_manager.filtered_data[index.row()]
        column = index.column()
        
        if role == Qt.ItemDataRole.CheckStateRole and column == 0:
            # Sélection/désélection de l'élément
            if value == Qt.CheckState.Checked:
                self.data_manager.select_item(item["id"], True)
            else:
                self.data_manager.select_item(item["id"], False)
            
            # Émettre un signal pour indiquer que les données ont changé
            self.dataChanged.emit(index, index, [Qt.ItemDataRole.CheckStateRole])
            return True
        
        elif role == Qt.ItemDataRole.EditRole:
            # Modification des métadonnées SEO
            if column == 4:  # Titre SEO
                self.data_manager.update_item(item["id"], seo_title=value)
                return True
            
            elif column == 5:  # Description SEO
                self.data_manager.update_item(item["id"], seo_description=value)
                return True
        
        return False
    
    def refresh(self) -> None:
        """Rafraîchit le modèle de données"""
        self.beginResetModel()
        self.endResetModel()

class MetadataFilterProxyModel(QSortFilterProxyModel):
    """Modèle proxy pour le filtrage des métadonnées"""
    
    def __init__(self, parent=None):
        """Initialisation du modèle proxy"""
        super().__init__(parent)
        self.search_text = ""
        self.content_type = "all"
        self.modified_only = False
        self.seo_issues = False
    
    def set_filters(self, search_text: str = "", content_type: str = "all", modified_only: bool = False, seo_issues: bool = False) -> None:
        """Définit les filtres"""
        self.search_text = search_text.lower()
        self.content_type = content_type
        self.modified_only = modified_only
        self.seo_issues = seo_issues
        self.invalidateFilter()
    
    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        """Détermine si une ligne est acceptée par le filtre"""
        # Récupération du modèle source
        source_model = self.sourceModel()
        
        if not source_model or not source_model.data_manager:
            return False
        
        # Récupération de l'élément
        if source_row >= len(source_model.data_manager.filtered_data):
            return False
        
        item = source_model.data_manager.filtered_data[source_row]
        
        # Filtre par type de contenu
        if self.content_type != "all" and item["type"] != self.content_type:
            return False
        
        # Filtre par texte de recherche
        if self.search_text:
            if (self.search_text not in item["title"].lower() and
                self.search_text not in item["url"].lower() and
                self.search_text not in item["seo_title"].lower() and
                self.search_text not in item["seo_description"].lower() and
                self.search_text not in item.get("title_h1", "").lower()):
                return False
        
        # Filtre par état de modification
        if self.modified_only and item["id"] not in source_model.data_manager.modified_items:
            return False
        
        # Filtre par problèmes SEO
        if self.seo_issues:
            has_issues = False
            
            # Vérification de la longueur du titre SEO
            if len(item["seo_title"]) < 30 or len(item["seo_title"]) > 60:
                has_issues = True
            
            # Vérification de la longueur de la description SEO
            if len(item["seo_description"]) < 120 or len(item["seo_description"]) > 160:
                has_issues = True
            
            if not has_issues:
                return False
        
        return True

class EditMetadataDialog(QDialog):
    """Boîte de dialogue d'édition des métadonnées"""
    
    def __init__(self, item: Dict[str, Any], parent=None):
        """Initialisation de la boîte de dialogue"""
        super().__init__(parent)
        
        self.item = item
        self.is_rank_math = self._detect_rank_math_seo()
        self.setup_ui()
        
    def _detect_rank_math_seo(self) -> bool:
        """Détecte si les métadonnées proviennent de Rank Math SEO"""
        # Vérifier si l'élément a des métadonnées Rank Math
        if "rank_math_title" in self.item or "rank_math_description" in self.item:
            return True
        
        # Vérifier dans les métadonnées originales
        if ("original_seo_title" in self.item and 
            "original_seo_title_source" in self.item and 
            self.item.get("original_seo_title_source") == "rank_math"):
            return True
            
        return False
    
    def setup_ui(self) -> None:
        """Configuration de l'interface utilisateur"""
        self.setWindowTitle("Édition des métadonnées SEO")
        self.setMinimumWidth(600)
        
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Informations sur l'élément
        info_group = QGroupBox("Informations")
        info_layout = QFormLayout(info_group)
        
        # ID
        id_label = QLabel(str(self.item["id"]))
        info_layout.addRow("ID:", id_label)
        
        # Type
        type_label = QLabel(self.item["type"])
        info_layout.addRow("Type:", type_label)
        
        # Titre
        title_label = QLabel(self.item["title"])
        title_label.setWordWrap(True)
        info_layout.addRow("Titre:", title_label)
        
        # URL
        url_label = QLabel(self.item["url"])
        url_label.setWordWrap(True)
        url_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse | Qt.TextInteractionFlag.TextSelectableByKeyboard)
        info_layout.addRow("URL:", url_label)
        
        # Source SEO
        if self.is_rank_math:
            seo_source_label = QLabel('<span style="color: #069B36; font-weight: bold;">Rank Math SEO</span>')
        else:
            seo_source_label = QLabel(self.item.get("seo_source", "Source SEO standard"))
        info_layout.addRow("Source SEO:", seo_source_label)
        
        layout.addWidget(info_group)
        
        # Métadonnées SEO
        if self.is_rank_math:
            seo_group = QGroupBox("Métadonnées Rank Math SEO")
            seo_group.setStyleSheet("QGroupBox { color: #069B36; font-weight: bold; }")
        else:
            seo_group = QGroupBox("Métadonnées SEO")
        
        seo_layout = QFormLayout(seo_group)
        
        # Titre H1
        self.title_h1_edit = QLineEdit(self.item.get("title_h1", self.item["title"]))
        self.title_h1_edit.setPlaceholderText("Titre H1")
        seo_layout.addRow("Titre H1:", self.title_h1_edit)
        
        # Titre SEO
        self.title_edit = QLineEdit(self.item["seo_title"])
        self.title_edit.setPlaceholderText("Titre SEO")
        self.title_edit.textChanged.connect(self.on_title_changed)
        
        # Label du titre SEO avec des informations spécifiques pour Rank Math
        if self.is_rank_math:
            title_label = QLabel("Titre SEO (Rank Math):")
            title_label.setToolTip("Ce titre sera utilisé par Rank Math SEO pour les moteurs de recherche")
        else:
            title_label = QLabel("Titre SEO:")
        
        seo_layout.addRow(title_label, self.title_edit)
        
        # Compteur de caractères pour le titre
        self.title_counter = QLabel()
        self.update_title_counter(self.item["seo_title"])
        seo_layout.addRow("", self.title_counter)
        
        # Description SEO
        self.description_edit = QTextEdit()
        self.description_edit.setPlainText(self.item["seo_description"])
        self.description_edit.setPlaceholderText("Description SEO")
        self.description_edit.textChanged.connect(self.on_description_changed)
        self.description_edit.setMaximumHeight(100)
        
        # Label de la description SEO avec des informations spécifiques pour Rank Math
        if self.is_rank_math:
            desc_label = QLabel("Description SEO (Rank Math):")
            desc_label.setToolTip("Cette description sera utilisée par Rank Math SEO pour les moteurs de recherche")
        else:
            desc_label = QLabel("Description SEO:")
            
        seo_layout.addRow(desc_label, self.description_edit)
        
        # Compteur de caractères pour la description
        self.description_counter = QLabel()
        self.update_description_counter(self.item["seo_description"])
        seo_layout.addRow("", self.description_counter)
        
        layout.addWidget(seo_group)
        
        # Prévisualisation SERP (Search Engine Results Page) pour Rank Math
        if self.is_rank_math:
            preview_group = QGroupBox("Prévisualisation SERP")
            preview_layout = QVBoxLayout(preview_group)
            
            # Titre de la prévisualisation
            self.preview_title = QLabel()
            self.preview_title.setWordWrap(True)
            self.preview_title.setStyleSheet("color: #1a0dab; font-size: 18px; text-decoration: none; font-weight: 400;")
            
            # URL de la prévisualisation
            self.preview_url = QLabel()
            self.preview_url.setWordWrap(True)
            self.preview_url.setStyleSheet("color: #006621; font-size: 14px;")
            
            # Description de la prévisualisation
            self.preview_description = QLabel()
            self.preview_description.setWordWrap(True)
            self.preview_description.setStyleSheet("color: #545454; font-size: 14px;")
            
            # Ajout des éléments à la prévisualisation
            preview_layout.addWidget(self.preview_title)
            preview_layout.addWidget(self.preview_url)
            preview_layout.addWidget(self.preview_description)
            
            layout.addWidget(preview_group)
            
            # Mise à jour initiale de la prévisualisation
            self.update_serp_preview()
            
            # Connexion des signaux pour mettre à jour la prévisualisation
            self.title_edit.textChanged.connect(self.update_serp_preview)
            self.description_edit.textChanged.connect(self.update_serp_preview)
        
        # Boutons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def on_title_changed(self) -> None:
        """Gestion du changement de titre SEO"""
        self.update_title_counter(self.title_edit.text())
    
    def on_description_changed(self) -> None:
        """Gestion du changement de description SEO"""
        self.update_description_counter(self.description_edit.toPlainText())
    
    def update_title_counter(self, text: str) -> None:
        """Mise à jour du compteur de caractères pour le titre"""
        length = len(text)
        
        # Détermination des limites en fonction de la source SEO
        if self.is_rank_math:
            # Limites spécifiques à Rank Math SEO
            min_length = 40
            max_length = 60
        else:
            # Limites génériques
            min_length = 30
            max_length = 60
        
        if length < min_length:
            self.title_counter.setText(f"<span style='color: red;'>{length} caractères (trop court, min. recommandé: {min_length})</span>")
        elif length > max_length:
            self.title_counter.setText(f"<span style='color: red;'>{length} caractères (trop long, max. recommandé: {max_length})</span>")
        else:
            self.title_counter.setText(f"<span style='color: green;'>{length} caractères (longueur optimale)</span>")
    
    def update_description_counter(self, text: str) -> None:
        """Mise à jour du compteur de caractères pour la description"""
        length = len(text)
        
        # Détermination des limites en fonction de la source SEO
        if self.is_rank_math:
            # Limites spécifiques à Rank Math SEO
            min_length = 120
            max_length = 160
        else:
            # Limites génériques
            min_length = 120
            max_length = 160
        
        if length < min_length:
            self.description_counter.setText(f"<span style='color: red;'>{length} caractères (trop court, min. recommandé: {min_length})</span>")
        elif length > max_length:
            self.description_counter.setText(f"<span style='color: red;'>{length} caractères (trop long, max. recommandé: {max_length})</span>")
        else:
            self.description_counter.setText(f"<span style='color: green;'>{length} caractères (longueur optimale)</span>")
    
    def update_serp_preview(self) -> None:
        """Mise à jour de la prévisualisation SERP"""
        if not hasattr(self, 'preview_title') or not hasattr(self, 'preview_url') or not hasattr(self, 'preview_description'):
            return
            
        # Récupération des valeurs actuelles
        title = self.title_edit.text() or self.item.get("seo_title", "")
        description = self.description_edit.toPlainText() or self.item.get("seo_description", "")
        url = self.item.get("url", "")
        
        # Troncature du titre (maximum 60 caractères pour Google)
        if len(title) > 60:
            display_title = title[:57] + "..."
        else:
            display_title = title
        
        # Troncature de la description (maximum 160 caractères pour Google)
        if len(description) > 160:
            display_description = description[:157] + "..."
        else:
            display_description = description
        
        # Formatage de l'URL pour la prévisualisation
        # Supprimer le protocole et tronquer si nécessaire
        display_url = url.replace("https://", "").replace("http://", "")
        if len(display_url) > 50:
            display_url = display_url[:47] + "..."
        
        # Mise à jour des labels de prévisualisation
        self.preview_title.setText(display_title)
        self.preview_url.setText(display_url)
        self.preview_description.setText(display_description)
    
    def get_metadata(self) -> Tuple[str, str, str]:
        """Récupère les métadonnées modifiées"""
        return self.title_edit.text(), self.description_edit.toPlainText(), self.title_h1_edit.text()

class MetadataWidget(QWidget):
    """Widget de gestion des métadonnées"""
    
    # Signaux
    status_message = pyqtSignal(str)
    
    def __init__(self, logger: logging.Logger):
        """Initialisation du widget de métadonnées"""
        super().__init__()
        
        self.logger = logger
        self.settings = QSettings("WP Meta Tools", "WordPress Meta Updater")
        
        self.wp_connector = None
        self.data_manager = None
        self.update_manager = None
        
        # Configuration de l'interface utilisateur
        self.setup_ui()
    
    def setup_ui(self) -> None:
        """Configuration de l'interface utilisateur"""
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Barre d'outils
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(16, 16))
        
        # Action Importer depuis WordPress
        import_action = QAction("Importer depuis WordPress", self)
        import_action.triggered.connect(self.import_from_wp)
        toolbar.addAction(import_action)
        
        # Action Exporter en CSV
        export_action = QAction("Exporter en CSV", self)
        export_action.triggered.connect(self.export_to_csv)
        toolbar.addAction(export_action)
        
        # Action Importer depuis CSV
        import_csv_action = QAction("Importer depuis CSV", self)
        import_csv_action.triggered.connect(self.import_from_csv)
        toolbar.addAction(import_csv_action)
        
        toolbar.addSeparator()
        
        # Action Mettre à jour les sélectionnés
        update_selected_action = QAction("Mettre à jour les sélectionnés", self)
        update_selected_action.triggered.connect(self.update_selected)
        toolbar.addAction(update_selected_action)
        
        # Action Mettre à jour tous les modifiés
        update_all_action = QAction("Mettre à jour tous les modifiés", self)
        update_all_action.triggered.connect(self.update_all_modified)
        toolbar.addAction(update_all_action)
        
        main_layout.addWidget(toolbar)
        
        # Groupe de filtres
        filter_group = QGroupBox("Filtres")
        filter_layout = QHBoxLayout(filter_group)
        filter_layout.setContentsMargins(10, 10, 10, 10)
        filter_layout.setSpacing(10)
        
        # Filtre par texte
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Rechercher...")
        self.search_edit.textChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.search_edit)
        
        # Filtre par type de contenu
        self.type_combo = QComboBox()
        self.type_combo.addItem("Tous les types", "all")
        self.type_combo.currentIndexChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.type_combo)
        
        # Filtre par état de modification
        self.modified_check = QCheckBox("Modifiés uniquement")
        self.modified_check.stateChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.modified_check)
        
        # Filtre par problèmes SEO
        self.seo_issues_check = QCheckBox("Problèmes SEO")
        self.seo_issues_check.stateChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.seo_issues_check)
        
        main_layout.addWidget(filter_group)
        
        # Tableau des métadonnées
        self.table_view = QTableView()
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSortingEnabled(True)
        self.table_view.doubleClicked.connect(self.on_table_double_clicked)
        self.table_view.clicked.connect(self.on_table_clicked)
        
        # Configuration des en-têtes
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        
        # Modèle de données
        self.table_model = MetadataTableModel()
        self.proxy_model = MetadataFilterProxyModel()
        self.proxy_model.setSourceModel(self.table_model)
        self.table_view.setModel(self.proxy_model)
        
        main_layout.addWidget(self.table_view)
        
        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # Barre d'état
        self.status_label = QLabel("Prêt")
        main_layout.addWidget(self.status_label)
    
    def set_wp_connector(self, wp_connector) -> None:
        """Définit le connecteur WordPress"""
        self.wp_connector = wp_connector
    
    def set_data_manager(self, data_manager) -> None:
        """Définit le gestionnaire de données"""
        self.data_manager = data_manager
        self.table_model.data_manager = data_manager
        
        # Connexion des signaux
        self.data_manager.data_changed.connect(self.on_data_changed)
        self.data_manager.import_progress.connect(self.on_import_progress)
        self.data_manager.export_progress.connect(self.on_export_progress)
    
    def set_update_manager(self, update_manager) -> None:
        """Définit le gestionnaire de mises à jour"""
        self.update_manager = update_manager
        
        # Connexion des signaux
        self.update_manager.update_started.connect(self.on_update_started)
        self.update_manager.update_progress.connect(self.on_update_progress)
        self.update_manager.update_completed.connect(self.on_update_completed)
        self.update_manager.update_error.connect(self.on_update_error)
    
    def update_content_types(self) -> None:
        """Mise à jour des types de contenu disponibles"""
        if not self.wp_connector:
            return
        
        # Sauvegarde de l'index actuel
        current_index = self.type_combo.currentIndex()
        
        # Déconnexion du signal pour éviter les appels pendant la mise à jour
        self.type_combo.currentIndexChanged.disconnect(self.apply_filters)
        
        # Effacement des types existants
        self.type_combo.clear()
        
        # Ajout de l'option "Tous les types"
        self.type_combo.addItem("Tous les types", "all")
        
        # Ajout des types de contenu disponibles
        for type_name, type_label in self.wp_connector.CONTENT_TYPES.items():
            self.type_combo.addItem(type_label, type_name)
        
        # Restauration de l'index
        if current_index < self.type_combo.count():
            self.type_combo.setCurrentIndex(current_index)
        
        # Reconnexion du signal
        self.type_combo.currentIndexChanged.connect(self.apply_filters)
    
    @pyqtSlot()
    def apply_filters(self) -> None:
        """Application des filtres"""
        if not self.data_manager:
            return
        
        # Récupération des critères de filtrage
        search_text = self.search_edit.text()
        content_type = self.type_combo.currentData()
        modified_only = self.modified_check.isChecked()
        seo_issues = self.seo_issues_check.isChecked()
        
        # Application des filtres
        self.proxy_model.set_filters(search_text, content_type, modified_only, seo_issues)
        
        # Mise à jour du statut
        filtered_count = self.proxy_model.rowCount()
        total_count = sum(len(items) for items in self.data_manager.data.values())
        
        self.status_label.setText(f"{filtered_count} éléments affichés sur {total_count}")
    
    @pyqtSlot(QModelIndex)
    def on_table_clicked(self, index: QModelIndex) -> None:
        """Gestion du clic sur le tableau"""
        if not self.data_manager:
            return
        
        # Récupération de l'index source
        source_index = self.proxy_model.mapToSource(index)
        
        if not source_index.isValid():
            return
        
        # Vérification si le clic est sur la première colonne (case à cocher)
        if source_index.column() == 0:
            # Récupération de l'élément
            row = source_index.row()
            
            if row >= len(self.data_manager.filtered_data):
                return
            
            item = self.data_manager.filtered_data[row]
            
            # Basculement de l'état de sélection
            is_selected = item["id"] in self.data_manager.selected_items
            self.data_manager.select_item(item["id"], not is_selected)
            
            # Rafraîchissement de la ligne
            self.table_model.dataChanged.emit(
                self.table_model.index(row, 0),
                self.table_model.index(row, 0),
                [Qt.ItemDataRole.CheckStateRole]
            )
    
    @pyqtSlot(QModelIndex)
    def on_table_double_clicked(self, index: QModelIndex) -> None:
        """Gestion du double-clic sur le tableau"""
        if not self.data_manager:
            return
        
        # Récupération de l'index source
        source_index = self.proxy_model.mapToSource(index)
        
        if not source_index.isValid():
            return
        
        # Récupération de l'élément
        row = source_index.row()
        
        if row >= len(self.data_manager.filtered_data):
            return
        
        item = self.data_manager.filtered_data[row]
        
        # Ouverture de la boîte de dialogue d'édition
        dialog = EditMetadataDialog(item, self)
        
        if dialog.exec():
            # Récupération des métadonnées modifiées
            seo_title, seo_description, title_h1 = dialog.get_metadata()
            
            # Mise à jour de l'élément
            self.data_manager.update_item(item["id"], seo_title, seo_description, title_h1)
    
    @pyqtSlot()
    def on_data_changed(self) -> None:
        """Gestion du changement de données"""
        # Rafraîchissement du modèle
        self.table_model.refresh()
        
        # Mise à jour du statut
        filtered_count = self.proxy_model.rowCount()
        total_count = sum(len(items) for items in self.data_manager.data.values())
        modified_count = len(self.data_manager.modified_items)
        
        self.status_label.setText(f"{filtered_count} éléments affichés sur {total_count} ({modified_count} modifiés)")
        self.status_message.emit(f"{filtered_count} éléments affichés sur {total_count} ({modified_count} modifiés)")
    
    @pyqtSlot(int, int, str)
    def on_import_progress(self, current: int, total: int, message: str) -> None:
        """Gestion de la progression de l'importation"""
        # Mise à jour de la barre de progression
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)
        
        # Mise à jour du statut
        self.status_label.setText(message)
        self.status_message.emit(message)
        
        # Traitement des événements pour éviter le gel de l'interface
        QApplication.processEvents()
    
    @pyqtSlot(int, int, str)
    def on_export_progress(self, current: int, total: int, message: str) -> None:
        """Gestion de la progression de l'exportation"""
        # Mise à jour de la barre de progression
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)
        
        # Mise à jour du statut
        self.status_label.setText(message)
        self.status_message.emit(message)
        
        # Traitement des événements pour éviter le gel de l'interface
        QApplication.processEvents()
    
    @pyqtSlot()
    def on_update_started(self) -> None:
        """Gestion du début de la mise à jour"""
        # Affichage de la barre de progression
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Mise à jour du statut
        self.status_label.setText("Mise à jour des métadonnées sur WordPress...")
        self.status_message.emit("Mise à jour des métadonnées sur WordPress...")
    
    @pyqtSlot(int, int)
    def on_update_progress(self, current: int, total: int) -> None:
        """Gestion de la progression de la mise à jour"""
        # Mise à jour de la barre de progression
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)
        
        # Mise à jour du statut
        self.status_label.setText(f"Mise à jour des métadonnées sur WordPress... ({current}/{total})")
        self.status_message.emit(f"Mise à jour des métadonnées sur WordPress... ({current}/{total})")
        
        # Traitement des événements pour éviter le gel de l'interface
        QApplication.processEvents()
    
    @pyqtSlot(dict)
    def on_update_completed(self, stats: Dict[str, Any]) -> None:
        """Gestion de la fin de la mise à jour"""
        # Masquage de la barre de progression
        self.progress_bar.setVisible(False)
        
        # Mise à jour du statut
        success_count = stats.get("success", 0)
        failed_count = stats.get("failed", 0)
        
        self.status_label.setText(f"Mise à jour terminée: {success_count} réussies, {failed_count} échouées")
        self.status_message.emit(f"Mise à jour terminée: {success_count} réussies, {failed_count} échouées")
        
        # Affichage des erreurs si nécessaire
        if failed_count > 0:
            errors = stats.get("errors", [])
            error_message = "Erreurs lors de la mise à jour:\n\n"
            
            for error in errors:
                error_message += f"- {error['type']} {error['id']} ({error['title']}): {error['error']}\n"
            
            QMessageBox.warning(
                self,
                "Erreurs de mise à jour",
                error_message,
                QMessageBox.StandardButton.Ok
            )
    
    @pyqtSlot(str)
    def on_update_error(self, error: str) -> None:
        """Gestion des erreurs de mise à jour"""
        # Masquage de la barre de progression
        self.progress_bar.setVisible(False)
        
        # Mise à jour du statut
        self.status_label.setText(f"Erreur lors de la mise à jour: {error}")
        self.status_message.emit(f"Erreur lors de la mise à jour: {error}")
        
        # Affichage de l'erreur
        QMessageBox.critical(
            self,
            "Erreur de mise à jour",
            f"Une erreur est survenue lors de la mise à jour:\n\n{error}",
            QMessageBox.StandardButton.Ok
        )
    
    @pyqtSlot()
    def import_from_wp(self) -> None:
        """Importation des données depuis WordPress"""
        if not self.wp_connector or not self.data_manager:
            QMessageBox.warning(
                self,
                "Erreur",
                "Connecteur WordPress ou gestionnaire de données non initialisé",
                QMessageBox.StandardButton.Ok
            )
            return
        
        # Création d'une boîte de dialogue pour les options d'importation
        import_dialog = QDialog(self)
        import_dialog.setWindowTitle("Options d'importation")
        import_dialog.setMinimumWidth(400)
        
        # Layout principal
        layout = QVBoxLayout(import_dialog)
        
        # Groupe de types de contenu
        content_group = QGroupBox("Types de contenu à importer")
        content_layout = QVBoxLayout(content_group)
        
        # Checkboxes pour les types de contenu
        content_checks = {}
        for type_name, type_label in self.wp_connector.CONTENT_TYPES.items():
            check = QCheckBox(type_label)
            check.setChecked(True)
            content_layout.addWidget(check)
            content_checks[type_name] = check
        
        layout.addWidget(content_group)
        
        # Groupe de catégories (pour les articles)
        category_group = QGroupBox("Filtrer par catégorie (optionnel)")
        category_layout = QFormLayout(category_group)
        
        # Combobox pour les catégories
        self.category_combo = QComboBox()
        self.category_combo.addItem("Toutes les catégories", "")
        # Ici, on pourrait ajouter une fonction pour récupérer les catégories depuis WordPress
        # Pour l'instant, on laisse juste l'option "Toutes les catégories"
        
        category_layout.addRow("Catégorie:", self.category_combo)
        layout.addWidget(category_group)
        
        # Boutons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(import_dialog.accept)
        button_box.rejected.connect(import_dialog.reject)
        layout.addWidget(button_box)
        
        # Affichage de la boîte de dialogue
        if import_dialog.exec() != QDialog.DialogCode.Accepted:
            return
        
        # Récupération des types de contenu sélectionnés
        selected_types = [
            type_name for type_name, check in content_checks.items()
            if check.isChecked()
        ]
        
        if not selected_types:
            QMessageBox.warning(
                self,
                "Erreur",
                "Veuillez sélectionner au moins un type de contenu",
                QMessageBox.StandardButton.Ok
            )
            return
        
        # Récupération de la catégorie sélectionnée
        selected_category = self.category_combo.currentData()
        
        # Affichage de la barre de progression et du message d'attente
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(0)  # Mode indéterminé
        self.status_label.setText("Connexion à WordPress et récupération des données...")
        self.status_message.emit("Connexion à WordPress et récupération des données...")
        
        # Mise à jour des types de contenu
        self.update_content_types()
        
        # Création d'un thread pour récupérer les données
        import threading
        
        def fetch_data_thread():
            try:
                # Récupération des données dans un thread séparé
                content_data = self.wp_connector.fetch_all_content(selected_types, selected_category)
                
                # Traitement des données dans le thread principal
                from PyQt6.QtCore import QMetaObject, Qt, Q_ARG
                QMetaObject.invokeMethod(
                    self, 
                    "_process_imported_data", 
                    Qt.ConnectionType.QueuedConnection,
                    Q_ARG(dict, content_data)
                )
            except Exception as e:
                # Gestion des erreurs
                from PyQt6.QtCore import QMetaObject, Qt, Q_ARG
                QMetaObject.invokeMethod(
                    self, 
                    "_handle_import_error", 
                    Qt.ConnectionType.QueuedConnection,
                    Q_ARG(str, str(e))
                )
        
        # Lancement du thread
        thread = threading.Thread(target=fetch_data_thread)
        thread.daemon = True
        thread.start()
    
    def _process_imported_data(self, content_data: dict) -> None:
        """Traite les données importées depuis WordPress"""
        # Passage en mode déterminé pour la barre de progression
        self.progress_bar.setMaximum(100)
        self.status_label.setText("Traitement des données importées...")
        self.status_message.emit("Traitement des données importées...")
        
        # Importation des données
        self.data_manager.import_from_wp(content_data)
    
    def _handle_import_error(self, error_message: str) -> None:
        """Gère les erreurs d'importation"""
        # Masquage de la barre de progression
        self.progress_bar.setVisible(False)
        
        # Affichage de l'erreur
        self.status_label.setText(f"Erreur lors de l'importation: {error_message}")
        self.status_message.emit(f"Erreur lors de l'importation: {error_message}")
        
        QMessageBox.critical(
            self,
            "Erreur d'importation",
            f"Une erreur est survenue lors de l'importation des données:\n\n{error_message}",
            QMessageBox.StandardButton.Ok
        )
    
    @pyqtSlot()
    def export_to_csv(self) -> None:
        """Exportation des données vers un fichier CSV"""
        if not self.data_manager or not self.data_manager.data:
            QMessageBox.warning(
                self,
                "Erreur",
                "Aucune donnée à exporter",
                QMessageBox.StandardButton.Ok
            )
            return
        
        # Création d'une boîte de dialogue pour les options d'exportation
        export_dialog = QDialog(self)
        export_dialog.setWindowTitle("Options d'exportation")
        export_dialog.setMinimumWidth(400)
        
        # Layout principal
        layout = QVBoxLayout(export_dialog)
        
        # Options d'exportation
        options_group = QGroupBox("Options d'exportation")
        options_layout = QVBoxLayout(options_group)
        
        # Option pour exporter toutes les données ou seulement les éléments sélectionnés
        export_all_check = QCheckBox("Exporter toutes les données")
        export_all_check.setChecked(True)
        options_layout.addWidget(export_all_check)
        
        export_selected_check = QCheckBox("Exporter uniquement les éléments sélectionnés")
        export_selected_check.setChecked(False)
        options_layout.addWidget(export_selected_check)
        
        # Connexion des signaux pour que les options soient mutuellement exclusives
        export_all_check.stateChanged.connect(lambda state: export_selected_check.setChecked(not state))
        export_selected_check.stateChanged.connect(lambda state: export_all_check.setChecked(not state))
        
        layout.addWidget(options_group)
        
        # Boutons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(export_dialog.accept)
        button_box.rejected.connect(export_dialog.reject)
        layout.addWidget(button_box)
        
        # Affichage de la boîte de dialogue
        if export_dialog.exec() != QDialog.DialogCode.Accepted:
            return
        
        # Récupération des options d'exportation
        export_all = export_all_check.isChecked()
        
        # Sélection du fichier de destination
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter vers CSV",
            "",
            "Fichiers CSV (*.csv)"
        )
        
        if not filepath:
            return
        
        # Ajout de l'extension .csv si nécessaire
        if not filepath.lower().endswith(".csv"):
            filepath += ".csv"
        
        # Exportation des données
        success = self.data_manager.export_to_csv(filepath, export_all)
        
        if success:
            QMessageBox.information(
                self,
                "Exportation réussie",
                f"Les données ont été exportées avec succès vers {filepath}",
                QMessageBox.StandardButton.Ok
            )
        else:
            QMessageBox.critical(
                self,
                "Erreur d'exportation",
                f"Une erreur est survenue lors de l'exportation des données",
                QMessageBox.StandardButton.Ok
            )
    
    @pyqtSlot()
    def import_from_csv(self) -> None:
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
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Importer depuis CSV",
            "",
            "Fichiers CSV (*.csv)"
        )
        
        if not filepath:
            return
        
        # Importation des données
        success, message, count = self.data_manager.import_from_csv(filepath)
        
        if success:
            QMessageBox.information(
                self,
                "Importation réussie",
                message,
                QMessageBox.StandardButton.Ok
            )
        else:
            QMessageBox.critical(
                self,
                "Erreur d'importation",
                message,
                QMessageBox.StandardButton.Ok
            )
    
    @pyqtSlot()
    def update_selected(self) -> None:
        """Mise à jour des éléments sélectionnés"""
        if not self.wp_connector or not self.data_manager or not self.update_manager:
            QMessageBox.warning(
                self,
                "Erreur",
                "Connecteur WordPress, gestionnaire de données ou gestionnaire de mises à jour non initialisé",
                QMessageBox.StandardButton.Ok
            )
            return
        
        # Récupération des éléments sélectionnés
        items_to_update = self.data_manager.get_items_for_update(selected_only=True)
        
        if not items_to_update:
            QMessageBox.warning(
                self,
                "Aucun élément sélectionné",
                "Veuillez sélectionner au moins un élément à mettre à jour",
                QMessageBox.StandardButton.Ok
            )
            return
        
        # Confirmation de la mise à jour
        if QMessageBox.question(
            self,
            "Confirmation",
            f"Voulez-vous mettre à jour {len(items_to_update)} éléments sélectionnés sur WordPress ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) != QMessageBox.StandardButton.Yes:
            return
        
        # Lancement de la mise à jour
        self.update_manager.update_items(items_to_update)
    
    @pyqtSlot()
    def update_all_modified(self) -> None:
        """Mise à jour de tous les éléments modifiés"""
        if not self.wp_connector or not self.data_manager or not self.update_manager:
            QMessageBox.warning(
                self,
                "Erreur",
                "Connecteur WordPress, gestionnaire de données ou gestionnaire de mises à jour non initialisé",
                QMessageBox.StandardButton.Ok
            )
            return
        
        # Récupération des éléments modifiés
        items_to_update = self.data_manager.get_items_for_update(selected_only=False)
        
        if not items_to_update:
            QMessageBox.warning(
                self,
                "Aucun élément modifié",
                "Aucun élément n'a été modifié",
                QMessageBox.StandardButton.Ok
            )
            return
        
        # Confirmation de la mise à jour
        if QMessageBox.question(
            self,
            "Confirmation",
            f"Voulez-vous mettre à jour {len(items_to_update)} éléments modifiés sur WordPress ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) != QMessageBox.StandardButton.Yes:
            return
        
        # Lancement de la mise à jour
        self.update_manager.update_items(items_to_update)
