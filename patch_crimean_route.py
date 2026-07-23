import json
from pathlib import Path
from atlas.map_builder import build_atlas

campaigns_path = Path("data/campaigns.json")

def patch_campaign_route():
    if not campaigns_path.exists():
        print("X Error: data/campaigns.json not found.")
        return

    with open(campaigns_path, "r", encoding="utf-8") as f:
        campaigns = json.load(f)

    # Route: Crimea (Bakhchisarai) -> Perekop -> Oka River Crossing -> Moscow
    # Coordinates in [Lon, Lat] format as typically used in Leaflet GeoJSON
    moscow_campaign = {
        "name": "Crimean Campaign (Burning of Moscow)",
        "start": 1571,
        "end": 1571,
        "summary": "Devlet I Giray's massive raid into Muscovy, resulting in the burning of Moscow.",
        "points": [
            [33.85, 44.75], # Bakhchisarai
            [33.68, 46.15], # Perekop
            [36.00, 48.00], # Steppe transition
            [37.50, 52.00], # Oka River approach
            [37.61, 55.75]  # Moscow
        ]
    }

    # Add the campaign if it doesn't already exist
    known_campaigns = {c["name"] for c in campaigns}
    if moscow_campaign["name"] not in known_campaigns:
        campaigns.append(moscow_campaign)
        with open(campaigns_path, "w", encoding="utf-8") as f:
            json.dump(campaigns, f, ensure_ascii=False, indent=2)
        print("✓ Successfully added Crimean-Moscow campaign route.")
    else:
        print("- Campaign route already exists.")

    # Rebuild the atlas
    print("Re-compiling atlas...")
    build_atlas("ottoman_europe_atlas.html")
    print("✓ Atlas rebuilt with updated campaign routes.")

if __name__ == "__main__":
    patch_campaign_route()