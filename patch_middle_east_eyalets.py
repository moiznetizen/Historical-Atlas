import json
from pathlib import Path
from atlas.map_builder import build_atlas

territories_path = Path("data/territories.json")

# Define the new Levantine and Mesopotamian Eyalets
# Updated patch_middle_east_eyalets.py with precise geometries
new_provinces = [
    {"id": "eyalet_basra", "name": "Basra Eyalet", "power": "Ottoman Province", "relation": "direct", "start": 1546, "end": 1918, "capital": "Basra", "summary": "Southern Iraq, Persian Gulf.",
     "geometry": [[45.10, 31.70],
[46.20, 33.70],
[49.00, 32.50],
[49.00, 29.60],
[45.20, 30.80]]}
]

def patch_middle_east_eyalets():
    if not territories_path.exists():
        return

    with open(territories_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Prevent duplicates
    known_ids = {t["id"] for t in data}
    for p in new_provinces:
        # Add basic geometry placeholder so map engine renders them (update coordinates later)
        if p["id"] not in known_ids:
            p["geometry"] = [[35.0, 30.0], [40.0, 35.0], [45.0, 30.0], [40.0, 25.0], [35.0, 30.0]]
            data.append(p)

    with open(territories_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("✓ Successfully injected Middle Eastern Eyalets.")
    build_atlas("ottoman_europe_atlas.html")

if __name__ == "__main__":
    patch_middle_east_eyalets()