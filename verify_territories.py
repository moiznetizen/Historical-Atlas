import json
with open("data/territories.json", "r") as f:
    data = json.load(f)
    ids = [t['id'] for t in data if 'poland' in t['id'] or 'lithuania' in t['id']]
    print(f"Found territories: {ids}")