import json
from pathlib import Path

battles_path = Path("data/battles.json")

if battles_path.exists():
    with open(battles_path, "r", encoding="utf-8") as f:
        battles = json.load(f)
    
    # 1. Check if the battle is already added to prevent duplicate layers
    if not any(b["name"] == "Battle of Djerba" for b in battles):
        djerba_marker = {
            "name": "Battle of Djerba",
            "date": "9–14 May 1560",
            "year": 1560,
            "lat": 33.87,
            "lon": 10.86,
            "kind": "naval",
            "commanders": "Piyale Pasha and Turgut Reis; Giovanni Andrea Doria (Christian Alliance)",
            "result": "Decisive Ottoman naval victory",
            "importance": "Shattered the combined Christian armada, marking the absolute high-water mark of Ottoman naval supremacy in the Mediterranean.",
            "casualties": "Heavy Christian alliance losses (half their fleet sunk/captured); minimal Ottoman losses."
        }
        
        # Injecting chronologically before the Siege of Malta (1565)
        battles.append(djerba_marker)
        
        with open(battles_path, "w", encoding="utf-8") as f:
            json.dump(battles, f, ensure_ascii=False, indent=2)
        print("✓ Successfully injected the Battle of Djerba into battles.json.")
    else:
        print("! Battle of Djerba is already present in your dataset.")

    # 2. Trigger the production atlas re-build to sync live onto the map
    print("\nRe-compiling layout assets...")
    try:
        from atlas.map_builder import build_atlas
        build_atlas("ottoman_europe_atlas.html")
        print("✓ SUCCESS! Battle of Djerba is now live in production.")
    except Exception as e:
        print(f"X Compilation error encountered: {e}")
else:
    print("X Error: Could not locate 'data/battles.json'.")
    