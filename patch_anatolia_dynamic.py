import json
from pathlib import Path

battles_path = Path("data/battles.json")
events_path = Path("data/events.json")
territories_path = Path("data/territories.json")

# ==============================================================================
# 1. NEW ANATOLIAN ENGAGEMENTS & ANNEXATIONS (DATA DEFINITIONS)
# ==============================================================================

new_anatolia_battles = [
    {"name": "Acquisition of the Hamid Beylik", "date": "1374", "year": 1374, "lat": 37.83, "lon": 30.52, "kind": "treaty", "commanders": "Murad I; Kemaleddin Hüseyin Bey", "result": "Territory purchased", "importance": "Expanded Ottoman control in southwestern Anatolia peacefully via purchase.", "casualties": "None."},
    {"name": "Union with Germiyan Beylik", "date": "1381", "year": 1381, "lat": 39.42, "lon": 29.98, "kind": "treaty", "commanders": "Bayezid I (Marriage); Suleyman Shah of Germiyan", "result": "Dynastic annexation", "importance": "Brought major central Anatolian territories under Ottoman control via dynastic marriage.", "casualties": "None."},
    {"name": "Annexation of Aydın & Saruhan", "date": "1390", "year": 1390, "lat": 38.35, "lon": 27.84, "kind": "expedition", "commanders": "Bayezid I", "result": "Western Beyliks annexed", "importance": "Unified the rich Aegean maritime principalities under direct Ottoman rule.", "casualties": "Minimal."},
    {"name": "Battle of Kırkdilim", "date": "1391", "year": 1391, "lat": 40.62, "lon": 34.85, "kind": "land", "commanders": "Bayezid I; Kadı Burhaneddin", "result": "Ottoman defeat", "importance": "Fought against the local rulers of Sivas and northern Anatolian coalitions.", "casualties": "Moderate."},
    {"name": "Battle of Ankara", "date": "28 July 1402", "year": 1402, "lat": 40.03, "lon": 32.86, "kind": "land", "commanders": "Bayezid I (Captured); Timur (Tamerlane)", "result": "Decisive Timurid victory", "importance": "Catastrophic defeat causing the collapse of first-wave Anatolian unification; launched the 11-year Ottoman Interregnum.", "casualties": "Extremely heavy on both sides."},
    {"name": "Siege of Smyrna", "date": "December 1402", "year": 1402, "lat": 38.42, "lon": 27.14, "kind": "siege", "commanders": "Timur; Knights Hospitaller defenders", "result": "Timurid victory", "importance": "Timur stormed the Christian coastal fortress, dismantling the last crusader outpost in Western Anatolia.", "casualties": "Garrison executed."},
    {"name": "Fall of Trebizond", "date": "15 August 1461", "year": 1461, "lat": 41.00, "lon": 39.72, "kind": "siege", "commanders": "Mehmed II; David Komnenos", "result": "Decisive Ottoman victory", "importance": "Annexed the Empire of Trebizond, completing complete Ottoman dominance over the Anatolian Black Sea rim.", "casualties": "Surrender terms negotiated."},
    {"name": "Battle of Otlukbeli", "date": "11 August 1473", "year": 1473, "lat": 40.12, "lon": 40.08, "kind": "land", "commanders": "Mehmed II; Uzun Hasan (Aq Qoyunlu)", "result": "Decisive Ottoman victory", "importance": "Shattered the Aq Qoyunlu coalition, securely cementing gun-powder supremacy over eastern Anatolia.", "casualties": "Heavy Persian/Turkoman losses."},
    {"name": "Battle of Chaldiran", "date": "23 August 1514", "year": 1514, "lat": 39.08, "lon": 44.25, "kind": "land", "commanders": "Selim I; Shah Ismail I (Safavid Empire)", "result": "Decisive Ottoman victory", "importance": "Halted Safavid western expansion, secured easternmost Anatolia, and unlocked northern Mesopotamia.", "casualties": "Severe Safavid losses."},
    {"name": "Battle of Turnadağ", "date": "13 June 1515", "year": 1515, "lat": 37.40, "lon": 36.32, "kind": "land", "commanders": "Hadım Sinan Pasha; Bozkurt of Dulkadir", "result": "Ottoman victory", "importance": "Annexed the Dulkadir Beylik, ending the last independent Anatolian buffer state and completing absolute political unification.", "casualties": "Dulkadir dynastic line ended."}
]

