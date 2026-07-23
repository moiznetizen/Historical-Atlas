import json
from pathlib import Path

territories_path = Path("data/territories.json")

if territories_path.exists():
    with open(territories_path, "r", encoding="utf-8") as f:
        territories = json.load(f)
        
    updated = False
    for t in territories:
        if t["id"] == "royal_hungary":
            t["name"] = "Kingdom of Royal Hungary"
            t["summary"] = "The slim crescent of the Hungarian realm held under Habsburg crown rule, directly bordering the Ottoman Eyalet of Budin on its eastern side."
            
            # Re-engineered slim geometry path:
            # The eastern edge now perfectly tracks the western frontier vertices of Budin
            # (17.35, 45.42 -> 17.88, 46.20 -> 18.30, 47.05 -> 18.82, 47.72)
            # while keeping its western front safely away from Vienna.
            t["geometry"] = [
                [17.15, 45.42], # Bottom-left corner (near Croatia frontier)
                [17.35, 45.42], # Connecting to Budin's southwest anchor point
                [17.88, 46.20], # Anchoring to Budin's western flank node
                [18.30, 47.05], # Anchoring to Budin's north-central flank node
                [18.82, 47.72], # Following Budin's northwestern node up into Slovakia
                [19.55, 49.55], # Reaching the northern peak summit point
                [18.50, 49.60], # Upper northwestern turn
                [17.20, 48.60], # Safeguarding Bratislava/Pressburg corridor
                [17.15, 46.60], # Safe western clearance away from Vienna
                [17.15, 45.42]  # Loop closure point
            ]
            updated = True
            break
            
    if updated:
        with open(territories_path, "w", encoding="utf-8") as f:
            json.dump(territories, f, ensure_ascii=False, indent=2)
        print("✓ Successfully updated Royal Hungary coordinates to cleanly border Budin Eyalet.")
    else:
        print("X Error: 'royal_hungary' entry was not found in territories.json.")

    # 2. Automatically re-compile the production atlas
    print("\nRe-compiling layout assets...")
    try:
        from atlas.map_builder import build_atlas
        build_atlas("ottoman_europe_atlas.html")
        print("✓ Production build updated! Clear browser cache and refresh 'ottoman_europe_atlas.html' to review.")
    except Exception as e:
        print(f"X Compilation error encountered: {e}")
else:
    print("X Error: Could not locate 'data/territories.json'.")
    