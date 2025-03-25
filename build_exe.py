#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de compilation pour créer un exécutable standalone
Utilise PyInstaller pour générer un .exe pour Windows
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def build_executable():
    """Compile l'application en un exécutable standalone"""
    print("Démarrage de la compilation de l'exécutable...")
    
    # Nom de l'application
    app_name = "WP_Meta_Updater"
    
    # Dossier de sortie
    output_dir = "dist"
    
    # Nettoyage des dossiers de compilation précédents
    for folder in ["build", "dist", f"{app_name}.spec"]:
        if os.path.exists(folder):
            if os.path.isdir(folder):
                shutil.rmtree(folder)
            else:
                os.remove(folder)
            print(f"Dossier/fichier nettoyé: {folder}")
    
    # Création du dossier de données
    data_folder = os.path.join(output_dir, "data")
    os.makedirs(data_folder, exist_ok=True)
    
    # Création du dossier de logs
    logs_folder = os.path.join(output_dir, "logs")
    os.makedirs(logs_folder, exist_ok=True)
    
    # Options PyInstaller
    pyinstaller_options = [
        "pyinstaller",
        "--name", app_name,
        "--windowed",  # Application GUI sans console
        "--onefile",   # Exécutable unique
        "--clean",     # Nettoie les fichiers temporaires
        "--noconfirm", # Ne pas demander de confirmation pour écraser les fichiers
        "--icon=ui/logo-wp-updater.png",  # Icône de l'application
        "--add-data", f"ui/logo-wp-updater.png;ui",  # Inclure le logo
        "main.py"      # Script principal
    ]
    
    # Exécution de PyInstaller
    print("Exécution de PyInstaller avec les options suivantes:")
    print(" ".join(pyinstaller_options))
    
    try:
        subprocess.run(pyinstaller_options, check=True)
        print("\nCompilation terminée avec succès!")
        
        # Chemin de l'exécutable généré
        exe_path = os.path.join(output_dir, f"{app_name}.exe")
        
        if os.path.exists(exe_path):
            print(f"\nExécutable créé: {exe_path}")
            print("\nVous pouvez maintenant distribuer cet exécutable.")
        else:
            print("\nERREUR: L'exécutable n'a pas été créé correctement.")
            return False
        
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"\nERREUR lors de la compilation: {e}")
        return False

if __name__ == "__main__":
    build_executable()
