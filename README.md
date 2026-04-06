# Dark Rotation Bot

Tracks and announces the Lost Ark dark grenade rotation with an always-on-top
overlay and configurable hotkeys. Confirms throws manually via hotkey.

---

## Features

- Always-on-top overlay shows current player, next player, and countdown bar
- Two-phase timing: player window → dark buff countdown (20 s normal / 25 s splendid)
- Auto-skips players whose grenade is still on cooldown
- Tracks per-player throw count; stops the rotation when everyone hits the cap
- Configurable hotkeys (works while Lost Ark is in focus)
- PyQt5 GUI for editing roster, rotation settings, hotkeys, and overlay — live while the bot is running
- Overlay position saves automatically when dragged; restores on next launch
- GUI window position also saves and restores on next launch

---

## Requirements

- Windows 10 or 11
- Python 3.11+ — https://www.python.org/downloads/

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/dark-rotation-bot.git
cd dark-rotation-bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the GUI

```bash
python gui.py
```

Edit your roster, hotkeys, and settings from the GUI. Click **Apply** to save,
then **▶ Launch** to start the bot.

---

## Running headlessly (no GUI)

If you prefer to run from the terminal without the config window:

```bash
python main.py
```

Edit `config.yaml` and `rosters/my_raid.yaml` manually before running.

---

## Hotkeys (defaults)

| Key | Action |
|-----|--------|
| F8  | Start / Stop rotation |
| F9  | Confirm dark thrown (starts 20–25 s buff countdown) |
| F10 | Dark missed (counts toward throw limit, advances to next player) |
| F11 | Quit |

Rebind any key in the GUI under the **Hotkeys** tab, or directly in `config.yaml`.

---

## How it works

1. Press **F8** (or click **▶ Launch** in the GUI) to start the rotation
2. The overlay announces the first player
3. **Phase 1 — Player window (20 s):**
   - Press **F9** when the player throws their dark grenade
   - If no confirm within 20 s, the bot fires a miss event automatically
4. **Phase 2 — Dark buff countdown:**
   - After a confirm, the buff timer runs (20 s normal / 25 s splendid)
   - A warning fires near the end, naming the next player
   - When the buff expires, the next player's window begins
5. Press **F10** if a player misses — counts the miss and advances to next player
6. Players on cooldown are skipped automatically
7. Once every player hits `max_throws_per_run`, the rotation ends

---

## Config reference

```yaml
rotation:
  warning_seconds: 5            # warning callout N seconds before next window
  dark_cooldown_seconds: 30     # skip players whose grenade is still on cooldown
  max_throws_per_run: 3         # per-player throw cap; rotation ends when all reach it
  active_roster: my_raid.yaml

hotkeys:
  start_stop: f8
  confirm: f9
  missed: f10
  quit: f11

overlay:
  position: {x: 0, y: 0}       # auto-saved when you drag the overlay
  width: 320
  height: 230
  opacity: 0.88
  font_size: 16

gui:
  position: {x: 100, y: 100}   # auto-saved when you move the GUI window
```

---

## Building a standalone .exe

To create a double-clickable executable (no terminal, no Python required):

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile gui.py
```

Output: `gui.exe` (PyInstaller places it in `dist/gui.exe` — move it to the project root). Re-run this command any time you update the code.
`config.yaml` and `rosters/` stay as live files next to the `.exe`.

---

## Multiple Rosters

Create additional `.yaml` files in the `rosters/` folder using the same format.
Change `active_roster` in `config.yaml` (or via the GUI) to switch between them.

---

## License

MIT
