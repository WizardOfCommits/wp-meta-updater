#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module de gestion des données
Gère l'importation et l'exportation des données, ainsi que la validation des métadonnées SEO
"""

import os
import csv
import json
import logging
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from PyQt6.QtCore import QObject, pyqtSignal, QCoreApplication

class DataManager(QObject):
    """Classe pour gérer les données de l'application"""
    
    # Signaux pour la communication avec l'interface utilisateur
    data_changed = pyqtSignal()
    import_progress = pyqtSignal(int, int, str)
    export_progress = pyqtSignal(int, int, str)
    
    def __init__(self, logger: logging.Logger):
        """Initialisation du gestionnaire de données"""
        super().__init__()
        self.logger = logger
        self.data = {}  # Données actuelles
        self.history = []  # Historique des modifications
        self.modified_items = set()  # Éléments modifiés
        self.selected_items = set()  # Éléments sélectionnés
        self.filtered_data = []  # Données filtrées pour l'affichage
        self.filter_criteria = {}  # Critères de filtrage
        self.session_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "session_data.json")
    
    def save_session_data(self) -> bool:
        """
        Sauvegarde les données de la session dans un fichier JSON
        
        Returns:
            Succès de la sauvegarde
        """
        if not self.data:
            self.logger.info("Aucune donnée à sauvegarder")
            return False
            
        try:
            # Création du répertoire data s'il n'existe pas
            os.makedirs(os.path.dirname(self.session_file), exist_ok=True)
            
            # Préparation des métadonnées
            metadata = {
                "timestamp": datetime.now().isoformat(),
                "version": "1.0",
                "total_items": sum(len(items) for items in self.data.values()),
                "content_types": list(self.data.keys())
            }
            
            # Sauvegarde dans un fichier JSON
            session_data = {
                "metadata": metadata,
                "modified_items": list(self.modified_items),
                "selected_items": list(self.selected_items),
                "filter_criteria": self.filter_criteria,
                "data": self.data
            }
            
            with open(self.session_file, "w", encoding="utf-8-sig") as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"Session sauvegardée: {metadata['total_items']} éléments dans {self.session_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la sauvegarde de la session: {str(e)}")
            return False
    
    def load_session_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Charge les données de la session depuis un fichier JSON
        
        Returns:
            Dictionnaire des données chargées ou None en cas d'erreur
        """
        if not os.path.exists(self.session_file):
            self.logger.info(f"Aucun fichier de session trouvé: {self.session_file}")
            return None
            
        try:
            with open(self.session_file, "r", encoding="utf-8-sig") as f:
                session_data = json.load(f)
            
            # Vérification de la structure des données
            if "data" not in session_data:
                self.logger.error("Structure de session invalide: clé 'data' manquante")
                return None
            
            # Restauration des éléments modifiés et sélectionnés
            if "modified_items" in session_data:
                self.modified_items = set(int(item_id) for item_id in session_data["modified_items"])
            
            if "selected_items" in session_data:
                self.selected_items = set(int(item_id) for item_id in session_data["selected_items"])
            
            # Restauration des critères de filtrage
            if "filter_criteria" in session_data:
                self.filter_criteria = session_data["filter_criteria"]
            
            # Restauration des données
            data = session_data["data"]
            
            self.logger.info(f"Session chargée: {sum(len(items) for items in data.values())} éléments depuis {self.session_file}")
            return data
            
        except Exception as e:
            self.logger.error(f"Erreur lors du chargement de la session: {str(e)}")
            return None
    
    def restore_session(self) -> bool:
        """
        Restaure la session précédente
        
        Returns:
            Succès de la restauration
        """
        try:
            # Chargement des données de session
            data = self.load_session_data()
            
            if not data:
                return False
            
            # Mise à jour des données
            self.data = data
            
            # Mise à jour des données filtrées
            self._apply_filters()
            
            # Notification de changement de données
            self.data_changed.emit()
            
            self.logger.info("Session restaurée avec succès")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la restauration de la session: {str(e)}")
            return False
    
    def select_item(self, item_id: int, selected: bool = True) -> None:
        """
        Sélectionne ou désélectionne un élément
        
        Args:
            item_id: ID de l'élément
            selected: True pour sélectionner, False pour désélectionner
        """
        if selected:
            self.selected_items.add(item_id)
        else:
            self.selected_items.discard(item_id)
    
    def update_original_values(self, item_id: int, seo_title: str = None, seo_description: str = None, title_h1: str = None) -> bool:
        """
        Met à jour les valeurs originales des métadonnées d'un élément après une mise à jour réussie
        
        Args:
            item_id: ID de l'élément
            seo_title: Titre SEO (None = pas de modification)
            seo_description: Description SEO (None = pas de modification)
            title_h1: Titre H1 (None = pas de modification)
            
        Returns:
            Succès de la mise à jour
        """
        # Recherche de l'élément dans toutes les données
        for content_type, items in self.data.items():
            for i, item in enumerate(items):
                if item["id"] == item_id:
                    # Mise à jour des valeurs originales
                    if seo_title is not None:
                        self.data[content_type][i]["original_seo_title"] = seo_title
                    
                    if seo_description is not None:
                        self.data[content_type][i]["original_seo_description"] = seo_description
                    
                    if title_h1 is not None:
                        self.data[content_type][i]["original_title_h1"] = title_h1
                    
                    # Retirer des éléments modifiés si les valeurs sont maintenant identiques aux originales
                    if (self.data[content_type][i]["seo_title"] == self.data[content_type][i]["original_seo_title"] and
                        self.data[content_type][i]["seo_description"] == self.data[content_type][i]["original_seo_description"] and
                        self.data[content_type][i]["title_h1"] == self.data[content_type][i]["original_title_h1"]):
                        self.modified_items.discard(item_id)
                    
                    return True
        
        return False
    
    def update_item(self, item_id: int, seo_title: str = None, seo_description: str = None, title_h1: str = None) -> bool:
        """
        Met à jour les métadonnées d'un élément
        
        Args:
            item_id: ID de l'élément
            seo_title: Nouveau titre SEO (None = pas de modification)
            seo_description: Nouvelle description SEO (None = pas de modification)
            title_h1: Nouveau titre H1 (None = pas de modification)
            
        Returns:
            Succès de la mise à jour
        """
        # Recherche de l'élément dans toutes les données
        for content_type, items in self.data.items():
            for i, item in enumerate(items):
                if item["id"] == item_id:
                    # Mise à jour du titre SEO
                    if seo_title is not None:
                        self.data[content_type][i]["seo_title"] = seo_title
                    
                    # Mise à jour de la description SEO
                    if seo_description is not None:
                        self.data[content_type][i]["seo_description"] = seo_description
                    
                    # Mise à jour du titre H1
                    if title_h1 is not None:
                        self.data[content_type][i]["title_h1"] = title_h1
                    
                    # Vérification si l'élément est modifié
                    if (self.data[content_type][i]["seo_title"] != self.data[content_type][i]["original_seo_title"] or
                        self.data[content_type][i]["seo_description"] != self.data[content_type][i]["original_seo_description"] or
                        self.data[content_type][i]["title_h1"] != self.data[content_type][i]["original_title_h1"]):
                        # Marquer comme modifié
                        self.modified_items.add(item_id)
                    else:
                        # Retirer des éléments modifiés si identique à l'original
                        self.modified_items.discard(item_id)
                    
                    # Mise à jour des données filtrées
                    self._apply_filters()
                    
                    # Notification de changement de données
                    self.data_changed.emit()
                    
                    return True
        
        return False
    
    def _apply_filters(self) -> None:
        """Applique les filtres aux données"""
        self.filtered_data = []
        
        for content_type, items in self.data.items():
            # Filtre par type de contenu
            if "content_type" in self.filter_criteria and self.filter_criteria["content_type"] != "all":
                if content_type != self.filter_criteria["content_type"]:
                    continue
            
            for item in items:
                # Filtre par texte de recherche
                if "search_text" in self.filter_criteria and self.filter_criteria["search_text"]:
                    search_text = self.filter_criteria["search_text"].lower()
                    
                    # Recherche dans le titre, l'URL, le titre SEO, la description SEO et le titre H1
                    if (search_text not in item["title"].lower() and
                        search_text not in item["url"].lower() and
                        search_text not in item["seo_title"].lower() and
                        search_text not in item["seo_description"].lower() and
                        search_text not in item.get("title_h1", "").lower()):
                        continue
                
                # Filtre par état de modification
                if "modified_only" in self.filter_criteria and self.filter_criteria["modified_only"]:
                    if item["id"] not in self.modified_items:
                        continue
                
                # Filtre par problèmes SEO
                if "seo_issues" in self.filter_criteria and self.filter_criteria["seo_issues"]:
                    has_issues = False
                    
                    # Vérification de la longueur du titre SEO
                    if len(item["seo_title"]) < 30 or len(item["seo_title"]) > 60:
                        has_issues = True
                    
                    # Vérification de la longueur de la description SEO
                    if len(item["seo_description"]) < 120 or len(item["seo_description"]) > 160:
                        has_issues = True
                    
                    if not has_issues:
                        continue
                
                # Ajout de l'élément aux données filtrées
                self.filtered_data.append(item)
    
    def import_from_wp(self, content_data: Dict[str, List[Dict[str, Any]]]) -> None:
        """
        Importe les données depuis WordPress
        
        Args:
            content_data: Dictionnaire avec les types de contenu comme clés et les listes d'éléments comme valeurs
        """
        self.logger.info("Importation des données depuis WordPress")
        
        try:
            # Vérification si des données de session existent
            if os.path.exists(self.session_file):
                # Demander à l'utilisateur s'il souhaite fusionner les données
                from PyQt6.QtWidgets import QMessageBox
                reply = QMessageBox.question(
                    None,
                    "Données de session existantes",
                    "Des données d'une session précédente ont été trouvées. Souhaitez-vous les conserver et fusionner avec les nouvelles données?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.Yes
                )
                
                if reply == QMessageBox.StandardButton.Yes:
                    # Charger les données de session existantes
                    existing_data = self.load_session_data()
                    if existing_data:
                        # Fusionner les données existantes avec les nouvelles
                        self.logger.info("Fusion des données existantes avec les nouvelles données")
                        
                        # Traitement par lots pour éviter de surcharger la mémoire
                        for content_type, items in existing_data.items():
                            if content_type not in content_data:
                                content_data[content_type] = []
                            
                            # Création d'un ensemble d'IDs existants pour une recherche plus rapide
                            existing_ids = set()
                            if content_type in content_data:
                                existing_ids = {item.get("id") for item in content_data[content_type]}
                            
                            # Traitement par lots de 100 éléments
                            batch_size = 100
                            for i in range(0, len(items), batch_size):
                                batch = items[i:i+batch_size]
                                
                                # Ajout des éléments non dupliqués
                                for item in batch:
                                    if item.get("id") not in existing_ids:
                                        content_data[content_type].append(item)
                                        existing_ids.add(item.get("id"))
                                
                                # Traitement des événements pour éviter le gel de l'interface
                                QCoreApplication.processEvents()
            
            # Réinitialisation des données
            self.data = {}
            self.filtered_data = []
            self.modified_items = set()
            
            # Traitement des données importées
            total_items = sum(len(items) for items in content_data.values())
            processed = 0
            
            for content_type, items in content_data.items():
                self.data[content_type] = []
                
                # Traitement par lots pour éviter de surcharger la mémoire
                batch_size = 100
                for i in range(0, len(items), batch_size):
                    batch = items[i:i+batch_size]
                    
                    for item in batch:
                        try:
                            processed += 1
                            self.import_progress.emit(processed, total_items, f"Traitement de {content_type} {item.get('id', 'inconnu')}")
                            
                            # Extraction des métadonnées SEO simplifiée
                            title_value = item.get("title", {}).get("rendered", "") if isinstance(item.get("title"), dict) else item.get("title", "")
                            metadata = {
                                "id": item.get("id", 0),
                                "type": content_type,
                                "title": title_value,
                                "url": item.get("link", ""),
                                "date_modified": item.get("modified", ""),
                                "seo_title": title_value,
                                "seo_description": "",
                                "original_seo_title": title_value,
                                "original_seo_description": "",
                                "title_h1": title_value,
                                "original_title_h1": title_value
                            }
                            
                            # Ajout des métadonnées à la liste
                            self.data[content_type].append(metadata)
                        except Exception as item_error:
                            # Gestion des erreurs par élément pour éviter d'interrompre tout le processus
                            self.logger.warning(f"Erreur lors du traitement de l'élément {item.get('id', 'inconnu')}: {str(item_error)}")
                    
                    # Traitement des événements pour éviter le gel de l'interface
                    QCoreApplication.processEvents()
            
            # Mise à jour des données filtrées
            self._apply_filters()
            
            # Notification de changement de données
            self.data_changed.emit()
            self.logger.info(f"Importation terminée: {total_items} éléments importés")
            
            # Sauvegarde automatique de la session après importation
            self.save_session_data()
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'importation depuis WordPress: {str(e)}")
            # Notification de changement de données même en cas d'erreur
            self.data_changed.emit()
    
    def import_from_csv(self, filepath: str, separator: str = None) -> Tuple[bool, str, int]:
        """
        Importe les données depuis un fichier CSV
        
        Args:
            filepath: Chemin du fichier CSV
            separator: Séparateur CSV (None = auto-détection)
            
        Returns:
            Tuple (succès, message, nombre d'éléments importés)
        """
        try:
            # Détection du séparateur
            if separator is None:
                # Essai de détection automatique du séparateur
                with open(filepath, 'r', encoding='utf-8-sig') as f:
                    first_line = f.readline().strip()
                
                if ';' in first_line:
                    separator = ';'
                elif ',' in first_line:
                    separator = ','
                elif '\t' in first_line:
                    separator = '\t'
                else:
                    separator = ','
            
            # Lecture du fichier CSV
            df = pd.read_csv(filepath, encoding="utf-8-sig", sep=separator)
            
            # Vérification des colonnes requises
            required_columns = ["id", "type"]
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                error_msg = f"Colonnes requises manquantes: {', '.join(missing_columns)}"
                self.logger.error(error_msg)
                return False, error_msg, 0
            
            # Conversion en liste de dictionnaires
            csv_data = df.to_dict(orient="records")
            
            # Mise à jour des données
            updated_count = 0
            
            for csv_item in csv_data:
                try:
                    # Conversion de l'ID en entier
                    item_id = int(csv_item["id"])
                    item_type = csv_item["type"]
                    
                    # Vérification si le type de contenu existe
                    if item_type not in self.data:
                        self.data[item_type] = []
                    
                    # Recherche de l'élément correspondant
                    found = False
                    
                    for i, item in enumerate(self.data[item_type]):
                        if item["id"] == item_id:
                            # Mise à jour des métadonnées SEO
                            if "seo_title" in csv_item:
                                self.data[item_type][i]["seo_title"] = csv_item["seo_title"]
                            
                            if "seo_description" in csv_item:
                                self.data[item_type][i]["seo_description"] = csv_item["seo_description"]
                            
                            # Mise à jour du titre H1
                            if "title_h1" in csv_item:
                                self.data[item_type][i]["title_h1"] = csv_item["title_h1"]
                            
                            # Marquer comme modifié si différent de l'original
                            if (self.data[item_type][i]["seo_title"] != self.data[item_type][i]["original_seo_title"] or
                                self.data[item_type][i]["seo_description"] != self.data[item_type][i]["original_seo_description"] or
                                self.data[item_type][i]["title_h1"] != self.data[item_type][i]["original_title_h1"]):
                                self.modified_items.add(item_id)
                            
                            updated_count += 1
                            found = True
                            break
                    
                    if not found:
                        # Si l'élément n'existe pas et que nous avons suffisamment d'informations, créer un nouvel élément
                        if "title" in csv_item and "url" in csv_item:
                            new_item = {
                                "id": item_id,
                                "type": item_type,
                                "title": csv_item["title"],
                                "url": csv_item["url"],
                                "date_modified": csv_item.get("date_modified", ""),
                                "seo_title": csv_item.get("seo_title", ""),
                                "seo_description": csv_item.get("seo_description", ""),
                                "title_h1": csv_item.get("title_h1", csv_item["title"]),
                                "original_seo_title": csv_item.get("original_seo_title", ""),
                                "original_seo_description": csv_item.get("original_seo_description", ""),
                                "original_title_h1": csv_item.get("original_title_h1", csv_item["title"])
                            }
                            
                            # Ajout à la liste
                            self.data[item_type].append(new_item)
                            updated_count += 1
                except Exception as item_error:
                    # Gestion des erreurs par élément pour éviter d'interrompre tout le processus
                    self.logger.warning(f"Erreur lors du traitement de l'élément {csv_item.get('id', 'inconnu')}: {str(item_error)}")
            
            # Mise à jour des données filtrées
            self._apply_filters()
            
            # Notification de changement de données
            self.data_changed.emit()
            
            # Sauvegarde automatique de la session après importation
            self.save_session_data()
            
            self.logger.info(f"Importation CSV réussie: {updated_count} éléments mis à jour depuis {filepath}")
            return True, f"Importation réussie: {updated_count} éléments mis à jour", updated_count
            
        except Exception as e:
            error_msg = f"Erreur lors de l'importation CSV: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg, 0
    
    def get_items_for_update(self, selected_only: bool = False) -> List[Dict[str, Any]]:
        """
        Récupère les éléments à mettre à jour
        
        Args:
            selected_only: Récupérer uniquement les éléments sélectionnés
            
        Returns:
            Liste des éléments à mettre à jour
        """
        items_to_update = []
        
        # Détermination des IDs à mettre à jour
        if selected_only:
            # Uniquement les éléments sélectionnés
            update_ids = self.selected_items
        else:
            # Tous les éléments modifiés
            update_ids = self.modified_items
        
        # Récupération des éléments correspondants
        for content_type, items in self.data.items():
            for item in items:
                if item["id"] in update_ids:
                    items_to_update.append(item)
        
        return items_to_update
    
    def export_to_csv(self, filepath: str, export_all: bool = True) -> bool:
        """
        Exporte les données vers un fichier CSV
        
        Args:
            filepath: Chemin du fichier CSV
            export_all: Exporter toutes les données ou seulement les éléments sélectionnés
            
        Returns:
            Succès de l'exportation
        """
        try:
            # Détermination des données à exporter
            export_data = []
            
            if export_all:
                # Exportation de toutes les données
                for content_type, items in self.data.items():
                    export_data.extend(items)
            else:
                # Exportation des éléments sélectionnés uniquement
                selected_ids = self.selected_items
                for item in self.filtered_data:
                    if item["id"] in selected_ids:
                        export_data.append(item)
            
            if not export_data:
                self.logger.warning("Aucune donnée à exporter")
                return False
            
            # Création du DataFrame pandas
            df = pd.DataFrame(export_data)
            
            # Réorganisation des colonnes
            columns = [
                "id", "type", "title", "url", "date_modified",
                "original_seo_title", "original_seo_description", "original_title_h1",
                "seo_title", "seo_description", "title_h1"
            ]
            
            # Filtrer les colonnes qui existent réellement dans le DataFrame
            existing_columns = [col for col in columns if col in df.columns]
            
            # Exportation vers CSV avec BOM UTF-8
            df.to_csv(
                filepath,
                columns=existing_columns,
                index=False,
                encoding="utf-8-sig",
                quoting=csv.QUOTE_ALL
            )
            
            self.logger.info(f"Exportation CSV réussie: {len(export_data)} éléments exportés vers {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'exportation CSV: {str(e)}")
            return False
