from cProfile import label
from pathlib import Path

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QPainter
from PyQt6.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QPushButton, QLabel, QAbstractButton

logo_sf = str(Path(__file__).parent.parent.parent /"data" / "global"/ "assets"/ "images"/"bouton_sf.png" )
logo_fantasy = str(Path(__file__).parent.parent.parent /"data" / "global"/ "assets"/ "images"/"bouton_fantasy.png" )
logo_horreur = str(Path(__file__).parent.parent.parent /"data" / "global"/ "assets"/ "images"/"bouton_horreur.png" )


class PicButton(QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap

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


        btn_horreur = PicButton(QPixmap(logo_horreur))
        btn_horreur.clicked.connect(self.horreur_select)
        self.main_layout.addWidget(btn_horreur,1,0,3,1)

        btn_SF = PicButton(QPixmap(logo_sf))
        btn_SF.clicked.connect(self.sf_select)

        self.main_layout.addWidget(btn_SF,1,1,3,1)

        btn_fantasy = PicButton(QPixmap(logo_fantasy))
        btn_fantasy.clicked.connect(self.fantasy_select)
        self.main_layout.addWidget(btn_fantasy,1,2,3,1)

        self.label = QLabel('Choisissez votre thème')
        self.main_layout.addWidget(self.label,0,1,Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel('Description du thème')
        self.main_layout.addWidget(self.label,4,1,Qt.AlignmentFlag.AlignCenter)

    def horreur_select(self):
        theme = "Horreur Lovecraftienne"
        return theme

    def sf_select(self):
        theme = "Science-Fiction"
        return theme

    def fantasy_select(self):
        theme = "Fantasy"
        return theme
