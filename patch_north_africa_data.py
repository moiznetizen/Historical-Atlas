import json
from pathlib import Path
from atlas.map_builder import build_atlas

# Paths to data files
battles_path = Path("data/battles.json")
events_path = Path("data/events.json")

def patch_north_africa():
    # 1. Define North African Battles
    new_battles = [
        {"name": "Battle of Ridaniya", "date": "1517", "year": 1517, "lat": 30.06, "lon": 31.25, "kind": "land", "commanders": "Selim I vs Tuman bay II", "result": "Ottoman victory", "importance": "Mamluk Sultanate destroyed; Egypt annexed.", "casualties": "Heavy Mamluk losses"},
        
        {"name": "Battle of Wadi al-Makhazin", "date": "1578", "year": 1578, "lat": 35.00, "lon": -6.00, "kind": "land", "commanders": "Ottoman-backed Saadi vs Portugal", "result": "Moroccan/Ottoman-backed victory", "importance": "Portugal defeated; Saadi independence secured.", "casualties": "High"}
    ]

    # 2. Define North African Events
    new_events = [
        {"year": 1516, "title": "Capture of Algiers", "body": "Ottoman foothold established in the Maghreb.", "sultan": "Selim I"},
        {"year": 1529, "title": "Capture of Peñón of Algiers", "body": "Spanish fortress taken by Hayreddin Barbarossa.", "sultan": "Suleiman I"},
        {"year": 1534, "title": "Capture of Tunis", "body": "Temporary Ottoman occupation of the city.", "sultan": "Suleiman I"},
        {"year": 1535, "title": "Conquest of Tunis", "body": "Spanish reconquest of Tunis.", "sultan": "Suleiman I"},
        {"year": 1551, "title": "Capture of Tripoli", "body": "Tripoli annexed into the Ottoman Empire.", "sultan": "Suleiman I"},
        {"year": 1574, "title": "Ottoman Reconquest of Tunis", "body": "Permanent annexation of Tunisia.", "sultan": "Selim II"}
    ]

    # Update Battles
    with open(battles_path, "r+", encoding="utf-8") as f:
        data = json.load(f)
        known = {b["name"] for b in data}
        for b in new_battles:
            if b["name"] not in known:
                data.append(b)
        f.seek(0)
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Update Events
    with open(events_path, "r+", encoding="utf-8") as f:
        data = json.load(f)
        known = {(e["year"], e["title"]) for e in data}
        for e in new_events:
            if (e["year"], e["title"]) not in known:
                data.append(e)
        data.sort(key=lambda x: x["year"])
        f.seek(0)
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("✓ North African battles and events injected.")
    
    # Rebuild
    build_atlas("ottoman_europe_atlas.html")
    print("✓ Atlas rebuilt.")

if __name__ == "__main__":
    patch_north_africa()