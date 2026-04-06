"""
gui.py - Dark Rotation Bot GUI entry point

Usage:
    python gui.py
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from modules.gui_app import ConfigApp

# When frozen as .exe, use the exe's directory. When running as script, use this file's directory.
BASE_DIR = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else os.path.dirname(os.path.abspath(__file__))


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    config_path = os.path.join(BASE_DIR, "config.yaml")
    window = ConfigApp(config_path)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
