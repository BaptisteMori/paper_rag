#!/usr/bin/env python
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")
sys.path.insert(0, os.environ.get("SRC", str(ROOT / "src")))
sys.path.insert(0, str(ROOT))  # pour le package migrations/
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "paper_rag.settings")

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
