#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Widget de planification des mises à jour
Permet de planifier des mises à jour automatiques
"""

import os
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox,
    QLabel, QLineEdit, QPushButton, QCheckBox, QComboBox,
    QMessageBox, QFileDialog, QProgressBar, QSpacerItem,
    QTableView, QHeaderView, QAbstractItemView, QSplitter,
    QTextEdit, QToolBar, QStatusBar, QDialog, QDialogButtonBox,
    QDateTimeEdit, QSpinBox
)
from PyQt6.QtCore import (
    Qt, QSettings, pyqtSignal, pyqtSlot, QSize, QTimer,
    QAbstractTableModel, QModelIndex, QSortFilterProxyModel,
    QDateTime
)
from PyQt6.QtGui import QIcon, QFont, QColor, QAction

class ScheduleTableModel(QAbstractTableModel):
    """Modèle de données pour le tableau des mises à jour planifiées"""
    
    def __init__(self, update_manager=None, parent=None):
        """Initialisation du modèle de données"""
        super().__init__(parent)
        self.update_manager = update_manager
        self.headers = [
            "ID", "Nom", "Date", "Récurrent", "Intervalle", "Statut"
        ]
        self.scheduled_updates = []
    
    def rowCount(self, parent=QModelIndex()) -> int:
        """Retourne le nombre de lignes"""
        if parent.isValid():
            return 0
        
        return len(self.scheduled_updates)
    
    def columnCount(self, parent=QModelIndex()) -> int:
        """Retourne le nombre de colonnes"""
        return len(self.headers)
    
    def data(self, index: QModelIndex, role=Qt.ItemDataRole.DisplayRole) -> Any:
        """Retourne les données pour un index donné"""
        if not index.isValid():
            return None
        
        if index.row() >= len(self.scheduled_updates) or index.row() < 0:
            return None
        
        update = self.scheduled_updates[index.row()]
        column = index.column()
        
        if role == Qt.ItemDataRole.DisplayRole:
            # Données à afficher
            if column == 0:
                return str(update["id"])
            elif column == 1:
                return update["name"]
            elif column == 2:
                schedule_time = datetime.fromisoformat(update["schedule_time"])
                return schedule_time.strftime("%d/%m/%Y %H:%M")
            elif column == 3:
                return "Oui" if update["recurring"] else "Non"
            elif column == 4:
                if update["recurring"]:
                    return f"{update['interval_days']} jours"
                else:
                    return "-"
            elif column == 5:
                status = update["status"]
                if status == "pending":
                    return "En attente"
                elif status == "running":
                    return "En cours"
                elif status == "completed":
                    return "Terminé"
                elif status == "error":
                    return "Erreur"
                elif status == "missed":
                    return "Manqué"
                else:
                    return status
        
        elif role == Qt.ItemDataRole.BackgroundRole:
            # Couleur de fond
            status = update["status"]
            if status == "pending":
                return QColor(255, 255, 200)  # Jaune clair
            elif status == "running":
                return QColor(200, 255, 200)  # Vert clair
            elif status == "completed":
                return QColor(200, 200, 255)  # Bleu clair
            elif status == "error":
                return QColor(255, 200, 200)  # Rouge clair
            elif status == "missed":
                return QColor(255, 200, 255)  # Rose clair
        
        elif role == Qt.ItemDataRole.ToolTipRole:
            # Infobulle
            if column == 5 and update["status"] == "error":
                return f"Erreur: {update.get('last_error', 'Inconnue')}"
        
        return None
    
    def headerData(self, section: int, orientation: Qt.Orientation, role=Qt.ItemDataRole.DisplayRole) -> Any:
        """Retourne les données d'en-tête"""
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.headers[section]
        
        return None
    
    def refresh(self) -> None:
        """Rafraîchit le modèle de données"""
        if self.update_manager:
            self.scheduled_updates = self.update_manager.get_scheduled_updates()
        else:
            self.scheduled_updates = []
        
        self.beginResetModel()
        self.endResetModel()

