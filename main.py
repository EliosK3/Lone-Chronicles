# main.py
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QPushButton, QLabel, QListWidget, QMessageBox
)
from PyQt6.QtCore import Qt
from pathlib import Path
from core.module_loader import ModuleLoader
from modules.yaml_loader.yaml_loader import YAMLLoaderManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lone Chronicles - Sélection d'Histoire")
        self.setGeometry(100, 100, 600, 400)
        self.module_loader = None
        self.scenario_manager = None
        self.character_manager = None
        self.yaml_loader = YAMLLoaderManager({})  # Pour charger les scénarios
        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        layout = QVBoxLayout()

        # Titre
        title = QLabel("Choisis une histoire :")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Liste des scénarios disponibles
        self.scenario_list = QListWidget()
        self.load_scenarios()
        self.scenario_list.itemDoubleClicked.connect(self.on_scenario_selected)
        layout.addWidget(self.scenario_list)

        # Bouton pour valider
        start_btn = QPushButton("Commencer l'Aventure")
        start_btn.clicked.connect(self.on_start_clicked)
        layout.addWidget(start_btn)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def load_scenarios(self):
        """Charge la liste des scénarios disponibles depuis le dossier data/scenarios."""
        scenarios_dir = Path("data/scenarios")
        if not scenarios_dir.exists():
            scenarios_dir.mkdir(parents=True, exist_ok=True)
            return

        for scenario_dir in scenarios_dir.iterdir():
            if scenario_dir.is_dir():
                scenario_yaml = scenario_dir / "scenario.yaml"
                if scenario_yaml.exists():
                    scenario_data = self.yaml_loader.load(scenario_yaml)
                    self.scenario_list.addItem(scenario_data["name"])

    def on_scenario_selected(self, item):
        """Appelé quand un scénario est sélectionné dans la liste."""
        self.selected_scenario = item.text()

    def on_start_clicked(self):
        """Appelé quand l'utilisateur clique sur 'Commencer l'Aventure'."""
        if not hasattr(self, "selected_scenario"):
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une histoire.")
            return

        # Charger les modules nécessaires pour ce scénario
        self.load_modules_for_scenario(self.selected_scenario)

        # Charger le scénario
        self.load_scenario(self.selected_scenario)

        # Charger ou créer le personnage
        self.load_or_create_character()

        # Passer à l'écran de jeu (à implémenter plus tard)
        self.show_game_screen()

    def load_modules_for_scenario(self, scenario_name: str):
        """Charge les modules nécessaires pour un scénario donné."""
        self.module_loader = ModuleLoader()
        self.module_loader.load_config(scenario_name)
        self.module_loader.load_all()

        # Récupérer les modules nécessaires
        self.scenario_manager = self.module_loader.get_module("scenario")
        self.character_manager = self.module_loader.get_module("character")
        self.yaml_loader = self.module_loader.get_module("yaml_loader")

        if self.scenario_manager is None:
            QMessageBox.critical(self, "Erreur", f"Impossible de charger le module 'scenario' pour '{scenario_name}'.")
            return
        if self.character_manager is None:
            QMessageBox.critical(self, "Erreur", f"Impossible de charger le module 'character' pour '{scenario_name}'.")

    def load_scenario(self, scenario_name: str):
        """Charge le scénario sélectionné."""
        try:
            self.scenario_manager.load_scenario(scenario_name)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de charger le scénario : {str(e)}")

    def load_or_create_character(self):
        """Charge le personnage existant ou en crée un nouveau."""
        try:
            self.character_manager.load_character()
            if not self.character_manager.get_character().get("name"):
                # Si le personnage n'a pas de nom, on en crée un nouveau
                self.create_new_character()
        except Exception as e:
            QMessageBox.warning(self, "Avertissement", f"Impossible de charger le personnage : {str(e)}. Création d'un nouveau personnage.")
            self.create_new_character()

    def create_new_character(self):
        """Crée un nouveau personnage avec des valeurs par défaut."""
        # Ici, on pourrait ouvrir une fenêtre de création de personnage.
        # Pour simplifier, on crée un personnage vide.
        self.character_manager.create_character(
            name="",
            age=0,
            history="",
            theme=self.scenario_manager.scenario_data.get("theme", "unknown")
        )

    def show_game_screen(self):
        """Affiche la première scène du scénario."""
        if self.scenario_manager is None:
            return

        # Récupérer la première scène
        scene_data = self.scenario_manager.get_current_scene()

        # Afficher la scène dans une boîte de dialogue (temporaire)
        choices_text = "\n".join(
            [f"{i+1}. {choice['text']}" for i, choice in enumerate(scene_data["choices"])]
        )
        QMessageBox.information(
            self,
            f"Scénario : {self.scenario_manager.scenario_name}",
            f"{scene_data['description']}\n\nChoix possibles :\n{choices_text}"
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())