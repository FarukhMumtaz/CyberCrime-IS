"""Frontend package"""
import sys
import pathlib

# Ensure project root is on path when frontend is imported
_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))