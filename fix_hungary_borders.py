import json
from pathlib import Path

territories_path = Path("data/territories.json")

if territories_path.exists():
    with open(territories_path, "r", encoding="utf-8") as f:
        territories = json.load(f)
        
    # Find and update the 'royal_hungary' polygon coordinates
    # We shift the westernmost edge eastward to approx 17.0° E - 17.5° E longitude,
    # cleanly leaving Vienna (16.37° E) on the Habsburg/Austrian side of the frontier.
    updated = False
    for t in territories:
        if t["id"] == "royal_hungary":
            t["name"] = "Kingdom of Royal Hungary"
            t["summary"] = "The slim crescent of the Hungarian realm held under Habsburg crown rule, acting as a highly contested frontier buffer zone."
            # Restructured slim polygon coordinates:
            t["geometry"] = [
                [17.15, 46.60], # Shifting border eastward away from Vienna's longitude
                [17.40, 47.90], 
                [18.55, 48.20], 
                [19.55, 49.55], 
                [18.50, 49.60], 
                [17.20, 48.60], 
                [17.15, 46.60]
            ]
            updated = True
            break
            
    if updated:
        with open(territories_path, "w", encoding="utf-8") as f:
            json.dump(territories, f, ensure_ascii=False, indent=2)
        print("✓ Successfully corrected Royal Hungary's polygon bounds to a historically accurate slim shape.")
    else:
        print("X Error: 'royal_hungary' entry was not found in territories.json.")

    # 2. Re-compile production atlas code to push layout changes live
    print("\nRe-compiling layout assets...")
    try:
        from atlas.map_builder import build_atlas
        build_atlas("ottoman_europe_atlas.html")
        print("✓ Production build updated! Clear browser cache and refresh 'ottoman_europe_atlas.html' to review.")
    except Exception as e:
        print(f"X Compilation error encountered: {e}")
else:
    print("X Error: Could not locate 'data/territories.json'.")
    