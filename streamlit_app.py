"""Streamlit Cloud entry point."""
import sys
import pathlib

ROOT     = pathlib.Path(__file__).resolve().parent
FRONTEND = ROOT / "frontend"

# Add BOTH paths here - before anything else runs
for _p in [str(ROOT), str(FRONTEND)]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

import runpy
runpy.run_path(str(FRONTEND / "app.py"), run_name="__main__")