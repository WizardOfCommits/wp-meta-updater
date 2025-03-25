#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
WordPress Meta Updater
Application de mise à jour des métadonnées SEO WordPress
Point d'entrée principal de l'application
"""

import sys
import os
import logging
from PyQt6.QtWidgets import QApplication

# Import du module principal
from main import main

if __name__ == "__main__":
    # Exécution de l'application
    main()
