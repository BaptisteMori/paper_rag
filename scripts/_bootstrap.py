"""Prepare Django env for scripts outside of src/

To bee imported first : `import _bootstrap  # noqa: F401`
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")
sys.path.insert(0, os.environ.get("SRC", str(ROOT / "src")))
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "paper_rag.settings")

import django  # noqa: E402

django.setup()  # indispensable avant d'importer un modèle
