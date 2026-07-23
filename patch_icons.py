import sys
from pathlib import Path

# Trigger atlas build after patching
from atlas.map_builder import build_atlas

builder_path = Path("atlas/map_builder.py")

if builder_path.exists():
    content = builder_path.read_text(encoding="utf-8")
    
    # 1. Update CSS: Remove circles, add specific icon styles
    # We replace the entire block that defined .battle-marker and .city-marker
    old_css = """.battle-marker, .city-marker {
  display: grid;
  place-items: center;
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.35);
}
.battle-marker {
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
    
    new_css = """.battle-marker, .treaty-marker, .city-marker {
  display: grid;
  place-items: center;
  font-size: 16px;
}
.battle-marker { color: #8f2f2a; }
.battle-marker.naval { color: #1f5b6d; }
.treaty-marker { color: #5f1b16; }
.city-marker {
  width: 6px;
  height: 6px;
  background: #241b18;
  border-radius: 50%;
  border: 1px solid #fbf6ea;
}"""

    if ".battle-marker" in content and "box-shadow: 0 2px 8px" in content:
        content = content.replace(old_css, new_css)

    # 2. Update JS: Replace function with new icon logic
    old_js = """function battleIcon(kind) {
  const naval = kind === "naval";
  return L.divIcon({className: "", html: `<span class="battle-marker ${naval ? "naval" : ""}">${naval ? "●" : "◆"}</span>`, iconSize: [22, 22], iconAnchor: [11, 11]});
}"""

    new_js = """function battleIcon(kind) {
  if (kind === "treaty") return L.divIcon({className: "", html: '<span class="treaty-marker">📄</span>', iconSize: [20, 20], iconAnchor: [10, 10]});
  const naval = kind === "naval";
  return L.divIcon({className: "", html: `<span class="battle-marker ${naval ? "naval" : ""}">⚔</span>`, iconSize: [20, 20], iconAnchor: [10, 10]});
}"""

    if "battleIcon(kind)" in content:
        content = content.replace(old_js, new_js)

    builder_path.write_text(content, encoding="utf-8")
    print("✓ Patched map_builder.py: Icons updated to ⚔, ⚓/⚔, and 📄.")

    # 3. Trigger rebuild
    print("\nRe-compiling layout assets...")
    try:
        build_atlas("ottoman_europe_atlas.html")
        print("✓ Build complete! Refresh your browser.")
    except Exception as e:
        print(f"X Build compilation error: {e}")
else:
    print("X Error: atlas/map_builder.py not found.")