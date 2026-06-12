# main.py
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))  # Pour les imports depuis src/

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QPushButton, QLabel, QListWidget, QMessageBox, QScrollArea
)
from PyQt6.QtCore import Qt
from src.core.module_loader import ModuleLoader
from src.modules.yaml_loader import YAMLLoaderManager

# --- FENÊTRE DE SÉLECTION D'HISTOIRE ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lone Chronicles - Sélection d'Histoire")
        self.setGeometry(100, 100, 600, 400)
        self.module_loader = None
        self.scenario = None
        self.character = None
        self.yaml_loader = YAMLLoaderManager()
        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Choisis une histoire :")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.scenario_list = QListWidget()
        self.load_scenarios()
        self.scenario_list.itemDoubleClicked.connect(self.on_scenario_selected)
        layout.addWidget(self.scenario_list)

        start_btn = QPushButton("Commencer l'Aventure")
        start_btn.clicked.connect(self.on_start_clicked)
        layout.addWidget(start_btn)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def load_scenarios(self):
        scenarios_dir = Path("data/themes/Fantasy/scenarios")
        if not scenarios_dir.exists():
            scenarios_dir.mkdir(parents=True, exist_ok=True)
            return

        for scenario_dir in scenarios_dir.iterdir():
            if scenario_dir.is_dir():
                scenario_yaml = scenario_dir / "scenario.yaml"
                if scenario_yaml.exists():
                    scenario_data = self.yaml_loader.load(str(scenario_yaml))
                    self.scenario_list.addItem(scenario_data["name"])

    def on_scenario_selected(self, item):
        self.selected_scenario = item.text()

    def on_start_clicked(self):
        if not hasattr(self, "selected_scenario"):
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une histoire.")
            return

        self.module_loader = ModuleLoader()
        self.module_loader.yaml_loader = self.yaml_loader

        try:
            self.module_loader.load_config(self.selected_scenario)
            self.module_loader.load_all()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de charger les modules : {str(e)}")
            return

        self.scenario = self.module_loader.get_module("scenario")
        self.character = self.module_loader.get_module("character")

        if self.scenario is None:
            QMessageBox.critical(self, "Erreur", "Module 'scenario' non chargé.")
            return
        if self.character is None:
            QMessageBox.critical(self, "Erreur", "Module 'character' non chargé.")
            return

        try:
            self.scenario.load_scenario(self.selected_scenario)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de charger le scénario : {str(e)}")
            return

        try:
            self.character.load_character()
            if not self.character.get_data().get("name"):
                self.create_new_character()
        except Exception as e:
            QMessageBox.warning(self, "Avertissement", f"Création d'un nouveau personnage : {str(e)}")
            self.create_new_character()

        self.show_game_screen()

    def create_new_character(self):
        theme = self.scenario.scenario_data.get("theme", "Fantasy")
        self.character.create_character(
            name="",
            age=0,
            history="",
            theme=theme
        )

    def show_game_screen(self):
        """Ouvre la fenêtre de jeu."""
        if self.scenario is None or self.character is None:
            return
        self.hide()
        self.game_window = GameWindow(self.scenario, self.character, self.yaml_loader)
        self.game_window.show()

# --- FENÊTRE DE JEU (INTERACTIVE) ---
class GameWindow(QMainWindow):
    def __init__(self, scenario_manager, character_manager, yaml_loader):
        super().__init__()
        self.scenario_manager = scenario_manager
        self.character_manager = character_manager
        self.yaml_loader = yaml_loader
        self.setWindowTitle(f"Lone Chronicles - {scenario_manager.scenario_name}")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()
        self.update_scene()

    def init_ui(self):
        main_widget = QWidget()
        layout = QVBoxLayout()

        # Zone de description (scrollable)
        self.scene_description = QLabel()
        self.scene_description.setWordWrap(True)
        self.scene_description.setStyleSheet("font-size: 14px;")
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.scene_description)
        layout.addWidget(scroll_area, stretch=2)

        # Zone pour les choix (boutons)
        self.choices_layout = QVBoxLayout()
        choices_widget = QWidget()
        choices_widget.setLayout(self.choices_layout)
        layout.addWidget(choices_widget, stretch=1)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
        self.apply_dark_style()

    def apply_dark_style(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #2b2b2b; color: #ffffff; }
            QLabel { color: #ffffff; }
            QPushButton {
                background-color: #3c3f41;
                color: #ffffff;
                border: 1px solid #555;
                padding: 8px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #4e5052; }
            QPushButton:pressed { background-color: #2a2d2e; }
            QScrollArea { background-color: #3a3a3a; border: none; }
        """)

    def update_scene(self):
        """Met à jour l'interface avec la scène actuelle."""
        # Efface les anciens choix
        for i in reversed(range(self.choices_layout.count())):
            widget = self.choices_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Récupère la scène actuelle
        scene_data = self.scenario_manager.get_current_scene()
        self.scene_description.setText(scene_data["description"])

        # Ajoute un bouton pour chaque choix
        for i, choice in enumerate(scene_data["choices"]):
            btn = QPushButton(choice["text"])
            btn.setStyleSheet("margin: 5px;")
            btn.clicked.connect(lambda _, index=i: self.handle_choice(index))
            self.choices_layout.addWidget(btn)

    def handle_choice(self, choice_index: int):
        """Gère le choix sélectionné."""
        character_data = self.character_manager.get_data()
        success = self.scenario_manager.choose(choice_index, character_data)

        if success:
            self.character_manager.save_character()
            self.update_scene()
        else:
            QMessageBox.warning(self, "Impossible", "Tu ne peux pas faire ce choix (condition non remplie).")

# --- LANCEMENT DE L'APPLICATION ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())