class ScheduleDialog(QDialog):
    """Boîte de dialogue de planification des mises à jour"""
    
    def __init__(self, data_manager=None, update_manager=None, parent=None):
        """Initialisation de la boîte de dialogue"""
        super().__init__(parent)
        
        self.data_manager = data_manager
        self.update_manager = update_manager
        
        self.setup_ui()
    
    def setup_ui(self) -> None:
        """Configuration de l'interface utilisateur"""
        self.setWindowTitle("Planification d'une mise à jour")
        self.setMinimumWidth(500)
        
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Groupe de paramètres de planification
        schedule_group = QGroupBox("Paramètres de planification")
        schedule_layout = QFormLayout(schedule_group)
        
        # Nom de la mise à jour
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Nom de la mise à jour")
        schedule_layout.addRow("Nom:", self.name_edit)
        
        # Date et heure de la mise à jour
        self.datetime_edit = QDateTimeEdit()
        self.datetime_edit.setDateTime(QDateTime.currentDateTime().addSecs(3600))  # +1 heure
        self.datetime_edit.setCalendarPopup(True)
        self.datetime_edit.setMinimumDateTime(QDateTime.currentDateTime())
        schedule_layout.addRow("Date et heure:", self.datetime_edit)
        
        # Mise à jour récurrente
        self.recurring_check = QCheckBox("Mise à jour récurrente")
        self.recurring_check.stateChanged.connect(self.on_recurring_changed)
        schedule_layout.addRow("", self.recurring_check)
        
        # Intervalle de récurrence
        self.interval_spin = QSpinBox()
        self.interval_spin.setMinimum(1)
        self.interval_spin.setMaximum(365)
        self.interval_spin.setValue(7)  # 7 jours par défaut
        self.interval_spin.setEnabled(False)
        schedule_layout.addRow("Intervalle (jours):", self.interval_spin)
        
        layout.addWidget(schedule_group)
        
        # Groupe de sélection des éléments
        items_group = QGroupBox("Éléments à mettre à jour")
        items_layout = QVBoxLayout(items_group)
        
        # Options de sélection
        options_layout = QHBoxLayout()
        
        # Option Tous les éléments modifiés
        self.all_modified_radio = QCheckBox("Tous les éléments modifiés")
        self.all_modified_radio.setChecked(True)
        options_layout.addWidget(self.all_modified_radio)
        
        # Option Éléments sélectionnés uniquement
        self.selected_only_radio = QCheckBox("Éléments sélectionnés uniquement")
        options_layout.addWidget(self.selected_only_radio)
        
        # Connexion des signaux pour exclusion mutuelle
        self.all_modified_radio.stateChanged.connect(self.on_all_modified_changed)
        self.selected_only_radio.stateChanged.connect(self.on_selected_only_changed)
        
        items_layout.addLayout(options_layout)
        
        # Informations sur les éléments
        self.items_info_label = QLabel()
        self.update_items_info()
        items_layout.addWidget(self.items_info_label)
        
        layout.addWidget(items_group)
        
        # Boutons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def on_recurring_changed(self, state: int) -> None:
        """Gestion du changement d'état de la case à cocher pour la récurrence"""
        self.interval_spin.setEnabled(state == Qt.CheckState.Checked.value)
    
    def on_all_modified_changed(self, state: int) -> None:
        """Gestion du changement d'état de la case à cocher pour tous les éléments modifiés"""
        if state == Qt.CheckState.Checked.value:
            self.selected_only_radio.setChecked(False)
        elif state == Qt.CheckState.Unchecked.value and not self.selected_only_radio.isChecked():
            self.selected_only_radio.setChecked(True)
        
        self.update_items_info()
    
    def on_selected_only_changed(self, state: int) -> None:
        """Gestion du changement d'état de la case à cocher pour les éléments sélectionnés uniquement"""
        if state == Qt.CheckState.Checked.value:
            self.all_modified_radio.setChecked(False)
        elif state == Qt.CheckState.Unchecked.value and not self.all_modified_radio.isChecked():
            self.all_modified_radio.setChecked(True)
        
        self.update_items_info()
    
    def update_items_info(self) -> None:
        """Mise à jour des informations sur les éléments"""
        if not self.data_manager:
            self.items_info_label.setText("Aucune donnée disponible")
            return
        
        if self.all_modified_radio.isChecked():
            # Tous les éléments modifiés
            count = len(self.data_manager.modified_items)
            self.items_info_label.setText(f"{count} éléments modifiés seront mis à jour")
        else:
            # Éléments sélectionnés uniquement
            count = len(self.data_manager.selected_items)
            self.items_info_label.setText(f"{count} éléments sélectionnés seront mis à jour")
    
    def get_schedule_params(self) -> Dict[str, Any]:
        """Récupère les paramètres de planification"""
        return {
            "name": self.name_edit.text(),
            "schedule_time": self.datetime_edit.dateTime().toPython(),
            "recurring": self.recurring_check.isChecked(),
            "interval_days": self.interval_spin.value() if self.recurring_check.isChecked() else 0,
            "selected_only": self.selected_only_radio.isChecked()
        }

