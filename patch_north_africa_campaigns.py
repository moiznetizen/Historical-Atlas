import json
from pathlib import Path
from atlas.map_builder import build_atlas

battles_path = Path("data/battles.json")

new_battles = [
    # ... (insert the JSON objects from step 1 here)
]

if battles_path.exists():
    with open(battles_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    known_names = {b["name"] for b in data}
    for b in new_battles:
        if b["name"] not in known_names:
            data.append(b)
            
    with open(battles_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("✓ Successfully injected new North African sieges and battles.")
    
    # Re-compile the atlas
    build_atlas("ottoman_europe_atlas.html")
    print("✓ Atlas rebuilt.")
    