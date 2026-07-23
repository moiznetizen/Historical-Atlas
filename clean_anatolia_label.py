from pathlib import Path

builder_path = Path("atlas/map_builder.py")

if builder_path.exists():
    content = builder_path.read_text(encoding="utf-8")
    
    # 1. Target and remove the blue masking pane completely if still present
    target_blue_box = """map.createPane("asiaMaskPane");
map.getPane("asiaMaskPane").style.zIndex = 320;
L.polygon([
  [34.0, 29.65],
  [34.0, 39.0],
  [42.35, 39.0],
  [42.35, 29.65]
], {
  pane: "asiaMaskPane",
  stroke: false,
  fillColor: "#8fb7bf",
  fillOpacity: 0.96,
  interactive: false
}).addTo(map);"""

    if target_blue_box in content:
        content = content.replace(target_blue_box, "")
        print("✓ Removed the blue mask box code block.")
    else:
        # Fallback regex search if spacing or previous edits altered the template
        import re
        content, count = re.subn(r'map\.createPane\("asiaMaskPane"\);.*?\}\)\.addTo\(map\);', '', content, flags=re.DOTALL)
        if count > 0:
            print("✓ Stripped the blue box code block via pattern matching.")

    # 2. Inject CSS style rules for the text layer (with doubled braces for Python f-string escaping)
    old_css_anchor = ".route-label {{"
    new_css_block = """.anatolia-map-label {{
  color: rgba(36, 27, 24, 0.55);
  font-family: "Cinzel", Georgia, serif;
  font-weight: 700;
  font-size: 14px;
  letter-spacing: 4px;
  text-transform: uppercase;
  text-align: center;
  pointer-events: none;
  white-space: nowrap;
}}
.route-label {{"""

    if ".anatolia-map-label" not in content:
        content = content.replace(old_css_anchor, new_css_block)
        print("✓ Injected CSS layout font properties for Anatolia text label.")

    # 3. Clean up any previous 'Ottoman Anatolia' text code to prevent multiple overlaps
    if "Ottoman Anatolia" in content:
        # Strip out the old label code block if it was previously written
        content = re.sub(r'// Static horizontal text label for Anatolia.*?\}\)\.addTo\(map\);', '', content, flags=re.DOTALL)
        content = re.sub(r'// Separate horizontal text layer for Anatolia.*?\}\)\.addTo\(map\);', '', content, flags=re.DOTALL)

    # 4. Add the clean Leaflet marker script with text saying strictly "Anatolia"
    old_js_anchor = "setYear(currentYear);"
    new_js_block = """// Dedicated standalone text layer for Anatolia
L.marker([39.20, 34.50], {{
  icon: L.divIcon({{
    className: "",
    html: '<div class="anatolia-map-label">Anatolia</div>',
    iconSize: [200, 30],
    iconAnchor: [100, 15]
  }}),
  interactive: false
}}).addTo(map);

setYear(currentYear);"""

    if "Anatolia" not in content or "anatolia-map-label" not in content:
        content = content.replace(old_js_anchor, new_js_block)
        print("✓ Appended separate text marker layer ('Anatolia') into map script.")

    # Save changes to data engine
    builder_path.write_text(content, encoding="utf-8")

    # 5. Automatically run the re-compiler to update the production HTML document
    print("\nRe-compiling layout assets...")
    try:
        from atlas.map_builder import build_atlas
        build_atlas("ottoman_europe_atlas.html")
        print("✓ Success! Blue box removed and standalone label updated to say 'Anatolia'.")
    except Exception as e:
        print(f"X Compilation error: {e}")
else:
    print("X Error: Could not locate 'atlas/map_builder.py'. Check your project path.")
    