import json
import re
from pathlib import Path

battles_path = Path("data/battles.json")
events_path = Path("data/events.json")
territories_path = Path("data/territories.json")

# ==============================================================================
# 1. NEW DATASET DEFINITIONS
# ==============================================================================

new_albanian_battles = [
    {"name": "Battle of Savra", "date": "1385", "year": 1385, "lat": 40.90, "lon": 19.65, "kind": "land", "commanders": "Hayreddin Pasha; Balša II of Zeta", "result": "Ottoman victory", "importance": "First major Ottoman military victory in Albania; established baseline suzerainty over regional princes.", "casualties": "Heavy local losses."},
    {"name": "Occupation of Krujë", "date": "1392", "year": 1392, "lat": 41.51, "lon": 19.79, "kind": "siege", "commanders": "Ottoman Rumelian forces; Thopia family defenders", "result": "Ottoman conquest", "importance": "Brought a highly critical northern Albanian fortress under direct garrison control.", "casualties": "Not securely recorded."},
    {"name": "Conquest of Vlorë, Berat and Kanina", "date": "1417", "year": 1417, "lat": 40.47, "lon": 19.49, "kind": "expedition", "commanders": "Evrenosoglu Ali Bey; Rugina Balšić", "result": "Ottoman victory", "importance": "Secured southern Albania and established a critical strategic foothold on the Adriatic coast.", "casualties": "Garrisons overwhelmed."},
    {"name": "Albanian Revolt (1432-1436)", "date": "1432", "year": 1432, "lat": 40.70, "lon": 19.95, "kind": "expedition", "commanders": "Ali Bey Evrenosoglu; Gjergj Arianiti", "result": "Rebellion suppressed", "importance": "First large-scale anti-Ottoman baseline resistance, eventually put down by Rumelian army forces.", "casualties": "Heavy on both sides."},
    {"name": "Capture of Krujë (Skanderbeg)", "date": "28 November 1443", "year": 1443, "lat": 41.51, "lon": 19.79, "kind": "siege", "commanders": "Gjergj Kastrioti (Skanderbeg); Ottoman garrison", "result": "Albanian victory", "importance": "Sparked the legendary Skanderbeg Rebellion and the formation of the League of Lezhë.", "casualties": "Ottoman garrison eliminated."},
    {"name": "Battle of Torvioll", "date": "29 June 1444", "year": 1444, "lat": 41.15, "lon": 20.35, "kind": "land", "commanders": "Skanderbeg; Ali Pasha", "result": "Albanian victory", "importance": "First massive field victory for Skanderbeg; shattered an invading Rumelian army.", "casualties": "Severe Ottoman losses."},
    {"name": "Battle of Mokra (1445)", "date": "10 October 1445", "year": 1445, "lat": 41.12, "lon": 20.60, "kind": "land", "commanders": "Skanderbeg; Firuz Pasha", "result": "Albanian victory", "importance": "Successfully repelled a secondary punitive force sent into central frontier zones.", "casualties": "Heavy Ottoman casualties."},
    {"name": "Battle of Otonetë", "date": "27 September 1446", "year": 1446, "lat": 41.60, "lon": 20.45, "kind": "land", "commanders": "Skanderbeg; Mustafa Pasha", "result": "Albanian victory", "importance": "Defeated an invading cavalry army, protecting the territorial Integrity of central Albania.", "casualties": "Moderate losses."},
    {"name": "Battle of Oranik (1448)", "date": "1448", "year": 1448, "lat": 41.48, "lon": 20.52, "kind": "land", "commanders": "Skanderbeg; Mustafa Pasha", "result": "Albanian victory", "importance": "Shattered an invading Ottoman relief army corps during the war with Venice.", "casualties": "Mustafa Pasha captured."},
    {"name": "Battle of Modrič", "date": "1452", "year": 1452, "lat": 41.38, "lon": 20.55, "kind": "land", "commanders": "Skanderbeg; Hamza Kastrioti (Ottoman service)", "result": "Albanian victory", "importance": "Defeated an Ottoman raiding and infiltration force within hours of contact.", "casualties": "Ottoman commanders killed."},
    {"name": "Battle of Pollog", "date": "22 April 1453", "year": 1453, "lat": 42.01, "lon": 20.97, "kind": "land", "commanders": "Skanderbeg; Ibrahim Pasha", "result": "Albanian victory", "importance": "Maintained defensive perimeter stability just prior to the fall of Constantinople.", "casualties": "Ibrahim Pasha killed."},
    {"name": "Battle of Berat (1455)", "date": "July 1455", "year": 1455, "lat": 40.70, "lon": 19.95, "kind": "siege", "commanders": "Isa Beg Evrenosoglu; Skanderbeg", "result": "Ottoman victory", "importance": "One of Skanderbeg's few major battlefield defeats, breaking the siege of the fortress.", "casualties": "Heavy Albanian losses."},
    {"name": "Battle of Albulena", "date": "2 September 1457", "year": 1457, "lat": 41.66, "lon": 19.73, "kind": "land", "commanders": "Skanderbeg; Isaac Bey Evrenosoglu and Hamza Kastrioti", "result": "Decisive Albanian victory", "importance": "Skanderbeg's greatest military masterpiece; completely routed a massive invading field force.", "casualties": "Very high Ottoman losses."},
    {"name": "Battle of Mokra (1462)", "date": "7 July 1462", "year": 1462, "lat": 41.12, "lon": 20.60, "kind": "land", "commanders": "Skanderbeg; Sinan Pasha", "result": "Albanian victory", "importance": "Destroyed an invading army column, securing the central mountain passes.", "casualties": "Ottoman routing losses."},
    {"name": "Battle of Vaikal (1465)", "date": "April 1465", "year": 1465, "lat": 41.52, "lon": 20.15, "kind": "land", "commanders": "Skanderbeg; Ballaban Pasha", "result": "Albanian victory", "importance": "Tactical check on Ottoman advances, though several crucial Albanian commanders were captured.", "casualties": "Heavy losses on both sides."},
    {"name": "Second Battle of Vaikal", "date": "1467", "year": 1467, "lat": 41.52, "lon": 20.15, "kind": "land", "commanders": "Skanderbeg; Ballaban Pasha", "result": "Albanian victory", "importance": "Ballaban Pasha was mortally wounded during the campaign, temporarily breaking the military encirclement.", "casualties": "Ballaban Pasha killed."},
    {"name": "Siege of Shkodër (1474)", "date": "1474", "year": 1474, "lat": 42.07, "lon": 19.51, "kind": "siege", "commanders": "Hadım Suleiman Pasha; Antonio Loredan (Venetian-Albanian garrison)", "result": "Venetian-Albanian victory", "importance": "Fierce defense of northern Albania; Ottoman forces withdrew due to high casualties and disease.", "casualties": "Severe Ottoman siege losses."},
    {"name": "Treaty of Constantinople (1479)", "date": "25 January 1479", "year": 1479, "lat": 41.01, "lon": 28.97, "kind": "treaty", "commanders": "Mehmed II; Venetian Republic diplomats", "result": "Shkodër ceded to Ottomans", "importance": "Venice cedes Shkodër and other Albanian ports, completing the classical conquest of Albania.", "casualties": "None."}
]

