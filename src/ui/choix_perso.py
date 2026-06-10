from pathlib import Path

from PyQt6.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QPushButton, QLabel, QAbstractButton

"""
todo:
def logo selon le thème
"""
logo_crea = str(Path(__file__).parent.parent.parent /"data" / "global"/ "assets"/ "images"/"bouton_sf.png" )
logo_choix = str(Path(__file__).parent.parent.parent /"data" / "global"/ "assets"/ "images"/"bouton_fantasy.png" )


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


class EcranSelecPerso(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.main_layout = QGridLayout(self)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.showMaximized()
        self.main_layout.setSpacing(2)
        self.selection = None

        # Dictionnaire des descriptions
        self.selec_descriptions = {
            "création": "Créez et personnaliser votre personnage de A à Z selon les règles et caractéristiques du thème sélectionné.",
            "utilisation": "Incarnez un des personnage enregistrer afin de vivre une aventure sans prise de tête.",
        }

        bouton_crea = PicButton(QPixmap(logo_crea))
        bouton_crea.clicked.connect(self.select_crea)
        self.main_layout.addWidget(bouton_crea,1,1,3,1)

        bouton_choix = PicButton(QPixmap(logo_choix))
        bouton_choix.clicked.connect(self.select_choix)
        self.main_layout.addWidget(bouton_choix,1,3,3,1)

        self.titre = QLabel('Voulez vous jouez un personnage existant où créez le votre?')
        self.main_layout.addWidget(self.titre,0,0,1,5,Qt.AlignmentFlag.AlignCenter)

        self.bottom_widget = QWidget(self)
        self.bottom_layout = QHBoxLayout(self.bottom_widget)

        self.valider = QPushButton('validation du choix')
        self.valider.clicked.connect(self.valider_selection)
        self.bottom_layout.addWidget(self.valider)

        self.label = QLabel('Description')
        self.bottom_layout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignCenter)

        self.retour = QPushButton('Retour à la sélection du thème')
        self.retour.clicked.connect(self.retour_theme)
        self.bottom_layout.addWidget(self.retour)
        self.main_layout.addWidget(self.bottom_widget, 4,0,1,5)


    def select_crea(self):
        self.selection = "création"
        self.label.setText(self.selec_descriptions[self.selection])
        return self.selection

    def select_choix(self):
        self.selection = "utilisation"
        self.label.setText(self.selec_descriptions[self.selection])
        return self.selection

    def retour_theme(self):
        self.stacked_widget.setCurrentIndex(1)

    def valider_selection(self):
        if self.selection == "utilisation":
            self.stacked_widget.setCurrentIndex(3)
        elif self.selection == "création":
            self.stacked_widget.setCurrentIndex(4)
