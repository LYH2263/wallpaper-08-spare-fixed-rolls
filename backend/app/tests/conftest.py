import os
import sys
import tempfile
from pathlib import Path

# Isolate the test database and make the app package importable before any app import.
os.environ["DATA_DIR"] = tempfile.mkdtemp(prefix="wallpaper-test-")
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
