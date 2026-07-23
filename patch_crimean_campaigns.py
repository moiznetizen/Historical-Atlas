import json
from pathlib import Path
from atlas.map_builder import build_atlas

battles_path = Path("data/battles.json")
events_path = Path("data/events.json")

# Crimean/Russian campaign battles
new_crimean_battles = [
    {"name": "Sack of Kyiv", "date": "1482", "year": 1482, "lat": 50.45, "lon": 30.52, "kind": "land", "commanders": "Mengli Giray", "result": "Crimean victory", "importance": "Major Crimean victory and sack of Kyiv.", "casualties": "Not recorded"},
    {"name": "Great Crimean Raid on Moscow", "date": "1521", "year": 1521, "lat": 55.75, "lon": 37.61, "kind": "land", "commanders": "Mehmed I Giray", "result": "Crimean victory", "importance": "Major raid, forces reached Moscow outskirts.", "casualties": "Heavy"},
    {"name": "Battle of Sudbishchi", "date": "1555", "year": 1555, "lat": 53.00, "lon": 37.00, "kind": "land", "commanders": "Devlet I Giray vs Russians", "result": "Russian victory", "importance": "Russian forces defeated Crimean raiders.", "casualties": "Heavy on both sides"},
    {"name": "Burning of Moscow", "date": "1571", "year": 1571, "lat": 55.75, "lon": 37.61, "kind": "land", "commanders": "Devlet I Giray", "result": "Crimean victory", "importance": "Devlet Giray burns Moscow; massive enslavement.", "casualties": "Not recorded"},
    {"name": "Battle near Moscow", "date": "1591", "year": 1591, "lat": 55.75, "lon": 37.61, "kind": "land", "commanders": "Ğazı II Giray", "result": "Russian victory", "importance": "Khan forced to retreat.", "casualties": "Not recorded"},
    {"name": "First Siege of Chyhyryn", "date": "1677", "year": 1677, "lat": 49.07, "lon": 32.65, "kind": "siege", "commanders": "Ottoman vs Russian-Cossack", "result": "Ottoman defeat", "importance": "Russians held the fortress.", "casualties": "Not recorded"},
    {"name": "Chyhyryn Campaign", "date": "1678", "year": 1678, "lat": 49.07, "lon": 32.65, "kind": "siege", "commanders": "Kara Mustafa", "result": "Ottoman victory", "importance": "Chyhyryn captured and destroyed.", "casualties": "Not recorded"}
]

# Crimean/Russian historical timeline events
new_crimean_events = [
    {"year": 1482, "title": "Sack of Kyiv", "body": "Mengli Giray leads a major Crimean victory against Muscovy.", "sultan": "Bayezid II"},
    {"year": 1521, "title": "Great Crimean Raid", "body": "Major Crimean victory reaching the outskirts of Moscow.", "sultan": "Suleiman I"},
    {"year": 1571, "title": "Burning of Moscow", "body": "Devlet I Giray burns Moscow, leading to massive enslavement.", "sultan": "Selim II"},
    {"year": 1678, "title": "Chyhyryn Campaign", "body": "Kara Mustafa captures and destroys Chyhyryn.", "sultan": "Mehmed IV"},
    {"year": 1681, "title": "Treaty of Bakhchisarai", "body": "Ottoman–Russian peace confirming control of southern Right-bank Ukraine.", "sultan": "Mehmed IV"}
]

# 1. Update battles.json
if battles_path.exists():
    with open(battles_path, "r", encoding="utf-8") as f:
        existing_battles = json.load(f)
    known = {b["name"] for b in existing_battles}
    added = 0
    for b in new_crimean_battles:
        if b["name"] not in known:
            existing_battles.append(b)
            added += 1
    with open(battles_path, "w", encoding="utf-8") as f:
        json.dump(existing_battles, f, ensure_ascii=False, indent=2)
    print(f"✓ Injected {added} new battle layers.")

# 2. Update events.json
if events_path.exists():
    with open(events_path, "r", encoding="utf-8") as f:
        existing_events = json.load(f)
    known_events = {(e["year"], e["title"]) for e in existing_events}
    added_events = 0
    for e in new_crimean_events:
        if (e["year"], e["title"]) not in known_events:
            existing_events.append(e)
            added_events += 1
    existing_events.sort(key=lambda x: x["year"])
    with open(events_path, "w", encoding="utf-8") as f:
        json.dump(existing_events, f, ensure_ascii=False, indent=2)
    print(f"✓ Injected {added_events} new timeline markers.")

# 3. Rebuild Atlas
print("\nRe-compiling interactive atlas visual layers...")
try:
    build_atlas("ottoman_europe_atlas.html")
    print("✓ Success! Atlas rebuilt.")
except Exception as e:
    print(f"X Compilation error: {e}")