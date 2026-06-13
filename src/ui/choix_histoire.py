from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QPushButton, QLabel

from cProfile import label
from pathlib import Path

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QFont
from PyQt6.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QPushButton, QLabel, QAbstractButton

"""
todo:
passer theme à selec perso
def ici quelle ui final utilisé si diff?
appliqué changement de style à la validation
"""
logo_sf = str(Path(__file__).parent.parent.parent / "data" / "global" / "assets" / "images" / "bouton_sf.png")
logo_fantasy = str(Path(__file__).parent.parent.parent / "data" / "global" / "assets" / "images" / "bouton_fantasy.png")
logo_horreur = str(Path(__file__).parent.parent.parent / "data" / "global" / "assets" / "images" / "bouton_horreur.png")
logo_pirate = str(Path(__file__).parent.parent.parent / "data" / "global" / "assets" / "images" / "bouton_pirate.png")

from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QSize, Qt
from PyQt6.QtGui import QPixmap, QPainter, QEnterEvent
from PyQt6.QtWidgets import QAbstractButton


class PicButton(QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap
        self.setFixedSize(450, 650)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()


class EcranHistoire(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.main_layout = QGridLayout(self)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.showMaximized()
        self.main_layout.setSpacing(2)

        self.current_theme = None
        self.scenario_buttons = {}


        # Dictionnaire des descriptions
        self.histoire_descriptions = {
            "Horreur": "Plongez dans un univers sombre et mystérieux, inspiré des œuvres de H.P. Lovecraft. Affrontez des horreurs indicibles et des énigmes complexes.",
            "Science-Fiction": "Explorez des galaxies lointaines, des technologies avancées et des civilisations extraterrestres.",
            "Fantasy": "Aventurez-vous dans un monde magique peuplé de créatures légendaires, de sorciers et de quêtes épiques.",
            "Pirate": "Naviguez sur les mers dangereuses, à la recherche de trésors et de gloire, mais méfiez-vous des pirates rivaux et des tempêtes."
        }

        self.titre = QLabel('Choisissez votre Histoire')
        self.main_layout.addWidget(self.titre, 0, 0, 1, 4, Qt.AlignmentFlag.AlignCenter)

        self.grille_widget = QWidget()
        self.grille_layout = QGridLayout(self.grille_widget)
        self.grille_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.grille_widget, 1, 0, 1, 4)

        self.bottom_widget = QWidget(self)
        self.bottom_layout = QHBoxLayout(self.bottom_widget)

        self.valider = QPushButton('validation de l\'histoire')
        self.valider.clicked.connect(self.valider_histoire)
        self.bottom_layout.addWidget(self.valider)

        self.label = QLabel('Description de l\'histoire')
        self.bottom_layout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignCenter)

        self.retour = QPushButton('Retour au menu principal')
        self.retour.clicked.connect(self.retour_themes)
        self.bottom_layout.addWidget(self.retour)
        self.main_layout.addWidget(self.bottom_widget, 4, 0, 1, 4)


    def retour_themes(self):
        self.stacked_widget.setCurrentIndex(1)

    def load_scenarios(self ,theme):
        """
        Charge les scénarios pour un thème donné et met à jour la grille de boutons.
        :param theme: Nom du thème (ex: "Fantasy", "Science-Fiction").
        """
        self.current_theme = theme
        self._clear_grille()  # Efface les anciens boutons

        # Chemin vers les scénarios du thème
        scenarios_path = Path(__file__).parent.parent.parent.parent / "data" / "themes" / theme / "scenarios"

        if not scenarios_path.exists():
            self.grille_layout.addWidget(
                QLabel(f"Aucun scénario trouvé pour le thème : {theme}"),
                1, 0, 1, -1,
                alignment=Qt.AlignmentFlag.AlignCenter
            )
            self.grille_layout.itemAt(1).widget().setStyleSheet("color: #ff5555; font-size: 16px;")
            return

        # Lister les dossiers (chaque dossier = un scénario)
        scenario_folders = [
            name for name in scenarios_path.iterdir()
            if name.is_dir()
        ]

        if not scenario_folders:
            self.grille_layout.addWidget(
                QLabel(f"Aucun scénario trouvé pour le thème : {theme}"),
                1, 0, 1, -1,
                alignment=Qt.AlignmentFlag.AlignCenter
            )
            self.grille_layout.itemAt(1).widget().setStyleSheet("color: #ff5555; font-size: 16px;")
            return

        # Créer un bouton pour chaque scénario
        row, col = 1, 0
        for scenario in scenario_folders:
            button = QPushButton(scenario.name.replace("_", " ").title())
            button.setFixedSize(300, 150)
            button.setFont(QFont("Arial", 14))
            button.setStyleSheet("""
                            QPushButton {
                                background-color: #1e1e1e;
                                color: #ffffff;
                                border: 2px solid #444444;
                                border-radius: 15px;
                                padding: 10px;
                            }
                            QPushButton:hover {
                                background-color: #2a2a2a;
                                border: 2px solid #666666;
                            }
                            QPushButton:pressed {
                                background-color: #0e0e0e;
                                border: 2px solid #888888;
                            }
                        """)
            button.clicked.connect(
                lambda _, s=scenario.name: self._on_scenario_selected(s)
            )
            self.grille_layout.addWidget(button, row, col)
            self.scenario_buttons[scenario.name] = button

            # Mise en page : 3 boutons par ligne
            col += 1
            if col >= 3:
                col = 0
                row += 1

    def _clear_grille(self):
        """Efface tous les widgets de la grille sauf le titre."""
        while self.grille_layout.count() > 1:
            child = self.grille_layout.takeAt(1)
            if child.widget():
                child.widget().deleteLater()


    def valider_histoire(self):
        pass