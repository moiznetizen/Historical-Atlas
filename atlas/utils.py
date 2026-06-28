"""Shared helpers for atlas data loading."""

from __future__ import annotations

import json
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_json(filename):
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))
