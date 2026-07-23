from pathlib import Path

builder_path = Path("atlas/map_builder.py")

if builder_path.exists():
    content = builder_path.read_text(encoding="utf-8")
    
    # Correct the double braces back to single braces so the functions execute properly
    content = content.replace("{{_css()}}", "{_css()}")
    content = content.replace("{{_shell()}}", "{_shell()}")
    content = content.replace("{{_script()}}", "{_script()}")
    
    builder_path.write_text(content, encoding="utf-8")
    print("✓ Successfully repaired brace syntax inside atlas/map_builder.py.")
    
    # Re-compile the map assets to bring back the full map visual interface
    print("\nRe-compiling layout assets...")
    try:
        from atlas.map_builder import build_atlas
        build_atlas("ottoman_europe_atlas.html")
        print("✓ SUCCESS! Your map has been fully recovered.")
    except Exception as e:
        print(f"X Compilation error: {e}")
else:
    print("X Error: Could not locate 'atlas/map_builder.py'.")