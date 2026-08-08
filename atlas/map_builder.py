"""Standalone Leaflet renderer for the Ottoman Europe atlas."""

from __future__ import annotations

import json
from pathlib import Path

from .historical_data import (
    BATTLES,
    BORDER_LINES,
    BOUNDS,
    CAMPAIGNS,
    CITIES,
    EVENTS,
    RIVERS,
    TERRITORIES,
    TIMELINE_END,
    TIMELINE_START,
)
from .styles import POWER_COLORS, css_palette_vars


def _polygon_feature(territory):
    geometry = territory["geometry"]
    is_polygon = isinstance(geometry[0][0], (int, float))
    coordinates = [geometry] if is_polygon else [[ring] for ring in geometry]
    geom_type = "Polygon" if is_polygon else "MultiPolygon"
    return {
        "type": "Feature",
        "geometry": {"type": geom_type, "coordinates": coordinates},
        "properties": {key: value for key, value in territory.items() if key != "geometry"},
    }


def _feature_collection(items):
    return {"type": "FeatureCollection", "features": [_polygon_feature(item) for item in items]}


def _json(value):
    return json.dumps(value, ensure_ascii=False)


def _css():
    legend_items = "\n".join(
        f".legend-{name.lower().replace(' ', '-')} {{ background: {color}; }}"
        for name, color in POWER_COLORS.items()
    )
    return f"""
@import url('https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400&family=Aref+Ruqaa:wght@400;700&family=Reem+Kufi:wght@400;600&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500&display=swap');
:root {{
  {css_palette_vars()}
  --glass: rgba(251, 246, 234, 0.92);
  --glass-strong: rgba(251, 246, 234, 0.98);
  --line: rgba(36, 27, 24, 0.16);
  --line-strong: rgba(36, 27, 24, 0.28);
  --accent: #b8860f;
  --accent-dark: #8a5f0a;
  --turquoise: #178f8c;
  --turquoise-dark: #0f6b68;
  --shadow-sm: 0 2px 8px rgba(28, 20, 16, 0.14);
  --shadow-md: 0 10px 32px rgba(28, 20, 16, 0.18);
  --shadow-lg: 0 22px 60px rgba(28, 20, 16, 0.28);
  --radius-sm: 8px;
  --radius-md: 14px;
  --radius-lg: 18px;
  --water: #b5d0e2;
  --ease: cubic-bezier(0.4, 0, 0.2, 1);
  --motif: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='34' height='34' viewBox='0 0 34 34'%3E%3Cg fill='none' stroke='%23b8860f' stroke-width='1' opacity='0.55'%3E%3Cpath d='M17 2 L26 9 L26 25 L17 32 L8 25 L8 9 Z'/%3E%3Cpath d='M17 2 L17 32 M8 9 L26 25 M26 9 L8 25'/%3E%3C/g%3E%3C/svg%3E");
}}
:root[data-theme="night"] {{
  --paper: #1b2420;
  --ink: #eee6d6;
  --glass: rgba(24, 30, 26, 0.90);
  --glass-strong: rgba(20, 26, 22, 0.96);
  --line: rgba(238, 230, 214, 0.14);
  --line-strong: rgba(238, 230, 214, 0.26);
  --water: #0e1a22;
  --accent: #e0b64a;
  --accent-dark: #f2d488;
  --turquoise: #3fb3af;
  --turquoise-dark: #6fd0cb;
  --shadow-sm: 0 2px 10px rgba(0, 0, 0, 0.35);
  --shadow-md: 0 10px 32px rgba(0, 0, 0, 0.45);
  --shadow-lg: 0 22px 60px rgba(0, 0, 0, 0.55);
  --motif: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='34' height='34' viewBox='0 0 34 34'%3E%3Cg fill='none' stroke='%23e0b64a' stroke-width='1' opacity='0.5'%3E%3Cpath d='M17 2 L26 9 L26 25 L17 32 L8 25 L8 9 Z'/%3E%3Cpath d='M17 2 L17 32 M8 9 L26 25 M26 9 L8 25'/%3E%3C/g%3E%3C/svg%3E");
}}
* {{ box-sizing: border-box; }}
html, body, #map {{
  width: 100%;
  height: 100%;
  margin: 0;
}}
body {{
  background: var(--water);
  color: var(--ink);
  font-family: "Inter", sans-serif;
  transition: background 0.4s var(--ease);
}}
#map {{
  background: var(--water);
  font-family: "Inter", sans-serif;
  transition: background 0.4s var(--ease);
}}
.leaflet-container {{
  font-family: "Inter", sans-serif;
  background: var(--water);
}}
::selection {{ background: var(--accent); color: #fff; }}
.atlas-title, .atlas-panel {{
  position: fixed;
  z-index: 900;
  color: var(--ink);
  background: var(--glass);
  border: 1px solid var(--line);
  box-shadow: var(--shadow-lg);
  backdrop-filter: blur(20px) saturate(1.4);
  -webkit-backdrop-filter: blur(20px) saturate(1.4);
  font-family: "Inter", sans-serif;
  transition: background 0.4s var(--ease), border-color 0.4s var(--ease), box-shadow 0.3s var(--ease), transform 0.3s var(--ease);
  animation: atlasRise 0.6s var(--ease);
}}
@keyframes atlasRise {{
  from {{ opacity: 0; transform: translateY(10px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}
.atlas-title {{
  top: 18px;
  left: 58px;
  width: min(460px, calc(100vw - 76px));
  padding: 20px 22px 20px;
  border-radius: var(--radius-lg);
  border-top: none;
  overflow: hidden;
}}
.atlas-title::before {{
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 6px;
  background: linear-gradient(90deg, var(--turquoise-dark), var(--accent) 35%, var(--accent) 65%, var(--turquoise-dark));
}}
.atlas-title::after {{
  content: "";
  position: absolute;
  inset: 0;
  background-image: var(--motif);
  background-size: 34px 34px;
  opacity: 0.06;
  pointer-events: none;
}}
.atlas-title-collapsible {{
  overflow: hidden;
  max-height: 220px;
  opacity: 1;
  transition: max-height 0.35s var(--ease), opacity 0.25s var(--ease), margin 0.35s var(--ease);
}}
.atlas-title.is-minimized {{
  padding-bottom: 16px;
}}
.atlas-title.is-minimized .atlas-title-flourish,
.atlas-title.is-minimized .atlas-title-translit {{
  display: none;
}}
.atlas-title.is-minimized .atlas-title-collapsible {{
  max-height: 0;
  opacity: 0;
  margin: 0;
}}
.atlas-title-row {{
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 10px;
  position: relative;
}}
.atlas-title-heading {{
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}}
.atlas-rosette {{
  flex-shrink: 0;
  width: 30px;
  height: 30px;
  color: var(--turquoise-dark);
  opacity: 0.85;
}}
.atlas-title-actions {{
  display: flex;
  gap: 6px;
  flex-shrink: 0;
  position: relative;
}}
.icon-toggle-btn {{
  width: 30px;
  height: 30px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.35);
  color: var(--accent-dark);
  cursor: pointer;
  font-size: 14px;
  transition: transform 0.2s var(--ease), background 0.2s var(--ease), box-shadow 0.2s var(--ease);
}}
:root[data-theme="night"] .icon-toggle-btn {{
  background: rgba(255, 255, 255, 0.06);
}}
.icon-toggle-btn:hover {{
  background: var(--accent);
  color: #fff;
  transform: translateY(-1px) scale(1.05);
  box-shadow: var(--shadow-sm);
}}
.icon-toggle-btn.is-active {{
  background: var(--accent-dark);
  color: #fff;
  border-color: var(--accent-dark);
}}
.atlas-title h1 {{
  margin: 0;
  font-family: 'Aref Ruqaa', 'Amiri', serif;
  font-size: clamp(32px, 3.4vw, 44px);
  font-weight: 700;
  letter-spacing: 0;
  line-height: 1.35;
  direction: rtl;
  background: linear-gradient(120deg, var(--accent-dark) 0%, var(--accent) 45%, var(--turquoise-dark) 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  color: var(--accent-dark);
  filter: drop-shadow(0 1px 0 rgba(255, 255, 255, 0.5));
}}
:root[data-theme="night"] .atlas-title h1 {{ filter: none; }}
.atlas-title-flourish {{
  display: block;
  width: 100%;
  height: 10px;
  margin-top: 2px;
  color: var(--accent);
  opacity: 0.8;
}}
.atlas-title-translit {{
  margin: 2px 0 0;
  font-family: 'Amiri', serif;
  font-style: italic;
  font-size: 12.5px;
  letter-spacing: 0.04em;
  color: var(--turquoise-dark);
  opacity: 0.9;
}}
.atlas-title p {{
  margin: 10px 0 0;
  color: rgba(36, 27, 24, 0.72);
  font-size: 12.5px;
  line-height: 1.55;
  font-family: "Inter", sans-serif;
  position: relative;
}}
:root[data-theme="night"] .atlas-title p {{ color: rgba(238, 230, 214, 0.68); }}
.atlas-shortcut-hint {{
  margin-top: 10px;
  font-size: 10.5px;
  letter-spacing: 0.02em;
  color: rgba(36, 27, 24, 0.5);
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  position: relative;
}}
:root[data-theme="night"] .atlas-shortcut-hint {{ color: rgba(238, 230, 214, 0.45); }}
.atlas-shortcut-hint kbd {{
  font-family: "JetBrains Mono", monospace;
  background: rgba(36, 27, 24, 0.08);
  border: 1px solid var(--line);
  border-radius: 4px;
  padding: 1px 5px;
  font-size: 10px;
}}
:root[data-theme="night"] .atlas-shortcut-hint kbd {{ background: rgba(238, 230, 214, 0.08); }}
.atlas-search {{
  position: relative;
  margin-top: 12px;
  font: 12px Inter, sans-serif;
}}
.atlas-search::before {{
  content: "";
  position: absolute;
  left: 10px;
  top: 50%;
  width: 13px;
  height: 13px;
  transform: translateY(-50%);
  background: var(--accent-dark);
  opacity: 0.55;
  -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2.5'%3E%3Ccircle cx='11' cy='11' r='7'/%3E%3Cline x1='21' y1='21' x2='16.65' y2='16.65'/%3E%3C/svg%3E") center/contain no-repeat;
  mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2.5'%3E%3Ccircle cx='11' cy='11' r='7'/%3E%3Cline x1='21' y1='21' x2='16.65' y2='16.65'/%3E%3C/svg%3E") center/contain no-repeat;
  pointer-events: none;
}}
.atlas-search span {{ display: none; }}
.atlas-search input {{
  width: 100%;
  border: 1px solid var(--line);
  border-radius: 9px;
  padding: 9px 12px 9px 32px;
  background: rgba(255, 255, 255, 0.5);
  color: var(--ink);
  font: 13px Inter, sans-serif;
  transition: border-color 0.2s var(--ease), background 0.2s var(--ease), box-shadow 0.2s var(--ease);
}}
:root[data-theme="night"] .atlas-search input {{ background: rgba(255, 255, 255, 0.06); }}
.atlas-search input:focus {{
  outline: none;
  border-color: var(--accent);
  background: rgba(255, 255, 255, 0.8);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent) 22%, transparent);
}}
:root[data-theme="night"] .atlas-search input:focus {{ background: rgba(255, 255, 255, 0.1); }}
.atlas-panel {{
  left: 50%;
  bottom: 18px;
  transform: translateX(-50%);
  width: min(960px, calc(100vw - 32px));
  border-radius: var(--radius-lg);
  overflow: hidden;
  transition: transform 0.35s var(--ease), max-height 0.35s var(--ease), background 0.4s var(--ease), border-color 0.4s var(--ease);
  max-height: 420px;
  display: flex;
  flex-direction: column;
  position: fixed;
}}
.atlas-panel::before {{
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--turquoise-dark), var(--accent) 35%, var(--accent) 65%, var(--turquoise-dark));
  z-index: 1;
}}
.atlas-panel.is-minimized {{
  max-height: 58px;
}}
.atlas-panel.is-minimized .atlas-tabs,
.atlas-panel.is-minimized .atlas-tab-panel {{
  display: none !important;
}}
.panel-toggle-btn {{
  width: 36px;
  height: 34px;
  border: 1px solid var(--line-strong);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.4);
  color: var(--accent-dark);
  cursor: pointer;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-family: Inter, sans-serif;
  transition: transform 0.2s var(--ease), background 0.2s var(--ease);
}}
:root[data-theme="night"] .panel-toggle-btn {{ background: rgba(255, 255, 255, 0.06); }}
.panel-toggle-btn:hover {{
  background: var(--accent);
  color: #fff;
  transform: translateY(-1px);
}}
.atlas-controls {{
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 14px;
  align-items: center;
  padding: 14px 16px 10px;
  flex-shrink: 0;
}}
.atlas-year {{
  min-width: 74px;
  color: var(--accent-dark);
  font-family: "JetBrains Mono", "Inter", sans-serif;
  font-size: 23px;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
  transition: color 0.4s var(--ease);
}}
.atlas-year-wrap {{
  display: flex;
  flex-direction: column;
  gap: 2px;
}}
.atlas-visible-chip {{
  font-family: "JetBrains Mono", "Inter", sans-serif;
  font-size: 9.5px;
  font-weight: 600;
  letter-spacing: 0.01em;
  color: var(--accent-dark);
  opacity: 0.62;
  white-space: nowrap;
  font-variant-numeric: tabular-nums;
}}
#atlas-slider {{
  width: 100%;
  accent-color: var(--accent);
  cursor: pointer;
}}
.atlas-buttons {{
  display: flex;
  gap: 7px;
}}
.atlas-button {{
  width: 36px;
  height: 34px;
  border: 1px solid var(--line-strong);
  border-radius: 8px;
  color: var(--accent-dark);
  background: rgba(255, 255, 255, 0.4);
  cursor: pointer;
  font-family: Inter, sans-serif;
  font-weight: 700;
  transition: transform 0.15s var(--ease), background 0.2s var(--ease), color 0.2s var(--ease), box-shadow 0.2s var(--ease);
}}
:root[data-theme="night"] .atlas-button {{ background: rgba(255, 255, 255, 0.06); }}
.atlas-button:hover {{
  background: var(--accent);
  color: #fff;
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}}
.atlas-button:active {{ transform: translateY(0) scale(0.94); }}
.atlas-button.is-active {{
  color: #fff;
  background: var(--accent);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent) 25%, transparent);
}}
#play-button.is-active {{ animation: playPulse 1.6s ease-in-out infinite; }}
@keyframes playPulse {{
  0%, 100% {{ box-shadow: 0 0 0 0 color-mix(in srgb, var(--accent) 45%, transparent); }}
  50% {{ box-shadow: 0 0 0 6px color-mix(in srgb, var(--accent) 0%, transparent); }}
}}
.atlas-speed {{
  width: 78px;
  height: 34px;
  border: 1px solid var(--line-strong);
  border-radius: 8px;
  color: var(--accent-dark);
  background: rgba(255, 255, 255, 0.4);
  font: 12px Inter, sans-serif;
  cursor: pointer;
}}
:root[data-theme="night"] .atlas-speed {{ background: rgba(255, 255, 255, 0.06); }}
.atlas-tabs {{
  display: flex;
  gap: 2px;
  padding: 0 16px;
  border-top: 1px solid var(--line);
  border-bottom: 1px solid var(--line);
  background: rgba(255, 255, 255, 0.14);
  flex-shrink: 0;
}}
:root[data-theme="night"] .atlas-tabs {{ background: rgba(0, 0, 0, 0.14); }}
.atlas-tab-btn {{
  border: none;
  background: transparent;
  color: rgba(36, 27, 24, 0.58);
  font: 600 12px Inter, sans-serif;
  padding: 10px 14px;
  cursor: pointer;
  position: relative;
  letter-spacing: 0.01em;
  transition: color 0.2s var(--ease);
}}
:root[data-theme="night"] .atlas-tab-btn {{ color: rgba(238, 230, 214, 0.5); }}
.atlas-tab-btn::after {{
  content: "";
  position: absolute;
  left: 14px;
  right: 14px;
  bottom: -1px;
  height: 2px;
  background: var(--accent);
  transform: scaleX(0);
  transition: transform 0.25s var(--ease);
}}
.atlas-tab-btn:hover {{ color: var(--accent-dark); }}
.atlas-tab-btn.is-active {{ color: var(--accent-dark); }}
.atlas-tab-btn.is-active::after {{ transform: scaleX(1); }}
.atlas-tab-panel {{
  overflow-y: auto;
  animation: tabFade 0.25s var(--ease);
}}
@keyframes tabFade {{
  from {{ opacity: 0; transform: translateY(4px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}
.atlas-tab-panel::-webkit-scrollbar {{ width: 8px; height: 8px; }}
.atlas-tab-panel::-webkit-scrollbar-thumb {{ background: var(--line-strong); border-radius: 6px; }}
.atlas-tab-panel::-webkit-scrollbar-track {{ background: transparent; }}
.atlas-filter-bar {{
  display: flex;
  gap: 14px;
  align-items: center;
  padding: 14px 16px;
  font: 12px Inter, sans-serif;
  flex-wrap: wrap;
}}
.atlas-filter-bar > span {{
  font-weight: 700;
  color: var(--accent-dark);
  margin-right: 4px;
  font-family: Inter, sans-serif;
}}
.filter-group {{
  display: inline-flex;
  gap: 6px;
  align-items: center;
  flex-wrap: wrap;
}}
.filter-chip {{
  padding: 5px 12px;
  border: 1px solid var(--line-strong);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.4);
  color: var(--accent-dark);
  cursor: pointer;
  font: 11px Inter, sans-serif;
  transition: transform 0.15s var(--ease), background 0.2s var(--ease), color 0.2s var(--ease), box-shadow 0.2s var(--ease);
}}
:root[data-theme="night"] .filter-chip {{ background: rgba(255, 255, 255, 0.06); }}
.filter-chip:hover {{ transform: translateY(-1px); box-shadow: var(--shadow-sm); }}
.filter-chip.is-active {{
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
}}
.atlas-checkbox-label {{
  display: inline-flex;
  gap: 6px;
  align-items: center;
  cursor: pointer;
  font-weight: 600;
  color: var(--accent-dark);
}}
.territory-opacity-group {{
  gap: 8px;
}}
.territory-opacity-group input[type="range"] {{
  width: 100px;
  accent-color: var(--accent);
  cursor: pointer;
}}
.territory-opacity-value {{
  font: 600 11px "JetBrains Mono", "Inter", sans-serif;
  color: var(--accent-dark);
  min-width: 34px;
}}
.battle-period-box {{
  width: 208px;
  color: var(--ink);
  background: var(--glass);
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
  backdrop-filter: blur(20px) saturate(1.4);
  -webkit-backdrop-filter: blur(20px) saturate(1.4);
  font-family: "Inter", sans-serif;
  margin-bottom: 10px;
  overflow: hidden;
  transition: background 0.4s var(--ease), border-color 0.4s var(--ease);
}}
.battle-period-header {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 9px 10px 9px 12px;
  font-size: 12px;
  font-weight: 700;
  color: var(--accent-dark);
  border-bottom: 1px solid var(--line);
}}
.battle-period-box.is-minimized .battle-period-header {{ border-bottom: none; }}
.battle-period-toggle {{
  width: 24px;
  height: 24px;
  border: 1px solid var(--line-strong);
  border-radius: 7px;
  background: rgba(255, 255, 255, 0.4);
  color: var(--accent-dark);
  cursor: pointer;
  font-size: 11px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s var(--ease), color 0.2s var(--ease);
}}
:root[data-theme="night"] .battle-period-toggle {{ background: rgba(255, 255, 255, 0.06); }}
.battle-period-toggle:hover {{ background: var(--accent); color: #fff; }}
.battle-period-body {{
  padding: 10px 12px 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}}
.battle-period-box.is-minimized .battle-period-body {{ display: none; }}
.battle-period-row {{
  display: flex;
  gap: 8px;
}}
.battle-period-row label {{
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 3px;
  font-size: 10.5px;
  font-weight: 600;
  color: var(--accent-dark);
}}
.battle-period-row input {{
  width: 100%;
  padding: 6px 7px;
  border: 1px solid var(--line-strong);
  border-radius: 7px;
  background: rgba(255, 255, 255, 0.5);
  color: var(--ink);
  font: 12px "JetBrains Mono", "Inter", sans-serif;
}}
:root[data-theme="night"] .battle-period-row input {{ background: rgba(255, 255, 255, 0.08); }}
.battle-period-row input:focus {{
  outline: none;
  border-color: var(--accent);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent) 22%, transparent);
}}
.battle-period-actions {{
  display: flex;
  gap: 6px;
}}
.battle-period-actions .filter-chip {{ flex: 1; text-align: center; }}
.battle-period-status {{
  font-size: 10px;
  color: var(--accent-dark);
  opacity: 0.75;
  min-height: 12px;
}}
.atlas-checkbox-label input {{ accent-color: var(--accent); cursor: pointer; }}
.atlas-story {{
  display: grid;
  grid-template-columns: auto 1fr;
  align-items: baseline;
  gap: 6px 14px;
  padding: 16px;
  font-size: 13px;
  line-height: 1.6;
  font-family: Inter, sans-serif;
}}
.atlas-story strong {{
  color: var(--accent-dark);
  font-family: 'Amiri', serif;
  font-size: 17px;
  font-weight: 700;
  white-space: nowrap;
}}
.atlas-story span {{ color: var(--ink); opacity: 0.88; }}
.atlas-legend {{
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 12px 16px 16px;
}}
.legend-search {{
  width: 100%;
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 7px 10px;
  background: rgba(255, 255, 255, 0.5);
  color: var(--ink);
  font: 12px Inter, sans-serif;
}}
:root[data-theme="night"] .legend-search {{ background: rgba(255, 255, 255, 0.06); }}
.legend-search:focus {{ outline: none; border-color: var(--accent); }}
.legend-grid {{
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  font: 12px/1.4 Inter, sans-serif;
}}
.atlas-stats {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
  gap: 8px;
  padding: 14px 16px;
}}
.atlas-stats span {{
  display: grid;
  gap: 3px;
  padding: 10px 12px;
  background: rgba(255, 255, 255, 0.28);
  border: 1px solid var(--line);
  border-radius: 10px;
  transition: transform 0.2s var(--ease), background 0.2s var(--ease);
}}
:root[data-theme="night"] .atlas-stats span {{ background: rgba(255, 255, 255, 0.04); }}
.atlas-stats span:hover {{ transform: translateY(-2px); background: rgba(255, 255, 255, 0.5); }}
:root[data-theme="night"] .atlas-stats span:hover {{ background: rgba(255, 255, 255, 0.08); }}
.atlas-stats b {{
  color: rgba(36, 27, 24, 0.55);
  font-size: 9.5px;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  font-family: Inter, sans-serif;
}}
:root[data-theme="night"] .atlas-stats b {{ color: rgba(238, 230, 214, 0.5); }}
.atlas-stats em {{
  min-width: 0;
  overflow: hidden;
  color: var(--accent-dark);
  font-size: 13px;
  font-weight: 700;
  font-style: normal;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-family: Inter, sans-serif;
  transition: color 0.3s var(--ease);
}}
.legend-chip {{
  display: inline-flex;
  gap: 6px;
  align-items: center;
  transition: opacity 0.2s var(--ease);
}}
.legend-swatch {{
  width: 16px;
  height: 11px;
  border: 1px solid rgba(36, 27, 24, 0.28);
  border-radius: 3px;
  flex-shrink: 0;
}}
.atlas-tooltip {{
  max-width: 290px;
  font-family: "Inter", sans-serif;
  line-height: 1.45;
}}
.atlas-tooltip b {{
  color: #5f1b16;
  font-family: 'Amiri', serif;
  font-size: 15px;
  font-weight: 700;
}}
.city-marker, .mecca-marker, .constantinople-marker, .edirne-marker, .bursa-marker, .vienna-marker, .fortress-marker, .battle-marker, .naval-marker, .treaty-marker, .raid-marker, .siege-marker, .raid-siege-marker, .sacked-marker, .revolt-marker, .mountain-marker, .forest-marker, .steppe-marker, .bridge-marker, .pass-marker, .iron-gates-marker {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  filter: drop-shadow(0 1px 2px rgba(44, 44, 42, 0.4));
}}
.anatolia-map-label {{
  color: rgba(36, 27, 24, 0.55);
  font-family: "Inter", sans-serif;
  font-weight: 700;
  font-size: 11px;
  letter-spacing: 2px;
  text-transform: uppercase;
  text-align: center;
  pointer-events: none;
  white-space: nowrap;
}}
.territory-label {{
  color: rgba(20, 32, 27, 0.86);
  font: 700 11px/1.15 Inter, sans-serif;
  text-align: center;
  text-transform: uppercase;
  text-shadow: 0 1px 0 rgba(251, 246, 234, 0.95), 0 -1px 0 rgba(251, 246, 234, 0.95), 1px 0 0 rgba(251, 246, 234, 0.95), -1px 0 0 rgba(251, 246, 234, 0.95);
  pointer-events: none;
}}
.territory-label.vassal {{
  color: rgba(28, 83, 53, 0.88);
}}
.territory-label.neighbour {{
  color: rgba(70, 73, 69, 0.76);
}}
.coord-readout, .fullscreen-faux {{
  padding: 6px 9px;
  border-radius: 7px;
  background: var(--glass);
  color: var(--ink);
  box-shadow: var(--shadow-sm);
  font: 12px "JetBrains Mono", "Inter", sans-serif;
  border: 1px solid var(--line);
  transition: background 0.4s var(--ease), color 0.4s var(--ease);
}}
.fullscreen-faux {{
  cursor: pointer;
  font-weight: 700;
  font-family: Inter, sans-serif;
  transition: transform 0.2s var(--ease), background 0.2s var(--ease), color 0.2s var(--ease);
}}
.fullscreen-faux:hover {{
  background: var(--accent);
  color: #fff;
  transform: scale(1.06);
}}
.documentary-mode .leaflet-control-container {{
  opacity: 0.18;
  transition: opacity 0.4s var(--ease);
}}
.is-exporting .leaflet-control-container {{
  opacity: 0 !important;
}}
.documentary-mode .atlas-title {{
  width: min(560px, calc(100vw - 36px));
}}
.documentary-mode .atlas-panel {{
  width: min(760px, calc(100vw - 32px));
}}

/* --- Marker + territory transition polish --- */
.leaflet-marker-icon {{
  animation: markerPop 0.4s var(--ease);
}}
@keyframes markerPop {{
  from {{ opacity: 0; transform: scale(0.4); }}
  to {{ opacity: 1; transform: scale(1); }}
}}
path.leaflet-interactive {{
  transition: fill-opacity 0.25s var(--ease), stroke-width 0.2s var(--ease), stroke-opacity 0.2s var(--ease);
}}

/* --- Loading overlay --- */
#atlas-loader {{
  position: fixed;
  inset: 0;
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap: 14px;
  background: radial-gradient(circle at 50% 40%, #dcd0b0 0%, #b5d0e2 75%);
  transition: opacity 0.6s var(--ease), visibility 0.6s;
}}
#atlas-loader.is-hidden {{
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
}}
.loader-mark {{
  width: 54px;
  height: 54px;
  border-radius: 50%;
  border: 3px solid rgba(36, 27, 24, 0.18);
  border-top-color: var(--direct);
  animation: loaderSpin 0.9s linear infinite;
}}
@keyframes loaderSpin {{
  to {{ transform: rotate(360deg); }}
}}
.loader-text {{
  font-family: 'Aref Ruqaa', 'Amiri', serif;
  font-size: 22px;
  color: var(--direct-dark);
  letter-spacing: 0.02em;
}}

/* --- Toast for search / navigation feedback --- */
.atlas-toast {{
  position: fixed;
  top: 18px;
  left: 50%;
  transform: translateX(-50%) translateY(-12px);
  z-index: 1500;
  background: var(--glass-strong);
  color: var(--ink);
  border: 1px solid var(--line);
  box-shadow: var(--shadow-md);
  border-radius: 10px;
  padding: 8px 16px;
  font: 600 12.5px Inter, sans-serif;
  opacity: 0;
  transition: opacity 0.25s var(--ease), transform 0.25s var(--ease);
  pointer-events: none;
}}
.atlas-toast.is-visible {{
  opacity: 1;
  transform: translateX(-50%) translateY(0);
}}

/* --- Ottoman imperial emblem --- */
.ottoman-emblem {{
  position: fixed;
  z-index: 850;
  top: 18px;
  left: 50%;
  transform: translateX(-50%);
  width: 66px;
  height: 66px;
  filter: drop-shadow(0 4px 14px rgba(0, 0, 0, 0.35));
  opacity: 0.92;
  animation: atlasRise 0.7s var(--ease);
  transition: transform 0.25s var(--ease), opacity 0.4s var(--ease);
  cursor: default;
}}
.ottoman-emblem:hover {{
  transform: translateX(-50%) scale(1.08);
}}
@media (max-width: 980px) {{
  .ottoman-emblem {{ display: none; }}
}}

/* --- Responsive layout --- */
@media (max-width: 760px) {{
  .atlas-title {{
    left: 54px;
    right: 12px;
    top: 12px;
    width: auto;
    padding: 12px 14px 14px;
  }}
  .atlas-title h1 {{ font-size: 22px; }}
  .atlas-title-translit {{ font-size: 10.5px; }}
  .atlas-rosette {{ width: 22px; height: 22px; }}
  .atlas-title p {{ display: none; }}
  .atlas-shortcut-hint {{ display: none; }}
  .atlas-panel {{
    left: 8px;
    right: 8px;
    bottom: 8px;
    width: auto;
    transform: none;
    max-height: 50vh;
  }}
  .atlas-controls {{
    grid-template-columns: auto 1fr;
    row-gap: 8px;
  }}
  .atlas-buttons {{ grid-column: 1 / -1; justify-content: space-between; }}
  .atlas-speed {{ display: none; }}
  .atlas-stats {{ grid-template-columns: repeat(2, 1fr); }}
  .atlas-story {{ grid-template-columns: 1fr; }}
  .leaflet-control-layers {{
    max-height: 40vh;
    overflow-y: auto;
    font-size: 12px;
    max-width: 46vw;
  }}
}}

/* --- Reduced motion: honor prefers-reduced-motion system setting --- */
@media (prefers-reduced-motion: reduce) {{
  *, *::before, *::after {{
    animation-duration: 0.001ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.001ms !important;
    scroll-behavior: auto !important;
  }}
  #play-button.is-active {{ animation: none !important; }}
  .leaflet-marker-icon {{ animation: none !important; }}
}}

/* --- Timeline: era ticks + Golden Age highlight band --- */
.atlas-slider-wrap {{ position: relative; width: 100%; }}
.golden-age-band {{
  position: absolute;
  top: 50%;
  height: 8px;
  transform: translateY(-50%);
  border-radius: 4px;
  background: linear-gradient(90deg, rgba(184,134,15,0.04), rgba(224,182,74,0.6), rgba(184,134,15,0.04));
  box-shadow: 0 0 10px 2px rgba(224,182,74,0.45);
  pointer-events: none;
  z-index: 1;
  display: none;
}}
.era-ticks {{
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 0;
  pointer-events: none;
  z-index: 2;
}}
.era-tick {{
  position: absolute;
  top: -13px;
  width: 2px;
  height: 14px;
  background: var(--accent-dark);
  opacity: 0.7;
  transform: translateX(-1px);
  pointer-events: auto;
  cursor: pointer;
}}
.era-tick::after {{
  content: attr(data-label);
  position: absolute;
  bottom: 18px;
  left: 50%;
  transform: translateX(-50%);
  white-space: nowrap;
  background: var(--glass-strong);
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 3px 7px;
  font: 600 10.5px "JetBrains Mono", monospace;
  color: var(--accent-dark);
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.15s var(--ease);
}}
.era-tick:hover::after {{ opacity: 1; }}
.era-tick:hover {{ opacity: 1; background: var(--accent); }}

/* --- Sultan tughra / monogram badge --- */
.sultan-badge {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  margin-left: 6px;
  font-family: 'Aref Ruqaa', 'Amiri', serif;
  font-weight: 700;
  font-size: 12px;
  color: #fff;
  background: linear-gradient(135deg, var(--accent), var(--accent-dark));
  box-shadow: var(--shadow-sm);
  vertical-align: middle;
  transition: background 0.4s var(--ease);
}}

/* --- Click-to-lock info card (territories & battles) --- */
.info-card {{
  position: fixed;
  z-index: 1300;
  top: 90px;
  right: 18px;
  width: min(300px, calc(100vw - 36px));
  background: var(--glass-strong);
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  padding: 16px 34px 16px 18px;
  color: var(--ink);
  font-family: "Inter", sans-serif;
  display: none;
}}
.info-card.is-visible {{ display: block; animation: atlasRise 0.3s var(--ease); }}
.info-card h3 {{
  margin: 0 0 6px;
  font-family: 'Amiri', serif;
  font-size: 17px;
  color: var(--accent-dark);
}}
.info-card p {{ margin: 4px 0; font-size: 12.5px; line-height: 1.5; }}
.info-card-close {{
  position: absolute;
  top: 10px;
  right: 10px;
  width: 22px;
  height: 22px;
  border: none;
  border-radius: 50%;
  background: rgba(36,27,24,0.08);
  color: var(--ink);
  cursor: pointer;
  font-size: 13px;
  line-height: 1;
}}
.info-card-close:hover {{ background: var(--accent); color: #fff; }}

/* --- Compare mode panel --- */
.compare-panel {{
  position: fixed;
  z-index: 1300;
  top: 90px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--glass-strong);
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  padding: 14px 18px;
  display: none;
  gap: 10px;
  align-items: center;
  font: 12px Inter, sans-serif;
  color: var(--ink);
}}
.compare-panel.is-visible {{ display: flex; flex-wrap: wrap; }}
.compare-panel label {{ display: inline-flex; gap: 6px; align-items: center; }}
.compare-panel input {{
  width: 66px;
  padding: 6px 8px;
  border: 1px solid var(--line-strong);
  border-radius: 7px;
  background: rgba(255,255,255,0.5);
  color: var(--ink);
  font: 12px "JetBrains Mono", monospace;
}}
.compare-panel button {{
  border: 1px solid var(--line-strong);
  border-radius: 7px;
  background: var(--accent);
  color: #fff;
  padding: 6px 12px;
  cursor: pointer;
  font: 600 12px Inter, sans-serif;
}}
.compare-panel button#compare-exit {{ background: transparent; color: var(--accent-dark); }}
.compare-legend {{ display: flex; gap: 10px; font-size: 11px; }}
.compare-legend span {{ display: inline-flex; align-items: center; gap: 4px; }}
.compare-swatch {{ width: 12px; height: 12px; border-radius: 3px; display: inline-block; }}

{legend_items}
"""