class ScheduleWidget(QWidget):
    """Widget de planification des mises à jour"""
    
    # Signaux
    status_message = pyqtSignal(str)
    
    def __init__(self, logger: logging.Logger):
        """Initialisation du widget de planification"""
        super().__init__()
        
        self.logger = logger
        self.settings = QSettings("WP Meta Tools", "WordPress Meta Updater")
        
        self.data_manager = None
        self.update_manager = None
        
        # Configuration de l'interface utilisateur
        self.setup_ui()
        
        # Démarrage du timer de rafraîchissement
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_table)
        self.refresh_timer.start(30000)  # Rafraîchissement toutes les 30 secondes
    
    def setup_ui(self) -> None:
        """Configuration de l'interface utilisateur"""
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Titre
        title_label = QLabel("Planification des mises à jour")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)
        
        # Description
        description_label = QLabel(
            "Planifiez des mises à jour automatiques pour vos métadonnées SEO. "
            "Vous pouvez planifier des mises à jour ponctuelles ou récurrentes."
        )
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(description_label)
        
        # Barre d'outils
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(16, 16))
        
        # Action Planifier une mise à jour
        schedule_action = QAction("Planifier une mise à jour", self)
        schedule_action.triggered.connect(self.show_schedule_dialog)
        toolbar.addAction(schedule_action)
        
        # Action Supprimer la mise à jour sélectionnée
        delete_action = QAction("Supprimer la mise à jour sélectionnée", self)
        delete_action.triggered.connect(self.delete_selected_update)
        toolbar.addAction(delete_action)
        
        # Action Rafraîchir
        refresh_action = QAction("Rafraîchir", self)
        refresh_action.triggered.connect(self.refresh_table)
        toolbar.addAction(refresh_action)
        
        main_layout.addWidget(toolbar)
        
        # Tableau des mises à jour planifiées
        self.table_view = QTableView()
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSortingEnabled(True)
        
        # Configuration des en-têtes
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        
        # Modèle de données
        self.table_model = ScheduleTableModel()
        self.table_view.setModel(self.table_model)
        
        main_layout.addWidget(self.table_view)
        
        # Barre d'état
        self.status_label = QLabel("Prêt")
        main_layout.addWidget(self.status_label)
    
    def set_data_manager(self, data_manager) -> None:
        """Définit le gestionnaire de données"""
        self.data_manager = data_manager
    
    def set_update_manager(self, update_manager) -> None:
        """Définit le gestionnaire de mises à jour"""
        self.update_manager = update_manager
        self.table_model.update_manager = update_manager
        
        # Connexion des signaux
        self.update_manager.scheduled_update_status.connect(self.on_scheduled_update_status)
        
        # Rafraîchissement du tableau
        self.refresh_table()
    
    @pyqtSlot()
    def refresh_table(self) -> None:
        """Rafraîchissement du tableau des mises à jour planifiées"""
        self.table_model.refresh()
        
        # Mise à jour du statut
        count = self.table_model.rowCount()
        self.status_label.setText(f"{count} mises à jour planifiées")
    
    @pyqtSlot()
    def show_schedule_dialog(self) -> None:
        """Affichage de la boîte de dialogue de planification"""
        if not self.data_manager or not self.update_manager:
            QMessageBox.warning(
                self,
                "Erreur",
                "Gestionnaire de données ou de mises à jour non initialisé",
                QMessageBox.StandardButton.Ok
            )
            return
        
        # Vérification des éléments à mettre à jour
        if not self.data_manager.modified_items and not self.data_manager.selected_items:
            QMessageBox.warning(
                self,
                "Erreur",
                "Aucun élément modifié ou sélectionné à mettre à jour",
                QMessageBox.StandardButton.Ok
            )
            return
        
        # Création de la boîte de dialogue
        dialog = ScheduleDialog(self.data_manager, self.update_manager, self)
        
        if dialog.exec():
            # Récupération des paramètres de planification
            params = dialog.get_schedule_params()
            
            # Récupération des éléments à mettre à jour
            if params["selected_only"]:
                items = self.data_manager.get_items_for_update(selected_only=True)
            else:
                items = self.data_manager.get_items_for_update(selected_only=False)
            
            if not items:
                QMessageBox.warning(
                    self,
                    "Erreur",
                    "Aucun élément à mettre à jour",
                    QMessageBox.StandardButton.Ok
                )
                return
            
            # Planification de la mise à jour
            success = self.update_manager.schedule_update(
                items,
                params["schedule_time"],
                params["name"],
                params["recurring"],
                params["interval_days"]
            )
            
            if success:
                QMessageBox.information(
                    self,
                    "Succès",
                    f"Mise à jour planifiée pour le {params['schedule_time'].strftime('%d/%m/%Y %H:%M')}",
                    QMessageBox.StandardButton.Ok
                )
                
                # Rafraîchissement du tableau
                self.refresh_table()
                
                # Mise à jour du statut
                self.status_label.setText(f"Mise à jour planifiée pour le {params['schedule_time'].strftime('%d/%m/%Y %H:%M')}")
                self.status_message.emit(f"Mise à jour planifiée pour le {params['schedule_time'].strftime('%d/%m/%Y %H:%M')}")
            else:
                QMessageBox.warning(
                    self,
                    "Erreur",
                    "Erreur lors de la planification de la mise à jour",
                    QMessageBox.StandardButton.Ok
                )
    
    @pyqtSlot()
    def delete_selected_update(self) -> None:
        """Suppression de la mise à jour sélectionnée"""
        if not self.update_manager:
            return
        
        # Récupération de l'index sélectionné
        indexes = self.table_view.selectionModel().selectedRows()
        
        if not indexes:
            QMessageBox.warning(
                self,
                "Erreur",
                "Aucune mise à jour sélectionnée",
                QMessageBox.StandardButton.Ok
            )
            return
        
        # Récupération de l'ID de la mise à jour
        row = indexes[0].row()
        update_id = int(self.table_model.data(self.table_model.index(row, 0)))
        
        # Confirmation de la suppression
        reply = QMessageBox.question(
            self,
            "Confirmation",
            "Voulez-vous vraiment supprimer cette mise à jour planifiée ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.No:
            return
        
        # Suppression de la mise à jour
        success = self.update_manager.cancel_scheduled_update(update_id)
        
        if success:
            QMessageBox.information(
                self,
                "Succès",
                "Mise à jour planifiée supprimée",
                QMessageBox.StandardButton.Ok
            )
            
            # Rafraîchissement du tableau
            self.refresh_table()
            
            # Mise à jour du statut
            self.status_label.setText("Mise à jour planifiée supprimée")
            self.status_message.emit("Mise à jour planifiée supprimée")
        else:
            QMessageBox.warning(
                self,
                "Erreur",
                "Erreur lors de la suppression de la mise à jour planifiée",
                QMessageBox.StandardButton.Ok
            )
    
    @pyqtSlot(dict)
    def on_scheduled_update_status(self, update: Dict[str, Any]) -> None:
        """Gestion du changement de statut d'une mise à jour planifiée"""
        # Rafraîchissement du tableau
        self.refresh_table()
        
        # Mise à jour du statut
        if update["status"] == "running":
            self.status_label.setText(f"Mise à jour '{update['name']}' en cours...")
            self.status_message.emit(f"Mise à jour '{update['name']}' en cours...")
        elif update["status"] == "completed":
            self.status_label.setText(f"Mise à jour '{update['name']}' terminée")
            self.status_message.emit(f"Mise à jour '{update['name']}' terminée")
        elif update["status"] == "error":
            self.status_label.setText(f"Erreur lors de la mise à jour '{update['name']}'")
            self.status_message.emit(f"Erreur lors de la mise à jour '{update['name']}'")
