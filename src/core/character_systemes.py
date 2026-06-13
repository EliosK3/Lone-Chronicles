"""
Système de personnage modulaire - architecture par composants (ECS-lite)
==========================================================================

Concept :
- Un Character est un simple conteneur (sac de composants/"briques")
- Chaque brique encapsule UNE responsabilité : Stats, Inventaire,
  Compétences, Faction, Dialogue, Statuts/Effets, IA, etc.
- Chaque brique peut être activée/désactivée indépendamment (ex: un PNJ
  décoratif aura "stats" mais pas "skills" ; un boss aura tout)
- Les personnages sont construits via des "templates" (dict/JSON) qui
  décrivent quels modules attacher et avec quelles données initiales
- Un bus d'événements permet aux briques de communiquer sans dépendre
  les unes des autres directement

Pour ajouter une nouvelle brique :
  1. Créer une classe héritant de Component
  2. L'enregistrer dans COMPONENT_REGISTRY
  3. L'utiliser dans tes templates de personnages
"""

from __future__ import annotations
from abc import ABC
from typing import Callable
import json


# ---------------------------------------------------------------------------
# 1. Base Component
# ---------------------------------------------------------------------------

class Component(ABC):
    """Classe de base pour toute brique attachable à un personnage."""

    name: str = "component"  # identifiant unique utilisé dans le registre

    def __init__(self, enabled: bool = True, **kwargs):
        self.owner: "Character" | None = None
        self.enabled = enabled

    def on_attach(self, character: "Character") -> None:
        """Appelé quand le composant est attaché à un personnage."""
        self.owner = character

    def on_detach(self) -> None:
        self.owner = None

    def update(self, dt: float) -> None:
        """Appelé chaque tick si le composant est actif. À surcharger si besoin."""
        pass

    def to_dict(self) -> dict:
        """Sérialisation par défaut (à compléter dans chaque sous-classe)."""
        return {"enabled": self.enabled}


# ---------------------------------------------------------------------------
# 2. Bus d'événements (communication inter-briques sans dépendances directes)
# ---------------------------------------------------------------------------

class EventBus:
    def __init__(self):
        self._listeners: dict[str, list[Callable]] = {}

    def subscribe(self, event: str, callback: Callable) -> None:
        self._listeners.setdefault(event, []).append(callback)

    def emit(self, event: str, **payload) -> None:
        for callback in self._listeners.get(event, []):
            callback(**payload)


# ---------------------------------------------------------------------------
# 3. Le personnage = conteneur de modules
# ---------------------------------------------------------------------------

class Character:
    def __init__(self, name: str):
        self.name = name
        self.components: dict[str, Component] = {}
        self.events = EventBus()

    def add(self, component: Component) -> "Character":
        component.on_attach(self)
        self.components[component.name] = component
        return self  # permet le chaînage : char.add(...).add(...)

    def remove(self, name: str) -> None:
        comp = self.components.pop(name, None)
        if comp:
            comp.on_detach()

    def has(self, name: str) -> bool:
        return name in self.components

    def get(self, name: str) -> Component | None:
        return self.components.get(name)

    def enable(self, name: str, state: bool = True) -> None:
        """Active/désactive une brique à la volée (ex: un PNJ devient hostile)."""
        if comp := self.components.get(name):
            comp.enabled = state

    def update(self, dt: float) -> None:
        for comp in self.components.values():
            if comp.enabled:
                comp.update(dt)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "components": {
                k: {"type": type(c).__name__, **c.to_dict()}
                for k, c in self.components.items()
            },
        }

    def __repr__(self) -> str:
        modules = ", ".join(
            f"{k}{'' if c.enabled else '(off)'}" for k, c in self.components.items()
        )
        return f"<Character {self.name} [{modules}]>"


# ---------------------------------------------------------------------------
# 4. Exemples de briques de base
# ---------------------------------------------------------------------------

class StatsComponent(Component):
    """Points de vie, mana, attributs de base."""
    name = "stats"

    def __init__(self, hp=10, mana=0, force=1, agilite=1, intelligence=1, **kwargs):
        super().__init__(**kwargs)
        self.hp_max = hp
        self.hp = hp
        self.mana = mana
        self.force = force
        self.agilite = agilite
        self.intelligence = intelligence

    def take_damage(self, amount: int) -> None:
        self.hp = max(0, self.hp - amount)
        if self.owner:
            self.owner.events.emit("damage_taken", character=self.owner, amount=amount)
            if self.hp == 0:
                self.owner.events.emit("character_died", character=self.owner)

    def to_dict(self) -> dict:
        return {
            **super().to_dict(),
            "hp": self.hp, "hp_max": self.hp_max, "mana": self.mana,
            "force": self.force, "agilite": self.agilite, "intelligence": self.intelligence,
        }


