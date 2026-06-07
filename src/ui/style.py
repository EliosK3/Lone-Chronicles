from pathlib import Path
from timeit import default_timer

from PyQt6.QtCore import QFile
from PyQt6.QtWidgets import QApplication

# Racine du projet (calculée depuis ce fichier)
RACINE_PROJET = Path(__file__).parent.parent.parent

# Style actuel appliqué (pour référence)
STYLE_ACTUEL = None

def appliquer_style(chemin_relatif):
    """
    Applique un fichier QSS à toute l'application.
    :param chemin_relatif: Chemin relatif depuis la racine du projet (ex: "data/themes/The Witcher/ui/style.qss")
    """
    global STYLE_ACTUEL
    chemin_absolu = RACINE_PROJET / chemin_relatif

    file = QFile(str(chemin_absolu))
    if file.exists():
        style_sheet = file.readAll().data().decode("utf-8")
        QApplication.instance().setStyleSheet(style_sheet)
        STYLE_ACTUEL = chemin_relatif
        file.close()
    else:
        print(f"⚠️ Erreur : Fichier {chemin_absolu} introuvable.")
