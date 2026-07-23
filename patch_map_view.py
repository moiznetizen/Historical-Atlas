from pathlib import Path

builder_path = Path("atlas/map_builder.py")

def patch_map_view():
    if not builder_path.exists():
        print("X Error: atlas/map_builder.py not found.")
        return

    content = builder_path.read_text(encoding="utf-8")
    
    # Target the map.fitBounds line
    old_fit = "map.fitBounds(ATLAS.bounds);"
    new_fit = "// map.fitBounds(ATLAS.bounds); // Snapping disabled\n    map.setView([38.0, 30.0], 4);"
    
    if old_fit in content:
        content = content.replace(old_fit, new_fit)
        builder_path.write_text(content, encoding="utf-8")
        print("✓ Successfully disabled auto-snap and set default view to center.")
    else:
        print("X Could not find fitBounds in map_builder.py. It might already be modified.")

if __name__ == "__main__":
    patch_map_view()
    