new_albanian_events = [
    {"year": 1443, "title": "Skanderbeg Rebellion begins", "body": "Gjergj Kastrioti (Skanderbeg) seizes Krujë and defects, launching a 25-year war of liberation that opens a deep pocket in western Rumelia.", "sultan": "Murad II", "population": "Balkan localized warfare", "largest_rival": "League of Lezhë and Hungary"},
    {"year": 1479, "title": "Albania fully conquered", "body": "Following the fall of Shkodër and the Treaty of Constantinople, Venetian-held outposts are ceded, incorporating Albania completely into Rumelia.", "sultan": "Mehmed II", "population": "Adriatic systems integrated", "largest_rival": "Habsburgs and Venice"}
]

# ==============================================================================
# 2. RUN PACKAGING LOGIC
# ==============================================================================

# Update battles.json safely
if battles_path.exists():
    with open(battles_path, "r", encoding="utf-8") as f:
        battles = json.load(f)
    known = {b["name"] for b in battles}
    added = 0
    for nb in new_albanian_battles:
        if nb["name"] not in known:
            battles.append(nb)
            added += 1
    with open(battles_path, "w", encoding="utf-8") as f:
        json.dump(battles, f, ensure_ascii=False, indent=2)
    print(f"✓ Injected {added} new historical battles & treaties into battles.json.")

