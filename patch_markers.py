import sys
from pathlib import Path

builder_path = Path("atlas/map_builder.py")

if builder_path.exists():
    content = builder_path.read_text(encoding="utf-8")
    
    # 1. Update CSS styles for markers
    old_css = """.battle-marker {
  width: 22px;
  height: 22px;
  color: #fff;
  background: #642016;
  font: 700 13px Inter, sans-serif;
}
.battle-marker.naval {
  background: #1f5b6d;
}
.city-marker {
  width: 10px;
  height: 10px;
  background: #2c1d16;
  border: 2px solid #fbf6ea;
}"""
    
    new_css = """.battle-marker, .city-marker {
  display: grid;
  place-items: center;
  border-radius: 50%;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.6);
}
.battle-marker {
  width: 11px;
  height: 11px;
  background: #8f2f2a;
  font-size: 0;
}
.battle-marker.naval {
  background: #1f5b6d;
}
.city-marker {
  width: 6px;
  height: 6px;
  background: #241b18;
  border: 1px solid #fbf6ea;
}"""

    if "/* Refined, smaller markers */" not in content:
        content = content.replace(old_css, new_css)
        # Add comment so we don't patch twice
        content = content.replace(".battle-marker, .city-marker {", "/* Refined, smaller markers */\n.battle-marker, .city-marker {")

    # 2. Update JS icon functions
    old_js_city = """function cityIcon() {
  return L.divIcon({className: "", html: '<span class="city-marker"></span>', iconSize: [14, 14], iconAnchor: [7, 7]});
}

function battleIcon(kind) {
  const naval = kind === "naval";
  return L.divIcon({className: "", html: `<span class="battle-marker ${naval ? "naval" : ""}">${naval ? "●" : "◆"}</span>`, iconSize: [22, 22], iconAnchor: [11, 11]});
}"""

    new_js_icons = """function cityIcon() {
  return L.divIcon({className: "", html: '<span class="city-marker"></span>', iconSize: [8, 8], iconAnchor: [4, 4]});
}

function battleIcon(kind) {
  const naval = kind === "naval";
  return L.divIcon({className: "", html: `<span class="battle-marker ${naval ? "naval" : ""}"></span>`, iconSize: [13, 13], iconAnchor: [6, 6]});
}"""

    if "iconSize: [8, 8]" not in content:
        content = content.replace(old_js_city, new_js_icons)

    builder_path.write_text(content, encoding="utf-8")
    print("✓ Successfully patched marker aesthetics.")

    # 3. Trigger map re-compilation
    try:
        from atlas.map_builder import build_atlas
        build_atlas("ottoman_europe_atlas.html")
        print("✓ Map build successfully reconstructed with new aesthetic markers!")
    except Exception as e:
        print(f"X Build compilation error: {e}")
else:
    print("X Error: atlas/map_builder.py not found.")
    