import json
from pathlib import Path
from atlas.map_builder import build_atlas

territories_path = Path("data/territories.json")

def patch_royal_hungary():
    if not territories_path.exists():
        print("X Error: data/territories.json not found.")
        return

    with open(territories_path, "r", encoding="utf-8") as f:
        territories = json.load(f)

    # 1. Clean slate: Remove any existing Royal Hungary versions
    banned_ids = {"royal_hungary", "royal_hungary_early", "royal_hungary_late"}
    territories = [t for t in territories if t["id"] not in banned_ids]

    # 2. Define the shrinking phases
    # Phase 1: Full extent before Uyvar Eyalet (1663)
    # Phase 2: Shrunken extent after Uyvar Eyalet establishment
    hungary_phases = [
        {
            "id": "royal_hungary_1526",
            "name": "Royal Hungary",
            "power": "Habsburg Monarchy",
            "relation": "neighbour",
            "start": 1526,
            "end": 1662,
            "capital": "Bratislava",
            "status": "Habsburg territory",
            "summary": "Full extent of Royal Hungary before the establishment of the Uyvar Eyalet.",
            "geometry": [
                [17.15, 45.42], [17.35, 45.42], [17.88, 46.2], [18.3, 47.05], 
                [18.82, 47.72], [19.55, 49.55], [18.5, 49.6], [17.2, 48.6], 
                [17.15, 46.6], [17.15, 45.42]
            ]
        },
        {
            "id": "royal_hungary_1663",
            "name": "Royal Hungary",
            "power": "Habsburg Monarchy",
            "relation": "neighbour",
            "start": 1663,
            "end": 1685,
            "capital": "Bratislava",
            "status": "Habsburg territory (reduced)",
            "summary": "Reduced Royal Hungary after the loss of territory to the Uyvar Eyalet.",
            "geometry": [
                [18.5, 49.6], [19.55, 49.55], [18.82, 47.72], 
                [18.85, 47.85], [18.3, 48.05], [17.2, 48.6], [18.5, 49.6]
            ]
        }
    ]

    territories.extend(hungary_phases)

    with open(territories_path, "w", encoding="utf-8") as f:
        json.dump(territories, f, ensure_ascii=False, indent=2)

    print("✓ Successfully patched Royal Hungary with dynamic shrinking phases.")
    
    # Re-compile
    print("\nRe-compiling interactive atlas visual layers...")
    try:
        build_atlas("ottoman_europe_atlas.html")
        print("✓ Atlas rebuilt.")
    except Exception as e:
        print(f"X Build failed: {e}")

if __name__ == "__main__":
    patch_royal_hungary()
    