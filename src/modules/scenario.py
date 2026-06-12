# src/core/scenario.py
import networkx as nx
from typing import Dict, Any, Optional
from pathlib import Path

class Scenario:
    """Gère un scénario sous forme de graphe NetworkX."""

    def __init__(self):
        self.graph = nx.DiGraph()
        self.current_scene: Optional[str] = None
        self.scenario_name: Optional[str] = None
        self.scenario_data: Dict[str, Any] = {}
        self.yaml_loader = None  # Sera initialisé par ModuleLoader

    def load_scenario(self, scenario_name: str):
        """Charge un scénario depuis data/scenarios/<name>/scenario.yaml."""
        self.scenario_name = scenario_name
        scenario_yaml = Path(f"data/themes/Fantasy/scenarios/{scenario_name}/scenario.yaml")
        if not scenario_yaml.exists():
            raise FileNotFoundError(f"Scénario '{scenario_name}' introuvable.")

        self.scenario_data = self.yaml_loader.load(str(scenario_yaml))
        self._build_graph()
        self.current_scene = self.scenario_data.get("start_scene")

    def _build_graph(self):
        """Construit le graphe à partir des données YAML."""
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
        """Retourne la scène actuelle."""
        if self.current_scene is None:
            raise ValueError("Aucun scénario chargé.")
        node = self.graph.nodes[self.current_scene]
        return {
            "id": self.current_scene,
            "description": node["description"],
            "choices": node["choices"]
        }

    def choose(self, choice_index: int, character_data: Dict[str, Any]) -> bool:
        """Applique un choix et passe à la scène suivante."""
        if self.current_scene is None:
            raise ValueError("Aucun scénario chargé.")

        choices = self.graph.nodes[self.current_scene]["choices"]
        if choice_index < 0 or choice_index >= len(choices):
            return False

        choice = choices[choice_index]
        if choice.get("condition") and not self._check_condition(choice["condition"], character_data):
            return False

        if choice.get("cost"):
            self._apply_cost(choice["cost"], character_data)

        self.current_scene = choice["next_scene"]
        return True

    def _check_condition(self, condition: Dict[str, Any], character_data: Dict[str, Any]) -> bool:
        """Vérifie une condition (ex: charisme > 10)."""
        variable = condition.get("variable")
        operator = condition.get("operator")
        value = condition.get("value")
        if None in (variable, operator, value):
            return True

        char_value = character_data.get("stats", {}).get(variable)
        if char_value is None:
            char_value = character_data.get("variables", {}).get(variable, 0)

        if operator == ">": return char_value > value
        if operator == ">=": return char_value >= value
        if operator == "<": return char_value < value
        if operator == "<=": return char_value <= value
        if operator == "==": return char_value == value
        if operator == "!=": return char_value != value
        return False

    def _apply_cost(self, cost: Dict[str, Any], character_data: Dict[str, Any]):
        """Applique un coût (ex: or -= 10)."""
        resource = cost.get("resource")
        value = cost.get("value", 0)
        if resource is None:
            return
        if resource in character_data.get("stats", {}):
            character_data["stats"][resource] += value
        elif resource in character_data.get("variables", {}):
            character_data["variables"][resource] += value