# src/core/character.py
from typing import Dict, Any
from pathlib import Path

class Character:
    """Gère la fiche personnage."""

    def __init__(self):
        self.data: Dict[str, Any] = {}
        self.yaml_loader = None  # Initialisé par ModuleLoader

    def create_character(self, name: str, age: int, history: str, theme: str):
        """Crée un personnage vide."""
        self.data = {
            "name": name,
            "age": age,
            "history": history,
            "theme": theme,
            "stats": {},
            "inventory": [],
            "variables": {}
        }

    def load_character(self, file_path: str = "data/player.yaml"):
        """Charge un personnage depuis data/player.yaml."""
        if Path(file_path).exists():
            self.data = self.yaml_loader.load(file_path)
        else:
            self.data = {
                "name": "", "age": 0, "history": "", "theme": "",
                "stats": {}, "inventory": [], "variables": {}
            }

    def save_character(self, file_path: str = "data/themes//Fantasy/personnages/player.yaml"):
        """Sauvegarde le personnage."""
        self.yaml_loader.save(self.data, file_path)

    def get_data(self) -> Dict[str, Any]:
        return self.data

    def set_stat(self, stat_name: str, value: Any):
        if "stats" not in self.data:
            self.data["stats"] = {}
        self.data["stats"][stat_name] = value

    def get_stat(self, stat_name: str) -> Any:
        return self.data.get("stats", {}).get(stat_name)

    def set_variable(self, var_name: str, value: Any):
        if "variables" not in self.data:
            self.data["variables"] = {}
        self.data["variables"][var_name] = value

    def get_variable(self, var_name: str) -> Any:
        return self.data.get("variables", {}).get(var_name)