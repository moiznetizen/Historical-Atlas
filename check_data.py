import json
from pathlib import Path

path = Path("data/territories.json")
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

for i, item in enumerate(data):
    if not isinstance(item, dict):
        print(f"Error found at index {i} in territories.json!")
        print(f"The item is a {type(item)}, but expected a dictionary.")
        print(f"Content: {item}")
        