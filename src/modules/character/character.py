# modules/character/character.py
from typing import Dict, Any, Optional
from pathlib import Path
from modules.yaml_loader.yaml_loader import YAMLLoaderManager

class CharacterManager:
    """Gère la fiche personnage (création, sauvegarde, chargement)."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.character_data: Dict[str, Any] = {}
        self.yaml_loader = YAMLLoaderManager({})

    def create_character(self, name: str, age: int, history: str, theme: str):
        """Crée un nouveau personnage avec des valeurs par défaut."""
        self.character_data = {
            "name": name,
            "age": age,
            "history": history,
            "theme": theme,
            "stats": {},
            "inventory": [],
            "variables": {}  # Pour les variables globales (ex: réputation, or)
        }

    def load_character(self, file_path: str = "data/player.yaml"):
        """Charge un personnage depuis un fichier YAML."""
        if Path(file_path).exists():
            self.character_data = self.yaml_loader.load(file_path)
        else:
            # Si le fichier n'existe pas, créer un personnage vide
            self.character_data = {
                "name": "",
                "age": 0,
                "history": "",
                "theme": "",
                "stats": {},
                "inventory": [],
                "variables": {}
            }

    def save_character(self, file_path: str = "data/player.yaml"):
        """Sauvegarde le personnage dans un fichier YAML."""
        self.yaml_loader.save(self.character_data, file_path)

    def get_character(self) -> Dict[str, Any]:
        """Retourne les données du personnage."""
        return self.character_data

    def set_stat(self, stat_name: str, value: Any):
        """Modifie une stat du personnage."""
        if "stats" not in self.character_data:
            self.character_data["stats"] = {}
        self.character_data["stats"][stat_name] = value

    def get_stat(self, stat_name: str) -> Any:
        """Récupère une stat du personnage."""
        return self.character_data.get("stats", {}).get(stat_name)

    def set_variable(self, var_name: str, value: Any):
        """Modifie une variable globale du personnage."""
        if "variables" not in self.character_data:
            self.character_data["variables"] = {}
        self.character_data["variables"][var_name] = value

    def get_variable(self, var_name: str) -> Any:
        """Récupère une variable globale du personnage."""
        return self.character_data.get("variables", {}).get(var_name)