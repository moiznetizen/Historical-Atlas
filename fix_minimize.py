import sys
from pathlib import Path

builder_path = Path("atlas/map_builder.py")

if builder_path.exists():
    content = builder_path.read_text(encoding="utf-8")
    
    # 1. Update CSS with proper f-string escaping (double curly braces)
    old_css = ".documentary-mode .atlas-panel {{\n  width: min(760px, calc(100vw - 32px));\n}}"
    new_css = """.documentary-mode .atlas-panel {{
  width: min(760px, calc(100vw - 32px));
}}
/* Minimize mechanics */
.atlas-panel {{
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), max-height 0.3s ease;
  max-height: 450px;
}}
.atlas-panel.is-minimized {{
  max-height: 58px;
}}
.atlas-panel.is-minimized .atlas-story,
.atlas-panel.is-minimized .atlas-stats,
.atlas-panel.is-minimized .atlas-legend {{
  display: none !important;
}}
.panel-toggle-btn {{
  width: 38px;
  height: 34px;
  border: 1px solid rgba(95, 27, 22, 0.35);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.46);
  color: var(--direct-dark);
  cursor: pointer;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}}
.panel-toggle-btn:hover {{
  background: var(--direct);
  color: #fff;
}}"""

    if "/* Minimize mechanics */" not in content:
        content = content.replace(old_css, new_css)

    # 2. Inject the HTML toggle button inside the control cluster 
    old_html = '<button class="atlas-button" id="doc-button" title="Toggle documentary mode">D</button>'
    new_html = '<button class="atlas-button" id="doc-button" title="Toggle documentary mode">D</button>\n      <button class="panel-toggle-btn" id="minimize-button" title="Minimize Panel">▼</button>'
    
    if 'id="minimize-button"' not in content:
        content = content.replace(old_html, new_html)

    # 3. Add JavaScript click handlers with proper f-string escaping (double curly braces)
    old_js = 'docButton.addEventListener("click", () => {{\n  document.body.classList.toggle("documentary-mode");\n  docButton.classList.toggle("is-active");\n}});'
    new_js = """docButton.addEventListener("click", () => {{
  document.body.classList.toggle("documentary-mode");
  docButton.classList.toggle("is-active");
}});
const minBtn = document.getElementById("minimize-button");
const atlasPanel = document.querySelector(".atlas-panel");
minBtn.addEventListener("click", () => {{
  const isMin = atlasPanel.classList.toggle("is-minimized");
  minBtn.textContent = isMin ? "▲" : "▼";
  minBtn.title = isMin ? "Expand Panel" : "Minimize Panel";
}});"""

    if "const minBtn =" not in content:
        content = content.replace(old_js, new_js)

    builder_path.write_text(content, encoding="utf-8")
    print("✓ Successfully injected minimize properties into template engine.")

    # 4. Trigger map re-compilation
    print("\nRe-compiling layout assets...")
    try:
        from atlas.map_builder import build_atlas
        build_atlas("ottoman_europe_atlas.html")
        print("✓ Map build successfully reconstructed!")
    except Exception as e:
        print(f"X Build compilation error: {e}")
else:
    print("X Error: atlas/map_builder.py not found.")