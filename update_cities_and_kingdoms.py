import json
from pathlib import Path

cities_path = Path("data/cities.json")
territories_path = Path("data/territories.json")
styles_path = Path("atlas/styles.py")

# 1. Update cities.json (Rename Iasi to Jessy, add Bosnasaray and Gyulafehérvár)
if cities_path.exists():
    with open(cities_path, "r", encoding="utf-8") as f:
        cities = json.load(f)
    
    updated_cities = []
    has_bosnasaray = False
    has_gyulafeherovar = False
    
    for city in cities:
        # Rename Iasi to Jessy
        if city[0] == "Iasi":
            city[0] = "Jessy"
        if city[0] == "Bosnasaray":
            has_bosnasaray = True
        if city[0] == "Gyulafehérvár":
            has_gyulafeherovar = True
        updated_cities.append(city)
        
    # Add new cities if missing
    if not has_bosnasaray:
        updated_cities.append(["Bosnasaray", 43.86, 18.41, 1463, "Bosnian administrative center (Sarajevo)."])
    if not has_gyulafeherovar:
        updated_cities.append(["Gyulafehérvár", 46.07, 23.57, 1541, "Historical capital of the Principality of Transylvania."])
        
    with open(cities_path, "w", encoding="utf-8") as f:
        json.dump(updated_cities, f, ensure_ascii=False, indent=2)
    print("✓ Successfully updated cities.json (Jessy, Bosnasaray, Gyulafehérvár added/modified).")

# 2. Update territories.json (Cover Hungary gap in green, add Royal Hungary)
if territories_path.exists():
    with open(territories_path, "r", encoding="utf-8") as f:
        territories = json.load(f)
        
    # Filter out existing duplicates if script is run multiple times
    territories = [t for t in territories if t["id"] not in ("hungary_gap_fill", "royal_hungary")]
    
    # Gap fill between Temesvar and Budin Eyalet (Colored green as an Ottoman Province)
    hungary_gap = {
        "id": "hungary_gap_fill",
        "name": "Central Hungary Link",
        "power": "Ottoman Province",
        "relation": "direct",
        "start": 1541,
        "end": 1699,
        "capital": "Buda",
        "status": "Direct Ottoman Province Link",
        "held": "1541-1699",
        "summary": "Territorial consolidation bridging the space between the Eyalets of Budin and Temesvar.",
        "geometry": [[19.45, 46.02], [19.70, 46.84], [21.38, 46.18], [20.28, 45.22], [19.30, 44.55], [19.45, 46.02]]
    }
    
    # Separate Kingdom entry for Royal Hungary
    royal_hungary = {
        "id": "royal_hungary",
        "name": "Kingdom of Royal Hungary",
        "power": "Royal Hungary",
        "relation": "neighbour",
        "start": 1526,
        "end": 1699,
        "capital": "Pressburg (Bratislava)",
        "status": "Separate Kingdom Framework",
        "held": "1526-1699",
        "summary": "The portion of medieval Hungary held as an independent separate kingdom, heavily backed by the Habsburgs.",
        "geometry": [[16.00, 46.22], [18.55, 47.68], [19.55, 49.55], [17.25, 50.95], [15.20, 48.60], [16.00, 46.22]]
    }
    
    territories.append(hungary_gap)
    territories.append(royal_hungary)
    
    with open(territories_path, "w", encoding="utf-8") as f:
        json.dump(territories, f, ensure_ascii=False, indent=2)
    print("✓ Successfully updated territories.json (Hungary gap covered, Royal Hungary added).")

# 3. Update atlas/styles.py to include a distinct theme color for Royal Hungary
if styles_path.exists():
    content = styles_path.read_text(encoding="utf-8")
    if '"Royal Hungary":' not in content:
        # Inject custom distinct copper/orange hex color code for Royal Hungary
        old_color_line = '"Habsburg Monarchy": "#8e918d",'
        new_color_line = '"Habsburg Monarchy": "#8e918d",\n    "Royal Hungary": "#d97706",'
        content = content.replace(old_color_line, new_color_line)
        styles_path.write_text(content, encoding="utf-8")
        print("✓ Successfully updated atlas/styles.py with distinct color styling for Royal Hungary.")

# 4. Trigger production map re-compilation
print("\nRe-compiling your layout assets...")
try:
    from atlas.map_builder import build_atlas
    build_atlas("ottoman_europe_atlas.html")
    print("✓ Complete! Refresh your browser window to test the changes.")
except Exception as e:
    print(f"X Compilation error: {e}")