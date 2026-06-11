from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QApplication

from src.ui.editor import Editor


class MenuPrincipal(QWidget):
    """ écran du menu principal"""
    def __init__(self, stacked_widget):
        super().__init__()
        self.editor_window = Editor()
        self.stacked_widget = stacked_widget

        # Layout principal : QGridLayout avec 3 colonnes
        self.main_layout = QGridLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        self.right_widget = QWidget()
        self.right_layout = QVBoxLayout(self.right_widget)
        btn_mode = QPushButton("☀︎ | ☽")
        self.right_layout.addWidget(btn_mode, 0,Qt.AlignmentFlag.AlignTop)
        self.main_layout.addWidget(self.right_widget, 0, 0, 3, 1)

        self.left_widget = QWidget()
        self.left_layout = QVBoxLayout(self.left_widget)
        btn_editor = QPushButton("éditeur")
        btn_editor.clicked.connect(self.ouvrir_editeur)
        self.left_layout.addWidget(btn_editor, 0,Qt.AlignmentFlag.AlignTop)
        self.main_layout.addWidget(self.left_widget, 0, 6, 3, 1)

        self.bottom_widget = QWidget()
        self.bottom_layout = QHBoxLayout(self.bottom_widget)
        self.main_layout.addWidget(self.bottom_widget, 4, 0, 1, 7)


        # Titre du menu
        title = QLabel("Menu Principal")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(title, 0, 1, 2,5)

        #bouton nouvelle partie
        btn_new_game = QPushButton("Nouvelle Partie")
        btn_new_game.clicked.connect(self.selection_theme)
        self.main_layout.addWidget(btn_new_game, 2,1,1,2)

        btn_charge_game = QPushButton("Charger Partie")
        btn_charge_game.clicked.connect(self.selection_theme)
        self.main_layout.addWidget(btn_charge_game, 2,4,1,2)

        btn_option = QPushButton("Option")
        btn_option.clicked.connect(self.selection_theme)
        self.main_layout.addWidget(btn_option, 3,1,1,2)

        # bouton pour quitter
        btn_quit = QPushButton("Quitter")
        btn_quit.clicked.connect(QApplication.quit)
        self.main_layout.addWidget(btn_quit, 3, 4,1,2)

    def selection_theme(self):
        self.stacked_widget.setCurrentIndex(1)

    def ouvrir_editeur(self):
        self.editor_window.show()