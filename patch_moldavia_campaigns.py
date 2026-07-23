import json
from pathlib import Path

battles_path = Path("data/battles.json")
events_path = Path("data/events.json")

# Coordinates calculated historically for precision on your atlas canvas:
# Chilia: 45.46N, 29.27E | Vaslui: 46.63N, 27.73E | Valea Albă: 46.96N, 26.56E
# Neamț Fortress: 47.21N, 26.34E | Suceava (1538): 47.64N, 26.25E | Roșcani/Cahul (1574): 45.90N, 28.20E

new_moldavian_battles = [
    {
        "name": "Attack on Chilia (Kilia)",
        "date": "1420",
        "year": 1420,
        "lat": 45.46,
        "lon": 29.27,
        "kind": "siege",
        "commanders": "Ottoman naval/land forces; Moldavian defenders under Alexandru cel Bun",
        "result": "Ottoman defeat / failed siege",
        "importance": "First recorded Ottoman military attempt to capture a stronghold in Moldavia.",
        "casualties": "Not securely recorded."
    },
    {"name": "Sack of Kyiv", "date": "1482", "year": 1482, "lat": 50.45, "lon": 30.52, "kind": "land", "commanders": "Mengli Giray", "result": "Crimean victory", "importance": "Major Crimean victory and sack of Kyiv.", "casualties": "Not recorded"},
    
    {"name": "Great Crimean Raid on Moscow", "date": "1521", "year": 1521, "lat": 55.75, "lon": 37.61, "kind": "land", "commanders": "Mehmed I Giray", "result": "Crimean victory", "importance": "Major raid, forces reached Moscow outskirts.", "casualties": "Heavy"},
    {"name": "Battle of Sudbishchi", "date": "1555", "year": 1555, "lat": 53.00, "lon": 37.00, "kind": "land", "commanders": "Devlet I Giray vs Russians", "result": "Russian victory", "importance": "Russian forces defeated Crimean raiders.", "casualties": "Heavy on both sides"},
    {"name": "Burning of Moscow", "date": "1571", "year": 1571, "lat": 55.75, "lon": 37.61, "kind": "land", "commanders": "Devlet I Giray", "result": "Crimean victory", "importance": "Devlet Giray burns Moscow; massive enslavement.", "casualties": "Not recorded"},
    {"name": "Battle near Moscow", "date": "1591", "year": 1591, "lat": 55.75, "lon": 37.61, "kind": "land", "commanders": "Ğazı II Giray", "result": "Russian victory", "importance": "Khan forced to retreat.", "casualties": "Not recorded"},
    {"name": "First Siege of Chyhyryn", "date": "1677", "year": 1677, "lat": 49.07, "lon": 32.65, "kind": "siege", "commanders": "Ottoman vs Russian-Cossack", "result": "Ottoman defeat", "importance": "Russians held the fortress.", "casualties": "Not recorded"},
    {"name": "Chyhyryn Campaign", "date": "1678", "year": 1678, "lat": 49.07, "lon": 32.65, "kind": "siege", "commanders": "Kara Mustafa", "result": "Ottoman victory", "importance": "Chyhyryn captured and destroyed.", "casualties": "Not recorded"},
    {
        "name": "Battle of Vaslui (Podul Înalt)",
        "date": "10 January 1475",
        "year": 1475,
        "lat": 46.63,
        "lon": 27.73,
        "kind": "land",
        "commanders": "Hadım Suleiman Pasha; Stephen the Great (Ștefan cel Mare)",
        "result": "Decisive Moldavian victory",
        "importance": "One of the greatest Christian tactical victories against Ottoman forces in the 15th century.",
        "casualties": "Extremely heavy Ottoman casualties."
    },
    {
        "name": "Battle of Valea Albă (Războieni)",
        "date": "26 July 1476",
        "year": 1476,
        "lat": 46.96,
        "lon": 26.56,
        "kind": "land",
        "commanders": "Mehmed II; Stephen the Great",
        "result": "Ottoman tactical victory",
        "importance": "Mehmed II defeated the main Moldavian field army but failed to permanently subdue the principality.",
        "casualties": "Severe losses on both sides."
    },
    {
        "name": "Siege of Neamț Fortress",
        "date": "August 1476",
        "year": 1476,
        "lat": 47.21,
        "lon": 26.34,
        "kind": "siege",
        "commanders": "Mehmed II; Moldavian garrison defenders",
        "result": "Ottoman failure / fortress held",
        "importance": "The fortress held out successfully, forcing Mehmed II to withdraw due to supply shortages and plague.",
        "casualties": "Not securely recorded."
    },
    {
        "name": "Suleiman's Moldavian Campaign (Capture of Suceava)",
        "date": "September 1538",
        "year": 1538,
        "lat": 47.64,
        "lon": 26.25,
        "kind": "siege",
        "commanders": "Suleiman the Magnificent; Petru Rareș (deposed)",
        "result": "Decisive Ottoman victory",
        "importance": "Suleiman captured the capital, annexed southern Bessarabia (Tighina/Bender), and firmly asserted vassal tracking over foreign policy.",
        "casualties": "Minimal battlefield combat losses; highly strategic campaign."
    },
    {
        "name": "Moldavian Campaign (Battle of Roșcani)",
        "date": "June 1574",
        "year": 1574,
        "lat": 45.90,
        "lon": 28.20,
        "kind": "land",
        "commanders": "Ottoman-Wallachian coalition forces; John III the Terrible (Ioan Vodă cel Cumplit)",
        "result": "Ottoman victory",
        "importance": "Suppressed a major anti-Ottoman rebellion and reasserted sovereign provincial tribute authority.",
        "casualties": "Heavy Moldavian rebel forces wiped out."
    }
]

