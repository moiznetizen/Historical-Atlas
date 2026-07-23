import json
from pathlib import Path
from atlas.map_builder import build_atlas

territories_path = Path("data/territories.json")

# Updated North African Eyalets with precise coordinates
north_africa_provinces = [
    {
        "id": "eyalet_algiers",
        "name": "Eyalet of Algiers",
        "power": "Ottoman Province",
        "relation": "direct",
        "start": 1533,
        "end": 1830,
        "capital": "Algiers",
        "status": "Barbary Coast province",
        "summary": "Extended westward to the Moroccan border.",
        # Ras Kebdana (-2.42, 35.14) to Algiers
        "geometry": [[-2.42, 35.14], [4.0, 37.0], [4.0, 34.0], [-2.42, 33.0], [-2.42, 35.14]]
    },
    {
        "id": "eyalet_egypt",
        "name": "Eyalet of Egypt",
        "power": "Ottoman Province",
        "relation": "direct",
        "start": 1517,
        "end": 1867,
        "capital": "Cairo",
        "status": "Ottoman province",
        "summary": "Western border anchored at Sallum.",
        # Sallum (25.16, 31.55) through Nile and Sudan
        "geometry": [[25.16, 31.55], [35.0, 31.55], [36.0, 22.0], [33.0, 15.0], [25.16, 15.0], [25.16, 31.55]]
    }
]

def patch_provinces():
    if territories_path.exists():
        with open(territories_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Remove old versions if they exist to prevent duplication
        data = [t for t in data if t["id"] not in ["eyalet_algiers", "eyalet_egypt"]]
        data.extend(north_africa_provinces)
        
        with open(territories_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("✓ Eyalet boundaries updated with Ras Kebdana and Sallum anchors.")
        
        build_atlas("ottoman_europe_atlas.html")
        print("✓ Atlas rebuilt.")

if __name__ == "__main__":
    patch_provinces()
    