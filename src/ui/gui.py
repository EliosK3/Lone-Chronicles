import sys
from pathlib import Path

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from src.ui.choix_perso import EcranSelecPerso
from src.ui.ecran_themes import EcranThemes
from src.ui.menu_principal import MenuPrincipal

from src.ui.style import appliquer_style
"""
todo:
branché autre class quand créer
"""
icon = str(Path(__file__).parent.parent.parent /"data" / "global"/ "assets"/ "images"/"Lone Chronicles.png" )

class FenetrePrincipale(QMainWindow):
    """Fenêtre principale de l'application"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lone Chronicles")
        self.setGeometry(100, 100, 800, 600)
        self.showMaximized()
        self.setWindowIcon(QIcon(icon))

        #appliquer_style("data/global/ui/default.qss")
        # Créer le stacked widget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        #créer les écrans
        self.menu_principal = MenuPrincipal(self.stacked_widget)
        self.ecran_theme = EcranThemes(self.stacked_widget)
        self.ecran_select_perso = EcranSelecPerso(self.stacked_widget)

        #lié les écrans au widget
        self.stacked_widget.addWidget(self.menu_principal)
        self.stacked_widget.addWidget(self.ecran_theme)
        self.stacked_widget.addWidget(self.ecran_select_perso)

        #afficher le widget
        self.stacked_widget.setCurrentIndex(0)

def lancer_interface():
    app = QApplication([])
    app.setStyleSheet("""
    QWidget {
    border: 1px solid red;
    }
    QLayout {
    background-color: rgba(255, 0, 0, 50);
    }""")
    fenetre = FenetrePrincipale()
    fenetre.show()
    app.exec()

if __name__ == '__main__':
    lancer_interface()