def _shell():
    legend = "".join(
        f'<span class="legend-chip"><span class="legend-swatch" style="background:{color}"></span>{name}</span>'
        for name, color in POWER_COLORS.items()
    )
    city_svg_legend = '<svg width="18" height="18" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle;"><circle cx="30" cy="30" r="15" fill="none" stroke="#2c2c2a" stroke-width="2"/><circle cx="30" cy="30" r="8" fill="#2c2c2a"/></svg>'
    fortress_svg_legend = '<svg width="18" height="18" viewBox="0 0 200 196" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle;"><polygon points="7,189 15,127 33,127 33,91 51,47 69,91 69,127 81,139 93,95 105,139 117,127 117,91 135,47 153,91 153,127 171,127 179,189" fill="#8c8c8c"/><polygon points="14,182 22,120 40,120 40,84 58,40 76,84 76,120 88,132 100,88 112,132 124,120 124,84 142,40 160,84 160,120 178,120 186,182" fill="#e5e5e5" stroke="#111111" stroke-width="6" stroke-linejoin="round"/><line x1="58" y1="40" x2="58" y2="13" stroke="#111111" stroke-width="4" stroke-linecap="round"/><path d="M58,13 C68,9 72,19 82,15 C74,23 68,17 58,21 Z" fill="#e5e5e5" stroke="#111111" stroke-width="3"/><line x1="142" y1="40" x2="142" y2="13" stroke="#111111" stroke-width="4" stroke-linecap="round"/><path d="M142,13 C152,9 156,19 166,15 C158,23 152,17 142,21 Z" fill="#e5e5e5" stroke="#111111" stroke-width="3"/><path d="M51,72 L51,62 A7,7 0 0 1 65,62 L65,72 Z" fill="#111111"/><path d="M135,72 L135,62 A7,7 0 0 1 149,62 L149,72 Z" fill="#111111"/><path d="M94,110 L94,102 A6,6 0 0 1 106,102 L106,110 Z" fill="#111111"/><path d="M82,182 L82,155 A18,18 0 0 1 118,155 L118,182 Z" fill="#111111"/><polygon points="50,160 58,146 58,174" fill="#111111"/><polygon points="70,160 62,146 62,174" fill="#111111"/><polygon points="130,160 138,146 138,174" fill="#111111"/><polygon points="150,160 142,146 142,174" fill="#111111"/></svg>'
    vienna_svg_legend = '<svg width="18" height="18" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle;"><polygon points="11,191 175,191 189,203 5,203" fill="#8c8c8c"/><polygon points="18,62 45,27 72,62" fill="#8c8c8c"/><polygon points="128,62 155,27 182,62" fill="#8c8c8c"/><rect x="18" y="62" width="40" height="129" fill="#8c8c8c"/><rect x="128" y="62" width="40" height="129" fill="#8c8c8c"/><polygon points="58,127 93,102 128,127 128,191 58,191" fill="#8c8c8c"/><polygon points="18,184 182,184 188,196 12,196" fill="#e5e5e5" stroke="#111111" stroke-width="5" stroke-linejoin="round"/><polygon points="18,55 45,20 72,55" fill="#e5e5e5" stroke="#111111" stroke-width="5" stroke-linejoin="round"/><polygon points="128,55 155,20 182,55" fill="#e5e5e5" stroke="#111111" stroke-width="5" stroke-linejoin="round"/><rect x="25" y="55" width="40" height="129" fill="#e5e5e5" stroke="#111111" stroke-width="5"/><rect x="135" y="55" width="40" height="129" fill="#e5e5e5" stroke="#111111" stroke-width="5"/><polygon points="65,120 100,95 135,120 135,184 65,184" fill="#e5e5e5" stroke="#111111" stroke-width="5" stroke-linejoin="round"/><circle cx="45" cy="90" r="7" fill="#111111"/><circle cx="45" cy="130" r="7" fill="#111111"/><circle cx="155" cy="90" r="7" fill="#111111"/><circle cx="155" cy="130" r="7" fill="#111111"/><path d="M88,184 L88,158 A12,12 0 0 1 112,158 L112,184 Z" fill="#111111"/></svg>'
    land_svg_legend = '<svg width="18" height="18" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle;"><line x1="10" y1="10" x2="50" y2="50" stroke="#2c2c2a" stroke-width="5" stroke-linecap="round"/><line x1="10" y1="50" x2="50" y2="10" stroke="#2c2c2a" stroke-width="5" stroke-linecap="round"/><circle cx="30" cy="30" r="4" fill="#2c2c2a"/></svg>'
    naval_svg_legend = '<svg width="18" height="18" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle;"><circle cx="30" cy="9" r="5.5" fill="none" stroke="#2c2c2a" stroke-width="2.5"/><line x1="30" y1="14.5" x2="30" y2="42" stroke="#2c2c2a" stroke-width="3.5" stroke-linecap="round"/><line x1="16" y1="21" x2="44" y2="21" stroke="#2c2c2a" stroke-width="3" stroke-linecap="round"/><path d="M30,42 Q14,44 12,30" fill="none" stroke="#2c2c2a" stroke-width="3" stroke-linecap="round"/><path d="M30,42 Q46,44 48,30" fill="none" stroke="#2c2c2a" stroke-width="3" stroke-linecap="round"/></svg>'
    treaty_svg_legend = '<svg width="18" height="18" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle;"><rect x="16" y="18" width="28" height="22" fill="none" stroke="#2c2c2a" stroke-width="2"/><ellipse cx="16" cy="29" rx="3" ry="11" fill="none" stroke="#2c2c2a" stroke-width="2"/><ellipse cx="44" cy="29" rx="3" ry="11" fill="none" stroke="#2c2c2a" stroke-width="2"/><line x1="22" y1="24" x2="38" y2="24" stroke="#2c2c2a" stroke-width="1.5"/><line x1="22" y1="29" x2="38" y2="29" stroke="#2c2c2a" stroke-width="1.5"/><line x1="22" y1="34" x2="38" y2="34" stroke="#2c2c2a" stroke-width="1.5"/><line x1="30" y1="40" x2="30" y2="46" stroke="#2c2c2a" stroke-width="2"/><circle cx="30" cy="49" r="5" fill="#2c2c2a"/></svg>'
    raid_svg_legend = '<svg width="18" height="18" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle;"><line x1="10" y1="15" x2="50" y2="45" stroke="#2c2c2a" stroke-width="5" stroke-linecap="round"/><line x1="10" y1="45" x2="50" y2="15" stroke="#2c2c2a" stroke-width="5" stroke-linecap="round"/><polygon points="50,10 68,16 50,23" fill="#2c2c2a"/><polygon points="10,10 -8,16 10,23" fill="#2c2c2a"/></svg>'
    siege_svg_legend = '<svg width="18" height="18" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle;"><circle cx="30" cy="30" r="27" fill="none" stroke="#2c2c2a" stroke-width="2"/><rect x="18" y="18" width="24" height="24" fill="none" stroke="#2c2c2a" stroke-width="2"/><line x1="18" y1="18" x2="42" y2="42" stroke="#2c2c2a" stroke-width="1.5"/><line x1="18" y1="42" x2="42" y2="18" stroke="#2c2c2a" stroke-width="1.5"/></svg>'
    raid_siege_svg_legend = '<svg width="18" height="18" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle;"><defs><marker id="arrowLegend" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#2c2c2a" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs><circle cx="30" cy="30" r="27" fill="none" stroke="#2c2c2a" stroke-width="2" stroke-linecap="round" stroke-dasharray="135 180" transform="rotate(140 30 30)"/><line x1="30" y1="30" x2="52" y2="52" stroke="#2c2c2a" stroke-width="2" marker-end="url(#arrowLegend)"/></svg>'
    sacked_svg_legend = '<svg width="18" height="18" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle;"><line x1="42" y1="30" x2="58" y2="30" stroke="#2c2c2a" stroke-width="4" stroke-linecap="round"/><line x1="38.5" y1="38.5" x2="49.8" y2="49.8" stroke="#2c2c2a" stroke-width="4" stroke-linecap="round"/><line x1="30" y1="42" x2="30" y2="58" stroke="#2c2c2a" stroke-width="4" stroke-linecap="round"/><line x1="21.5" y1="38.5" x2="10.2" y2="49.8" stroke="#2c2c2a" stroke-width="4" stroke-linecap="round"/><line x1="18" y1="30" x2="2" y2="30" stroke="#2c2c2a" stroke-width="4" stroke-linecap="round"/><line x1="21.5" y1="21.5" x2="10.2" y2="10.2" stroke="#2c2c2a" stroke-width="4" stroke-linecap="round"/><line x1="30" y1="18" x2="30" y2="2" stroke="#2c2c2a" stroke-width="4" stroke-linecap="round"/><line x1="38.5" y1="21.5" x2="49.8" y2="10.2" stroke="#2c2c2a" stroke-width="4" stroke-linecap="round"/></svg>'
    revolt_svg_legend = '<svg width="18" height="18" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle;"><rect x="23" y="38" width="14" height="16" rx="3" fill="#2c2c2a"/><rect x="15" y="24" width="30" height="18" rx="8" fill="#2c2c2a"/><circle cx="21" cy="18" r="7" fill="#2c2c2a"/><circle cx="30" cy="14" r="8" fill="#2c2c2a"/><circle cx="39" cy="18" r="7" fill="#2c2c2a"/><path d="M13,30 C10,25 14,19 20,20 L24,25 L15,34 Z" fill="#2c2c2a"/></svg>'
    campaign_svg_legend = '<svg width="18" height="18" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle;"><defs><marker id="arrowLegend" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#2c2c2a" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs><path d="M4,38 L16,20 L28,45 L40,20 L52,45 L58,38" fill="none" stroke="#2c2c2a" stroke-width="3" stroke-dasharray="6 4" marker-end="url(#arrowLegend)"/></svg>'
    mountain_svg_legend = '<svg width="18" height="18" viewBox="0 0 60 60" fill="none" stroke="#3B2E22" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle;"><path d="M8,52 L20,25 L24,29 L30,10 L36,26 L40,22 L52,52"/><path d="M26,32 L31,27 L36,32"/><path d="M31,42 L37,37 L43,43"/></svg>'
    forest_svg_legend = '<svg width="18" height="18" viewBox="0 0 64 108" style="vertical-align: middle;"><rect x="27" y="88" width="10" height="20" rx="2" fill="#6B4A32" stroke="#1a1a1a" stroke-width="2.5"/><path d="M32 0 L52 34 L42 30 L58 58 L46 53 L64 88 L0 88 L18 53 L6 58 L22 30 L12 34 Z" fill="#6FA579" stroke="#1a1a1a" stroke-width="3" stroke-linejoin="round"/></svg>'
    steppe_svg_legend = '<svg width="18" height="18" viewBox="0 0 64 84" style="vertical-align: middle;"><path d="M32 76 C30 55 26 40 14 22 C22 34 27 44 30 58 C27 38 24 24 16 6 C25 20 29 32 32 48 C32 30 32 16 32 0 C36 16 36 30 34 48 C39 32 43 20 50 8 C44 26 41 40 36 58 C41 44 47 34 56 22 C46 40 40 55 36 76 Z" fill="#C9A24A" stroke="#1a1a1a" stroke-width="3" stroke-linejoin="round"/></svg>'
    bridge_svg_legend = '<svg width="18" height="18" viewBox="0 0 220 220" style="vertical-align: middle;"><path d="M110,20 L110,70 L30,160 L15,160" fill="none" stroke="#111111" stroke-width="26" stroke-linejoin="miter" stroke-linecap="butt"/><path d="M50,180 L50,130 L130,40 L145,40" fill="none" stroke="#111111" stroke-width="26" stroke-linejoin="miter" stroke-linecap="butt"/></svg>'
    pass_svg_legend = '<svg width="18" height="18" viewBox="0 0 200 130" style="vertical-align: middle;"><g transform="translate(5,15) scale(0.85)"><path d="M8,52 L20,25 L24,29 L30,10 L36,26 L40,22 L52,52 Z" fill="#FFFFFF" stroke="#000000" stroke-width="2.4" stroke-linejoin="round"/></g><g transform="translate(140,15) scale(0.85)"><path d="M8,52 L20,25 L24,29 L30,10 L36,26 L40,22 L52,52 Z" fill="#FFFFFF" stroke="#000000" stroke-width="2.4" stroke-linejoin="round"/></g><g transform="translate(72,38) scale(0.32)"><path d="M110,20 L110,70 L30,160 L15,160" fill="none" stroke="#000000" stroke-width="26" stroke-linejoin="miter" stroke-linecap="butt"/><path d="M50,180 L50,130 L130,40 L145,40" fill="none" stroke="#000000" stroke-width="26" stroke-linejoin="miter" stroke-linecap="butt"/></g></svg>'
    iron_gates_svg_legend = '<svg width="18" height="18" viewBox="0 0 170 100" style="vertical-align: middle;"><path d="M5,20 L55,20 L35,100 L5,100 Z" fill="#8A7560" stroke="#3B2E22" stroke-width="2.4" stroke-linejoin="round"/><path d="M165,20 L115,20 L135,100 L165,100 Z" fill="#8A7560" stroke="#3B2E22" stroke-width="2.4" stroke-linejoin="round"/><path d="M0,58 Q25,52 40,58 Q55,64 70,58 Q85,52 100,58 Q115,64 130,58 Q145,52 170,58" fill="none" stroke="#3C6E8A" stroke-width="2.6" stroke-linecap="round"/></svg>'
    return f"""
<div id="atlas-loader">
  <div class="loader-mark"></div>
  <div class="loader-text" dir="rtl" lang="ota">دولت عليه عثمانیه</div>
</div>
<div id="map"></div>
<div class="atlas-toast" id="atlas-toast"></div>
<div class="info-card" id="info-card">
  <button class="info-card-close" id="info-card-close" aria-label="Close">&times;</button>
  <div id="info-card-body"></div>
</div>
<div class="compare-panel" id="compare-panel">
  <label><span data-i18n="compare_year_a">Year A</span> <input type="number" id="compare-year-a"></label>
  <label><span data-i18n="compare_year_b">Year B</span> <input type="number" id="compare-year-b"></label>
  <button id="compare-apply" data-i18n="compare_apply">Show changes</button>
  <button id="compare-exit" data-i18n="compare_exit">Exit</button>
  <div class="compare-legend">
    <span><span class="compare-swatch" style="background:#2f9e44"></span><span data-i18n="compare_gained">Gained</span></span>
    <span><span class="compare-swatch" style="background:#c92a2a"></span><span data-i18n="compare_lost">Lost</span></span>
    <span><span class="compare-swatch" style="background:#e8590c"></span><span data-i18n="compare_changed">Changed power</span></span>
  </div>
</div>
<div class="ottoman-emblem" title="Ottoman Imperial Ensign &mdash; crescent and star">
  <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <radialGradient id="emblemGold" cx="35%" cy="30%" r="75%">
        <stop offset="0%" stop-color="#f4dd8a"/>
        <stop offset="55%" stop-color="#c9a227"/>
        <stop offset="100%" stop-color="#8a6a13"/>
      </radialGradient>
      <radialGradient id="emblemField" cx="40%" cy="35%" r="70%">
        <stop offset="0%" stop-color="#c23b3b"/>
        <stop offset="100%" stop-color="#7c1414"/>
      </radialGradient>
    </defs>
    <circle cx="50" cy="50" r="48" fill="url(#emblemGold)"/>
    <circle cx="50" cy="50" r="41" fill="url(#emblemField)" stroke="#f4dd8a" stroke-width="1.5"/>
    <circle cx="50" cy="50" r="45.5" fill="none" stroke="#f4dd8a" stroke-width="1" opacity="0.8"/>
    <g fill="none" stroke="#f4dd8a" stroke-width="1" opacity="0.55">
      <circle cx="50" cy="50" r="34.5"/>
    </g>
    <path d="M60 32 A20 20 0 1 0 60 68 A16 16 0 1 1 60 32 Z" fill="#f9f1d8"/>
    <path d="M67 45.5 L69.6 51.6 L76.2 52.2 L71.2 56.6 L72.7 63.1 L67 59.6 L61.3 63.1 L62.8 56.6 L57.8 52.2 L64.4 51.6 Z" fill="#f9f1d8"/>
  </svg>
</div>
<div class="atlas-title">
  <div class="atlas-title-row">
    <div class="atlas-title-heading">
      <svg class="atlas-rosette" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
        <g stroke="currentColor" stroke-width="1.3">
          <circle cx="20" cy="20" r="17" opacity="0.5"/>
          <path d="M20 3 L20 37 M3 20 L37 20 M7 7 L33 33 M33 7 L7 33" opacity="0.55"/>
          <path d="M20 8 L27.3 15 V25 L20 32 L12.7 25 V15 Z" opacity="0.9"/>
        </g>
      </svg>
      <div>
        <h1 lang="ota" dir="rtl">دولت عليه عثمانیه</h1>
        <svg class="atlas-title-flourish" viewBox="0 0 200 10" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M0 5 Q50 -3 100 5 T200 5" fill="none" stroke="currentColor" stroke-width="1"/>
          <circle cx="100" cy="5" r="2.2" fill="currentColor"/>
          <circle cx="70" cy="4" r="1.1" fill="currentColor"/>
          <circle cx="130" cy="4" r="1.1" fill="currentColor"/>
        </svg>
        <p class="atlas-title-translit">Devlet-i &Acirc;liyye-i Osm&acirc;niyye &middot; The Sublime Ottoman State</p>
      </div>
    </div>
    <div class="atlas-title-actions">
      <button class="icon-toggle-btn" id="theme-toggle" title="Toggle day/night theme">&#9789;</button>
      <button class="icon-toggle-btn" id="lang-toggle" data-i18n-title="lang_toggle_title" title="Switch to Turkish">EN</button>
      <button class="icon-toggle-btn" id="link-button" data-i18n-title="copy_link_title" title="Copy link to this year">&#128279;</button>
      <button class="icon-toggle-btn" id="title-minimize-button" title="Minimize Title">&#9650;</button>
    </div>
  </div>
  <div class="atlas-title-collapsible">
    <p data-i18n="subtitle">Interactive historical atlas of the Ottoman Empire's expansion on all major frontiers.</p>
    <label class="atlas-search"><span>Search</span><input id="atlas-search" list="atlas-search-list" placeholder="Search a city, battle, or province&hellip;" data-i18n-placeholder="search_placeholder" autocomplete="off"><datalist id="atlas-search-list"></datalist></label>
    <div class="atlas-shortcut-hint">
      <span><kbd>&larr;</kbd><kbd>&rarr;</kbd> <span data-i18n="hint_step">step year</span></span>
      <span><kbd>space</kbd> <span data-i18n="hint_play">play/pause</span></span>
      <span><kbd>/</kbd> <span data-i18n="hint_search">search</span></span>
      <span><kbd>n</kbd> <span data-i18n="hint_night">night mode</span></span>
    </div>
  </div>
</div>
<div class="atlas-panel">
  <div class="atlas-controls">
    <div class="atlas-year-wrap">
      <div class="atlas-year" id="atlas-year">{TIMELINE_START}</div>
      <div class="atlas-visible-chip" id="atlas-visible-chip" title="Currently visible on the map"></div>
    </div>
    <div class="atlas-slider-wrap">
      <div class="golden-age-band" id="golden-age-band"></div>
      <input id="atlas-slider" type="range" min="{TIMELINE_START}" max="1701" value="{TIMELINE_START}" step="1" aria-label="Timeline year">
      <div class="era-ticks" id="era-ticks"></div>
    </div>
    <div class="atlas-buttons">
      <button class="atlas-button" id="prev-button" title="Previous event">&lt;</button>
      <button class="atlas-button" id="play-button" title="Play or pause timeline">&#9654;</button>
      <button class="atlas-button" id="next-button" title="Next event">&gt;</button>
      <button class="atlas-button" id="doc-button" title="Toggle documentary mode">D</button>
      <button class="atlas-button" id="compare-button" title="Compare two years">C</button>
      <button class="atlas-button" id="export-view-button" data-i18n-title="export_view_title" title="Screenshot current view">&#128247;</button>
      <button class="atlas-button" id="export-whole-button" data-i18n-title="export_whole_title" title="Export Ottoman territories, whole map">&#128506;</button>
      <select class="atlas-speed" id="speed-control" title="Timeline speed">
        <option value="320" data-i18n="speed_slow">Slow</option>
        <option value="180" selected data-i18n="speed_normal">Normal</option>
        <option value="80" data-i18n="speed_fast">Fast</option>
      </select>
      <button class="panel-toggle-btn" id="minimize-button" title="Minimize Panel">&#9660;</button>
    </div>
  </div>
  <nav class="atlas-tabs" role="tablist">
    <button class="atlas-tab-btn is-active" data-tab="story" role="tab" data-i18n="tab_story">Chronicle</button>
    <button class="atlas-tab-btn" data-tab="stats" role="tab" data-i18n="tab_stats">Realm Stats</button>
    <button class="atlas-tab-btn" data-tab="filters" role="tab" data-i18n="tab_filters">Filters</button>
    <button class="atlas-tab-btn" data-tab="legend" role="tab" data-i18n="tab_legend">Legend</button>
  </nav>
  <div class="atlas-tab-panel" data-tab-panel="story">
    <div class="atlas-story">
      <strong id="event-title">Gallipoli seized</strong>
      <span id="event-body">The Ottomans gain their first permanent European foothold on the Dardanelles.</span>
    </div>
  </div>
  <div class="atlas-tab-panel" data-tab-panel="stats" hidden>
    <div class="atlas-stats">
      <span><b data-i18n="stat_year">Current Year</b><em id="stat-year">{TIMELINE_START}</em></span>
      <span><b data-i18n="stat_sultan">Sultan</b><em id="stat-sultan">Orhan</em><span class="sultan-badge" id="sultan-tughra">O</span></span>
      <span><b data-i18n="stat_territory">Territory</b><em id="stat-territory">0 layers</em></span>
      <span><b data-i18n="stat_population">Population</b><em id="stat-population">Frontier polity</em></span>
      <span><b data-i18n="stat_provinces">Provinces</b><em id="stat-provinces">0</em></span>
      <span><b data-i18n="stat_vassals">Vassals</b><em id="stat-vassals">0</em></span>
      <span><b data-i18n="stat_rival">Largest Rival</b><em id="stat-rival">Byzantine Empire</em></span>
    </div>
  </div>
  <div class="atlas-tab-panel" data-tab-panel="filters" hidden>
    <div class="atlas-filter-bar">
      <div class="filter-group">
        <span data-i18n="filter_fortress">Fortress Filter:</span>
        <button class="filter-chip is-active" data-defense="all" data-i18n="filter_all">All</button>
        <button class="filter-chip" data-defense="renaissance_bastion" data-i18n="filter_star">Star Forts</button>
        <button class="filter-chip" data-defense="earthwork_abatis" data-i18n="filter_earthwork">Earthworks</button>
        <button class="filter-chip" data-defense="medieval_stone" data-i18n="filter_stone">Stone</button>
        <button class="filter-chip" data-defense="transitional" data-i18n="filter_transitional">Transitional</button>
      </div>
      <div class="filter-group" style="margin-left: auto;">
        <span data-i18n="filter_era">Battle Era:</span>
        <button class="filter-chip era-chip is-active" data-era="0" data-i18n="filter_all">All</button>
        <button class="filter-chip era-chip" data-era="1453">1453 +</button>
        <button class="filter-chip era-chip" data-era="1566">1566 +</button>
        <button class="filter-chip era-chip" data-era="1606">1606 +</button>
        <button class="filter-chip era-chip" data-era="1683">1683 +</button>
      </div>
      <div class="filter-group">
        <span data-i18n="filter_unrest">Unrest:</span>
        <button class="filter-chip is-active" id="revolt-toggle" data-i18n="filter_revolts">Revolts</button>
      </div>
      <div class="filter-group territory-opacity-group">
        <span>Territory Fill:</span>
        <input type="range" id="territory-opacity-slider" min="20" max="100" value="100" step="5" aria-label="Territory fill opacity">
        <span class="territory-opacity-value" id="territory-opacity-value">100%</span>
      </div>
    </div>
  </div>
  <div class="atlas-tab-panel" data-tab-panel="legend" hidden>
    <div class="atlas-legend">
      <input class="legend-search" id="legend-search" type="search" placeholder="Filter legend by name&hellip;">
      <div class="legend-grid" id="legend-grid">{legend}<span class="legend-chip"><span class="legend-swatch" style="background:transparent;border-style:dashed"></span>Vassal or temporary rule</span><span class="legend-chip"><span class="legend-swatch" style="background:#111111"></span>Defensive line</span><span class="legend-chip"><span class="legend-swatch" style="background:#5bc0de"></span>Rivers</span><span class="legend-chip">{city_svg_legend} city</span><span class="legend-chip">{fortress_svg_legend} fortress</span><span class="legend-chip">{vienna_svg_legend} Vienna</span><span class="legend-chip">{land_svg_legend} land battle</span><span class="legend-chip">{naval_svg_legend} naval battle</span><span class="legend-chip">{treaty_svg_legend} treaty</span><span class="legend-chip">{raid_svg_legend} raid</span><span class="legend-chip">{siege_svg_legend} siege</span><span class="legend-chip">{raid_siege_svg_legend} raid/siege</span><span class="legend-chip">{sacked_svg_legend} sacked</span><span class="legend-chip">{revolt_svg_legend} revolt</span><span class="legend-chip">{campaign_svg_legend} campaign route</span><span class="legend-chip">{mountain_svg_legend} mountain range</span><span class="legend-chip">{forest_svg_legend} forest ecoregion</span><span class="legend-chip">{steppe_svg_legend} steppe ecoregion</span><span class="legend-chip">{bridge_svg_legend} bridge</span><span class="legend-chip">{pass_svg_legend} mountain pass</span><span class="legend-chip">{iron_gates_svg_legend} Iron Gates</span></div>
    </div>
  </div>
</div>
"""