new_anatolia_events = [
    {"year": 1402, "title": "Battle of Ankara & Collapse", "body": "Timur crushes Bayezid I. The first Anatolian unification fractures as old beyliks re-assert independence during the Ottoman Interregnum.", "sultan": "Bayezid I", "population": "Empire fractured in civil war", "largest_rival": "Timurid Empire"},
    {"year": 1473, "title": "Battle of Otlukbeli", "body": "Mehmed II uses modern artillery to defeat Uzun Hasan, extending absolute hegemony deep into the eastern Anatolian highlands.", "sultan": "Mehmed II", "population": "Eastern border consolidated", "largest_rival": "Aq Qoyunlu Confederation"},
    {"year": 1515, "title": "Political Unification of Anatolia", "body": "Following victory at Turnadağ, the last major independent Anatolian beylik is formally eliminated, bringing Asia Minor under total Ottoman administration.", "sultan": "Selim I", "population": "Unified imperial heartland", "largest_rival": "Safavid Persia"}
]

# ==============================================================================
# 2. FILE UPDATE IMPLEMENTATION
# ==============================================================================

# Append battles/treaties safely
if battles_path.exists():
    with open(battles_path, "r", encoding="utf-8") as f:
        battles = json.load(f)
    known = {b["name"] for b in battles}
    added = 0
    for nb in new_anatolia_battles:
        if nb["name"] not in known:
            battles.append(nb)
            added += 1
    with open(battles_path, "w", encoding="utf-8") as f:
        json.dump(battles, f, ensure_ascii=False, indent=2)
    print(f"✓ Injected {added} new Anatolian strategic battles & beylik treaties.")

