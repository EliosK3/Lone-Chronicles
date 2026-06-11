import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel

from src.ui.editor_scenario_tab import GraphEditor


# Assure-toi que le fichier est dans le même dossier ou que le chemin est correct

class Editor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fenêtre avec onglets")
        self.setGeometry(100, 100, 1000, 800)

        # Création du QTabWidget
        tabs = QTabWidget()

        # Création des onglets
        tab1 = QWidget()
        tab1_layout = QVBoxLayout()
        tab1_layout.addWidget(QLabel("Contenu de l'onglet 1"))
        tab1.setLayout(tab1_layout)

        # tab2 contient maintenant l'éditeur de graphe
        tab2 = GraphEditor()  # On utilise directement GraphEditor comme onglet

        # Ajout des onglets au QTabWidget
        tabs.addTab(tab1, "Onglet 1")
        tabs.addTab(tab2, "Éditeur de Scénario")

        # Définir le QTabWidget comme widget central
        self.setCentralWidget(tabs)