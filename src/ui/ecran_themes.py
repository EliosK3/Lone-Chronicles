from cProfile import label
from pathlib import Path

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QPainter
from PyQt6.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QPushButton, QLabel, QAbstractButton

"""
todo:
passer theme à selec perso
def ici quelle ui final utilisé si diff?
appliqué changement de style à la validation
"""
logo_sf = str(Path(__file__).parent.parent.parent /"data" / "global"/ "assets"/ "images"/"bouton_sf.png" )
logo_fantasy = str(Path(__file__).parent.parent.parent /"data" / "global"/ "assets"/ "images"/"bouton_fantasy.png" )
logo_horreur = str(Path(__file__).parent.parent.parent /"data" / "global"/ "assets"/ "images"/"bouton_horreur.png" )
logo_pirate = str(Path(__file__).parent.parent.parent /"data" / "global"/ "assets"/ "images"/"bouton_pirate.png" )


from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QSize, Qt
from PyQt6.QtGui import QPixmap, QPainter, QEnterEvent
from PyQt6.QtWidgets import QAbstractButton

class PicButton(QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap
        self.setFixedSize(450,650)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()


class EcranThemes(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.main_layout = QGridLayout(self)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.showMaximized()
        self.main_layout.setSpacing(2)
        self.theme = None

        # Dictionnaire des descriptions
        self.theme_descriptions = {
            "Horreur": "Plongez dans un univers sombre et mystérieux, inspiré des œuvres de H.P. Lovecraft. Affrontez des horreurs indicibles et des énigmes complexes.",
            "Science-Fiction": "Explorez des galaxies lointaines, des technologies avancées et des civilisations extraterrestres.",
            "Fantasy": "Aventurez-vous dans un monde magique peuplé de créatures légendaires, de sorciers et de quêtes épiques.",
            "Pirate": "Naviguez sur les mers dangereuses, à la recherche de trésors et de gloire, mais méfiez-vous des pirates rivaux et des tempêtes."
        }

        btn_horreur = PicButton(QPixmap(logo_horreur))
        btn_horreur.clicked.connect(self.horreur_select)
        self.main_layout.addWidget(btn_horreur,1,0,3,1)

        btn_SF = PicButton(QPixmap(logo_sf))
        btn_SF.clicked.connect(self.sf_select)

        self.main_layout.addWidget(btn_SF,1,1,3,1)

        btn_fantasy = PicButton(QPixmap(logo_fantasy))
        btn_fantasy.clicked.connect(self.fantasy_select)
        self.main_layout.addWidget(btn_fantasy,1,2,3,1)

        btn_pirate = PicButton(QPixmap(logo_pirate))
        btn_pirate.clicked.connect(self.select_pirate)
        self.main_layout.addWidget(btn_pirate,1,3,3,1)

        self.titre = QLabel('Choisissez votre thème')
        self.main_layout.addWidget(self.titre,0,0,1,4,Qt.AlignmentFlag.AlignCenter)

        self.bottom_widget = QWidget(self)
        self.bottom_layout = QHBoxLayout(self.bottom_widget)

        self.valider = QPushButton('validation du thème')
        self.valider.clicked.connect(self.valider_theme)
        self.bottom_layout.addWidget(self.valider)

        self.label = QLabel('Description du thème')
        self.bottom_layout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignCenter)

        self.retour = QPushButton('Retour au menu principal')
        self.retour.clicked.connect(self.retour_menu)
        self.bottom_layout.addWidget(self.retour)
        self.main_layout.addWidget(self.bottom_widget, 4,0,1,4)

    def horreur_select(self):
        self.theme = "Horreur"
        self.label.setText(self.theme_descriptions[self.theme])
        return self.theme

    def sf_select(self):
        self.theme = "Science-Fiction"
        self.label.setText(self.theme_descriptions[self.theme])
        return self.theme

    def fantasy_select(self):
        self.theme = "Fantasy"
        self.label.setText(self.theme_descriptions[self.theme])
        return self.theme

    def select_pirate(self):
        self.theme = "Pirate"
        self.label.setText(self.theme_descriptions[self.theme])
        return self.theme

    def retour_menu(self):
        self.stacked_widget.setCurrentIndex(0)

    def valider_theme(self):
        self.stacked_widget.setCurrentIndex(2)
