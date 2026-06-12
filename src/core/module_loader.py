# src/core/module_loader.py
import importlib
from typing import Dict, Any, Optional
from pathlib import Path

class ModuleLoader:
    """Charge dynamiquement les modules depuis src/core/ et src/modules/."""

    def __init__(self):
        self.modules: Dict[str, Any] = {}
        self.config: Dict[str, Any] = {"active_modules": [], "module_config": {}}
        self.yaml_loader = None  # Sera initialisé depuis main.py

    def load_config(self, scenario_name: str):
        """Charge la config des modules pour un scénario."""
        modules_yaml = Path(f"data/themes/Fantasy/scenarios/{scenario_name}/modules.yaml")
        if modules_yaml.exists():
            self.config = self.yaml_loader.load(str(modules_yaml))
        else:
            self.config = {"active_modules": [], "module_config": {}}

    def load_module(self, module_name: str):
        """Charge un module depuis src/core/ ou src/modules/."""
        if module_name not in self.config["active_modules"]:
            return None

        if module_name in self.modules:
            return self.modules[module_name]

        try:
            module_path = f"src.modules.{module_name}"
            module = importlib.import_module(module_path)
        except ImportError as e:
            print(f"Erreur : module {module_name} introuvable : {str(e)}")
            return None

        # Instancier la classe (convention : nom du module en PascalCase)
        class_name = module_name.capitalize()
        if module_name == "yaml_loader":
            class_name = "YAMLLoaderManager"  # Cas spécial
        manager_class = getattr(module, class_name, None)
        if manager_class:
            module_config = self.config.get("module_config", {}).get(module_name, {})
            self.modules[module_name] = manager_class()
            # Passer yaml_loader aux modules qui en ont besoin
            if hasattr(self.modules[module_name], 'yaml_loader'):
                self.modules[module_name].yaml_loader = self.yaml_loader
            return self.modules[module_name]
        return None

    def load_all(self):
        """Charge tous les modules activés."""
        for module_name in self.config["active_modules"]:
            self.load_module(module_name)

    def get_module(self, module_name: str) -> Any:
        """Retourne un module chargé."""
        return self.modules.get(module_name)

    def unload_all(self):
        """Désactive tous les modules."""
        self.modules.clear()