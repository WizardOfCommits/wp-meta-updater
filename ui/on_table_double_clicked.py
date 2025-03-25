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