# Append timeline event triggers safely
if events_path.exists():
    with open(events_path, "r", encoding="utf-8") as f:
        events = json.load(f)
    known_ev = {(e["year"], e["title"]) for e in events}
    added_ev = 0
    for ne in new_anatolia_events:
        if (ne["year"], ne["title"]) not in known_ev:
            events.append(ne)
            added_ev += 1
    events.sort(key=lambda x: x["year"])
    with open(events_path, "w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=2)
    print(f"✓ Synced {added_ev} timeline milestone indicators into chronological sequence.")

# ==============================================================================
# 3. DYNAMIC CUMULATIVE GEOMETRY GENERATION FOR ANATOLIA (ID: "anatolia_core")
# ==============================================================================
if territories_path.exists():
    with open(territories_path, "r", encoding="utf-8") as f:
        territories = json.load(f)
        
    # Purge old standalone single-state Anatolian entries if present to protect timeline integrity
    territories = [t for t in territories if t["id"] != "anatolia_core"]
    
    dynamic_anatolia_sequence = [
        {
            "id": "anatolia_core",
            "name": "Ottoman Anatolia (Early Expansion)",
            "power": "Ottoman Province",
            "relation": "direct",
            "start": 1352,
            "end": 1389,
            "capital": "Bursa",
            "status": "Core Northwestern Beylik Foundation",
            "held": "1352-Present",
            "summary": "Initial territorial footprint focused on northwestern Asia Minor, absorbing the Hamid and Germiyan properties via dynamic treaties and peaceful unions.",
            "geometry": [[26.00, 39.50], [30.50, 40.50], [31.50, 38.50], [29.00, 37.00], [26.00, 39.50]]
        },
        {
            "id": "anatolia_core",
            "name": "Ottoman Anatolia (First Unification)",
            "power": "Ottoman Province",
            "relation": "direct",
            "start": 1390,
            "end": 1401,
            "capital": "Bursa",
            "status": "Western & Central Hegemony",
            "held": "1352-Present",
            "summary": "Bayezid I aggressively annexes the western coastal beyliks (Aydın, Saruhan, Menteşe) and subdues Konya, expanding the direct provincial polygon eastward.",
            "geometry": [[26.00, 36.50], [26.00, 40.50], [31.50, 41.50], [35.00, 39.00], [32.50, 36.50], [26.00, 36.50]]
        },
        {
            "id": "anatolia_core",
            "name": "Ottoman Anatolia (Interregnum Fracture)",
            "power": "Ottoman Province",
            "relation": "direct",
            "start": 1402,
            "end": 1412,
            "capital": "Bursa / Amasya split",
            "status": "Civil War & Territorial Fracture",
            "held": "1352-Present",
            "summary": "Following defeat at the Battle of Ankara (1402), Timur dismantles the unified province, restoring old local beyliks and shrinking the direct Ottoman boundary footprint.",
            "geometry": [[26.50, 39.80], [30.00, 40.50], [31.00, 39.00], [28.50, 38.00], [26.50, 39.80]]
        },
        {
            "id": "anatolia_core",
            "name": "Ottoman Anatolia (Consolidation Era)",
            "power": "Ottoman Province",
            "relation": "direct",
            "start": 1413,
            "end": 1460,
            "capital": "Bursa",
            "status": "Re-annexation Phase",
            "held": "1352-Present",
            "summary": "Mehmed I and Murad II successfully suppress internal civil conflicts and reclaim the lost maritime Aegean beyliks.",
            "geometry": [[26.00, 36.50], [26.00, 40.50], [31.50, 41.50], [35.00, 39.00], [32.50, 36.50], [26.00, 36.50]]
        },
        {
            "id": "anatolia_core",
            "name": "Ottoman Anatolia (Eastern Imperial Integration)",
            "power": "Ottoman Province",
            "relation": "direct",
            "start": 1461,
            "end": 1514,
            "capital": "Istanbul administration",
            "status": "Black Sea Rim & Eastern Conquest",
            "held": "1352-Present",
            "summary": "Mehmed II completely closes out independent resistance by seizing Sinop, conquering the Empire of Trebizond (1461), and decisively securing eastern Anatolia at Otlukbeli (1473).",
            "geometry": [[26.00, 36.00], [26.00, 41.00], [35.00, 42.00], [40.00, 41.50], [39.50, 38.00], [36.00, 36.50], [26.00, 36.00]]
        },
        {
            "id": "anatolia_core",
            "name": "Ottoman Anatolia (Complete Political Unification)",
            "power": "Ottoman Province",
            "relation": "direct",
            "start": 1515,
            "end": 1900,
            "capital": "Istanbul administration",
            "status": "Total Mainland Consolidation",
            "held": "1352-Present",
            "summary": "Following Selim I's victories at Chaldiran and Turnadağ (1515), the final independent Anatolian beyliks are entirely absorbed, establishing the classical imperial heartland borders.",
            "geometry": [[26.00, 36.00], [26.00, 41.50], [35.00, 42.20], [41.50, 41.50], [44.50, 39.50], [42.00, 36.50], [36.00, 36.00], [26.00, 36.00]]
        }
    ]
    
    territories.extend(dynamic_anatolia_sequence)
    with open(territories_path, "w", encoding="utf-8") as f:
        json.dump(territories, f, ensure_ascii=False, indent=2)
    print("✓ Successfully injected non-overlapping chronological entries into territories.json.")

# ==============================================================================
# 4. COMPILER TRIGGER
# ==============================================================================
print("\nRe-compiling your interactive layout code...")
try:
    from atlas.map_builder import build_atlas
    build_atlas("ottoman_europe_atlas.html")
    print("✓ SUCCESS! Dynamic Anatolian advance system is fully live in production.")
except Exception as e:
    print(f"X Compilation error: {e}")
    