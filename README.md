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
- Optional OpenCV auto-detection: scans boss debuff bar for Dark / Splendid Dark Grenade icon and auto-confirms with correct timer (20s / 25s)
- Detection region configurable via manual spinboxes or drag-to-draw tool in the Overlay tab
- `Dark Timer.exe` ships with the Splendid Dark Grenade as its icon

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
then **▶ Launch** to arm the bot (overlay appears, audio pre-renders), then press **F8** to start the rotation.

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

1. Click **▶ Launch** — the GUI hides, the overlay appears, and audio clips are pre-rendered in the background
2. Press **F8** when you're ready — the rotation starts and the first player is announced
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
pyinstaller --noconsole --onefile --icon=assets/icon.ico --name="Dark Timer" --clean --hidden-import=edge_tts --hidden-import=aiohttp gui.py
```

Output: `dist/Dark Timer.exe` — move it to the project root. Re-run this command any time you update the code.
`config.yaml`, `rosters/`, and `assets/` stay as live files next to the `.exe`.

---

## Multiple Rosters

Create additional `.yaml` files in the `rosters/` folder using the same format.
Change `active_roster` in `config.yaml` (or via the GUI) to switch between them.

---

## License

MIT

---

## Changelog

### v1.3.2
- **Audio cue system:** TTS voice callouts via Microsoft Edge neural voices (Andrew / Jenny selectable in Audio tab). Announces the current player's name, warns the next player, confirms throws, and plays an optional chime on auto-detection
- **Audio tab:** New GUI tab with master enable toggle, per-cue checkboxes (announce, warning, confirmed, rotation complete, chime), voice selector, volume slider, and Test Voice button. All options gray out visually when audio is disabled
- **Phase 1 warning:** `[Player], get ready` now fires 5 seconds before a player's window closes — even if no dark was confirmed — so the next player always gets a heads-up
- **Launch / F8 split:** Clicking **▶ Launch** arms the bot (overlay shows, audio pre-renders) but does not start the timer. Press **F8** when ready — audio clips are guaranteed loaded by then, so the first announce always plays
- **GUI hides on Launch:** Config window disappears when the bot is armed, freeing screen space and preventing accidental roster resets. A **■** stop button in the top-right of the overlay tears down the bot and restores the GUI
- **Tab reorder:** Audio tab moved before Overlay tab
- **Removed:** "Dark missed" TTS cue (F10 advances the rotation silently)
- **Cleanup:** Removed legacy `main.py` headless entry point; removed unused `mutagen` dependency

### v1.3.1
- **Throw counts on overlay:** player names now show their throw count inline (e.g. `Valslayer  1/3`, `Mabi  0/3`)
- **Spam protection:** duplicate confirms are ignored while the dark buff is active — throw count can no longer exceed the cap
- **Window icon:** title bar and taskbar now show the grenade icon at runtime
- **Taskbar fix:** app registers its own Windows App User Model ID so it gets a dedicated taskbar button instead of grouping under Python

### v1.3.0
- **Overlay tab redesign:** single scrollable left column replaces the fixed right panel — controls never clip or stretch as the window is resized
- **Appearance preview moved inline:** sits next to the Position/Size spinboxes; Region preview sits next to the detection region controls
- **Window resize cap:** maximum window size capped at 1050×680 to prevent excessive stretching
- **Text contrast pass:** all gray text lifted across every tab (`#444`→`#777`, `#555`→`#888`, `#666`→`#999`, `#aaa`→`#ccc`)
- **Font size pass:** UI-wide bump (9px→11px, 11px→13px, 13px→14px); spinboxes now render at 14px
- **Auto-detection card:** checkbox is wrapped in a styled card with a gold indicator when enabled — much easier to notice and toggle
- **Buff display fix:** "DARK NOW" stays on the thrower (e.g. Valslayer) for the full 20/25s buff countdown, with the next player shown as "NEXT"; the overlay only switches to the next player when the buff expires
- **Renamed executable:** `gui.exe` → `Dark Timer.exe`

### v1.2.0
- **Detection region spinboxes:** X, Y, W, H inputs in the Overlay tab let you set the debuff scan region manually — no tool required
- **"Draw Region on Screen" button:** Drag a box over the debuff strip and the spinboxes fill automatically; hit Apply to save
- **gui.exe icon:** Now uses the Splendid Dark Grenade image as the application icon
- **Frozen path fix:** `gui.exe` now correctly finds `config.yaml` and `rosters/` next to the executable on any machine

### v1.1.0
- **Auto-detection:** Optional OpenCV-based grenade detection scans the boss debuff bar automatically. When the Dark Grenade or Splendid Dark Grenade icon is detected, the timer starts at 20s or 25s respectively — no manual confirm needed.
- **Visual region selector:** "Set Detection Region" button in the Overlay tab opens a full-screen drag-to-select tool. Draw a box over the boss debuff strip and coordinates are saved automatically, relative to the Lost Ark window (works on any monitor setup).
- **Lost Ark window auto-detection:** Detection coordinates are stored relative to the Lost Ark window position via `pywin32`, so they remain correct regardless of which monitor the game is on.
- **Auto-detection toggle:** Enable/disable in the Overlay tab — off by default so it doesn't affect performance on weaker machines.
- Manual F9 confirm and F10 miss still work at all times as fallback.
- New dependencies: `opencv-python`, `pywin32`, `mss`

### v1.0.0
- Initial release
- PyQt5 tabbed config GUI (Roster, Rotation, Hotkeys, Overlay)
- Always-on-top overlay HUD with countdown bar
- Live Apply: push config changes to running bot without restart
- Overlay and GUI window positions auto-save on drag/move
- Hotkey rebinding via click-to-capture UI
- Headless terminal mode via `main.py`
- Standalone `gui.exe` build