def _script():
    return f"""
const ATLAS = {{
  bounds: {_json([[30.0, 5.0], [56.5, 45.0]])},
  territories: {_json(_feature_collection(TERRITORIES))},
  events: {_json(EVENTS)},
  cities: {_json(CITIES)},
  battles: {_json(BATTLES)},
  campaigns: {_json(CAMPAIGNS)},
  border_lines: {_json(BORDER_LINES)},
  rivers: {_json(RIVERS)},
  colors: {_json(POWER_COLORS)},
  start: {TIMELINE_START},
  end: 1701
}};

const MOUNTAIN_RANGES = {{
  "Alps": {{
    coords: [[43.75, 7.5], [45.8, 6.9], [46.5, 8.0], [47.0, 11.4], [47.4, 13.8]],
    color: "#3B2E22"
  }},
  "Carpathians": {{
    coords: [[48.3, 17.1], [49.2, 20.0], [48.0, 24.0], [45.6, 25.5], [45.3, 22.9]],
    color: "#43362A"
  }},
  "Dinaric Alps": {{
    coords: [[45.4, 14.5], [44.0, 17.0], [43.0, 19.0], [42.0, 20.0], [41.0, 20.2]],
    color: "#4A3324"
  }},
  "Balkan Mountains": {{
    coords: [[43.4, 23.3], [43.0, 25.5], [42.7, 27.5]],
    color: "#3A2E24"
  }},
  "Caucasus": {{
    coords: [[43.4, 41.0], [43.0, 43.0], [42.7, 45.0], [41.2, 47.5]],
    color: "#4A2E22"
  }},
  "Ural Mountains": {{
    coords: [[68.5, 65.0], [63.0, 59.5], [58.0, 59.0], [51.0, 58.5]],
    color: "#33281F"
  }}
}};

const FOREST_REGIONS = {{
  "Balkan Forest": {{
    coords: [[43.5, 23.0], [42.8, 24.5], [42.2, 26.0], [41.8, 24.0], [42.5, 22.0]],
    density: 100,
    baseSize: 22,
    colors: ["#5F9468", "#6FA579", "#77AC80"],
    seed: 10
  }},
  "Pannonian Forest": {{
    coords: [[47.5, 17.0], [47.0, 19.5], [46.2, 18.5], [46.0, 16.5]],
    density: 90,
    baseSize: 22,
    colors: ["#5F9468", "#6FA579", "#77AC80"],
    seed: 11
  }},
  "Vienna Woods (Wienerwald)": {{
    coords: [[48.3, 15.8], [48.1, 16.2], [47.8, 16.0], [47.9, 15.5]],
    density: 80,
    baseSize: 20,
    colors: ["#5F9468", "#6FA579", "#77AC80"],
    seed: 12
  }},
  "Carpathian Foothill Forests": {{
    coords: [[50.2, 20.0], [49.5, 22.5], [48.8, 24.0], [48.2, 22.0], [49.0, 19.5]],
    density: 130,
    baseSize: 22,
    colors: ["#5F9468", "#6FA579", "#77AC80"],
    seed: 13
  }},
  "Upper Danube Riparian Forest": {{
    coords: [[48.6, 13.5], [48.3, 14.8], [48.1, 15.6], [48.5, 14.0]],
    density: 70,
    baseSize: 20,
    colors: ["#5F9468", "#6FA579", "#77AC80"],
    seed: 14
  }},
  "Dinaric Mixed Forests": {{
    coords: [[44.5, 16.5], [43.5, 18.5], [42.0, 20.0], [40.5, 20.5], [41.2, 19.0], [43.0, 17.0]],
    density: 140,
    baseSize: 22,
    colors: ["#5F9468", "#6FA579", "#77AC80"],
    seed: 15
  }},
  "East European forest steppe": {{
    coords: [
      [54.0, 56.0], [53.0, 45.0], [51.5, 39.0], [50.5, 34.0],
      [49.0, 30.0], [48.0, 27.0], [46.5, 26.5], [47.5, 30.0],
      [49.5, 36.0], [51.0, 42.0], [52.5, 50.0], [53.5, 55.0]
    ],
    density: 120,
    baseSize: 22,
    colors: ["#5F9468", "#6FA579", "#77AC80"],
    seed: 7
  }}
}};

const STEPPE_REGIONS = {{
  "Eurasian steppe": {{
    coords: [
      [47.5, 19.0], [46.5, 30.0], [46.0, 38.0], [45.0, 46.0],
      [48.0, 55.0], [51.0, 62.0], [52.5, 55.0], [50.5, 44.0],
      [49.0, 34.0], [48.0, 24.0]
    ],
    density: 150,
    baseSize: 20,
    colors: ["#C9A24A", "#B99A3E", "#D4B25A"],
    seed: 3
  }}
}};

const BRIDGES = {{
  "Stari Most (Mostar)": [43.3374, 17.8154],
  "Osijek Bridge": [45.5550, 18.6955],
  "Mehmed Pasa Sokolovic Bridge (Visegrad)": [43.7864, 19.2903],
  "Mustafa Pasha Bridge (Svilengrad)": [41.9756, 26.2115],
  "Arslanagic Bridge (Trebinje)": [42.7120, 18.3440],
  "Stone Bridge (Skopje)": [41.9973, 21.4318],
  "Old Bridge of Prizren": [42.2137, 20.7397],
  "Kurd Kuli Bridge (Mostar)": [43.3412, 17.8131],
  "Vizier's Bridge (Podgorica)": [42.4452, 19.2611],
  "Carrying Bridge over the Maritsa (Edirne)": [41.6742, 26.5556],
  "Zhaohui/Bosphorus/Danube historical pontoon bridges": [44.8125, 20.4612],
  "Raab Bridge (Gyor, Hungary)": [47.6833, 17.6333],
  "Esztergom Danube Bridge (historical site / boat bridge, Hungary)": [47.7910, 18.7403],
  "Vienna Danube Wooden Bridge": [48.2082, 16.3738],
  "Enns Bridge (Upper/Lower Austria border)": [48.1417, 14.4833],
  "Vistula Bridge at Cracow": [50.0647, 19.9450],
  "San Bridge at Przemysl": [49.7833, 22.7667],
  "Dnieper Boat Bridge at Kiev": [50.4501, 30.5234]
}};

const MOUNTAIN_PASSES = {{
  "Shipka Pass": [42.7500, 25.3333],
  "Predeal Pass": [45.5000, 25.5833],
  "Vratnik Pass": [44.9667, 14.9667],
  "Katara Pass": [39.7000, 21.2333],
  "Dukagjin Pass (Bogicica area)": [42.5500, 20.0833],
  "Oylat Pass (Bursa region)": [39.9500, 29.6167],
  "Derbend Pass (Gates of Alexander / Caspian Gates)": [42.0667, 48.2833],
  "Darial Gorge Pass (Caucasian Gates)": [42.7500, 44.4667],
  "Rouska Pass (Balkans)": [42.9167, 25.5833],
  "Eisentor / Iron Gates Pass": [44.6750, 22.5000],
  "Torzhat / Dukla Pass (Carpathians)": [49.4167, 21.6833],
  "Verecke Pass (Carpathians)": [48.8333, 23.3167]
}};

const IRON_GATES = {{
  "Iron Gates (Djerdap)": [44.6750, 22.5000]
}};

const map = L.map("map", {{
  zoomControl: true,
}});

map.setView([45.0, 20.0], 5);

L.tileLayer("https://{{s}}.basemaps.cartocdn.com/rastertiles/voyager_nolabels/{{z}}/{{x}}/{{y}}{{r}}.png", {{
  attribution: "OpenStreetMap contributors, CARTO",
  maxZoom: 18,
  crossOrigin: true
}}).addTo(map);

let currentYear = ATLAS.start;
let currentDefenseFilter = "all";
let territoryOpacityScale = 1;
let battleMinYear = 0;
let showRevolts = true;
let timer = null;
const yearEl = document.getElementById("atlas-year");
const visibleChipEl = document.getElementById("atlas-visible-chip");
function updateVisibleCountChip() {{
  if (!visibleChipEl) return;
  const battleCount = battleGroup.getLayers().length + navalGroup.getLayers().length +
    treatyGroup.getLayers().length + raidGroup.getLayers().length + siegeGroup.getLayers().length +
    raidSiegeGroup.getLayers().length + sackedGroup.getLayers().length + revoltGroup.getLayers().length;
  const cityCount = cityGroup.getLayers().length;
  const territoryCount = territoryLayer.getLayers().length;
  visibleChipEl.textContent = territoryCount + " realms · " + cityCount + " sites · " + battleCount + " events";
}}
const slider = document.getElementById("atlas-slider");
const prevButton = document.getElementById("prev-button");
const playButton = document.getElementById("play-button");
const nextButton = document.getElementById("next-button");
const docButton = document.getElementById("doc-button");
const speedControl = document.getElementById("speed-control");
const searchInput = document.getElementById("atlas-search");
const searchList = document.getElementById("atlas-search-list");
const eventTitle = document.getElementById("event-title");
const eventBody = document.getElementById("event-body");
const statYear = document.getElementById("stat-year");
const statSultan = document.getElementById("stat-sultan");
const statTerritory = document.getElementById("stat-territory");
const statPopulation = document.getElementById("stat-population");
const statProvinces = document.getElementById("stat-provinces");
const statVassals = document.getElementById("stat-vassals");
const statRival = document.getElementById("stat-rival");
const sultanTughra = document.getElementById("sultan-tughra");

L.control.scale({{imperial: false, position: "bottomleft"}}).addTo(map);

let battlePeriodFrom = null;
let battlePeriodTo = null;

const battlePeriodControl = L.control({{position: "topright"}});
battlePeriodControl.onAdd = function() {{
  const div = L.DomUtil.create("div", "battle-period-box");
  div.innerHTML =
    '<div class="battle-period-header">' +
      '<span>Battle Period</span>' +
      '<button class="battle-period-toggle" id="battle-period-toggle" title="Minimize">&#9660;</button>' +
    '</div>' +
    '<div class="battle-period-body" id="battle-period-body">' +
      '<div class="battle-period-row">' +
        '<label>From<input type="number" id="battle-year-from" placeholder="' + ATLAS.start + '"></label>' +
        '<label>To<input type="number" id="battle-year-to" placeholder="' + ATLAS.end + '"></label>' +
      '</div>' +
      '<div class="battle-period-actions">' +
        '<button class="filter-chip" id="battle-period-apply">Apply</button>' +
        '<button class="filter-chip" id="battle-period-reset">Reset</button>' +
      '</div>' +
      '<div class="battle-period-status" id="battle-period-status"></div>' +
    '</div>';
  L.DomEvent.disableClickPropagation(div);
  L.DomEvent.disableScrollPropagation(div);
  return div;
}};
battlePeriodControl.addTo(map);

const coordControl = L.control({{position: "bottomleft"}});
coordControl.onAdd = function() {{
  const div = L.DomUtil.create("div", "coord-readout");
  div.textContent = "Move cursor for coordinates";
  map.on("mousemove", event => {{
    div.textContent = event.latlng.lat.toFixed(2) + "N, " + event.latlng.lng.toFixed(2) + "E";
  }});
  return div;
}};
coordControl.addTo(map);

const fullControl = L.control({{position: "topleft"}});
fullControl.onAdd = function() {{
  const div = L.DomUtil.create("button", "fullscreen-faux");
  div.type = "button";
  div.textContent = "⛶";
  div.title = "Fullscreen";
  L.DomEvent.on(div, "click", event => {{
    L.DomEvent.stop(event);
    if (!document.fullscreenElement) {{
      document.documentElement.requestFullscreen?.();
    }} else {{
      document.exitFullscreen?.();
    }}
  }});
  return div;
}};
fullControl.addTo(map);

const resetViewControl = L.control({{position: "topleft"}});
resetViewControl.onAdd = function() {{
  const div = L.DomUtil.create("button", "fullscreen-faux");
  div.type = "button";
  div.textContent = "⌂";
  div.title = "Reset map view";
  L.DomEvent.on(div, "click", event => {{
    L.DomEvent.stop(event);
    map.flyTo([45.0, 20.0], 5, {{duration: 0.75}});
    showToast("View reset");
  }});
  return div;
}};
resetViewControl.addTo(map);

const mini = L.map(document.createElement("div"), {{attributionControl: false, zoomControl: false, interactive: false}});
const miniControl = L.control({{position: "bottomright"}});
miniControl.onAdd = function() {{
  const div = mini.getContainer();
  div.style.width = "150px";
  div.style.height = "96px";
  div.style.border = "1px solid rgba(36,27,24,.24)";
  div.style.borderRadius = "8px";
  div.style.overflow = "hidden";
  return div;
}};
miniControl.addTo(map);
L.tileLayer("https://{{s}}.basemaps.cartocdn.com/light_nolabels/{{z}}/{{x}}/{{y}}{{r}}.png", {{maxZoom: 8, crossOrigin: true}}).addTo(mini);
mini.fitBounds(ATLAS.bounds);

function activeInYear(item, year) {{
  const props = item.properties || item;
  return props.start <= year && year <= props.end;
}}

function styleFor(feature) {{
  const props = feature.properties;
  const relation = props.relation;
  const color = ATLAS.colors[props.power] || "#cccccc";
  return {{
    color: relation === "neighbour" ? "#5f665f" : "#111111",
    weight: relation === "neighbour" ? 1.1 : 1.55,
    fillColor: color,
    fillOpacity: (relation === "neighbour" ? 0.4 : (relation === "vassal" ? 0.55 : 0.7)) * territoryOpacityScale,
    dashArray: relation === "direct" ? null : "8 5"
  }};
}}

function tooltip(feature) {{
  const p = feature.properties;
  const end = p.end > 1900 ? "later" : p.end;
  return '<div class="atlas-tooltip"><b>' + p.name + '</b><br>' + p.status + ' · ' + p.start + '-' + end + '<br><em>' + p.capital + '</em><br>' + p.summary + '</div>';
}}

const territoryLayer = L.geoJSON(null, {{
  style: styleFor,
  onEachFeature: (feature, layer) => {{
    layer.bindTooltip(tooltip(feature), {{sticky: true, opacity: 0.96}});
    layer.on("mouseover", () => layer.setStyle({{weight: 2.7, fillOpacity: Math.min((styleFor(feature).fillOpacity || 0.5) + 0.14, 0.9)}}));
    layer.on("mouseout", () => layer.setStyle(styleFor(feature)));
    layer.on("click", () => {{
      const p = feature.properties;
      const end = p.end > 1900 ? "later" : p.end;
      openInfoCard(
        '<h3>' + p.name + '</h3>' +
        '<p><b>' + t("info_ruler") + ':</b> ' + (p.power || p.status || "&mdash;") + '</p>' +
        '<p><b>' + t("info_since") + ':</b> ' + p.start + '&ndash;' + end + '</p>' +
        '<p><b>' + t("info_capital") + ':</b> ' + (p.capital || "&mdash;") + '</p>' +
        (p.summary ? '<p>' + p.summary + '</p>' : '')
      );
    }});
  }}
}}).addTo(map);

const steppeGroup = L.layerGroup().addTo(map);
const forestGroup = L.layerGroup().addTo(map);
const riverGroup = L.layerGroup().addTo(map);
const mountainGroup = L.layerGroup().addTo(map);
const bridgeGroup = L.layerGroup().addTo(map);
const passGroup = L.layerGroup().addTo(map);
const ironGatesGroup = L.layerGroup().addTo(map);
const cityGroup = L.layerGroup().addTo(map);
const battleGroup = L.layerGroup().addTo(map);
const navalGroup = L.layerGroup().addTo(map);
const treatyGroup = L.layerGroup().addTo(map);
const raidGroup = L.layerGroup().addTo(map);
const siegeGroup = L.layerGroup().addTo(map);
const raidSiegeGroup = L.layerGroup().addTo(map);
const sackedGroup = L.layerGroup().addTo(map);
const revoltGroup = L.layerGroup().addTo(map);
const campaignGroup = L.layerGroup().addTo(map);

const labelGroup = L.layerGroup().addTo(map);
const regionalLabelGroup = L.layerGroup().addTo(map);
const borderLineGroup = L.layerGroup().addTo(map);

function renderBorderLines(year) {{
  borderLineGroup.clearLayers();
  ATLAS.border_lines.forEach(line => {{
    if (line.start <= year && year <= line.end) {{
      const latlngs = line.points.map(pt => [pt[1], pt[0]]);
      
      L.polyline(latlngs, {{
        color: "#111111",
        weight: 4,
        opacity: 0.9,
        lineCap: "round",
        lineJoin: "round"
      }}).bindTooltip(
        '<div class="atlas-tooltip"><b>' + line.name + '</b><br>' + line.start + '-' + line.end + '<br>' + line.summary + '</div>',
        {{sticky: true}}
      ).addTo(borderLineGroup);

      for (let i = 0; i < latlngs.length - 1; i++) {{
        const p1 = latlngs[i];
        const p2 = latlngs[i + 1];
        
        const dx = p2[1] - p1[1];
        const dy = p2[0] - p1[0];
        const dist = Math.sqrt(dx * dx + dy * dy);
        const steps = Math.max(2, Math.floor(dist / 0.15));

        for (let s = 1; s < steps; s++) {{
          const ratio = s / steps;
          const midLat = p1[0] + dy * ratio;
          const midLon = p1[1] + dx * ratio;

          const angle = Math.atan2(dy, dx) + Math.PI / 2;
          const tickLength = 0.04;
          
          const tickLat = midLat + Math.sin(angle) * tickLength;
          const tickLon = midLon + Math.cos(angle) * tickLength;

          L.polyline([[midLat, midLon], [tickLat, tickLon]], {{
            color: "#111111",
            weight: 2.5,
            opacity: 0.8
          }}).addTo(borderLineGroup);
        }}
      }}
    }}
  }});
}}

function renderRivers(year) {{
  riverGroup.clearLayers();
  ATLAS.rivers.forEach(river => {{
    if (river.start <= year && year <= river.end) {{
      const latlngs = river.points.map(pt => [pt[1], pt[0]]);
      L.polyline(latlngs, {{
        color: "#5bc0de",
        weight: 2.5,
        opacity: 0.75,
        smoothFactor: 1.2
      }}).bindTooltip(
        '<div class="atlas-tooltip"><b>' + river.name + '</b><br>' + river.summary + '</div>',
        {{sticky: true}}
      ).addTo(riverGroup);
    }}
  }});
}}

function haversineKm(p1, p2) {{
  const rad = Math.PI / 180;
  const lat1 = p1[0] * rad, lon1 = p1[1] * rad;
  const lat2 = p2[0] * rad, lon2 = p2[1] * rad;
  const dlat = lat2 - lat1, dlon = lon2 - lon1;
  const a = Math.sin(dlat / 2) ** 2 + Math.cos(lat1) * Math.cos(lat2) * Math.sin(dlon / 2) ** 2;
  return 2 * 6371.0 * Math.asin(Math.sqrt(a));
}}

function bearingDeg(p1, p2) {{
  const rad = Math.PI / 180;
  const lat1 = p1[0] * rad, lon1 = p1[1] * rad;
  const lat2 = p2[0] * rad, lon2 = p2[1] * rad;
  const dlon = lon2 - lon1;
  const x = Math.sin(dlon) * Math.cos(lat2);
  const y = Math.cos(lat1) * Math.sin(lat2) - Math.sin(lat1) * Math.cos(lat2) * Math.cos(dlon);
  return (Math.atan2(x, y) * (180 / Math.PI) + 360) % 360;
}}

function interpolatePt(p1, p2, frac) {{
  return [p1[0] + (p2[0] - p1[0]) * frac, p1[1] + (p2[1] - p1[1]) * frac];
}}

function pointsAlongLine(coords, spacingKm) {{
  const out = [];
  let carry = 0.0;
  for (let i = 0; i < coords.length - 1; i++) {{
    const segLen = haversineKm(coords[i], coords[i + 1]);
    if (segLen === 0) continue;
    const brg = bearingDeg(coords[i], coords[i + 1]);
    let distIntoSeg = spacingKm - carry;
    while (distIntoSeg <= segLen) {{
      const pt = interpolatePt(coords[i], coords[i + 1], distIntoSeg / segLen);
      out.push([pt, brg]);
      distIntoSeg += spacingKm;
    }}
    carry = segLen - (distIntoSeg - spacingKm);
  }}
  return out;
}}

function mountainIconHtml(rotationDeg, size = 34, color = "#3B2E22") {{
  return '<div style="transform: rotate(' + (rotationDeg - 90) + 'deg); width:' + size + 'px; height:' + size + 'px;">' +
    '<svg width="' + size + '" height="' + size + '" viewBox="0 0 60 60" fill="none" stroke="' + color + '" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">' +
    '<path d="M8,52 L20,25 L24,29 L30,10 L36,26 L40,22 L52,52"/>' +
    '<path d="M26,32 L31,27 L36,32"/>' +
    '<path d="M31,42 L37,37 L43,43"/>' +
    '</svg>' +
    '</div>';
}}

function renderMountainRanges(year) {{
  mountainGroup.clearLayers();
  for (const [name, data] of Object.entries(MOUNTAIN_RANGES)) {{
    const pts = pointsAlongLine(data.coords, 18);
    pts.forEach(([pt, brg]) => {{
      const icon = L.divIcon({{
        className: "",
        html: mountainIconHtml(brg, 34, data.color),
        iconSize: [34, 34],
        iconAnchor: [17, 17]
      }});
      L.marker(pt, {{icon: icon}}).bindTooltip('<div class="atlas-tooltip"><b>' + name + '</b></div>', {{sticky: true}}).addTo(mountainGroup);
    }});
    L.polyline(data.coords, {{color: data.color, weight: 1, opacity: 0.25}}).addTo(mountainGroup);
  }}
}}

function pointInPolygon(point, vs) {{
  const x = point[0], y = point[1];
  let inside = false;
  for (let i = 0, j = vs.length - 1; i < vs.length; j = i++) {{
    const xi = vs[i][0], yi = vs[i][1];
    const xj = vs[j][0], yj = vs[j][1];
    const intersect = ((yi > y) !== (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi);
    if (intersect) inside = !inside;
  }}
  return inside;
}}

function forestIconHtml(size = 26, rotationDeg = 0, tierColor = "#6FA579", trunkColor = "#6B4A32") {{
  return '<div style="transform: rotate(' + rotationDeg + 'deg); width:' + size + 'px; height:' + size + 'px;">' +
    '<svg width="' + size + '" height="' + size + '" viewBox="0 0 64 108">' +
    '<rect x="27" y="88" width="10" height="20" rx="2" fill="' + trunkColor + '" stroke="#1a1a1a" stroke-width="2.5"/>' +
    '<path d="M32 0 L52 34 L42 30 L58 58 L46 53 L64 88 L0 88 L18 53 L6 58 L22 30 L12 34 Z" fill="' + tierColor + '" stroke="#1a1a1a" stroke-width="3" stroke-linejoin="round"/>' +
    '</svg>' +
    '</div>';
}}

function steppeIconHtml(size = 26, rotationDeg = 0, color = "#C9A24A") {{
  return '<div style="transform: rotate(' + rotationDeg + 'deg); width:' + size + 'px; height:' + size + 'px;">' +
    '<svg width="' + size + '" height="' + size + '" viewBox="0 0 64 84">' +
    '<path d="M32 76 C30 55 26 40 14 22 C22 34 27 44 30 58 C27 38 24 24 16 6 C25 20 29 32 32 48 C32 30 32 16 32 0 C36 16 36 30 34 48 C39 32 43 20 50 8 C44 26 41 40 36 58 C41 44 47 34 56 22 C46 40 40 55 36 76 Z" fill="' + color + '" stroke="#1a1a1a" stroke-width="3" stroke-linejoin="round"/>' +
    '</svg>' +
    '</div>';
}}

function bridgeIconHtml(size = 30, color = "#111111") {{
  return '<div style="width:' + size + 'px; height:' + size + 'px;">' +
    '<svg width="' + size + '" height="' + size + '" viewBox="0 0 220 220">' +
    '<path d="M110,20 L110,70 L30,160 L15,160" fill="none" stroke="' + color + '" stroke-width="26" stroke-linejoin="miter" stroke-linecap="butt"/>' +
    '<path d="M50,180 L50,130 L130,40 L145,40" fill="none" stroke="' + color + '" stroke-width="26" stroke-linejoin="miter" stroke-linecap="butt"/>' +
    '</svg>' +
    '</div>';
}}

function passIconHtml(size = 40, outline = "#000000", fill = "#FFFFFF") {{
  return '<div style="width:' + size + 'px; height:' + size + 'px;">' +
    '<svg width="' + size + '" height="' + size + '" viewBox="0 0 200 130">' +
    '<g transform="translate(5,15) scale(0.85)">' +
    '<path d="M8,52 L20,25 L24,29 L30,10 L36,26 L40,22 L52,52 Z" fill="' + fill + '" stroke="' + outline + '" stroke-width="2.4" stroke-linejoin="round"/>' +
    '<path d="M26,32 L31,27 L36,32" fill="none" stroke="' + outline + '" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>' +
    '<path d="M31,42 L37,37 L43,43" fill="none" stroke="' + outline + '" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>' +
    '</g>' +
    '<g transform="translate(140,15) scale(0.85)">' +
    '<path d="M8,52 L20,25 L24,29 L30,10 L36,26 L40,22 L52,52 Z" fill="' + fill + '" stroke="' + outline + '" stroke-width="2.4" stroke-linejoin="round"/>' +
    '<path d="M26,32 L31,27 L36,32" fill="none" stroke="' + outline + '" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>' +
    '<path d="M31,42 L37,37 L43,43" fill="none" stroke="' + outline + '" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>' +
    '</g>' +
    '<g transform="translate(72,38) scale(0.32)">' +
    '<path d="M110,20 L110,70 L30,160 L15,160" fill="none" stroke="' + outline + '" stroke-width="26" stroke-linejoin="miter" stroke-linecap="butt"/>' +
    '<path d="M50,180 L50,130 L130,40 L145,40" fill="none" stroke="' + outline + '" stroke-width="26" stroke-linejoin="miter" stroke-linecap="butt"/>' +
    '</g>' +
    '</svg>' +
    '</div>';
}}

function ironGatesIconHtml(size = 44, outline = "#3B2E22", rock = "#8A7560", water = "#3C6E8A") {{
  return '<div style="width:' + size + 'px; height:' + size + 'px;">' +
    '<svg width="' + size + '" height="' + size + '" viewBox="0 0 170 100">' +
    '<path d="M5,20 L55,20 L35,100 L5,100 Z" fill="' + rock + '" stroke="' + outline + '" stroke-width="2.4" stroke-linejoin="round"/>' +
    '<path d="M165,20 L115,20 L135,100 L165,100 Z" fill="' + rock + '" stroke="' + outline + '" stroke-width="2.4" stroke-linejoin="round"/>' +
    '<path d="M0,58 Q25,52 40,58 Q55,64 70,58 Q85,52 100,58 Q115,64 130,58 Q145,52 170,58" fill="none" stroke="' + water + '" stroke-width="2.6" stroke-linecap="round"/>' +
    '</svg>' +
    '</div>';
}}

function pseudoRandom(seed) {{
  let x = Math.sin(seed++) * 10000;
  return x - Math.floor(x);
}}

function renderForestRegions(year) {{
  forestGroup.clearLayers();
  for (const [name, data] of Object.entries(FOREST_REGIONS)) {{
    const coords = data.coords;
    let minLat = Infinity, maxLat = -Infinity, minLon = Infinity, maxLon = -Infinity;
    coords.forEach(pt => {{
      if (pt[0] < minLat) minLat = pt[0];
      if (pt[0] > maxLat) maxLat = pt[0];
      if (pt[1] < minLon) minLon = pt[1];
      if (pt[1] > maxLon) maxLon = pt[1];
    }});

    const points = [];
    let seed = data.seed || 1;
    let attempts = 0;
    const maxAttempts = data.density * 200;

    while (points.length < data.density && attempts < maxAttempts) {{
      const lat = minLat + pseudoRandom(seed++) * (maxLat - minLat);
      const lon = minLon + pseudoRandom(seed++) * (maxLon - minLon);
      if (pointInPolygon([lat, lon], coords)) {{
        points.push([lat, lon]);
      }}
      attempts++;
    }}

    points.forEach((pt, idx) => {{
      const size = data.baseSize + Math.floor(pseudoRandom(seed + idx) * 14) - 6;
      const rotation = Math.floor(pseudoRandom(seed + idx * 7) * 17) - 8;
      const color = data.colors[Math.floor(pseudoRandom(seed + idx * 13) * data.colors.length)];
      const icon = L.divIcon({{
        className: "",
        html: forestIconHtml(size, rotation, color),
        iconSize: [size, size],
        iconAnchor: [size / 2, size / 2]
      }});
      L.marker(pt, {{icon: icon}}).bindTooltip('<div class="atlas-tooltip"><b>' + name + '</b></div>', {{sticky: true}}).addTo(forestGroup);
    }});

    L.polygon(coords, {{color: "#3A5A3E", weight: 1, opacity: 0.4, fill: false}}).addTo(forestGroup);
  }}
}}

function renderSteppeRegions(year) {{
  steppeGroup.clearLayers();
  for (const [name, data] of Object.entries(STEPPE_REGIONS)) {{
    const coords = data.coords;
    let minLat = Infinity, maxLat = -Infinity, minLon = Infinity, maxLon = -Infinity;
    coords.forEach(pt => {{
      if (pt[0] < minLat) minLat = pt[0];
      if (pt[0] > maxLat) maxLat = pt[0];
      if (pt[1] < minLon) minLon = pt[1];
      if (pt[1] > maxLon) maxLon = pt[1];
    }});

    const points = [];
    let seed = data.seed || 1;
    let attempts = 0;
    const maxAttempts = data.density * 200;

    while (points.length < data.density && attempts < maxAttempts) {{
      const lat = minLat + pseudoRandom(seed++) * (maxLat - minLat);
      const lon = minLon + pseudoRandom(seed++) * (maxLon - minLon);
      if (pointInPolygon([lat, lon], coords)) {{
        points.push([lat, lon]);
      }}
      attempts++;
    }}

    points.forEach((pt, idx) => {{
      const size = data.baseSize + Math.floor(pseudoRandom(seed + idx) * 14) - 6;
      const rotation = Math.floor(pseudoRandom(seed + idx * 7) * 21) - 10;
      const color = data.colors[Math.floor(pseudoRandom(seed + idx * 13) * data.colors.length)];
      const icon = L.divIcon({{
        className: "",
        html: steppeIconHtml(size, rotation, color),
        iconSize: [size, size],
        iconAnchor: [size / 2, size / 2]
      }});
      L.marker(pt, {{icon: icon}}).bindTooltip('<div class="atlas-tooltip"><b>' + name + '</b></div>', {{sticky: true}}).addTo(steppeGroup);
    }});

    L.polygon(coords, {{color: "#8A7530", weight: 1, opacity: 0.4, fill: false}}).addTo(steppeGroup);
  }}
}}

function renderBridges() {{
  bridgeGroup.clearLayers();
  for (const [name, coords] of Object.entries(BRIDGES)) {{
    const icon = L.divIcon({{
      className: "",
      html: bridgeIconHtml(30, "#111111"),
      iconSize: [30, 30],
      iconAnchor: [15, 15]
    }});
    L.marker(coords, {{icon: icon}}).bindTooltip('<div class="atlas-tooltip"><b>' + name + '</b></div>', {{sticky: true}}).addTo(bridgeGroup);
  }}
}}

function renderMountainPasses() {{
  passGroup.clearLayers();
  for (const [name, coords] of Object.entries(MOUNTAIN_PASSES)) {{
    const icon = L.divIcon({{
      className: "",
      html: passIconHtml(40, "#000000", "#FFFFFF"),
      iconSize: [40, 40],
      iconAnchor: [20, 20]
    }});
    L.marker(coords, {{icon: icon}}).bindTooltip('<div class="atlas-tooltip"><b>' + name + '</b></div>', {{sticky: true}}).addTo(passGroup);
  }}
}}

function renderIronGates() {{
  ironGatesGroup.clearLayers();
  for (const [name, coords] of Object.entries(IRON_GATES)) {{
    const icon = L.divIcon({{
      className: "",
      html: ironGatesIconHtml(44, "#3B2E22", "#8A7560", "#3C6E8A"),
      iconSize: [44, 44],
      iconAnchor: [22, 22]
    }});
    L.marker(coords, {{icon: icon}}).bindTooltip('<div class="atlas-tooltip"><b>' + name + '</b></div>', {{sticky: true}}).addTo(ironGatesGroup);
  }}
}}

function cityIcon(name) {{
  if (name === "Mecca") {{
    const svgContent = '<svg width="24" height="24" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg">' +
      '<path d="M30,10 C20,10,12,18,12,30 C12,42,20,50,30,50 C22,47,17,39,17,30 C17,21,22,13,30,10 Z" fill="#2c2c2a"/>' +
      '<polygon points="42,13 44,19 50,19 45,23 47,29 42,25 37,29 39,23 34,19 40,19" fill="#2c2c2a"/>' +
      '</svg>';
    return L.divIcon({{
      className: "",
      html: '<span class="mecca-marker">' + svgContent + '</span>',
      iconSize: [24, 24],
      iconAnchor: [12, 12]
    }});
  }} else if (name === "Constantinople") {{
    const svgContent = '<svg width="24" height="24" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg">' +
      '<rect x="8" y="46" width="44" height="6" fill="none" stroke="#2c2c2a" stroke-width="2"/>' +
      '<rect x="18" y="30" width="24" height="16" fill="none" stroke="#2c2c2a" stroke-width="2"/>' +
      '<path d="M18,30 A12,12 0 0 1 42,30" fill="none" stroke="#2c2c2a" stroke-width="2.5"/>' +
      '<path d="M26,46 A4,4 0 0 1 34,46" fill="none" stroke="#2c2c2a" stroke-width="1.5"/>' +
      '<line x1="30" y1="18" x2="30" y2="9" stroke="#2c2c2a" stroke-width="2"/>' +
      '<path d="M27,8 A4,4 0 1,0 33,8 A3,3 0 1,1 27,8 Z" fill="#2c2c2a"/>' +
      '<line x1="12" y1="44" x2="12" y2="16" stroke="#2c2c2a" stroke-width="2.5" stroke-linecap="round"/>' +
      '<line x1="48" y1="44" x2="48" y2="16" stroke="#2c2c2a" stroke-width="2.5" stroke-linecap="round"/>' +
      '<polygon points="9,16 12,9 15,16" fill="#2c2c2a"/>' +
      '<polygon points="45,16 48,9 51,16" fill="#2c2c2a"/>' +
      '</svg>';
    return L.divIcon({{
      className: "",
      html: '<span class="constantinople-marker">' + svgContent + '</span>',
      iconSize: [24, 24],
      iconAnchor: [12, 12]
    }});
  }} else if (name === "Edirne") {{
    const svgContent = '<svg width="24" height="24" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg">' +
      '<rect x="18" y="32" width="24" height="16" fill="none" stroke="#2c2c2a" stroke-width="2"/>' +
      '<path d="M18,32 A12,12 0 0 1 42,32" fill="none" stroke="#2c2c2a" stroke-width="2.5"/>' +
      '<line x1="30" y1="20" x2="30" y2="13" stroke="#2c2c2a" stroke-width="1.5"/>' +
      '<circle cx="30" cy="11" r="2.2" fill="#2c2c2a"/>' +
      '<line x1="10" y1="48" x2="10" y2="24" stroke="#2c2c2a" stroke-width="2" stroke-linecap="round"/>' +
      '<polygon points="7.5,24 10,18 12.5,24" fill="#2c2c2a"/>' +
      '<line x1="50" y1="48" x2="50" y2="24" stroke="#2c2c2a" stroke-width="2" stroke-linecap="round"/>' +
      '<polygon points="47.5,24 50,18 52.5,24" fill="#2c2c2a"/>' +
      '</svg>';
    return L.divIcon({{
      className: "",
      html: '<span class="edirne-marker">' + svgContent + '</span>',
      iconSize: [24, 24],
      iconAnchor: [12, 12]
    }});
  }} else if (name === "Bursa") {{
    const svgContent = '<svg width="24" height="24" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg">' +
      '<rect x="16" y="34" width="20" height="14" fill="none" stroke="#2c2c2a" stroke-width="2"/>' +
      '<path d="M16,34 A10,10 0 0 1 36,34" fill="none" stroke="#2c2c2a" stroke-width="2"/>' +
      '<line x1="26" y1="24" x2="26" y2="18" stroke="#2c2c2a" stroke-width="1.5"/>' +
      '<circle cx="26" cy="16" r="2" fill="#2c2c2a"/>' +
      '<line x1="42" y1="48" x2="42" y2="26" stroke="#2c2c2a" stroke-width="2.5" stroke-linecap="round"/>' +
      '<polygon points="39,26 42,19 45,26" fill="#2c2c2a"/>' +
      '<path d="M6,48 A6,6 0 0 1 18,48 Z" fill="none" stroke="#2c2c2a" stroke-width="1.5"/>' +
      '</svg>';
    return L.divIcon({{
      className: "",
      html: '<span class="bursa-marker">' + svgContent + '</span>',
      iconSize: [24, 24],
      iconAnchor: [12, 12]
    }});
  }} else if (name === "Vienna") {{
    const svgContent = '<svg width="26" height="26" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">' +
      /* drop shadow / rear wall */
      '<rect x="20" y="118" width="160" height="72" fill="#8c8c8c"/>' +
      '<rect x="42" y="70" width="34" height="120" fill="#8c8c8c"/>' +
      '<rect x="124" y="70" width="34" height="120" fill="#8c8c8c"/>' +
      '<rect x="86" y="52" width="28" height="138" fill="#8c8c8c"/>' +
      /* curtain wall with crenellations */
      '<rect x="14" y="112" width="172" height="66" fill="#e5e5e5" stroke="#111111" stroke-width="5"/>' +
      '<path d="M14,112 L14,96 L28,96 L28,112 L42,112 L42,96 L56,96 L56,112 L70,112 L70,96 L84,96 L84,112 L98,112 L98,96 L112,96 L112,112 L126,112 L126,96 L140,96 L140,112 L154,112 L154,96 L168,96 L168,112 L186,112" fill="none" stroke="#111111" stroke-width="5" stroke-linejoin="round"/>' +
      /* corner towers */
      '<rect x="34" y="62" width="30" height="128" fill="#e5e5e5" stroke="#111111" stroke-width="5"/>' +
      '<path d="M34,62 L34,44 L45,44 L45,62 M53,62 L53,44 L64,44 L64,62" fill="none" stroke="#111111" stroke-width="5" stroke-linejoin="round"/>' +
      '<polygon points="49,10 68,44 30,44" fill="#7c2020" stroke="#111111" stroke-width="5" stroke-linejoin="round"/>' +
      '<rect x="116" y="62" width="30" height="128" fill="#e5e5e5" stroke="#111111" stroke-width="5"/>' +
      '<path d="M116,62 L116,44 L127,44 L127,62 M135,62 L135,44 L146,44 L146,62" fill="none" stroke="#111111" stroke-width="5" stroke-linejoin="round"/>' +
      '<polygon points="131,10 150,44 112,44" fill="#7c2020" stroke="#111111" stroke-width="5" stroke-linejoin="round"/>' +
      /* central keep with spired roof, taller than the flanking towers */
      '<rect x="78" y="44" width="44" height="146" fill="#e5e5e5" stroke="#111111" stroke-width="5"/>' +
      '<path d="M78,44 L78,24 L90,24 L90,44 M110,44 L110,24 L122,24 L122,44" fill="none" stroke="#111111" stroke-width="5" stroke-linejoin="round"/>' +
      '<polygon points="100,-6 128,24 72,24" fill="#7c2020" stroke="#111111" stroke-width="5" stroke-linejoin="round"/>' +
      '<line x1="100" y1="-6" x2="100" y2="-20" stroke="#111111" stroke-width="4" stroke-linecap="round"/>' +
      '<circle cx="100" cy="-23" r="4" fill="#111111"/>' +
      /* windows and gate */
      '<rect x="44" y="90" width="10" height="14" fill="#111111"/>' +
      '<rect x="44" y="130" width="10" height="14" fill="#111111"/>' +
      '<rect x="126" y="90" width="10" height="14" fill="#111111"/>' +
      '<rect x="126" y="130" width="10" height="14" fill="#111111"/>' +
      '<rect x="93" y="72" width="14" height="16" fill="#111111"/>' +
      '<path d="M86,190 L86,156 A14,14 0 0 1 114,156 L114,190 Z" fill="#111111"/>' +
      /* portcullis bars over the gate */
      '<path d="M90,190 L90,168 M100,190 L100,158 M110,190 L110,168" stroke="#e5e5e5" stroke-width="2.5"/>' +
      '</svg>';
    return L.divIcon({{
      className: "",
      html: '<span class="vienna-marker">' + svgContent + '</span>',
      iconSize: [26, 26],
      iconAnchor: [13, 13]
    }});
  }}
  const svgContent = '<svg width="24" height="24" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg">' +
    '<circle cx="30" cy="30" r="15" fill="none" stroke="#2c2c2a" stroke-width="1.5"/>' +
    '<circle cx="30" cy="30" r="8" fill="#2c2c2a"/>' +
    '</svg>';
  return L.divIcon({{
    className: "",
    html: '<span class="city-marker">' + svgContent + '</span>',
    iconSize: [24, 24],
    iconAnchor: [12, 12]
  }});
}}

function fortressIcon() {{
  const svgContent = '<svg width="24" height="24" viewBox="0 0 200 196" xmlns="http://www.w3.org/2000/svg">' +
    '<polygon points="7,189 15,127 33,127 33,91 51,47 69,91 69,127 81,139 93,95 105,139 117,127 117,91 135,47 153,91 153,127 171,127 179,189" fill="#8c8c8c"/>' +
    '<polygon points="14,182 22,120 40,120 40,84 58,40 76,84 76,120 88,132 100,88 112,132 124,120 124,84 142,40 160,84 160,120 178,120 186,182" fill="#e5e5e5" stroke="#111111" stroke-width="6" stroke-linejoin="round"/>' +
    '<line x1="58" y1="40" x2="58" y2="13" stroke="#111111" stroke-width="4" stroke-linecap="round"/>' +
    '<path d="M58,13 C68,9 72,19 82,15 C74,23 68,17 58,21 Z" fill="#e5e5e5" stroke="#111111" stroke-width="3"/>' +
    '<line x1="142" y1="40" x2="142" y2="13" stroke="#111111" stroke-width="4" stroke-linecap="round"/>' +
    '<path d="M142,13 C152,9 156,19 166,15 C158,23 152,17 142,21 Z" fill="#e5e5e5" stroke="#111111" stroke-width="3"/>' +
    '<path d="M51,72 L51,62 A7,7 0 0 1 65,62 L65,72 Z" fill="#111111"/>' +
    '<path d="M135,72 L135,62 A7,7 0 0 1 149,62 L149,72 Z" fill="#111111"/>' +
    '<path d="M94,110 L94,102 A6,6 0 0 1 106,102 L106,110 Z" fill="#111111"/>' +
    '<path d="M82,182 L82,155 A18,18 0 0 1 118,155 L118,182 Z" fill="#111111"/>' +
    '<polygon points="50,160 58,146 58,174" fill="#111111"/>' +
    '<polygon points="70,160 62,146 62,174" fill="#111111"/>' +
    '<polygon points="130,160 138,146 138,174" fill="#111111"/>' +
    '<polygon points="150,160 142,146 142,174" fill="#111111"/>' +
    '</svg>';
  return L.divIcon({{
    className: "",
    html: '<span class="fortress-marker">' + svgContent + '</span>',
    iconSize: [24, 24],
    iconAnchor: [12, 12]
  }});
}}

function landBattleIcon() {{
  const svgContent = '<svg width="24" height="24" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg">' +
    '<line x1="10" y1="10" x2="50" y2="50" stroke="#2c2c2a" stroke-width="4" stroke-linecap="round"/>' +
    '<line x1="10" y1="50" x2="50" y2="10" stroke="#2c2c2a" stroke-width="4" stroke-linecap="round"/>' +
    '<circle cx="30" cy="30" r="3" fill="#2c2c2a"/>' +
    '</svg>';
  return L.divIcon({{
    className: "",
    html: '<span class="battle-marker">' + svgContent + '</span>',
    iconSize: [24, 24],
    iconAnchor: [12, 12]
  }});
}}

function navalBattleIcon() {{
  const svgContent = '<svg width="24" height="24" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg">' +
    '<circle cx="30" cy="9" r="5.5" fill="none" stroke="#2c2c2a" stroke-width="2.5"/>' +
    '<line x1="30" y1="14.5" x2="30" y2="42" stroke="#2c2c2a" stroke-width="3.5" stroke-linecap="round"/>' +
    '<line x1="16" y1="21" x2="44" y2="21" stroke="#2c2c2a" stroke-width="3" stroke-linecap="round"/>' +
    '<path d="M30,42 Q14,44 12,30" fill="none" stroke="#2c2c2a" stroke-width="3" stroke-linecap="round"/>' +
    '<path d="M30,42 Q46,44 48,30" fill="none" stroke="#2c2c2a" stroke-width="3" stroke-linecap="round"/>' +
    '</svg>';
  return L.divIcon({{
    className: "",
    html: '<span class="naval-marker">' + svgContent + '</span>',
    iconSize: [24, 24],
    iconAnchor: [12, 12]
  }});
}}

function treatyIcon() {{
  const svgContent = '<svg width="24" height="24" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg">' +
    '<rect x="16" y="18" width="28" height="22" fill="none" stroke="#2c2c2a" stroke-width="2"/>' +
    '<ellipse cx="16" cy="29" rx="3" ry="11" fill="none" stroke="#2c2c2a" stroke-width="2"/>' +
    '<ellipse cx="44" cy="29" rx="3" ry="11" fill="none" stroke="#2c2c2a" stroke-width="2"/>' +
    '<line x1="22" y1="24" x2="38" y2="24" stroke="#2c2c2a" stroke-width="1.5"/>' +
    '<line x1="22" y1="29" x2="38" y2="29" stroke="#2c2c2a" stroke-width="1.5"/>' +
    '<line x1="22" y1="34" x2="38" y2="34" stroke="#2c2c2a" stroke-width="1.5"/>' +
    '<line x1="30" y1="40" x2="30" y2="46" stroke="#2c2c2a" stroke-width="2"/>' +
    '<circle cx="30" cy="49" r="5" fill="#2c2c2a"/>' +
    '</svg>';
  return L.divIcon({{
    className: "",
    html: '<span class="treaty-marker">' + svgContent + '</span>',
    iconSize: [24, 24],
    iconAnchor: [12, 12]
  }});
}}

function battleIcon(kind) {{
  const isNaval = kind === "naval";
  const isTreaty = kind === "treaty";
  if (isNaval) {{
    return navalBattleIcon();
  }} else if (isTreaty) {{
    return treatyIcon();
  }}
  return landBattleIcon();
}}

function raidIcon() {{
  const svgContent = '<svg width="24" height="24" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg">' +
    '<line x1="10" y1="15" x2="50" y2="45" stroke="#2c2c2a" stroke-width="4" stroke-linecap="round"/>' +
    '<line x1="10" y1="45" x2="50" y2="15" stroke="#2c2c2a" stroke-width="4" stroke-linecap="round"/>' +
    '<polygon points="50,10 65,16 50,22" fill="#2c2c2a"/>' +
    '<polygon points="10,10 -5,16 10,22" fill="#2c2c2a"/>' +
    '</svg>';
  return L.divIcon({{
    className: "",
    html: '<span class="raid-marker">' + svgContent + '</span>',
    iconSize: [24, 24],
    iconAnchor: [12, 12]
  }});
}}

function siegeIcon() {{
  const svgContent = '<svg width="24" height="24" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg">' +
    '<circle cx="30" cy="30" r="27" fill="none" stroke="#2c2c2a" stroke-width="2"/>' +
    '<rect x="18" y="18" width="24" height="24" fill="none" stroke="#2c2c2a" stroke-width="2"/>' +
    '<line x1="18" y1="18" x2="42" y2="42" stroke="#2c2c2a" stroke-width="1.5"/>' +
    '<line x1="18" y1="42" x2="42" y2="18" stroke="#2c2c2a" stroke-width="1.5"/>' +
    '</svg>';
  return L.divIcon({{
    className: "",
    html: '<span class="siege-marker">' + svgContent + '</span>',
    iconSize: [24, 24],
    iconAnchor: [12, 12]
  }});
}}

function raidSiegeIcon() {{
  const svgContent = '<svg width="24" height="24" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg">' +
    '<defs>' +
    '<marker id="arrowIcon" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">' +
    '<path d="M2 1L8 5L2 9" fill="none" stroke="#2c2c2a" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>' +
    '</marker>' +
    '</defs>' +
    '<circle cx="30" cy="30" r="27" fill="none" stroke="#2c2c2a" stroke-width="2" stroke-linecap="round" stroke-dasharray="135 180" transform="rotate(140 30 30)"/><line x1="30" y1="30" x2="52" y2="52" stroke="#2c2c2a" stroke-width="2" marker-end="url(#arrowIcon)"/>' +
    '</svg>';
  return L.divIcon({{
    className: "",
    html: '<span class="raid-siege-marker">' + svgContent + '</span>',
    iconSize: [24, 24],
    iconAnchor: [12, 12]
  }});
}}

function sackedIcon() {{
  const svgContent = '<svg width="24" height="24" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg">' +
    '<line x1="42" y1="30" x2="58" y2="30" stroke="#2c2c2a" stroke-width="3" stroke-linecap="round"/>' +
    '<line x1="38.5" y1="38.5" x2="49.8" y2="49.8" stroke="#2c2c2a" stroke-width="3" stroke-linecap="round"/>' +
    '<line x1="30" y1="42" x2="30" y2="58" stroke="#2c2c2a" stroke-width="3" stroke-linecap="round"/>' +
    '<line x1="21.5" y1="38.5" x2="10.2" y2="49.8" stroke="#2c2c2a" stroke-width="3" stroke-linecap="round"/>' +
    '<line x1="18" y1="30" x2="2" y2="30" stroke="#2c2c2a" stroke-width="3" stroke-linecap="round"/>' +
    '<line x1="21.5" y1="21.5" x2="10.2" y2="10.2" stroke="#2c2c2a" stroke-width="3" stroke-linecap="round"/>' +
    '<line x1="30" y1="18" x2="30" y2="2" stroke="#2c2c2a" stroke-width="3" stroke-linecap="round"/>' +
    '<line x1="38.5" y1="21.5" x2="49.8" y2="10.2" stroke="#2c2c2a" stroke-width="3" stroke-linecap="round"/>' +
    '</svg>';
  return L.divIcon({{
    className: "",
    html: '<span class="sacked-marker">' + svgContent + '</span>',
    iconSize: [24, 24],
    iconAnchor: [12, 12]
  }});
}}

function revoltIcon() {{
  const svgContent = '<svg width="24" height="24" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg">' +
    '<rect x="23" y="38" width="14" height="16" rx="3" fill="#2c2c2a"/>' +
    '<rect x="15" y="24" width="30" height="18" rx="8" fill="#2c2c2a"/>' +
    '<circle cx="21" cy="18" r="7" fill="#2c2c2a"/>' +
    '<circle cx="30" cy="14" r="8" fill="#2c2c2a"/>' +
    '<circle cx="39" cy="18" r="7" fill="#2c2c2a"/>' +
    '<path d="M13,30 C10,25 14,19 20,20 L24,25 L15,34 Z" fill="#2c2c2a"/>' +
    '</svg>';
  return L.divIcon({{
    className: "",
    html: '<span class="revolt-marker">' + svgContent + '</span>',
    iconSize: [24, 24],
    iconAnchor: [12, 12]
  }});
}}

function featureCenter(feature) {{
  const geom = feature.geometry;
  const rings = geom.type === "Polygon" ? geom.coordinates : geom.coordinates.flat();
  const ring = rings.reduce((best, current) => current.length > best.length ? current : best, rings[0]);
  const sum = ring.reduce((acc, point) => [acc[0] + point[0], acc[1] + point[1]], [0, 0]);
  return [sum[1] / ring.length, sum[0] / ring.length];
}}

function renderTerritoryLabels(features) {{
  labelGroup.clearLayers();
  features.forEach(feature => {{
    const p = feature.properties;
    const center = featureCenter(feature);
    const className = "territory-label " + p.relation;
    L.marker(center, {{
      icon: L.divIcon({{className: "", html: '<div class="' + className + '">' + p.name + '</div>', iconSize: [132, 40], iconAnchor: [66, 20]}}),
      interactive: false
    }}).addTo(labelGroup);
  }});
}}

function renderPoints(year) {{
  cityGroup.clearLayers();
  battleGroup.clearLayers();
  navalGroup.clearLayers();
  treatyGroup.clearLayers();
  raidGroup.clearLayers();
  siegeGroup.clearLayers();
  raidSiegeGroup.clearLayers();
  sackedGroup.clearLayers();
  revoltGroup.clearLayers();
  campaignGroup.clearLayers();

  ATLAS.cities.forEach(item => {{
    let name, lat, lon, start, note, kind, defenseType;
    if (Array.isArray(item)) {{
      name = item[0]; lat = item[1]; lon = item[2]; start = item[3]; note = item[4]; kind = item[5]; defenseType = item[6] || "general";
    }} else {{
      name = item.name; lat = item.lat; lon = item.lon; start = item.start; note = item.note || item.summary; kind = item.kind; defenseType = item.defense_type || "general";
    }}

    const isFortress = kind === "fortress" || defenseType !== "general";
    
    if (isFortress && currentDefenseFilter !== "all" && defenseType !== currentDefenseFilter) {{
      return;
    }}

    if (start === null || start <= year) {{
      const icon = isFortress ? fortressIcon() : cityIcon(name);
      const tooltipLabel = isFortress ? "<b>Fortress: " + name + "</b><br>" + (note || "") + (defenseType !== "general" ? "<br><i>Type: " + defenseType.replace("_", " ") + "</i>" : "") : "<b>" + name + "</b><br><span>" + (note || "") + "</span>";
      
      L.marker([lat, lon], {{icon: icon}})
        .bindTooltip('<div class="atlas-tooltip">' + tooltipLabel + '</div>', {{sticky: true}})
        .addTo(cityGroup);
    }}
  }});

  ATLAS.battles.forEach(battle => {{
    const hasCustomPeriod = battlePeriodFrom !== null || battlePeriodTo !== null;
    const inRange = hasCustomPeriod
      ? (battlePeriodFrom === null || battle.year >= battlePeriodFrom) && (battlePeriodTo === null || battle.year <= battlePeriodTo)
      : battle.year <= year && (!battleMinYear || battle.year >= battleMinYear);
    if (inRange) {{
      const isNaval = battle.kind === "naval";
      const isTreaty = battle.kind === "treaty";
      const isRaid = battle.kind === "raid";
      const isSiege = battle.kind === "siege";
      const isRaidSiege = battle.kind === "raid/siege";
      const isSacked = battle.kind === "sacked";
      const isRevolt = battle.kind === "revolt";

      if (isRevolt && !showRevolts) {{
        return;
      }}

      let targetGroup = battleGroup;
      let icon = battleIcon(battle.kind);

      if (isNaval) {{
        targetGroup = navalGroup;
        icon = navalBattleIcon();
      }} else if (isTreaty) {{
        targetGroup = treatyGroup;
        icon = treatyIcon();
      }} else if (isRaid) {{
        targetGroup = raidGroup;
        icon = raidIcon();
      }} else if (isSiege) {{
        targetGroup = siegeGroup;
        icon = siegeIcon();
      }} else if (isRaidSiege) {{
        targetGroup = raidSiegeGroup;
        icon = raidSiegeIcon();
      }} else if (isSacked) {{
        targetGroup = sackedGroup;
        icon = sackedIcon();
      }} else if (isRevolt) {{
        targetGroup = revoltGroup;
        icon = revoltIcon();
      }}

      L.marker([battle.lat, battle.lon], {{icon: icon}})
        .bindTooltip('<div class="atlas-tooltip"><b>' + battle.name + '</b><br>' + battle.date + ' · ' + battle.kind + '</div>', {{sticky: true}})
        .on("click", () => openInfoCard(
          '<h3>' + battle.name + '</h3>' +
          '<p><b>' + t("info_date") + ':</b> ' + battle.date + ' &middot; ' + battle.kind + '</p>' +
          '<p><b>' + t("info_commanders") + ':</b> ' + battle.commanders + '</p>' +
          '<p><b>' + t("info_result") + ':</b> ' + battle.result + '</p>' +
          '<p><b>' + t("info_importance") + ':</b> ' + battle.importance + '</p>' +
          '<p><b>' + t("info_casualties") + ':</b> ' + battle.casualties + '</p>'
        ))
        .addTo(targetGroup);
    }}
  }});

  ATLAS.campaigns.forEach(route => {{
    if (route.start <= year) {{
      const latlngs = route.points.map(pt => [pt[1], pt[0]]);
      const visiblePoints = route.end <= year ? latlngs : latlngs.slice(0, Math.max(2, Math.ceil(latlngs.length * 0.55)));
      L.polyline(visiblePoints, {{
        color: "#2c2c2a",
        weight: 3,
        opacity: 0.85,
        dashArray: "6 4",
        lineCap: "round",
        lineJoin: "round"
      }}).bindTooltip('<div class="atlas-tooltip"><b>' + route.name + '</b><br>' + route.summary + '</div>', {{sticky: true}}).addTo(campaignGroup);
    }}
  }});

  if (typeof updateVisibleCountChip === "function") {{
    updateVisibleCountChip();
  }}
}}

function eventFor(year) {{
  return ATLAS.events.filter(event => event.year <= year).sort((a, b) => b.year - a.year)[0] || ATLAS.events[0];
}}

function nearestEventYear(direction) {{
  const years = ATLAS.events.map(event => event.year).sort((a, b) => a - b);
  if (direction < 0) {{
    return [...years].reverse().find(year => year < currentYear) || ATLAS.start;
  }}
  return years.find(year => year > currentYear) || ATLAS.end;
}}

function updateStats(year, event, activeFeatures) {{
  const provinces = activeFeatures.filter(feature => feature.properties.power === "Ottoman Province").length;
  const vassals = activeFeatures.filter(feature => feature.properties.relation === "vassal").length;
  statYear.textContent = year;
  const sultanName = event.sultan || "Unknown";
  statSultan.textContent = sultanName;
  statTerritory.textContent = activeFeatures.length + " layers";
  statPopulation.textContent = event.population || "Historical estimate varies";
  statProvinces.textContent = provinces;
  statVassals.textContent = vassals;
  statRival.textContent = event.largest_rival || "Regional rivals";
  if (sultanTughra) {{
    sultanTughra.textContent = sultanName.trim().charAt(0) || "?";
    sultanTughra.title = sultanName;
  }}
}}

function setYear(year) {{
  currentYear = Math.max(ATLAS.start, Math.min(ATLAS.end, Number(year)));
  slider.value = currentYear;
  yearEl.textContent = currentYear;
  const event = eventFor(currentYear);
  eventTitle.textContent = event.year + " · " + event.title;
  eventBody.textContent = event.body;
  const activeFeatures = ATLAS.territories.features.filter(feature => activeInYear(feature, currentYear));
  territoryLayer.clearLayers();
  territoryLayer.addData({{
    type: "FeatureCollection",
    features: activeFeatures
  }});
  renderTerritoryLabels(activeFeatures);
  renderPoints(currentYear);
  renderBorderLines(currentYear);
  renderRivers(currentYear);
  renderSteppeRegions(currentYear);
  renderForestRegions(currentYear);
  renderMountainRanges(currentYear);
  renderBridges();
  renderMountainPasses();
  renderIronGates();
  updateStats(currentYear, event, activeFeatures);
  if (window.history && window.history.replaceState) {{
    window.history.replaceState(null, "", "#year=" + currentYear);
  }}
}}

function togglePlay() {{
  if (timer) {{
    clearInterval(timer);
    timer = null;
    playButton.textContent = "▶";
    playButton.classList.remove("is-active");
    return;
  }}
  playButton.textContent = "Ⅱ";
  playButton.classList.add("is-active");
  timer = setInterval(() => {{
    const next = currentYear >= ATLAS.end ? ATLAS.start : currentYear + 2;
    setYear(next);
  }}, Number(speedControl.value));
}}

slider.addEventListener("input", event => setYear(event.target.value));
prevButton.addEventListener("click", () => setYear(nearestEventYear(-1)));
nextButton.addEventListener("click", () => setYear(nearestEventYear(1)));
playButton.addEventListener("click", togglePlay);
speedControl.addEventListener("change", () => {{
  if (timer) {{
    togglePlay();
    togglePlay();
  }}
}});
docButton.addEventListener("click", () => {{
  document.body.classList.toggle("documentary-mode");
  docButton.classList.toggle("is-active");
}});

const minBtn = document.getElementById("minimize-button");
const atlasPanel = document.querySelector(".atlas-panel");
minBtn.addEventListener("click", () => {{
  const isMin = atlasPanel.classList.toggle("is-minimized");
  minBtn.innerHTML = isMin ? "&#9650;" : "&#9660;";
  minBtn.title = isMin ? "Expand Panel" : "Minimize Panel";
}});

const titleMinBtn = document.getElementById("title-minimize-button");
const atlasTitle = document.querySelector(".atlas-title");
titleMinBtn.addEventListener("click", () => {{
  const isMin = atlasTitle.classList.toggle("is-minimized");
  titleMinBtn.innerHTML = isMin ? "&#9660;" : "&#9650;";
  titleMinBtn.title = isMin ? "Expand Title" : "Minimize Title";
}});

/* --- Tabs --- */
const tabButtons = document.querySelectorAll(".atlas-tab-btn");
const tabPanels = document.querySelectorAll(".atlas-tab-panel");
function activateTab(name) {{
  tabButtons.forEach(btn => btn.classList.toggle("is-active", btn.getAttribute("data-tab") === name));
  tabPanels.forEach(panel => {{
    const match = panel.getAttribute("data-tab-panel") === name;
    panel.hidden = !match;
  }});
}}
tabButtons.forEach(btn => btn.addEventListener("click", () => {{
  if (atlasPanel.classList.contains("is-minimized")) {{
    atlasPanel.classList.remove("is-minimized");
    minBtn.innerHTML = "&#9660;";
    minBtn.title = "Minimize Panel";
  }}
  activateTab(btn.getAttribute("data-tab"));
}}));

/* --- Legend filter search --- */
const legendSearch = document.getElementById("legend-search");
const legendGrid = document.getElementById("legend-grid");
if (legendSearch && legendGrid) {{
  legendSearch.addEventListener("input", () => {{
    const query = legendSearch.value.trim().toLowerCase();
    legendGrid.querySelectorAll(".legend-chip").forEach(chip => {{
      const text = chip.textContent.trim().toLowerCase();
      chip.style.display = !query || text.includes(query) ? "inline-flex" : "none";
    }});
  }});
}}

/* --- Day / night theme toggle --- */
const themeToggle = document.getElementById("theme-toggle");
themeToggle.addEventListener("click", () => {{
  const isNight = document.documentElement.getAttribute("data-theme") === "night";
  document.documentElement.setAttribute("data-theme", isNight ? "day" : "night");
  themeToggle.innerHTML = isNight ? "&#9789;" : "&#9788;";
  themeToggle.classList.toggle("is-active", !isNight);
}});

/* --- Era markers + Golden Age band on the timeline slider --- */
const ERA_MARKERS = [
  {{year: 1453, label: "1453 \\u2014 Fall of Constantinople"}},
  {{year: 1521, label: "1521 \\u2014 Belgrade falls"}},
  {{year: 1566, label: "1566 \\u2014 Death of Suleiman"}},
  {{year: 1683, label: "1683 \\u2014 Siege of Vienna"}},
  {{year: 1699, label: "1699 \\u2014 Treaty of Karlowitz"}}
];
const GOLDEN_AGE = {{start: 1520, end: 1566}};
function yearToPercent(year) {{
  return ((year - ATLAS.start) / (ATLAS.end - ATLAS.start)) * 100;
}}
function renderEraTicks() {{
  const ticksEl = document.getElementById("era-ticks");
  const bandEl = document.getElementById("golden-age-band");
  if (ticksEl) {{
    ticksEl.innerHTML = "";
    ERA_MARKERS.forEach(marker => {{
      if (marker.year < ATLAS.start || marker.year > ATLAS.end) return;
      const tick = document.createElement("div");
      tick.className = "era-tick";
      tick.style.left = yearToPercent(marker.year) + "%";
      tick.setAttribute("data-label", marker.label);
      tick.title = marker.label;
      tick.addEventListener("click", () => setYear(marker.year));
      ticksEl.appendChild(tick);
    }});
  }}
  if (bandEl) {{
    const bandStart = Math.max(GOLDEN_AGE.start, ATLAS.start);
    const bandEnd = Math.min(GOLDEN_AGE.end, ATLAS.end);
    if (bandEnd > bandStart) {{
      bandEl.style.display = "block";
      bandEl.style.left = yearToPercent(bandStart) + "%";
      bandEl.style.width = (yearToPercent(bandEnd) - yearToPercent(bandStart)) + "%";
    }}
  }}
}}

/* --- Click-to-lock info card (territories & battles) --- */
const infoCard = document.getElementById("info-card");
const infoCardBody = document.getElementById("info-card-body");
const infoCardClose = document.getElementById("info-card-close");
function openInfoCard(html) {{
  if (!infoCard || !infoCardBody) return;
  infoCardBody.innerHTML = html;
  infoCard.classList.add("is-visible");
}}
function closeInfoCard() {{
  if (infoCard) infoCard.classList.remove("is-visible");
}}
if (infoCardClose) infoCardClose.addEventListener("click", closeInfoCard);

/* --- English / Turkish UI language toggle --- */
const TRANSLATIONS = {{
  subtitle: {{en: "Interactive historical atlas of the Ottoman Empire's expansion on all major frontiers.", tr: "Osmanl\\u0131 \\u0130mparatorlu\\u011fu'nun t\\u00fcm b\\u00fcy\\u00fck cephelerdeki geni\\u015flemesini g\\u00f6steren etkile\\u015fimli tarihi atlas."}},
  search_placeholder: {{en: "Search a city, battle, or province\\u2026", tr: "Bir \\u015fehir, sava\\u015f veya eyalet ara\\u2026"}},
  hint_step: {{en: "step year", tr: "y\\u0131l ilerlet"}},
  hint_play: {{en: "play/pause", tr: "oynat/duraklat"}},
  hint_search: {{en: "search", tr: "ara"}},
  hint_night: {{en: "night mode", tr: "gece modu"}},
  tab_story: {{en: "Chronicle", tr: "Kronik"}},
  tab_stats: {{en: "Realm Stats", tr: "Devlet \\u0130statistikleri"}},
  tab_filters: {{en: "Filters", tr: "Filtreler"}},
  tab_legend: {{en: "Legend", tr: "Lejant"}},
  stat_year: {{en: "Current Year", tr: "Mevcut Y\\u0131l"}},
  stat_sultan: {{en: "Sultan", tr: "Sultan"}},
  stat_territory: {{en: "Territory", tr: "Toprak"}},
  stat_population: {{en: "Population", tr: "N\\u00fcfus"}},
  stat_provinces: {{en: "Provinces", tr: "Eyaletler"}},
  stat_vassals: {{en: "Vassals", tr: "Vasal Devletler"}},
  stat_rival: {{en: "Largest Rival", tr: "En B\\u00fcy\\u00fck Rakip"}},
  filter_fortress: {{en: "Fortress Filter:", tr: "Kale Filtresi:"}},
  filter_all: {{en: "All", tr: "T\\u00fcm\\u00fc"}},
  filter_star: {{en: "Star Forts", tr: "Y\\u0131ld\\u0131z Kaleler"}},
  filter_earthwork: {{en: "Earthworks", tr: "Toprak Tabyalar"}},
  filter_stone: {{en: "Stone", tr: "Ta\\u015f"}},
  filter_transitional: {{en: "Transitional", tr: "Ge\\u00e7i\\u015f D\\u00f6nemi"}},
  filter_era: {{en: "Battle Era:", tr: "Sava\\u015f D\\u00f6nemi:"}},
  filter_unrest: {{en: "Unrest:", tr: "Huzursuzluk:"}},
  filter_revolts: {{en: "Revolts", tr: "İsyanlar"}},
  speed_slow: {{en: "Slow", tr: "Yava\\u015f"}},
  speed_normal: {{en: "Normal", tr: "Normal"}},
  speed_fast: {{en: "Fast", tr: "H\\u0131zl\\u0131"}},
  compare_year_a: {{en: "Year A", tr: "Y\\u0131l A"}},
  compare_year_b: {{en: "Year B", tr: "Y\\u0131l B"}},
  compare_apply: {{en: "Show changes", tr: "De\\u011fi\\u015fiklikleri g\\u00f6ster"}},
  compare_exit: {{en: "Exit", tr: "\\u00c7\\u0131k\\u0131\\u015f"}},
  compare_gained: {{en: "Gained", tr: "Kazan\\u0131lan"}},
  compare_lost: {{en: "Lost", tr: "Kaybedilen"}},
  compare_changed: {{en: "Changed power", tr: "El de\\u011fi\\u015ftirdi"}},
  info_ruler: {{en: "Ruler", tr: "H\\u00fck\\u00fcmdar"}},
  info_since: {{en: "Since", tr: "Beri"}},
  info_capital: {{en: "Capital", tr: "Ba\\u015fkent"}},
  info_date: {{en: "Date", tr: "Tarih"}},
  info_commanders: {{en: "Commanders", tr: "Komutanlar"}},
  info_result: {{en: "Result", tr: "Sonu\\u00e7"}},
  info_importance: {{en: "Importance", tr: "\\u00d6nem"}},
  info_casualties: {{en: "Casualties", tr: "Kay\\u0131plar"}},
  lang_toggle_title: {{en: "Switch to Turkish", tr: "\\u0130ngilizceye ge\\u00e7"}},
  copy_link_title: {{en: "Copy link to this year", tr: "Bu y\\u0131l\\u0131n ba\\u011flant\\u0131s\\u0131n\\u0131 kopyala"}},
  compare_title: {{en: "Compare two years", tr: "\\u0130ki y\\u0131l\\u0131 kar\\u015f\\u0131la\\u015ft\\u0131r"}},
  export_view_title: {{en: "Screenshot current view", tr: "Mevcut g\\u00f6r\\u00fcn\\u00fcm\\u00fc anl\\u0131k g\\u00f6r\\u00fcnt\\u00fcle"}},
  export_whole_title: {{en: "Export Ottoman territories, whole map", tr: "Osmanl\\u0131 topraklar\\u0131n\\u0131, t\\u00fcm harita olarak d\\u0131\\u015fa aktar"}}
}};
let currentLang = "en";
function t(key) {{
  const entry = TRANSLATIONS[key];
  if (!entry) return key;
  return entry[currentLang] || entry.en;
}}
const langToggle = document.getElementById("lang-toggle");
function applyLanguage(lang) {{
  currentLang = lang;
  document.querySelectorAll("[data-i18n]").forEach(el => {{ el.textContent = t(el.getAttribute("data-i18n")); }});
  document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {{ el.setAttribute("placeholder", t(el.getAttribute("data-i18n-placeholder"))); }});
  document.querySelectorAll("[data-i18n-title]").forEach(el => {{ el.setAttribute("title", t(el.getAttribute("data-i18n-title"))); }});
  if (langToggle) langToggle.textContent = lang === "en" ? "EN" : "TR";
}}
if (langToggle) {{
  langToggle.addEventListener("click", () => applyLanguage(currentLang === "en" ? "tr" : "en"));
}}

/* --- Compare mode: outline territorial change between two years --- */
let compareLayer = null;
const comparePanel = document.getElementById("compare-panel");
const compareYearA = document.getElementById("compare-year-a");
const compareYearB = document.getElementById("compare-year-b");
const compareButton = document.getElementById("compare-button");
const compareApply = document.getElementById("compare-apply");
const compareExit = document.getElementById("compare-exit");
function exitCompareMode() {{
  if (compareLayer) {{ map.removeLayer(compareLayer); compareLayer = null; }}
  if (comparePanel) comparePanel.classList.remove("is-visible");
  if (compareButton) compareButton.classList.remove("is-active");
}}
function runCompare() {{
  const yearA = Math.max(ATLAS.start, Math.min(ATLAS.end, parseInt(compareYearA.value, 10) || ATLAS.start));
  const yearB = Math.max(ATLAS.start, Math.min(ATLAS.end, parseInt(compareYearB.value, 10) || ATLAS.end));
  const featuresA = ATLAS.territories.features.filter(f => activeInYear(f, yearA));
  const featuresB = ATLAS.territories.features.filter(f => activeInYear(f, yearB));
  const powerA = new Map(featuresA.map(f => [f.properties.name, f.properties.power]));
  const powerB = new Map(featuresB.map(f => [f.properties.name, f.properties.power]));
  const outlines = [];
  featuresB.forEach(f => {{
    const name = f.properties.name;
    if (!powerA.has(name)) outlines.push({{feature: f, status: "gained"}});
    else if (powerA.get(name) !== powerB.get(name)) outlines.push({{feature: f, status: "changed"}});
  }});
  featuresA.forEach(f => {{
    if (!powerB.has(f.properties.name)) outlines.push({{feature: f, status: "lost"}});
  }});
  if (compareLayer) map.removeLayer(compareLayer);
  const colorFor = status => status === "gained" ? "#2f9e44" : status === "lost" ? "#c92a2a" : "#e8590c";
  compareLayer = L.geoJSON({{type: "FeatureCollection", features: outlines.map(o => o.feature)}}, {{
    style: feature => {{
      const entry = outlines.find(o => o.feature === feature);
      return {{color: colorFor(entry ? entry.status : "changed"), weight: 3.2, fill: false, dashArray: entry && entry.status === "lost" ? "5 4" : null}};
    }},
    onEachFeature: (feature, layer) => {{
      const entry = outlines.find(o => o.feature === feature);
      layer.bindTooltip('<div class="atlas-tooltip"><b>' + feature.properties.name + '</b><br>' + (entry ? entry.status : '') + '</div>', {{sticky: true}});
    }}
  }}).addTo(map);
  showToast(yearA + " \\u2192 " + yearB + ": " + outlines.length + " territories changed");
}}
if (compareButton) {{
  compareButton.addEventListener("click", () => {{
    const isActive = compareButton.classList.toggle("is-active");
    if (isActive) {{
      compareYearA.value = Math.max(ATLAS.start, currentYear - 50);
      compareYearB.value = currentYear;
      if (comparePanel) comparePanel.classList.add("is-visible");
    }} else {{
      exitCompareMode();
    }}
  }});
}}
if (compareApply) compareApply.addEventListener("click", runCompare);
if (compareExit) compareExit.addEventListener("click", exitCompareMode);

/* --- Print / export: parchment-framed PNG, rendered from Leaflet's own layers
   (not a DOM screenshot) so territory polygons never drift out of place. --- */
function frameAndDownload(sourceCanvas, year, captionText) {{
  const margin = 60;
  const canvas = document.createElement("canvas");
  canvas.width = sourceCanvas.width + margin * 2;
  canvas.height = sourceCanvas.height + margin * 2 + 40;
  const ctx = canvas.getContext("2d");
  ctx.fillStyle = "#fbf6ea";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.drawImage(sourceCanvas, margin, margin);
  ctx.strokeStyle = "#8a5f0a";
  ctx.lineWidth = 6;
  ctx.strokeRect(margin / 2, margin / 2, canvas.width - margin, canvas.height - margin);
  ctx.strokeStyle = "#b8860f";
  ctx.lineWidth = 1.5;
  ctx.strokeRect(margin - 8, margin - 8, sourceCanvas.width + 16, sourceCanvas.height + 16);

  /* Year badge in the top corner of the map */
  const badgeText = String(year);
  ctx.font = "700 26px Georgia, serif";
  const badgeTextWidth = ctx.measureText(badgeText).width;
  const badgePadX = 18;
  const badgePadY = 12;
  const badgeW = badgeTextWidth + badgePadX * 2;
  const badgeH = 26 + badgePadY * 2;
  const badgeX = margin + 16;
  const badgeY = margin + 16;
  ctx.fillStyle = "rgba(251, 246, 234, 0.92)";
  ctx.strokeStyle = "#8a5f0a";
  ctx.lineWidth = 2;
  const radius = 8;
  ctx.beginPath();
  ctx.moveTo(badgeX + radius, badgeY);
  ctx.arcTo(badgeX + badgeW, badgeY, badgeX + badgeW, badgeY + badgeH, radius);
  ctx.arcTo(badgeX + badgeW, badgeY + badgeH, badgeX, badgeY + badgeH, radius);
  ctx.arcTo(badgeX, badgeY + badgeH, badgeX, badgeY, radius);
  ctx.arcTo(badgeX, badgeY, badgeX + badgeW, badgeY, radius);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();
  ctx.fillStyle = "#241b18";
  ctx.textAlign = "left";
  ctx.textBaseline = "middle";
  ctx.fillText(badgeText, badgeX + badgePadX, badgeY + badgeH / 2 + 1);
  ctx.textBaseline = "alphabetic";

  ctx.fillStyle = "#241b18";
  ctx.font = "600 22px Georgia, serif";
  ctx.textAlign = "center";
  ctx.fillText(captionText, canvas.width / 2, canvas.height - margin / 2 + 8);

  const link = document.createElement("a");
  link.download = "ottoman-atlas-" + year + ".png";
  link.href = canvas.toDataURL("image/png");
  link.click();
}}

function captureMapToCanvas(onDone) {{
  if (typeof html2canvas === "undefined") {{
    showToast("Export tool failed to load");
    return;
  }}
  const mapEl = document.getElementById("map");
  document.body.classList.add("is-exporting");

  const mapRect = mapEl.getBoundingClientRect();
  const dpr = window.devicePixelRatio > 1 ? 2 : 1.5;

  const master = document.createElement("canvas");
  master.width = Math.max(1, Math.round(mapRect.width * dpr));
  master.height = Math.max(1, Math.round(mapRect.height * dpr));
  const ctx = master.getContext("2d");
  ctx.fillStyle = "#b5d0e2";
  ctx.fillRect(0, 0, master.width, master.height);

  /* Each Leaflet pane carries its own independent CSS transform for
     GPU-accelerated panning. Asking html2canvas to resolve the whole
     #map tree at once means it has to correctly compose those nested,
     sibling transforms itself -- and it doesn't reliably. Instead we
     capture each pane on its own (a much shallower transform depth)
     and place it using the browser's own getBoundingClientRect, which
     is always correct regardless of how the transform math resolves. */
  const paneSelectors = [
    ".leaflet-tile-pane",
    ".leaflet-overlay-pane",
    ".leaflet-shadow-pane",
    ".leaflet-marker-pane"
  ];
  const panes = paneSelectors.map(sel => mapEl.querySelector(sel)).filter(Boolean);

  function captureNext(i) {{
    if (i >= panes.length) {{
      document.body.classList.remove("is-exporting");
      onDone(master);
      return;
    }}
    const pane = panes[i];
    html2canvas(pane, {{
      useCORS: true,
      allowTaint: false,
      backgroundColor: null,
      scale: dpr,
      logging: false
    }}).then(paneCanvas => {{
      const rect = pane.getBoundingClientRect();
      const dx = Math.round((rect.left - mapRect.left) * dpr);
      const dy = Math.round((rect.top - mapRect.top) * dpr);
      ctx.drawImage(paneCanvas, dx, dy);
      captureNext(i + 1);
    }}).catch(() => {{
      /* a pane can be empty (e.g. no shadows this year) - skip rather than abort */
      captureNext(i + 1);
    }});
  }}

  captureNext(0);
}}

/* Option 1: screenshot exactly what's currently in view, no reframing */
const exportViewButton = document.getElementById("export-view-button");
if (exportViewButton) {{
  exportViewButton.addEventListener("click", () => {{
    showToast("Preparing export\\u2026");
    captureMapToCanvas(sourceCanvas => {{
      frameAndDownload(sourceCanvas, currentYear, "Ottoman Europe Historical Atlas \\u2014 " + currentYear);
    }});
  }});
}}

/* Option 2: fit the whole Ottoman realm for the current year, then screenshot */
const exportWholeButton = document.getElementById("export-whole-button");
if (exportWholeButton) {{
  exportWholeButton.addEventListener("click", () => {{
    const ottomanFeatures = ATLAS.territories.features.filter(feature =>
      activeInYear(feature, currentYear) && (feature.properties.power || "").indexOf("Ottoman") === 0
    );
    if (!ottomanFeatures.length) {{
      showToast("No Ottoman territory active this year");
      return;
    }}
    const bounds = L.geoJSON({{type: "FeatureCollection", features: ottomanFeatures}}).getBounds();
    const originalCenter = map.getCenter();
    const originalZoom = map.getZoom();
    showToast("Preparing export\\u2026");
    map.once("moveend", () => {{
      /* give tiles a moment to finish loading at the new extent before capture */
      setTimeout(() => {{
        captureMapToCanvas(sourceCanvas => {{
          frameAndDownload(sourceCanvas, currentYear, "The Ottoman Realm \\u2014 " + currentYear);
          map.setView(originalCenter, originalZoom, {{animate: false}});
        }});
      }}, 700);
    }});
    map.fitBounds(bounds, {{padding: [40, 40], animate: false}});
  }});
}}

/* --- Copy a bookmarkable link to the current year --- */
const linkButton = document.getElementById("link-button");
if (linkButton) {{
  linkButton.addEventListener("click", () => {{
    const url = window.location.href.split("#")[0] + "#year=" + currentYear;
    if (navigator.clipboard && navigator.clipboard.writeText) {{
      navigator.clipboard.writeText(url).then(() => showToast("Link copied")).catch(() => showToast(url));
    }} else {{
      showToast(url);
    }}
  }});
}}

/* --- Toast helper --- */
const toastEl = document.getElementById("atlas-toast");
let toastTimer = null;
function showToast(message) {{
  if (!toastEl) return;
  toastEl.textContent = message;
  toastEl.classList.add("is-visible");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toastEl.classList.remove("is-visible"), 2200);
}}

/* --- Loading overlay --- */
const loaderEl = document.getElementById("atlas-loader");
function hideLoader() {{
  if (loaderEl) loaderEl.classList.add("is-hidden");
}}
map.whenReady(() => setTimeout(hideLoader, 250));
setTimeout(hideLoader, 3000);

/* --- Keyboard shortcuts --- */
document.addEventListener("keydown", event => {{
  const tag = (event.target.tagName || "").toLowerCase();
  const typing = tag === "input" || tag === "select" || tag === "textarea";
  if (event.key === "/" && !typing) {{
    event.preventDefault();
    searchInput.focus();
    return;
  }}
  if (typing) return;
  if (event.code === "Space") {{
    event.preventDefault();
    togglePlay();
  }} else if (event.key === "ArrowRight") {{
    setYear(currentYear + (event.shiftKey ? 10 : 1));
  }} else if (event.key === "ArrowLeft") {{
    setYear(currentYear - (event.shiftKey ? 10 : 1));
  }} else if (event.key.toLowerCase() === "n") {{
    themeToggle.click();
  }} else if (event.key.toLowerCase() === "d") {{
    docButton.click();
  }} else if (event.key === "Escape") {{
    searchInput.blur();
    closeInfoCard();
  }}
}});

document.querySelectorAll(".filter-chip[data-defense]").forEach(btn => {{
  btn.addEventListener("click", () => {{
    document.querySelectorAll(".filter-chip[data-defense]").forEach(b => b.classList.remove("is-active"));
    btn.classList.add("is-active");
    currentDefenseFilter = btn.getAttribute("data-defense");
    renderPoints(currentYear);
  }});
}});

document.querySelectorAll(".filter-chip[data-era]").forEach(btn => {{
  btn.addEventListener("click", () => {{
    document.querySelectorAll(".filter-chip[data-era]").forEach(b => b.classList.remove("is-active"));
    btn.classList.add("is-active");
    battleMinYear = parseInt(btn.getAttribute("data-era"), 10) || 0;
    renderPoints(currentYear);
  }});
}});

const revoltToggle = document.getElementById("revolt-toggle");
if (revoltToggle) {{
  revoltToggle.addEventListener("click", () => {{
    showRevolts = !showRevolts;
    revoltToggle.classList.toggle("is-active", showRevolts);
    renderPoints(currentYear);
  }});
}}

const territoryOpacitySlider = document.getElementById("territory-opacity-slider");
const territoryOpacityValue = document.getElementById("territory-opacity-value");
if (territoryOpacitySlider) {{
  territoryOpacitySlider.addEventListener("input", () => {{
    territoryOpacityScale = Number(territoryOpacitySlider.value) / 100;
    territoryOpacityValue.textContent = territoryOpacitySlider.value + "%";
    territoryLayer.setStyle(styleFor);
  }});
}}

/* --- Battle custom time period box --- */
const battlePeriodToggle = document.getElementById("battle-period-toggle");
const battlePeriodBoxEl = document.querySelector(".battle-period-box");
const battlePeriodFromInput = document.getElementById("battle-year-from");
const battlePeriodToInput = document.getElementById("battle-year-to");
const battlePeriodApplyBtn = document.getElementById("battle-period-apply");
const battlePeriodResetBtn = document.getElementById("battle-period-reset");
const battlePeriodStatus = document.getElementById("battle-period-status");

battlePeriodToggle.addEventListener("click", () => {{
  const isMin = battlePeriodBoxEl.classList.toggle("is-minimized");
  battlePeriodToggle.innerHTML = isMin ? "&#9650;" : "&#9660;";
  battlePeriodToggle.title = isMin ? "Expand" : "Minimize";
}});

battlePeriodApplyBtn.addEventListener("click", () => {{
  const fromVal = battlePeriodFromInput.value.trim();
  const toVal = battlePeriodToInput.value.trim();
  battlePeriodFrom = fromVal === "" ? null : parseInt(fromVal, 10);
  battlePeriodTo = toVal === "" ? null : parseInt(toVal, 10);
  if (battlePeriodFrom === null && battlePeriodTo === null) {{
    battlePeriodStatus.textContent = "";
  }} else {{
    battlePeriodStatus.textContent = "Showing " + (battlePeriodFrom ?? ATLAS.start) + "\\u2013" + (battlePeriodTo ?? ATLAS.end);
  }}
  renderPoints(currentYear);
}});

battlePeriodResetBtn.addEventListener("click", () => {{
  battlePeriodFromInput.value = "";
  battlePeriodToInput.value = "";
  battlePeriodFrom = null;
  battlePeriodTo = null;
  battlePeriodStatus.textContent = "";
  renderPoints(currentYear);
}});

L.marker([39.20, 34.50], {{
  icon: L.divIcon({{
    className: "",
    html: '<div class="anatolia-map-label">Anatolia</div>',
    iconSize: [200, 30],
    iconAnchor: [100, 15]
  }}),
  interactive: false
}}).addTo(regionalLabelGroup);

const regionalLabels = [
  {{name: "Galicia", lat: 49.30, lon: 24.20}},
  {{name: "Bessarabia", lat: 46.85, lon: 29.25}},
  {{name: "Volhynia", lat: 50.80, lon: 25.50}},
  {{name: "Ruthenia", lat: 49.80, lon: 27.50}},
  {{name: "Duchy of Carniola", lat: 45.95, lon: 14.75}},
  {{name: "Bukovina", lat: 48.25, lon: 26.00}},
  {{name: "Southern Bug River", lat: 48.55, lon: 31.30}}, 
  {{name: "Danube River", lat: 45.15, lon: 28.45}}, 
  {{name: "Dniester River", lat: 48.37, lon: 27.27}}, 
  {{name: "Prut River", lat: 45.47, lon: 28.20}}, 
  {{name: "Dnieper River", lat: 47.38, lon: 33.40}}, 
  {{name: "Don River", lat: 47.22, lon: 39.71}}, 
  {{name: "Volga River", lat: 48.70, lon: 44.51}},
  {{name: "Iron Gates", lat: 44.67, lon: 22.53}},
  {{name: "Crown of the Kingdom of Poland", lat: 51.50, lon: 19.50}}, 
  {{name: "Grand Duchy of Lithuania", lat: 54.68, lon: 25.27}}, 
  {{name: "Kievan Rus", lat: 55.45, lon: 37.37}}, 
  {{name: "Cossack Ukraine", lat: 49.80, lon: 31.50}},
  {{name: "Maghreb", lat: 30.00, lon: 5.00}}, 
  {{name: "Egypt", lat: 26.82, lon: 30.80}}, 
  {{name: "Hejaz", lat: 24.00, lon: 39.50}}, 
  {{name: "Levant", lat: 34.80, lon: 36.50}}, 
  {{name: "Mesopotamia", lat: 33.30, lon: 44.30}},
  {{name: "Desolate Kipchak Steppe", lat: 47.50, lon: 37.00}}, 
  {{name: "Archduchy of Austria", lat: 48.20, lon: 14.30}},
  {{name: "Duchy of Styria", lat: 47.07, lon: 15.44}}, 
  {{name: "Crownlands of Bohemia", lat: 49.80, lon: 15.50}}, 
  {{name: "Italian Maritime Lordships", lat: 44.50, lon: 12.00}},
  {{name: "Balkan Peninsula", lat: 43.50, lon: 21.50}}, 
  {{name: "Kingdom of Croatia", lat: 45.10, lon: 15.80}}, 
  {{name: "Lands of St. Stephen's Crown", lat: 47.20, lon: 19.50}},
  {{name: "Dalmatia", lat: 43.50, lon: 16.40}},
  {{name: "Crimean Peninsula", lat: 45.30, lon: 34.30}},
  {{name: "Lesser Poland", lat: 50.06, lon: 19.94}},
  {{name: "Greater Poland", lat: 52.40, lon: 16.92}},
  {{name: "Mazovia", lat: 52.22, lon: 21.01}},
  {{name: "Samogitia", lat: 55.65, lon: 22.88}},
  {{name: "Black Ruthenia", lat: 53.38, lon: 25.82}},
  {{name: "Pontic-Caspian Steppe", lat: 47.50, lon: 47.00}},
  {{name: "Carpathian Mountains", lat: 49.00, lon: 24.50}},
  {{name: "Caucasus Mountains", lat: 42.30, lon: 44.00}},
  {{name: "Ural Mountains", lat: 60.00, lon: 60.00}},
  {{name: "Pripet Marshes", lat: 52.00, lon: 27.50}},
  {{name: "Monastic State of the Teutonic Knights", lat: 54.02, lon: 21.57}},
  {{name: "Kingdom of England", lat: 52.35, lon: -1.17}},
  {{name: "Kingdom of France", lat: 46.60, lon: 2.21}},
  {{name: "Crown of Aragon", lat: 41.59, lon: 0.88}},
  {{name: "Crown of Castile", lat: 40.41, lon: -3.70}},
  {{name: "Electorate of Saxony", lat: 51.10, lon: 13.38}},
  {{name: "Duchy of Bavaria", lat: 48.79, lon: 11.49}},
  {{name: "Electorate of Brandenburg", lat: 52.52, lon: 13.40}},
  {{name: "Palatinate", lat: 49.48, lon: 8.46}},
  {{name: "Archduchy of Austria", lat: 48.20, lon: 14.30}},
  {{name: "Kingdom of Sicily", lat: 37.59, lon: 14.01}},
  {{name: "Kingdom of Naples", lat: 40.85, lon: 14.26}},
  {{name: "Papal States", lat: 41.90, lon: 12.50}},
  {{name: "Republic of Genoa", lat: 44.40, lon: 8.93}},
  {{name: "Low Countries", lat: 50.85, lon: 4.35}},
  {{name: "Kingdom of Denmark", lat: 55.67, lon: 12.56}},
  {{name: "Duchy of Holstein", lat: 54.20, lon: 9.70}},
  {{name: "Duchy of Mecklenburg", lat: 53.63, lon: 11.87}},
  {{name: "Free City of Lübeck", lat: 53.86, lon: 10.68}},
  {{name: "Kingdom of Sweden", lat: 59.32, lon: 18.06}},
  {{name: "Kingdom of Norway", lat: 59.91, lon: 10.75}},
  {{name: "Peloponnese", lat: 37.60, lon: 22.00}},
  {{name: "Macedonia", lat: 40.65, lon: 22.90}},
  {{name: "Thrace", lat: 41.12, lon: 25.40}},
  {{name: "Thessaly", lat: 39.64, lon: 22.42}},
  {{name: "Epirus", lat: 39.66, lon: 20.85}},
  {{name: "Central Greece", lat: 38.55, lon: 23.00}},
  {{name: "Crete", lat: 35.24, lon: 24.80}},
  {{name: "Cyclades", lat: 37.00, lon: 25.30}},
  {{name: "Dodecanese", lat: 36.43, lon: 28.22}},
  {{name: "Volga Bulgaria", lat: 54.90, lon: 49.00}},
  {{name: "Tsarate of Bulgaria", lat: 42.73, lon: 25.48}},
  {{name: "Serbian Empire and Despotate", lat: 44.01, lon: 21.00}},
  {{name: "Principality of Albania", lat: 41.32, lon: 19.81}},
  {{name: "Kingdom of Macedonia", lat: 41.60, lon: 21.74}},
  {{name: "Medieval Realm of Rascia and Kosovo", lat: 42.60, lon: 20.90}},
  {{name: "Wallachia", lat: 44.43, lon: 26.10}},
  {{name: "Moldavia", lat: 47.00, lon: 28.85}},
  {{name: "Transylvania", lat: 46.77, lon: 23.59}},
  {{name: "Upper Hungary", lat: 48.71, lon: 21.25}},
  {{name: "Transdanubia", lat: 47.18, lon: 17.84}},
  {{name: "The Pannonian Plain", lat: 46.85, lon: 19.50}},
  {{name: "Szeklerland", lat: 46.35, lon: 25.80}},
  {{name: "Tatra Mountains", lat: 49.17, lon: 20.03}},
  {{name: "Podolian Upland", lat: 49.25, lon: 26.50}},
  {{name: "Southern Carpathians", lat: 45.50, lon: 24.50}},
  {{name: "Great Hungarian Plain", lat: 47.00, lon: 20.50}},
  {{name: "Little Hungarian Plain", lat: 47.75, lon: 17.50}},
  {{name: "Sudeten Mountains", lat: 50.75, lon: 16.30}},
  {{name: "Western Carpathians", lat: 49.20, lon: 19.50}},
  {{name: "Danubian Plain", lat: 43.50, lon: 25.00}},
  {{name: "Serbian Carpathians", lat: 44.40, lon: 22.00}},
  {{name: "Balkan Mountains", lat: 42.70, lon: 25.00}},
  {{name: "Dinaric Alps", lat: 43.50, lon: 18.50}},
  {{name: "Ore Mountains", lat: 50.50, lon: 13.00}},
  {{name: "Bohemian Forest", lat: 49.00, lon: 13.50}},
  {{name: "Alps", lat: 46.88, lon: 9.68}},
  {{name: "Black Sea", lat: 43.38, lon: 34.46}},
  {{name: "Red Sea", lat: 20.00, lon: 38.00}},
  {{name: "Mediterranean Sea", lat: 35.00, lon: 18.00}},
  {{name: "Caspian Sea", lat: 41.59, lon: 50.63}},
  {{name: "Sea of Marmara", lat: 40.70, lon: 28.20}},
  {{name: "Dardanelles", lat: 40.22, lon: 26.40}},
  {{name: "Bosphorus Strait", lat: 41.12, lon: 29.07}},
  {{name: "Sea of Azov", lat: 46.10, lon: 36.80}},
  {{name: "Adriatic Sea", lat: 42.50, lon: 17.50}},
  {{name: "Aegean Sea", lat: 39.00, lon: 25.00}},
  {{name: "Ionian Sea", lat: 38.00, lon: 20.00}},
  {{name: "Sava River", lat: 44.81, lon: 20.46}},
  {{name: "Rhine Valley", lat: 50.00, lon: 7.50}},
  {{name: "Pyrenees", lat: 42.68, lon: 0.82}},
  {{name: "Balearic Islands", lat: 39.50, lon: 3.00}},
  {{name: "Sardinia", lat: 40.12, lon: 9.01}},
  {{name: "Corsica", lat: 42.04, lon: 9.09}},
  {{name: "Vienna Basin", lat: 48.15, lon: 16.40}},
  {{name: "Dniester Corridor", lat: 48.50, lon: 28.00}},
  {{name: "Prut Valley", lat: 46.50, lon: 27.80}},
  {{name: "Morava–Vardar Corridor", lat: 42.00, lon: 21.40}},
  {{name: "Adriatic Coast", lat: 43.00, lon: 16.00}},
  {{name: "Black Sea Littoral", lat: 44.00, lon: 32.00}},
  {{name: "Silesia", lat: 50.06, lon: 19.94}},
  {{name: "Moravia", lat: 49.20, lon: 16.61}},
  {{name: "Granada", lat: 37.18, lon: -3.59}}
];

regionalLabels.forEach(reg => {{
  L.marker([reg.lat, reg.lon], {{
    icon: L.divIcon({{
      className: "",
      html: '<div class="anatolia-map-label">' + reg.name + '</div>',
      iconSize: [160, 30],
      iconAnchor: [80, 15]
    }}),
    interactive: false
  }}).addTo(regionalLabelGroup);
}});

const searchItems = [
  ...ATLAS.territories.features.map(feature => ({{label: feature.properties.name, year: feature.properties.start, latlng: null}})),
  ...ATLAS.cities.map(item => {{
    const name = Array.isArray(item) ? item[0] : item.name;
    const lat = Array.isArray(item) ? item[1] : item.lat;
    const lon = Array.isArray(item) ? item[2] : item.lon;
    const start = Array.isArray(item) ? item[3] : item.start;
    return {{label: name, year: start || currentYear, latlng: [lat, lon]}};
  }}),
  ...ATLAS.battles.map(battle => ({{label: battle.name, year: battle.year, latlng: [battle.lat, battle.lon]}}))
];
searchItems.forEach(item => {{
  const option = document.createElement("option");
  option.value = item.label;
  searchList.appendChild(option);
}});
searchInput.addEventListener("change", () => {{
  const item = searchItems.find(candidate => candidate.label.toLowerCase() === searchInput.value.toLowerCase());
  if (!item) return;
  setYear(item.year || currentYear);
  if (item.latlng) map.flyTo(item.latlng, 7, {{duration: 0.9}});
  showToast("Jumped to " + item.label);
  searchInput.blur();
}});

L.control.layers(null, {{
  "Territories and neighbours": territoryLayer,
  "Steppe Ecoregions": steppeGroup,
  "Forest Ecoregions": forestGroup,
  "Rivers": riverGroup,
  "Mountain Ranges": mountainGroup,
  "Bridges": bridgeGroup,
  "Mountain Passes": passGroup,
  "Iron Gates": ironGatesGroup,
  "Cities & Fortresses": cityGroup,
  "Land Battles": battleGroup,
  "Naval Battles": navalGroup,
  "Treaties": treatyGroup,
  "Raids": raidGroup,
  "Sieges": siegeGroup,
  "Raids/Sieges": raidSiegeGroup,
  "Sacked": sackedGroup,
  "Revolts": revoltGroup,
  "Campaign routes": campaignGroup,
  "Territory labels": labelGroup,
  "Regional Area Labels": regionalLabelGroup,
  "Defensive lines": borderLineGroup
}}, {{collapsed: window.innerWidth < 760, position: "topright"}}).addTo(map);

/* --- Bookmarkable years: read #year=YYYY from the URL on load --- */
const hashMatch = window.location.hash.match(/year=(\\d+)/);
if (hashMatch) {{
  const hashYear = Math.max(ATLAS.start, Math.min(ATLAS.end, parseInt(hashMatch[1], 10)));
  if (!Number.isNaN(hashYear)) currentYear = hashYear;
}}

renderEraTicks();
setYear(currentYear);
"""


def build_atlas(output_path="ottoman_europe_atlas.html"):
    """Build and save the interactive atlas."""
    output = Path(output_path)
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Ottoman Europe Historical Atlas</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
  <style>{_css()}</style>
</head>
<body>
  {_shell()}
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script src="https://unpkg.com/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
  <script>{_script()}</script>
</body>
</html>
"""
    output.write_text(html, encoding="utf-8")
    print(f"Atlas saved to {output.resolve()}")
    return output