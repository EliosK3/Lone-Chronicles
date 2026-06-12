# modules/yaml_loader/yaml_loader.py
import yaml
from typing import Dict, Any
from pathlib import Path

class YAMLLoaderManager:
    """Gère la lecture et l'écriture des fichiers YAML."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def load(self, file_path: str) -> Dict[str, Any]:
        """Charge un fichier YAML et retourne son contenu sous forme de dict."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Fichier introuvable : {file_path}")

        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def save(self, data: Dict[str, Any], file_path: str):
        """Sauvegarde un dict dans un fichier YAML."""
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)  # Crée les dossiers parents si nécessaire
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False)