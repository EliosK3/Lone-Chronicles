# src/modules/yaml_loader/yaml_loader.py
import yaml
from typing import Dict, Any
from pathlib import Path

class YAMLLoaderManager:
    """Gère la lecture/écriture des fichiers YAML."""

    def __init__(self):
        pass

    def load(self, file_path: str) -> Dict[str, Any]:
        """Charge un fichier YAML."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Fichier introuvable : {file_path}")
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def save(self, data: Dict[str, Any], file_path: str):
        """Sauvegarde un dict en YAML."""
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False)