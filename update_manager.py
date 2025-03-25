#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module de gestion des mises à jour
Gère la planification et l'exécution des mises à jour des métadonnées SEO
"""

import os
import json
import logging
import threading
import time
from typing import Dict, List, Any, Optional, Tuple, Callable
from datetime import datetime, timedelta
from PyQt6.QtCore import QObject, pyqtSignal

class UpdateManager(QObject):
    """Classe pour gérer les mises à jour des métadonnées SEO"""
    
    # Signaux pour la communication avec l'interface utilisateur
    update_started = pyqtSignal()
    update_progress = pyqtSignal(int, int, str)
    update_completed = pyqtSignal(dict)
    update_error = pyqtSignal(str)
    scheduled_update_status = pyqtSignal(dict)
    
    def __init__(self, logger: logging.Logger, wp_connector=None, data_manager=None, wp_direct_connector=None):
        """Initialisation du gestionnaire de mises à jour"""
        super().__init__()
        self.logger = logger
        self.wp_connector = wp_connector
        self.wp_direct_connector = wp_direct_connector
        self.data_manager = data_manager
        
        self.is_updating = False
        self.cancel_update = False
        self.update_thread = None
        
        self.scheduled_updates = []
        self.scheduler_thread = None
        self.scheduler_running = False
        
        # État de la connexion MySQL
        self.mysql_connection_available = False
        
        # Chargement des mises à jour planifiées
        self._load_scheduled_updates()
    
    def set_wp_connector(self, wp_connector) -> None:
        """Définit le connecteur WordPress"""
        self.wp_connector = wp_connector
    
    def set_wp_direct_connector(self, wp_direct_connector) -> None:
        """Définit le connecteur direct WordPress"""
        self.wp_direct_connector = wp_direct_connector
    
    def set_data_manager(self, data_manager) -> None:
        """Définit le gestionnaire de données"""
        self.data_manager = data_manager
    
    def set_mysql_connection_available(self, available: bool) -> None:
        """
        Définit la disponibilité de la connexion MySQL
        
        Args:
            available: Indique si la connexion MySQL est disponible
        """
        self.mysql_connection_available = available
        self.logger.info(f"Connexion MySQL disponible: {available}")
    
    def update_items(self, items: List[Dict[str, Any]], selected_only: bool = False, method: str = "api") -> None:
        """
        Alias pour update_metadata pour compatibilité avec l'interface utilisateur
        
        Args:
            items: Liste des éléments à mettre à jour
            selected_only: Indique si seuls les éléments sélectionnés doivent être mis à jour
            method: Méthode de mise à jour ("api" ou "mysql")
        """
        self.update_metadata(items, selected_only, method)
    
    def update_metadata(self, items: List[Dict[str, Any]], selected_only: bool = False, method: str = "api") -> None:
        """
        Lance la mise à jour des métadonnées SEO
        
        Args:
            items: Liste des éléments à mettre à jour
            selected_only: Indique si seuls les éléments sélectionnés doivent être mis à jour
            method: Méthode de mise à jour ("api" ou "mysql")
        """
        if self.is_updating:
            self.logger.warning("Une mise à jour est déjà en cours")
            self.update_error.emit("Une mise à jour est déjà en cours")
            return
        
        if not items:
            self.logger.warning("Aucun élément à mettre à jour")
            self.update_error.emit("Aucun élément à mettre à jour")
            return
        
        # Vérification de la méthode de mise à jour
        if method == "api":
            # Vérification du connecteur API
            if not self.wp_connector:
                self.logger.error("Connecteur WordPress API non configuré")
                self.update_error.emit("Connecteur WordPress API non configuré")
                return
            
            # Vérification de la connexion à WordPress
            if not self.wp_connector.api_url or not self.wp_connector.auth_token:
                self.logger.error("Connexion WordPress API non configurée")
                self.update_error.emit("Connexion WordPress API non configurée. Veuillez configurer la connexion dans l'onglet Connexion API.")
                return
        elif method == "mysql":
            # Vérification du connecteur MySQL
            if not self.wp_direct_connector:
                self.logger.error("Connecteur WordPress MySQL non configuré")
                self.update_error.emit("Connecteur WordPress MySQL non configuré")
                return
            
            # Vérification de la disponibilité de la connexion MySQL
            if not self.mysql_connection_available:
                self.logger.error("Connexion MySQL non disponible")
                self.update_error.emit("Connexion MySQL non disponible. Veuillez configurer la connexion dans l'onglet Connexion MySQL.")
                return
        else:
            self.logger.error(f"Méthode de mise à jour non reconnue: {method}")
            self.update_error.emit(f"Méthode de mise à jour non reconnue: {method}")
            return
        
        # Lancement de la mise à jour dans un thread séparé
        self.is_updating = True
        self.cancel_update = False
        self.update_started.emit()
        
        self.update_thread = threading.Thread(
            target=self._update_thread,
            args=(items, selected_only, method)
        )
        self.update_thread.daemon = True
        self.update_thread.start()
    
    def _update_thread(self, items: List[Dict[str, Any]], selected_only: bool, method: str) -> None:
        """
        Thread de mise à jour des métadonnées SEO
        
        Args:
            items: Liste des éléments à mettre à jour
            selected_only: Indique si seuls les éléments sélectionnés doivent être mis à jour
            method: Méthode de mise à jour ("api" ou "mysql")
        """
        try:
            self.logger.info(f"Début de la mise à jour de {len(items)} éléments (méthode: {method})")
            
            # Fonction de callback pour la progression
            def progress_callback(current: int, total: int) -> None:
                if self.cancel_update:
                    raise Exception("Mise à jour annulée par l'utilisateur")
                
                item_index = min(current, len(items) - 1)
                item = items[item_index]
                message = f"Mise à jour de {item['type']} {item['id']} - {item['title']}"
                
                self.update_progress.emit(current, total, message)
            
            # Exécution de la mise à jour selon la méthode choisie
            if method == "api":
                stats = self.wp_connector.bulk_update_metadata(items, progress_callback)
            else:  # method == "mysql"
                # Connexion à la base de données
                if not self.wp_direct_connector.connect():
                    raise Exception("Impossible de se connecter à la base de données MySQL")
                
                try:
                    # Mise à jour des métadonnées
                    stats = self.wp_direct_connector.bulk_update_metadata(items, progress_callback)
                finally:
                    # Fermeture de la connexion
                    self.wp_direct_connector.disconnect()
            
            # Journalisation des résultats
            self._log_update_results(stats, selected_only, method)
            
            # Notification de fin de mise à jour
            self.update_completed.emit(stats)
            
            # Mise à jour des éléments modifiés dans le gestionnaire de données
            if self.data_manager and stats["success"] > 0:
                # Marquer les éléments comme non modifiés après une mise à jour réussie
                for item in items:
                    if item["id"] in self.data_manager.modified_items:
                        # Vérifier si l'élément a été mis à jour avec succès
                        success = True
                        for error in stats.get("errors", []):
                            if error["id"] == item["id"]:
                                success = False
                                break
                        
                        if success:
                            # Mettre à jour les valeurs originales
                            self.data_manager.update_original_values(
                                item["id"], 
                                item["seo_title"], 
                                item["seo_description"],
                                item.get("title_h1")
                            )
                
                # Notification du changement de données
                self.data_manager.data_changed.emit()
            
        except Exception as e:
            error_msg = f"Erreur lors de la mise à jour: {str(e)}"
            self.logger.error(error_msg)
            self.update_error.emit(error_msg)
        
        finally:
            self.is_updating = False
    
    def cancel_current_update(self) -> None:
        """Annule la mise à jour en cours"""
        if self.is_updating:
            self.cancel_update = True
            self.logger.info("Annulation de la mise à jour en cours")
    
    def _log_update_results(self, stats: Dict[str, Any], selected_only: bool, method: str = "api") -> None:
        """
        Journalise les résultats de la mise à jour
        
        Args:
            stats: Statistiques de mise à jour
            selected_only: Indique si seuls les éléments sélectionnés ont été mis à jour
            method: Méthode de mise à jour utilisée
        """
        # Création du répertoire de logs si nécessaire
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
        os.makedirs(log_dir, exist_ok=True)
        
        # Nom du fichier de log
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"update_{timestamp}.json")
        
        # Données du log
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "type": "selected" if selected_only else "all_modified",
            "method": method,
            "stats": stats,
            "errors": stats.get("errors", [])
        }
        
        # Écriture du log
        with open(log_file, "w", encoding="utf-8-sig") as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Résultats de mise à jour enregistrés dans {log_file}")
    
    def schedule_update(self, items: List[Dict[str, Any]], schedule_time: datetime, name: str = "", recurring: bool = False, interval_days: int = 0, method: str = "api") -> bool:
        """
        Planifie une mise à jour des métadonnées SEO
        
        Args:
            items: Liste des éléments à mettre à jour
            schedule_time: Date et heure de la mise à jour
            name: Nom de la mise à jour planifiée
            recurring: Indique si la mise à jour est récurrente
            interval_days: Intervalle en jours pour les mises à jour récurrentes
            method: Méthode de mise à jour ("api" ou "mysql")
            
        Returns:
            Succès de la planification
        """
        if not items:
            self.logger.warning("Aucun élément à mettre à jour")
            return False
        
        if schedule_time < datetime.now():
            self.logger.warning("La date de planification est dans le passé")
            return False
        
        # Création de la mise à jour planifiée
        scheduled_update = {
            "id": int(time.time()),
            "name": name or f"Mise à jour planifiée du {schedule_time.strftime('%d/%m/%Y %H:%M')}",
            "schedule_time": schedule_time.isoformat(),
            "created_at": datetime.now().isoformat(),
            "recurring": recurring,
            "interval_days": interval_days if recurring else 0,
            "items": [{"id": item["id"], "type": item["type"]} for item in items],
            "method": method,
            "status": "pending"
        }
        
        # Ajout à la liste des mises à jour planifiées
        self.scheduled_updates.append(scheduled_update)
        
        # Sauvegarde des mises à jour planifiées
        self._save_scheduled_updates()
        
        # Démarrage du planificateur si nécessaire
        if not self.scheduler_running:
            self._start_scheduler()
        
        self.logger.info(f"Mise à jour planifiée pour le {schedule_time.strftime('%d/%m/%Y %H:%M')} (méthode: {method})")
        return True
    
    def cancel_scheduled_update(self, update_id: int) -> bool:
        """
        Annule une mise à jour planifiée
        
        Args:
            update_id: ID de la mise à jour planifiée
            
        Returns:
            Succès de l'annulation
        """
        for i, update in enumerate(self.scheduled_updates):
            if update["id"] == update_id:
                self.scheduled_updates.pop(i)
                self._save_scheduled_updates()
                self.logger.info(f"Mise à jour planifiée {update_id} annulée")
                return True
        
        self.logger.warning(f"Mise à jour planifiée {update_id} non trouvée")
        return False
    
    def get_scheduled_updates(self) -> List[Dict[str, Any]]:
        """
        Récupère la liste des mises à jour planifiées
        
        Returns:
            Liste des mises à jour planifiées
        """
        return self.scheduled_updates
    
    def _start_scheduler(self) -> None:
        """Démarre le planificateur de mises à jour"""
        if self.scheduler_running:
            return
        
        self.scheduler_running = True
        self.scheduler_thread = threading.Thread(target=self._scheduler_thread)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
        
        self.logger.info("Planificateur de mises à jour démarré")
    
    def _stop_scheduler(self) -> None:
        """Arrête le planificateur de mises à jour"""
        self.scheduler_running = False
        self.logger.info("Planificateur de mises à jour arrêté")
    
    def _scheduler_thread(self) -> None:
        """Thread du planificateur de mises à jour"""
        while self.scheduler_running:
            try:
                now = datetime.now()
                
                # Vérification des mises à jour planifiées
                for update in self.scheduled_updates:
                    schedule_time = datetime.fromisoformat(update["schedule_time"])
                    
                    # Si la mise à jour est prévue dans les 60 prochaines secondes
                    if now <= schedule_time < now + timedelta(seconds=60) and update["status"] == "pending":
                        # Mise à jour du statut
                        update["status"] = "running"
                        self._save_scheduled_updates()
                        self.scheduled_update_status.emit(update)
                        
                        # Exécution de la mise à jour
                        self._execute_scheduled_update(update)
                        
                        # Si la mise à jour est récurrente, planifier la prochaine
                        if update["recurring"] and update["interval_days"] > 0:
                            next_time = schedule_time + timedelta(days=update["interval_days"])
                            update["schedule_time"] = next_time.isoformat()
                            update["status"] = "pending"
                        else:
                            # Suppression de la mise à jour non récurrente
                            self.scheduled_updates.remove(update)
                        
                        self._save_scheduled_updates()
                
                # Attente avant la prochaine vérification
                time.sleep(30)
                
            except Exception as e:
                self.logger.error(f"Erreur dans le planificateur: {str(e)}")
                time.sleep(60)  # Attente plus longue en cas d'erreur
    
    def _execute_scheduled_update(self, update: Dict[str, Any]) -> None:
        """
        Exécute une mise à jour planifiée
        
        Args:
            update: Mise à jour planifiée à exécuter
        """
        try:
            self.logger.info(f"Exécution de la mise à jour planifiée: {update['name']} (méthode: {update.get('method', 'api')})")
            
            # Récupération des éléments à mettre à jour
            items_to_update = []
            
            for item_ref in update["items"]:
                item_id = item_ref["id"]
                item_type = item_ref["type"]
                
                # Recherche de l'élément dans les données
                if self.data_manager and item_type in self.data_manager.data:
                    for item in self.data_manager.data[item_type]:
                        if item["id"] == item_id:
                            items_to_update.append(item)
                            break
            
            if not items_to_update:
                self.logger.warning(f"Aucun élément trouvé pour la mise à jour planifiée: {update['name']}")
                return
            
            # Détermination de la méthode de mise à jour
            method = update.get("method", "api")
            
            # Exécution de la mise à jour selon la méthode choisie
            if method == "api":
                if not self.wp_connector:
                    self.logger.error(f"Connecteur WordPress API non configuré pour la mise à jour planifiée: {update['name']}")
                    update["status"] = "error"
                    update["last_error"] = "Connecteur WordPress API non configuré"
                    return
                
                stats = self.wp_connector.bulk_update_metadata(items_to_update)
            else:  # method == "mysql"
                if not self.wp_direct_connector:
                    self.logger.error(f"Connecteur WordPress MySQL non configuré pour la mise à jour planifiée: {update['name']}")
                    update["status"] = "error"
                    update["last_error"] = "Connecteur WordPress MySQL non configuré"
                    return
                
                # Connexion à la base de données
                if not self.wp_direct_connector.connect():
                    self.logger.error(f"Impossible de se connecter à la base de données MySQL pour la mise à jour planifiée: {update['name']}")
                    update["status"] = "error"
                    update["last_error"] = "Impossible de se connecter à la base de données MySQL"
                    return
                
                try:
                    # Mise à jour des métadonnées
                    stats = self.wp_direct_connector.bulk_update_metadata(items_to_update)
                finally:
                    # Fermeture de la connexion
                    self.wp_direct_connector.disconnect()
            
            # Journalisation des résultats
            self._log_update_results(stats, False, method)
            
            # Mise à jour du statut
            update["status"] = "completed"
            update["last_run"] = datetime.now().isoformat()
            update["last_result"] = {
                "success": stats["success"],
                "failed": stats["failed"]
            }
            
            self.logger.info(f"Mise à jour planifiée terminée: {update['name']}")
            
        except Exception as e:
            error_msg = f"Erreur lors de l'exécution de la mise à jour planifiée: {str(e)}"
            self.logger.error(error_msg)
            
            update["status"] = "error"
            update["last_error"] = str(e)
    
    def _save_scheduled_updates(self) -> None:
        """Sauvegarde les mises à jour planifiées"""
        try:
            # Création du répertoire de données si nécessaire
            data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
            os.makedirs(data_dir, exist_ok=True)
            
            # Chemin du fichier de sauvegarde
            save_file = os.path.join(data_dir, "scheduled_updates.json")
            
            # Sauvegarde des données
            with open(save_file, "w", encoding="utf-8-sig") as f:
                json.dump(self.scheduled_updates, f, indent=2, ensure_ascii=False)
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la sauvegarde des mises à jour planifiées: {str(e)}")
    
    def _load_scheduled_updates(self) -> None:
        """Charge les mises à jour planifiées"""
        try:
            # Chemin du fichier de sauvegarde
            data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
            save_file = os.path.join(data_dir, "scheduled_updates.json")
            
            # Vérification de l'existence du fichier
            if not os.path.exists(save_file):
                self.scheduled_updates = []
                return
            
            # Chargement des données
            with open(save_file, "r", encoding="utf-8-sig") as f:
                self.scheduled_updates = json.load(f)
            
            # Mise à jour des statuts
            now = datetime.now()
            
            for update in self.scheduled_updates:
                schedule_time = datetime.fromisoformat(update["schedule_time"])
                
                # Si la mise à jour est dépassée et non récurrente
                if schedule_time < now and not update["recurring"]:
                    update["status"] = "missed"
                
                # Si la mise à jour est en cours d'exécution (probablement interrompue)
                if update["status"] == "running":
                    update["status"] = "pending"
                
                # Ajout de la méthode de mise à jour si elle n'existe pas
                if "method" not in update:
                    update["method"] = "api"
            
            self.logger.info(f"Chargement de {len(self.scheduled_updates)} mises à jour planifiées")
            
        except Exception as e:
            self.logger.error(f"Erreur lors du chargement des mises à jour planifiées: {str(e)}")
            self.scheduled_updates = []