class InventoryComponent(Component):
    """Sac d'objets avec capacité limitée."""
    name = "inventory"

    def __init__(self, capacity=10, items=None, **kwargs):
        super().__init__(**kwargs)
        self.capacity = capacity
        self.items: list[str] = list(items) if items else []

    def add_item(self, item: str) -> bool:
        if len(self.items) >= self.capacity:
            return False
        self.items.append(item)
        return True

    def to_dict(self) -> dict:
        return {**super().to_dict(), "capacity": self.capacity, "items": self.items}


class SkillsComponent(Component):
    """Compétences/sorts et leur niveau."""
    name = "skills"

    def __init__(self, skills=None, **kwargs):
        super().__init__(**kwargs)
        self.skills: dict[str, int] = dict(skills) if skills else {}

    def level_of(self, skill_name: str) -> int:
        return self.skills.get(skill_name, 0)

    def to_dict(self) -> dict:
        return {**super().to_dict(), "skills": self.skills}


class FactionComponent(Component):
    """Appartenance à une faction et réputation."""
    name = "faction"

    def __init__(self, faction="neutre", reputation=0, **kwargs):
        super().__init__(**kwargs)
        self.faction = faction
        self.reputation = reputation

    def to_dict(self) -> dict:
        return {**super().to_dict(), "faction": self.faction, "reputation": self.reputation}


class DialogueComponent(Component):
    """Lignes de dialogue par clé (greet, farewell, quest_offer, ...)."""
    name = "dialogue"

    def __init__(self, lines=None, **kwargs):
        super().__init__(**kwargs)
        self.lines: dict[str, str] = dict(lines) if lines else {}

    def say(self, key: str) -> str:
        return self.lines.get(key, "...")

    def to_dict(self) -> dict:
        return {**super().to_dict(), "lines": self.lines}


# ---------------------------------------------------------------------------
# 5. Registre + Factory : construire un personnage depuis un template
# ---------------------------------------------------------------------------

COMPONENT_REGISTRY: dict[str, type[Component]] = {
    "stats": StatsComponent,
    "inventory": InventoryComponent,
    "skills": SkillsComponent,
    "faction": FactionComponent,
    "dialogue": DialogueComponent,
}


def build_character(template: dict) -> Character:
    """
    Construit un personnage à partir d'un template, ex :

    {
      "name": "Garde du village",
      "modules": {
        "stats": {"hp": 20, "force": 3},
        "inventory": {"capacity": 5, "items": ["épée"]},
        "faction": {"faction": "village", "reputation": 0},
        "dialogue": {"enabled": False, "lines": {"greet": "Halte !"}}
      }
    }

    Un module absent du template = brique non présente du tout
    (et non juste désactivée), pour garder les persos légers.
    Pour la désactiver tout en la gardant : "enabled": false dans ses données.
    """
    char = Character(template["name"])
    for mod_name, mod_data in template.get("modules", {}).items():
        comp_class = COMPONENT_REGISTRY.get(mod_name)
        if comp_class is None:
            raise ValueError(f"Module inconnu : '{mod_name}'")
        char.add(comp_class(**mod_data))
    return char


# ---------------------------------------------------------------------------
# 6. Exemple d'utilisation
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    template = {
        "name": "Garde du village",
        "modules": {
            "stats": {"hp": 20, "force": 3},
            "inventory": {"capacity": 5, "items": ["épée"]},
            "faction": {"faction": "village", "reputation": 0},
            "dialogue": {"enabled": False, "lines": {"greet": "Halte !"}},
        },
    }

    garde = build_character(template)
    print(garde)
    print(json.dumps(garde.to_dict(), indent=2, ensure_ascii=False))

    # Activer le dialogue dynamiquement (ex: événement narratif)
    garde.enable("dialogue", True)
    print(garde.get("dialogue").say("greet"))

    # S'abonner à un événement émis par une brique
    garde.events.subscribe(
        "character_died",
        lambda character: print(f"{character.name} est mort !")
    )
    garde.get("stats").take_damage(25)