# Update events.json safely
if events_path.exists():
    with open(events_path, "r", encoding="utf-8") as f:
        events = json.load(f)
    known_ev = {(e["year"], e["title"]) for e in events}
    added_ev = 0
    for ne in new_albanian_events:
        if (ne["year"], ne["title"]) not in known_ev:
            events.append(ne)
            added_ev += 1
    events.sort(key=lambda x: x["year"])
    with open(events_path, "w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=2)
    print(f"✓ Injected {added_ev} timeline milestone indicators into events.json.")

# ==============================================================================
# 3. OVERWRITE RUMELIA CHRONOLOGY FOR DYNAMIC ALBANIA POCKETS
# ==============================================================================

if territories_path.exists():
    with open(territories_path, "r", encoding="utf-8") as f:
        territories = json.load(f)
    
    # Clean out any previous configurations of rumelia to prevent layering leaks
    territories = [t for t in territories if t["id"] != "rumelia"]
    
    # Re-build the sequential multi-state polygon configuration for the ID "rumelia"
    # Geometries are mathematically altered to pull back during 1443-1478 to reflect Skanderbeg's pocket
    dynamic_rumelia_sequence = [
        {
            "id": "rumelia",
            "name": "Rumelia Eyalet",
            "power": "Ottoman Province",
            "relation": "direct",
            "start": 1362,
            "end": 1384,
            "capital": "Edirne",
            "status": "Core European expansion sphere",
            "held": "1362-1867",
            "summary": "Administrative center focused strictly on Thrace following the structural organization of Adrianople.",
            "geometry": [[25.50, 40.20], [29.10, 40.60], [29.45, 41.50], [28.85, 42.15], [27.20, 41.80], [25.50, 40.20]]
        },
        {
            "id": "rumelia",
            "name": "Rumelia Eyalet",
            "power": "Ottoman Province",
            "relation": "direct",
            "start": 1385,
            "end": 1442,
            "capital": "Sofia",
            "status": "First Phase Western Expansion",
            "held": "1362-1867",
            "summary": "Expanded deep into the Balkans and the Adriatic coast, incorporating early Albanian principalities after the Battle of Savra (1385).",
            # This geometry fully extends westward into Albania (down to 19.45E)
            "geometry": [[19.45, 40.45], [21.20, 41.10], [25.50, 40.20], [29.10, 40.60], [29.45, 41.50], [28.85, 42.15], [28.30, 43.20], [24.85, 44.15], [21.40, 43.40], [19.45, 41.50], [19.45, 40.45]]
        },
        {
            "id": "rumelia",
            "name": "Rumelia Eyalet",
            "power": "Ottoman Province",
            "relation": "direct",
            "start": 1443,
            "end": 1478,
            "capital": "Sofia",
            "status": "Balkan Theater - Skanderbeg Pocket Left Uncolored",
            "held": "1362-1867",
            "summary": "During the Skanderbeg Rebellion, central and northern Albania successfully seceded from direct provincial rule, leaving a liberated pocket.",
            # CRITICAL CORRECTION: Western bounds pulled back eastward to 20.40E, leaving Albania unshaded (uncolored)
            "geometry": [[20.40, 40.45], [21.20, 41.10], [25.50, 40.20], [29.10, 40.60], [29.45, 41.50], [28.85, 42.15], [28.30, 43.20], [24.85, 44.15], [21.40, 43.40], [20.40, 41.50], [20.40, 40.45]]
        },
        {
            "id": "rumelia",
            "name": "Rumelia Eyalet",
            "power": "Ottoman Province",
            "relation": "direct",
            "start": 1479,
            "end": 1867,
            "capital": "Sofia, later Monastir",
            "status": "Peak Integration Consolidation",
            "held": "1362-1867",
            "summary": "Peak consolidated layout of classical Rumelia. Albania is completely re-integrated into direct provincial administration following the Treaty of Constantinople.",
            # Re-extends all the way out to cover all missing sections of Greece, Thrace, and Albania
            "geometry": [[18.35, 42.28], [18.95, 41.80], [19.45, 40.45], [20.55, 39.35], [21.55, 38.25], [22.40, 36.40], [23.10, 36.30], [23.60, 37.95], [24.75, 37.95], [24.95, 39.25], [26.30, 40.20], [29.10, 40.60], [29.45, 41.50], [28.85, 42.05], [28.30, 43.20], [27.55, 43.75], [26.40, 44.10], [24.85, 44.15], [23.10, 44.05], [21.80, 44.55], [20.55, 45.10], [19.20, 44.88], [18.35, 44.05], [18.35, 42.28]]
        }
    ]
    
    territories.extend(dynamic_rumelia_sequence)
    with open(territories_path, "w", encoding="utf-8") as f:
        json.dump(territories, f, ensure_ascii=False, indent=2)
    print("✓ Successfully configured single-ID sequential Rumelia geometries with dynamic Albanian pocket tracking.")

# ==============================================================================
# 4. RE-COMPILE PRODUCTION MAP
# ==============================================================================
print("\nRe-compiling interactive layout layers...")
try:
    from atlas.map_builder import build_atlas
    build_atlas("ottoman_europe_atlas.html")
    print("✓ SUCCESS! Production atlas successfully reconstructed with dynamic Albanian features.")
except Exception as e:
    print(f"X Compilation mistake: {e}")
    