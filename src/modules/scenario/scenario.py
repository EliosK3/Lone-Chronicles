# modules/scenario/scenario.py
import networkx as nx
from typing import Dict, Any, List, Optional
from pathlib import Path
from modules.yaml_loader.yaml_loader import YAMLLoaderManager

class ScenarioManager:
    """Gère le chargement et l'exécution d'un scénario sous forme de graphe."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.graph = nx.DiGraph()
        self.current_scene: Optional[str] = None
        self.scenario_name: Optional[str] = None
        self.scenario_data: Dict[str, Any] = {}
        self.yaml_loader = YAMLLoaderManager({})  # On initialise un YAMLLoader pour ce module

    def load_scenario(self, scenario_name: str):
        """Charge un scénario depuis son dossier."""
        self.scenario_name = scenario_name
        scenario_yaml = Path(f"data/scenarios/{scenario_name}/scenario.yaml")

        if not scenario_yaml.exists():
            raise FileNotFoundError(f"Scénario '{scenario_name}' introuvable : {scenario_yaml}")

        self.scenario_data = self.yaml_loader.load(scenario_yaml)
        self._build_graph()
        self.current_scene = self.scenario_data.get("start_scene")

    def _build_graph(self):
        """Construit le graphe NetworkX à partir des données du scénario."""
        self.graph = nx.DiGraph()

        for scene_id, scene_data in self.scenario_data.get("scenes", {}).items():
            self.graph.add_node(
                scene_id,
                description=scene_data.get("description", ""),
                choices=scene_data.get("choices", [])
            )

            for choice in scene_data.get("choices", []):
                self.graph.add_edge(
                    scene_id,
                    choice["next_scene"],
                    choice_text=choice["text"],
                    condition=choice.get("condition"),
                    cost=choice.get("cost")
                )

    def get_current_scene(self) -> Dict[str, Any]:
        """Retourne les données de la scène actuelle."""
        if self.current_scene is None:
            raise ValueError("Aucun scénario chargé.")

        node_data = self.graph.nodes[self.current_scene]
        return {
            "id": self.current_scene,
            "description": node_data["description"],
            "choices": node_data["choices"]
        }

    def choose(self, choice_index: int, character_data: Dict[str, Any]) -> bool:
        """
        Applique un choix et passe à la scène suivante.
        Retourne True si le choix est valide, False sinon.
        """
        if self.current_scene is None:
            raise ValueError("Aucun scénario chargé.")

        choices = self.graph.nodes[self.current_scene]["choices"]
        if choice_index < 0 or choice_index >= len(choices):
            return False

        choice = choices[choice_index]
        next_scene = choice["next_scene"]

        # Vérifier la condition (si elle existe)
        if choice.get("condition"):
            if not self._check_condition(choice["condition"], character_data):
                return False

        # Appliquer le coût (si il existe)
        if choice.get("cost"):
            self._apply_cost(choice["cost"], character_data)

        self.current_scene = next_scene
        return True

    def _check_condition(self, condition: Dict[str, Any], character_data: Dict[str, Any]) -> bool:
        """Vérifie si une condition est remplie."""
        variable = condition.get("variable")
        operator = condition.get("operator")
        value = condition.get("value")

        if variable is None or operator is None or value is None:
            return True  # Pas de condition = toujours vrai

        # Récupérer la valeur depuis les stats ou variables du personnage
        char_value = character_data.get("stats", {}).get(variable)
        if char_value is None:
            char_value = character_data.get("variables", {}).get(variable, 0)

        if operator == ">":
            return char_value > value
        elif operator == ">=":
            return char_value >= value
        elif operator == "<":
            return char_value < value
        elif operator == "<=":
            return char_value <= value
        elif operator == "==":
            return char_value == value
        elif operator == "!=":
            return char_value != value
        else:
            return False

    def _apply_cost(self, cost: Dict[str, Any], character_data: Dict[str, Any]):
        """Applique un coût (ex: retirer des ressources)."""
        resource = cost.get("resource")
        value = cost.get("value", 0)

        if resource is None:
            return

        # Appliquer le coût aux stats ou variables
        if resource in character_data.get("stats", {}):
            character_data["stats"][resource] += value
        elif resource in character_data.get("variables", {}):
            character_data["variables"][resource] += value