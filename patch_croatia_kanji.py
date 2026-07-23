import json
from pathlib import Path
from atlas.map_builder import build_atlas

territories_path = Path("data/territories.json")

def patch_croatia_kanji():
    if not territories_path.exists():
        print("X Error: data/territories.json not found.")
        return

    with open(territories_path, "r", encoding="utf-8") as f:
        territories = json.load(f)

    # 1. CLEAN SLATE: Remove ALL conflicting IDs
    # This ensures that even if you ran an old patch file, the file is scrubbed clean
    banned_ids = {"kingdom_of_croatia", "croatia_early", "croatia_late", "croatia_1526", "croatia_1600", "kanji"}
    territories = [t for t in territories if t["id"] not in banned_ids]

    # 2. DEFINITIVE PHASES (Using your high-precision coordinates)
    croatia_phases = [
        {
            "id": "croatia_1526",
            "name": "Kingdom of Croatia",
            "power": "Kingdom of Croatia",
            "relation": "neighbour",
            "start": 1526,
            "end": 1599,
            "capital": "Zagreb",
            "status": "Habsburg borderland",
            "summary": "Full extent of the Kingdom of Croatia prior to the loss of territory to Kanije.",
            "geometry": [
                [17.1157, 46.1867], [16.7544, 46.0311], [16.7279, 45.8761], [16.5209, 45.8076], 
                [16.3568, 45.6810], [16.1500, 45.6603], [16.0403, 45.6208], [16.0562, 45.5243], 
                [15.7948, 45.5026], [15.7865, 45.2901], [15.7630, 45.1354], [15.7676, 44.9522], 
                [15.7714, 44.7980], [15.9368, 44.6938], [15.9544, 44.4917], [15.9045, 44.2888], 
                [16.0285, 44.1359], [16.1502, 44.0889], [16.2863, 43.9550], [16.3552, 43.7916], 
                [16.5158, 43.7445], [17.1426, 43.4953], [17.2088, 43.3406], [17.4336, 43.2048], 
                [17.6445, 43.0974], [17.8024, 43.0189], [17.8809, 42.9407], [18.0909, 42.8514], 
                [18.1954, 42.7823], [18.4307, 42.6625], [18.5229, 42.6612], [18.7928, 42.9485], 
                [19.0388, 43.2500], [19.2732, 43.4918], [19.5861, 43.9782], [20.1436, 44.3028], 
                [19.6157, 44.3738], [19.4169, 44.5035], [19.3291, 44.6983], [19.2391, 44.8447], 
                [19.1460, 44.9139], [19.0455, 45.1666], [18.6931, 45.3163], [18.4109, 45.5706], 
                [18.0741, 45.9895], [17.5341, 46.2055], [17.0878, 46.1770], [17.1157, 46.1867]
            ]
        },
        {
            "id": "croatia_1600",
            "name": "Kingdom of Croatia",
            "power": "Kingdom of Croatia",
            "relation": "neighbour",
            "start": 1600,
            "end": 1685,
            "capital": "Zagreb",
            "status": "Habsburg borderland (reduced)",
            "summary": "Reduced Croatian territory after the establishment of the Kanji Eyalet.",
            "geometry": [
                [16.2690, 46.5853], [16.7765, 46.3919], [17.1119, 46.1852], [16.8944, 46.0784],
                [16.7675, 45.9966], [16.6225, 45.8137], [16.3868, 45.6999], [16.0333, 45.6176],
                [16.0605, 45.5160], [15.8158, 45.5033], [15.7705, 44.7681], [15.4080, 44.3742],
                [15.2448, 44.3548], [14.9548, 44.6457], [14.9185, 44.8067], [14.9185, 45.0953],
                [15.2267, 45.5478], [15.5530, 45.9525], [15.7071, 46.2103], [15.8974, 46.2291],
                [16.0061, 46.3293], [16.3687, 46.4044], [16.2599, 46.6040], [16.2690, 46.5853]
            ]
        },
        {
            "id": "kanji",
            "name": "Kanji Eyalet",
            "power": "Ottoman Province",
            "relation": "direct",
            "start": 1600,
            "end": 1685,
            "capital": "Kanije",
            "status": "Ottoman frontier eyalet",
            "summary": "Administrative province carved from the Croatian borderlands.",
            "geometry": [
                [17.0472, 46.2076], [16.8708, 46.2794], [16.7567, 46.4012], [16.5181, 46.5084],
                [16.3417, 46.5512], [16.0616, 46.6652], [15.9993, 46.7719], [16.0097, 46.9209],
                [16.1550, 47.0200], [16.2172, 47.1401], [16.4766, 46.9988], [16.4869, 47.1119],
                [16.4558, 47.2036], [16.4869, 47.3092], [16.4869, 47.4216], [16.6114, 47.4427],
                [16.9538, 47.3233], [17.2546, 47.2177], [17.5970, 47.1048], [17.7526, 46.9634],
                [18.1053, 46.7861], [18.1261, 46.7008], [18.0535, 46.4441], [18.0950, 46.3009],
                [18.0016, 46.1933], [18.0327, 46.0135], [17.0472, 46.2076]
            ]
        }
    ]

    territories.extend(croatia_phases)

    with open(territories_path, "w", encoding="utf-8") as f:
        json.dump(territories, f, ensure_ascii=False, indent=2)

    print("✓ Successfully patched Croatia with dynamic shrinking phases and Kanji.")
    
    # Re-compile
    print("\nRe-compiling interactive atlas visual layers...")
    try:
        build_atlas("ottoman_europe_atlas.html")
        print("✓ Atlas rebuilt.")
    except Exception as e:
        print(f"X Build failed: {e}")

if __name__ == "__main__":
    patch_croatia_kanji()
    