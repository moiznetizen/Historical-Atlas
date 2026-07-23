import json
from pathlib import Path
from atlas.map_builder import build_atlas

territories_path = Path("data/territories.json")

if territories_path.exists():
    with open(territories_path, "r", encoding="utf-8") as f:
        territories = json.load(f)
    
    # 1. Clear out ANY previous version of rumelia data
    territories = [t for t in territories if not t["id"].startswith("rumelia")]
    
    # 2. Define sequential stages with UNIQUE IDs
    dynamic_rumelia = [
        {"id": "rumelia_1362", "name": "Rumelia Eyalet", "power": "Ottoman Province", "relation": "direct", "start": 1362, "end": 1384, "capital": "Edirne", "summary": "Thrace Core", "geometry": [[25.50, 40.20], [29.10, 40.60], [29.45, 41.50], [28.85, 42.15], [27.20, 41.80], [25.50, 40.20]]},
        {"id": "rumelia_1385", "name": "Rumelia Eyalet", "power": "Ottoman Province", "relation": "direct", "start": 1385, "end": 1396, "capital": "Sofia", "summary": "Balkan expansion", "geometry": [[21.20, 41.10], [25.50, 40.20], [29.10, 40.60], [29.45, 41.50], [28.85, 42.15], [28.30, 43.20], [27.55, 43.75], [24.85, 44.15], [21.40, 43.40], [21.20, 41.10]]},
        {"id": "rumelia_1397", "name": "Rumelia Eyalet", "power": "Ottoman Province", "relation": "direct", "start": 1397, "end": 1459, "capital": "Sofia", "summary": "Thessaly expansion", "geometry": [[20.20, 39.10], [21.55, 38.10], [24.75, 37.95], [24.95, 39.25], [29.10, 40.60], [29.45, 41.50], [28.85, 42.15], [28.30, 43.20], [27.55, 43.75], [24.85, 44.15], [21.40, 43.40], [20.20, 39.10]]},
        {"id": "rumelia_1460", "name": "Rumelia Eyalet", "power": "Ottoman Province", "relation": "direct", "start": 1460, "end": 1867, "capital": "Sofia", "summary": "Peak consolidation", "geometry": [[18.35, 42.28], [18.95, 41.80], [19.45, 40.45], [20.55, 39.35], [21.55, 38.25], [22.40, 36.40], [23.10, 36.30], [23.60, 37.95], [24.75, 37.95], [24.95, 39.25], [26.30, 40.20], [29.10, 40.60], [29.45, 41.50], [28.85, 42.05], [28.30, 43.20], [27.55, 43.75], [26.40, 44.10], [24.85, 44.15], [23.10, 44.05], [21.80, 44.55], [20.55, 45.10], [19.20, 44.88], [18.35, 44.05], [18.35, 42.28]]}
    ]
    
    territories.extend(dynamic_rumelia)
    
    with open(territories_path, "w", encoding="utf-8") as f:
        json.dump(territories, f, ensure_ascii=False, indent=2)
    
    print("✓ Patched Rumelia with unique sequential IDs.")
    build_atlas("ottoman_europe_atlas.html")
else:
    print("X territories.json not found.")
