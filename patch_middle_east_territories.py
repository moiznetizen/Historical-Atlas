import json
from pathlib import Path
from atlas.map_builder import build_atlas

territories_path = Path("data/territories.json")

def patch_middle_east():
    if not territories_path.exists():
        print("X Error: data/territories.json not found.")
        return

    with open(territories_path, "r", encoding="utf-8") as f:
        territories = json.load(f)

    # 1. Clean slate: Remove any existing Middle East/Caucasus entries to prevent duplicates
    banned_ids = {"eyalet_baghdad", "eyalet_tabriz", "eyalet_yerevan", "caucasus_front"}
    territories = [t for t in territories if t["id"] not in banned_ids]

    # 2. Define sequential expansion/contraction phases
    me_phases = [
        {
            "id": "eyalet_baghdad",
            "name": "Eyalet of Baghdad",
            "power": "Ottoman Province",
            "relation": "direct",
            "start": 1534,
            "end": 1622,
            "capital": "Baghdad",
            "summary": "Incorporated after 1534; lost to Safavids in 1623.",
            "geometry": [[43.0, 31.0], [45.0, 35.0], [47.0, 33.0], [45.0, 29.0], [43.0, 31.0]]
        },
        {
            "id": "eyalet_baghdad_recovered",
            "name": "Eyalet of Baghdad",
            "power": "Ottoman Province",
            "relation": "direct",
            "start": 1638,
            "end": 1685,
            "capital": "Baghdad",
            "summary": "Permanently recovered after the 1638 Siege.",
            "geometry": [[43.0, 31.0], [45.0, 35.0], [47.0, 33.0], [45.0, 29.0], [43.0, 31.0]]
        },
        {
            "id": "eyalet_tabriz",
            "name": "Ottoman Tabriz Zone",
            "power": "Ottoman Province",
            "relation": "temporary",
            "start": 1585,
            "end": 1603,
            "capital": "Tabriz",
            "summary": "Temporary occupation during the height of the 1590 Treaty gains.",
            "geometry": [[45.0, 37.0], [48.0, 39.0], [49.0, 37.0], [47.0, 35.0], [45.0, 37.0]]
        }
    ]

    territories.extend(me_phases)

    with open(territories_path, "w", encoding="utf-8") as f:
        json.dump(territories, f, ensure_ascii=False, indent=2)

    print("✓ Successfully patched Middle East/Caucasus territories.")
    build_atlas("ottoman_europe_atlas.html")

if __name__ == "__main__":
    patch_middle_east()