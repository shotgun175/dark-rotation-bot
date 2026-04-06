"""
roster.py - Load, save, and manage player rotation lists
"""

import os
import yaml


class RosterManager:
    def __init__(self, rosters_dir: str):
        self.rosters_dir = rosters_dir
        self.current_roster_name = None
        self.players = []

    # ------------------------------------------------------------------
    # Load / Save
    # ------------------------------------------------------------------

    def load(self, filename: str) -> list[str]:
        """Load a roster YAML file. Returns list of player names."""
        path = os.path.join(self.rosters_dir, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Roster file not found: {path}")

        with open(path, "r") as f:
            data = yaml.safe_load(f)

        self.players = [str(p) for p in data.get("players", [])]
        self.current_roster_name = data.get("name", filename)
        print(f"[Roster] Loaded '{self.current_roster_name}': {self.players}")
        return self.players

    def save(self, filename: str, name: str, players: list[str]):
        """Save a roster to a YAML file."""
        path = os.path.join(self.rosters_dir, filename)
        data = {"name": name, "players": players}
        with open(path, "w") as f:
            yaml.dump(data, f, default_flow_style=False)
        print(f"[Roster] Saved '{name}' to {path}")

    def list_rosters(self) -> list[str]:
        """Return all .yaml files in the rosters directory."""
        return [
            f for f in os.listdir(self.rosters_dir)
            if f.endswith(".yaml") or f.endswith(".yml")
        ]

    # ------------------------------------------------------------------
    # Player management (runtime edits, not persisted until save())
    # ------------------------------------------------------------------

    def set_players(self, players: list[str]):
        self.players = list(players)

    def add_player(self, name: str, position: int = None):
        if position is None:
            self.players.append(name)
        else:
            self.players.insert(position, name)

    def remove_player(self, name: str) -> bool:
        if name in self.players:
            self.players.remove(name)
            return True
        return False

    def move_player(self, name: str, new_index: int):
        if name not in self.players:
            return
        self.players.remove(name)
        self.players.insert(new_index, name)

    def get_players(self) -> list[str]:
        return list(self.players)
