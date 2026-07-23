import json
from pathlib import Path
from atlas.map_builder import build_atlas

def patch_events():
    events_path = Path("data/events.json")
    if not events_path.exists():
        print("X Error: data/events.json not found.")
        return

    with open(events_path, "r", encoding="utf-8") as f:
        events = json.load(f)

    # New events to add
    new_events = [
        {"year": 1677, "title": "First Siege of Chyhyryn", "body": "Ottoman defeat; Russians and Cossacks held the fortress."},
        {"year": 1678, "title": "Chyhyryn campaign", "body": "Ottoman victory; Kara Mustafa captured and destroyed Chyhyryn."},
        {"year": 1681, "title": "Treaty of Bakhchisarai", "body": "Ottoman–Russian peace; confirmed control of southern Right-bank Ukraine."},
        {"year": 1482, "title": "Sack of Kyiv", "body": "Major Crimean victory; sack of the city."},
        {"year": 1521, "title": "Great Crimean Raid on Moscow", "body": "Major Crimean victory; forces reached the outskirts of Moscow."},
        {"year": 1571, "title": "Burning of Moscow", "body": "Led by Devlet I Giray; massive enslavement and destruction."},
        {"year": 1591, "title": "Battle near Moscow", "body": "Crimean invasion under Ğazı II Giray; Russian victory."},
        {"year": 1648, "title": "Khmelnytsky Uprising Alliance", "body": "Crimean Khanate allies with Bohdan Khmelnytsky against Poland."}
    ]

    # Append events if they don't already exist
    existing_years = {e["year"] for e in events}
    for event in new_events:
        if event["year"] not in existing_years:
            events.append(event)
            print(f"✓ Added event: {event['title']}")

    # Sort events by year
    events.sort(key=lambda x: x["year"])

    with open(events_path, "w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=2)

    print("\n✓ Events updated. Rebuilding Atlas...")
    build_atlas("ottoman_europe_atlas.html")

if __name__ == "__main__":
    patch_events()
    