new_moldavian_timeline_events = [
    {
        "year": 1475,
        "title": "Battle of Vaslui",
        "body": "Stephen the Great crushes a much larger Ottoman army in Moldavia, delaying direct subjection.",
        "sultan": "Mehmed II",
        "population": "Balkan and Danubian flashpoints",
        "largest_rival": "Hungary and Moldavia"
    },
    {
        "year": 1538,
        "title": "Suleiman subdues Moldavia",
        "body": "Suleiman the Magnificent invades Moldavia, takes Suceava, deposes Petru Rareș, and annexes Bender/Tighina.",
        "sultan": "Suleiman I",
        "population": "Consolidated northern vassal system",
        "largest_rival": "Habsburg Monarchy"
    },
    {"year": 1482, "title": "Sack of Kyiv", "body": "Mengli Giray leads a major Crimean victory against Muscovy.", "sultan": "Bayezid II"},
    {"year": 1521, "title": "Great Crimean Raid", "body": "Major Crimean victory reaching the outskirts of Moscow.", "sultan": "Suleiman I"},
    {"year": 1571, "title": "Burning of Moscow", "body": "Devlet I Giray burns Moscow, leading to massive enslavement.", "sultan": "Selim II"},
    {"year": 1678, "title": "Chyhyryn Campaign", "body": "Kara Mustafa captures and destroys Chyhyryn.", "sultan": "Mehmed IV"},
    {"year": 1681, "title": "Treaty of Bakhchisarai", "body": "Ottoman–Russian peace confirming control of southern Right-bank Ukraine.", "sultan": "Mehmed IV"}
]

# 1. Update data/battles.json safely without duplicate overlays
if battles_path.exists():
    with open(battles_path, "r", encoding="utf-8") as f:
        existing_battles = json.load(f)
    
    # Avoid overlapping entries by tracking battle name signatures
    known_names = {b["name"] for b in existing_battles}
    added_battles = 0
    for b in new_moldavian_battles:
        if b["name"] not in known_names:
            existing_battles.append(b)
            added_battles += 1
            
    with open(battles_path, "w", encoding="utf-8") as f:
        json.dump(existing_battles, f, ensure_ascii=False, indent=2)
    print(f"✓ successfully injected {added_battles} new interactive battle tracking layers into battles.json.")

# 2. Update data/events.json timeline milestones safely
if events_path.exists():
    with open(events_path, "r", encoding="utf-8") as f:
        existing_events = json.load(f)
        
    known_years_titles = {(e["year"], e["title"]) for e in existing_events}
    added_events = 0
    for e in new_moldavian_timeline_events:
        if (e["year"], e["title"]) not in known_years_titles:
            existing_events.append(e)
            added_events += 1
            
    # Keep the chronology perfectly ordered for the slider engine mechanics
    existing_events.sort(key=lambda x: x["year"])
    
    with open(events_path, "w", encoding="utf-8") as f:
        json.dump(existing_events, f, ensure_ascii=False, indent=2)
    print(f"✓ successfully added {added_events} major Moldavian political markers to events.json.")

# 3. Trigger build layout asset compiler
print("\nRe-compiling interactive atlas visual layers...")
try:
    from atlas.map_builder import build_atlas
    build_atlas("ottoman_europe_atlas.html")
    print("✓ Complete! All Moldavian campaign milestones are successfully deployed in production code.")
except Exception as e:
    print(f"X Compilation mistake: {e}")