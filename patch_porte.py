import json
from pathlib import Path

builder_path = Path("atlas/map_builder.py")

def patch_porte():
    if not builder_path.exists():
        print("X Error: atlas/map_builder.py not found.")
        return

    content = builder_path.read_text(encoding="utf-8")

    # 1. Inject Star CSS
    css_to_add = """
.capital-star {
    font-size: 20px;
    color: #c5a059;
    display: flex;
    align-items: center;
    justify-content: center;
    text-shadow: 0 0 3px #000;
}
"""
    if ".capital-star" not in content:
        # Append to the end of the existing CSS block in _css()
        content = content.replace("}} '''", f".capital-star {{ {css_to_add} }} '''")

    # 2. Update renderPoints logic for the Star
    old_render = """L.marker([lat, lon], {icon: cityIcon()})      
   .bindTooltip(${name}${note}, {sticky: true})         .addTo(cityGroup);"""
    
    new_render = """const isCapital = (name === "Constantinople");
      L.marker([lat, lon], {
          icon: isCapital ? L.divIcon({className: "capital-star", html: "★", iconSize: [20, 20], iconAnchor: [10, 10]}) : cityIcon()
      })
      .bindTooltip(${name}${note}, {sticky: true})
      .addTo(cityGroup);"""

    if "const isCapital" not in content:
        content = content.replace(old_render, new_render)

    builder_path.write_text(content, encoding="utf-8")
    print("✓ Successfully patched map_builder.py with Porte star marker.")

    # 3. Trigger rebuild
    try:
        from atlas.map_builder import build_atlas
        build_atlas("ottoman_europe_atlas.html")
        print("✓ Map reconstructed with star marker!")
    except Exception as e:
        print(f"X Compilation error: {e}")

if __name__ == "__main__":
    patch_porte()