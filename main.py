"""
main.py - Dark Rotation Bot entry point
Wires together engine, overlay, and hotkeys.

Usage:
    python main.py
"""

import os
import sys
import yaml
import time


# ------------------------------------------------------------------
# Load config
# ------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_config() -> dict:
    path = os.path.join(BASE_DIR, "config.yaml")
    with open(path, "r") as f:
        return yaml.safe_load(f)


# ------------------------------------------------------------------
# Main bot class
# ------------------------------------------------------------------

class DarkRotationBot:
    def __init__(self):
        self.config = load_config()
        self._started = False

        # Lazy imports (so missing libs give a clear error message)
        from modules.roster  import RosterManager
        from modules.engine  import RotationEngine
        from modules.overlay import OverlayWindow
        from modules.hotkeys import HotkeyManager

        # --- Roster ---
        self.roster = RosterManager(os.path.join(BASE_DIR, "rosters"))
        roster_file = self.config.get("rotation", {}).get("active_roster", "my_raid.yaml")
        players = self.roster.load(roster_file)

        # --- Engine ---
        self.engine = RotationEngine(self.config, self._on_engine_event)
        self.engine.set_players(players)

        # --- Overlay ---
        self.overlay = OverlayWindow(
            self.config.get("overlay", {}),
            get_status_fn=self.engine.get_status,
        )

        # --- Hotkeys ---
        self.hotkeys = HotkeyManager(
            self.config.get("hotkeys", {}),
            callbacks={
                "start_stop": self._hotkey_start_stop,
                "confirm":    self._hotkey_confirm,
                "missed":     self._hotkey_missed,
                "quit":       self._hotkey_quit,
            },
        )

    # ------------------------------------------------------------------
    # Hotkey handlers
    # ------------------------------------------------------------------

    def _hotkey_start_stop(self):
        if self._started:
            print("[Bot] Stopping rotation.")
            self.engine.stop()
            self._started = False
        else:
            print("[Bot] Starting rotation.")
            self.engine.start()
            self._started = True

    def _hotkey_quit(self):
        print("[Bot] Quitting.")
        self.engine.stop()
        self.hotkeys.stop()
        self.overlay.stop()

    def _hotkey_missed(self):
        if self._started:
            self.engine.on_dark_missed()

    def _hotkey_confirm(self):
        if self._started:
            status = self.engine.get_status()
            player = status.get("current_player", "Unknown")
            self.engine.on_dark_detected(player, is_splendid=False)

    # ------------------------------------------------------------------
    # Engine event handler
    # ------------------------------------------------------------------

    def _on_engine_event(self, event_type: str, data: dict):
        if event_type == "announce":
            player = data["player"]
            print(f"[Bot] Announcing: {player}")

        elif event_type == "cooldown_skip":
            player = data["player"]
            print(f"[Bot] Cooldown skip: {player}")
            self.overlay.set_status_message(f"{player} on cooldown", "#ffaa00")

        elif event_type == "player_exhausted":
            player = data["player"]
            count = data["count"]
            print(f"[Bot] {player} exhausted ({count} throws)")
            self.overlay.set_status_message(f"{player} done ({count} throws)", "#888888")

        elif event_type == "rotation_complete":
            print("[Bot] Rotation complete.")
            self.overlay.set_status_message("Rotation complete", "#aaaaaa")

        elif event_type == "warning":
            nxt = data["next"]
            secs = data["seconds"]
            print(f"[Bot] Warning: {nxt} up in {secs}s")
            self.overlay.set_status_message(f"Next up: {nxt} in {secs}s", "#ffdd44")

        elif event_type == "confirmed":
            player = data["player"]
            print(f"[Bot] Confirmed: {player}")
            self.overlay.flash("#1a4a1a")
            self.overlay.set_status_message(f"OK {player} confirmed", "#44ff88")

        elif event_type == "missed":
            player = data["player"]
            print(f"[Bot] MISSED: {player}")
            self.overlay.flash("#4a1a1a")
            self.overlay.set_status_message(f"X {player} missed", "#ff4444")

        elif event_type == "state_change":
            print(f"[Bot] State -> {data['state']}")

    # ------------------------------------------------------------------
    # Run
    # ------------------------------------------------------------------

    def run(self):
        print("\n===========================================")
        print("  Dark Rotation Bot — Ready")
        print("===========================================")
        print(f"  F8  -> Start / Stop")
        print(f"  F9  -> Confirm dark thrown")
        print(f"  F10 -> Dark missed")
        print(f"  F11 -> Quit")
        print("===========================================\n")

        self.overlay.start()
        self.hotkeys.start()

        try:
            while True:
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\n[Bot] Shutting down...")
            self.engine.stop()
            self.hotkeys.stop()
            self.overlay.stop()
            print("[Bot] Goodbye.")


# ------------------------------------------------------------------
# Entry point
# ------------------------------------------------------------------

if __name__ == "__main__":
    bot = DarkRotationBot()
    bot.run()
