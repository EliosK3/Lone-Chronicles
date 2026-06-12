# core/module_loader.py
import importlib
from typing import Dict, Any, Optional
from pathlib import Path

class ModuleLoader:
    """Charge et gère les modules activés pour un scénario donné."""

    def __init__(self, scenario_config: Optional[Dict[str, Any]] = None):
        self.modules: Dict[str, Any] = {}  # {nom_module: instance}
        self.config = scenario_config if scenario_config else {"active_modules": [], "module_config": {}}

    def load_config(self, scenario_name: str):
        """Charge la configuration des modules pour un scénario donné."""
        modules_yaml = Path(f"data/scenarios/{scenario_name}/modules.yaml")
        if modules_yaml.exists():
            from modules.yaml_loader.yaml_loader import YAMLLoaderManager
            yaml_loader = YAMLLoaderManager({})
            self.config = yaml_loader.load(modules_yaml)
        else:
            self.config = {"active_modules": [], "module_config": {}}

    def load_module(self, module_name: str):
        """Charge un module par son nom."""
        if module_name not in self.config["active_modules"]:
            return None  # Module non activé pour ce scénario

        if module_name in self.modules:
            return self.modules[module_name]  # Déjà chargé

        try:
            # Importer dynamiquement le module
            module_path = f"modules.{module_name}.{module_name}"
            module = importlib.import_module(module_path)
        except ImportError as e:
            print(f"Erreur : impossible de charger le module {module_name} : {str(e)}")
            return None

        # Instancier la classe principale du module
        class_name = f"{module_name.capitalize()}Manager"
        manager_class = getattr(module, class_name, None)
        if manager_class:
            module_config = self.config.get("module_config", {}).get(module_name, {})
            self.modules[module_name] = manager_class(module_config)
            return self.modules[module_name]
        return None

    def load_all(self):
        """Charge tous les modules activés pour le scénario."""
        for module_name in self.config["active_modules"]:
            self.load_module(module_name)

    def get_module(self, module_name: str) -> Any:
        """Récupère une instance de module."""
        return self.modules.get(module_name)

    def unload_all(self):
        """Désactive tous les modules."""
        self.modules.clear()