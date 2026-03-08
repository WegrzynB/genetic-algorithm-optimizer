# uruchamia całą aplikację (główny skrypt)
# `py scripts\run_gui.py`

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ga_optimizer.gui.app import run_app

if __name__ == "__main__":
    run_app()