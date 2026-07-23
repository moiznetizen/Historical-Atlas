from pathlib import Path

builder_path = Path("atlas/map_builder.py")

# Complete, error-free source for atlas/map_builder.py with all combined updates built-in
pristine_code = """\"\"\"Standalone Leaflet renderer for the Ottoman Europe atlas.\"\"\"

from __future__ import annotations

import json
from pathlib import Path

from .historical_data import (
    BATTLES,
    BOUNDS,
    CAMPAIGNS,
    CITIES,
    EVENTS,
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
    legend_items = "\\n".join(
        f".legend-{name.lower().replace(' ', '-')} {{ background: {color}; }}"
        for name, color in POWER_COLORS.items()
    )
    return f\"\"\"
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Libre+Baskerville:wght@400;700&family=Inter:wght@500;700&display=swap');
:root {{
  {css_palette_vars()}
  --glass: rgba(251, 246, 234, 0.92);
  --line: rgba(36, 27, 24, 0.20);
}}
html, body, #map {{
  width: 100%;
  height: 100%;
  margin: 0;
}}
body {{
  background: #8fb7bf;
  color: var(--ink);
}}
#map {{
  background: #8fb7bf;
  font-family: "Libre Baskerville", Georgia, serif;
}}
.leaflet-container {{
  font-family: "Libre Baskerville", Georgia, serif;
}}
.atlas-title, .atlas-panel {{
  position: fixed;
  z-index: 900;
  color: var(--ink);
  background: var(--glass);
  border: 1px solid var(--line);
  box-shadow: 0 18px 55px rgba(28, 20, 16, 0.27);
  backdrop-filter: blur(16px);
}}
.atlas-title {{
  top: 18px;
  left: 58px;
  width: min(440px, calc(100vw - 76px));
  padding: 18px 20px;
  border-radius: 12px;
}}
.atlas-title h1 {{
  margin: 0;
  font-family: Cinzel, Georgia, serif;
  font-size: clamp(22px, 2.2vw, 30px);
  letter-spacing: 0;
}}
.atlas-title p {{
  margin: 8px 0 0;
  color: rgba(36, 27, 24, 0.72);
  font-size: 13px;
  line-height: 1.55;
}}
.atlas-search {{
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 8px;
  align-items: center;
  margin-top: 12px;
  font: 12px Inter, sans-serif;
}}
.atlas-search input {{
  min-width: 0;
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 8px 10px;
  background: rgba(255, 255, 255, 0.58);
  color: var(--ink);
  font: 13px Inter, sans-serif;
}}
/* Panel Minimize Styles */
.atlas-panel {{
  left: 50%;
  bottom: 18px;
  transform: translateX(-50%);
  width: min(940px, calc(100vw - 32px));
  border-radius: 14px;
  overflow: hidden;
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
}}
.atlas-controls {{
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 14px;
  align-items: center;
  padding: 14px 16px 10px;
}}
.atlas-year {{
  min-width: 74px;
  color: var(--direct-dark);
  font-family: Cinzel, Georgia, serif;
  font-size: 24px;
  font-weight: 700;
}}
#atlas-slider {{
  width: 100%;
  accent-color: var(--direct);
}}
.atlas-buttons {{
  display: flex;
  gap: 8px;
}}
.atlas-button {{
  width: 38px;
  height: 34px;
  border: 1px solid rgba(95, 27, 22, 0.35);
  border-radius: 8px;
  color: var(--direct-dark);
  background: rgba(255, 255, 255, 0.46);
  cursor: pointer;
  font-family: Inter, sans-serif;
  font-weight: 700;
}}
.atlas-button.is-active {{
  color: #fff;
  background: var(--direct);
}}
.atlas-speed {{
  width: 76px;
  height: 34px;
  border: 1px solid rgba(95, 27, 22, 0.35);
  border-radius: 8px;
  color: var(--direct-dark);
  background: rgba(255, 255, 255, 0.46);
  font: 12px Inter, sans-serif;
}}
.atlas-story {{
  display: grid;
  grid-template-columns: 170px 1fr;
  gap: 12px;
  padding: 0 16px 14px;
  font-size: 13px;
  line-height: 1.55;
}}
.atlas-story strong {{
  color: var(--direct-dark);
  font-family: Cinzel, Georgia, serif;
  font-size: 15px;
}}
.atlas-legend {{
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  padding: 10px 16px;
  border-top: 1px solid var(--line);
  background: rgba(255, 255, 255, 0.24);
  font: 12px/1.4 Inter, sans-serif;
}}
.atlas-stats {{
  display: grid;
  grid-template-columns: repeat(7, minmax(92px, 1fr));
  gap: 1px;
  border-top: 1px solid var(--line);
  background: rgba(36, 27, 24, 0.12);
  font-family: Inter, sans-serif;
}}
.atlas-stats span {{
  display: grid;
  gap: 2px;
  padding: 8px 10px;
  background: rgba(255, 255, 255, 0.24);
}}
.atlas-stats b {{
  color: rgba(36, 27, 24, 0.62);
  font-size: 10px;
  text-transform: uppercase;
}}
.atlas-stats em {{
  min-width: 0;
  overflow: hidden;
  color: var(--direct-dark);
  font-size: 12px;
  font-style: normal;
  text-overflow: ellipsis;
  white-space: nowrap;
}}
.legend-chip {{
  display: inline-flex;
  gap: 6px;
  align-items: center;
}}
.legend-swatch {{
  width: 16px;
  height: 11px;
  border: 1px solid rgba(36, 27, 24, 0.28);
  border-radius: 3px;
}}
.atlas-tooltip {{
  max-width: 290px;
  font-family: "Libre Baskerville", Georgia, serif;
  line-height: 1.45;
}}
.atlas-tooltip b {{
  color: #5f1b16;
  font-family: Cinzel, Georgia, serif;
}}
.city-marker {{
  display: grid;
  place-items: center;
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.35);
  width: 10px;
  height: 10px;
  background: #2c1d16;
  border: 2px solid #fbf6ea;
}}
/* Aesthetic compact pointers CSS */
.battle-marker {{
  width: 12px;
  height: 12px;
  color: #8f2f2a;
  font-family: Inter, sans-serif;
  font-weight: 700;
  font-size: 11px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  text-shadow: 0 1px 0 #fbf6ea, 0 -1px 0 #fbf6ea, 1px 0 0 #fbf6ea, -1px 0 0 #fbf6ea;
  cursor: pointer;
}}
.battle-marker.naval {{
  color: #1f5b6d;
}}
.battle-marker.treaty {{
  color: #c7a06a;
}}
.anatolia-map-label {{
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
.route-label {{
  color: #4b2118;
  font: 700 12px Inter, sans-serif;
}}
.coord-readout, .fullscreen-faux {{
  padding: 5px 8px;
  border-radius: 6px;
  background: rgba(251, 246, 234, 0.86);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.18);
  font: 12px Inter, sans-serif;
}}
.fullscreen-faux {{
  cursor: pointer;
  font-weight: 700;
}}
.documentary-mode .leaflet-control-container {{
  opacity: 0.18;
}}
.documentary-mode .atlas-title {{
  width: min(560px, calc(100vw - 36px));
}}
.documentary-mode .atlas-panel {{
  width: min(760px, calc(100vw - 32px));
}}
{legend_items}
@media (max-width: 720px) {{
  .atlas-title {{
    top: 10px;
    left: 52px;
    width: calc(100vw - 62px);
    padding: 14px;
  }}
  .atlas-panel {{
    bottom: 8px;
    width: calc(100vw - 16px);
  }}
  .atlas-controls {{
    grid-template-columns: 1fr auto;
  }}
  #atlas-slider {{
    grid-column: 1 / -1;
  }}
  .atlas-story {{
    grid-template-columns: 1fr;
  }}
  .atlas-stats {{
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }}
}}
\"\"\"


def _shell():
    legend = "".join(
        f'<span class="legend-chip"><span class="legend-swatch" style="background:{color}"></span>{name}</span>'
        for name, color in POWER_COLORS.items()
    )
    return f\"\"\"
<div id="map"></div>
<div class="atlas-title">
  <h1>Ottoman Europe Atlas</h1>
  <p>Interactive historical atlas of Ottoman European expansion and neighbouring powers, focused on the Danube, Balkan, Black Sea, and Adriatic frontiers.</p>
  <label class="atlas-search"><span>Search</span><input id="atlas-search" list="atlas-search-list" placeholder="City, battle, province"><datalist id="atlas-search-list"></datalist></label>
</div>
<div class="atlas-panel">
  <div class="atlas-controls">
    <div class="atlas-year" id="atlas-year">{TIMELINE_START}</div>
    <input id="atlas-slider" type="range" min="{TIMELINE_START}" max="{TIMELINE_END}" value="{TIMELINE_START}" step="1" aria-label="Timeline year">
    <div class="atlas-buttons">
      <button class="atlas-button" id="prev-button" title="Previous event">&lt;</button>
      <button class="atlas-button" id="play-button" title="Play or pause timeline">▶</button>
      <button class="atlas-button" id="next-button" title="Next event">&gt;</button>
      <button class="atlas-button" id="doc-button" title="Toggle documentary mode">D</button>
      <button class="panel-toggle-btn" id="minimize-button" title="Minimize Panel">▼</button>
      <select class="atlas-speed" id="speed-control" title="Timeline speed">
        <option value="320">Slow</option>
        <option value="180" selected>Normal</option>
        <option value="80">Fast</option>
      </select>
    </div>
  </div>
  <div class="atlas-story">
    <strong id="event-title">Gallipoli seized</strong>
    <span id="event-body">The Ottomans gain their first permanent European foothold on the Dardanelles.</span>
  </div>
  <div class="atlas-stats">
    <span><b>Current Year</b><em id="stat-year">{TIMELINE_START}</em></span>
    <span><b>Sultan</b><em id="stat-sultan">Orhan</em></span>
    <span><b>Territory</b><em id="stat-territory">0 layers</em></span>
    <span><b>Population</b><em id="stat-population">Frontier polity</em></span>
    <span><b>Provinces</b><em id="stat-provinces">0</em></span>
    <span><b>Vassals</b><em id="stat-vassals">0</em></span>
    <span><b>Largest Rival</b><em id="stat-rival">Byzantine Empire</em></span>
  </div>
  <div class="atlas-legend">{legend}<span class="legend-chip"><span class="legend-swatch" style="background:transparent;border-style:dashed"></span>Vassal or temporary rule</span><span class="legend-chip">⚔ land battle</span><span class="legend-chip">⚓ naval battle</span></div>
</div>
\"\"\"


def _script():
    return f\"\"\"
const ATLAS = {{
  bounds: {_json([[30.0, 5.0], [56.5, 45.0]])},
  territories: {_json(_feature_collection(TERRITORIES))},
  events: {_json(EVENTS)},
  cities: {_json(CITIES)},
  battles: {_json(BATTLES)},
  campaigns: {_json(CAMPAIGNS)},
  colors: {_json(POWER_COLORS)},
  start: {TIMELINE_START},
  end: {TIMELINE_END}
}};

const map = L.map("map", {{
  zoomControl: true,
  maxBounds: ATLAS.bounds,
  maxBoundsViscosity: 0.4
}});
map.fitBounds(ATLAS.bounds);

L.tileLayer("https://{{s}}.basemaps.cartocdn.com/rastertiles/voyager_nolabels/{{z}}/{{x}}/{{y}}{{r}}.png", {{
  attribution: "OpenStreetMap contributors, CARTO",
  maxZoom: 18
}}).addTo(map);

let currentYear = ATLAS.start;
let timer = null;
const yearEl = document.getElementById("atlas-year");
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

L.control.scale({{imperial: false, position: "bottomleft"}}).addTo(map);

const coordControl = L.control({{position: "bottomleft"}});
coordControl.onAdd = function() {{
  const div = L.DomUtil.create("div", "coord-readout");
  div.textContent = "Move cursor for coordinates";
  map.on("mousemove", event => {{
    div.textContent = `${{event.latlng.lat.toFixed(2)}}N, ${{event.latlng.lng.toFixed(2)}}E`;
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
L.tileLayer("https://{{s}}.basemaps.cartocdn.com/light_nolabels/{{z}}/{{x}}/{{y}}{{r}}.png", {{maxZoom: 8}}).addTo(mini);
mini.fitBounds(ATLAS.bounds);

function activeInYear(item, year) {{
  const props = item.properties || item;
  return props.start <= year && year <= props.end;
}}

function styleFor(feature) {{
  const props = feature.properties;
  const relation = props.relation;
  const color = props.start === currentYear ? ATLAS.colors["Current Conquest"] : (ATLAS.colors[props.power] || "#0f5b44");
  return {{
    color: relation === "neighbour" ? "#5f665f" : "#5f1b16",
    weight: relation === "neighbour" ? 1.1 : 1.55,
    fillColor: color,
    fillOpacity: relation === "neighbour" ? 0.34 : relation === "vassal" ? 0.55 : relation === "temporary" ? 0.58 : 0.76,
    dashArray: relation === "direct" || relation === "neighbour" ? null : "8 5"
  }};
}}

function tooltip(feature) {{
  const p = feature.properties;
  const end = p.end > 1900 ? "later" : p.end;
  return `<div class="atlas-tooltip"><b>${{p.name}}</b><br>${{p.status}} · ${{p.start}}-${{end}}<br><em>${{p.capital}}</em><br>${{p.summary}}</div>`;
}}

const territoryLayer = L.geoJSON(null, {{
  style: styleFor,
  onEachFeature: (feature, layer) => {{
    layer.bindTooltip(tooltip(feature), {{sticky: true, opacity: 0.96}});
    layer.on("mouseover", () => layer.setStyle({{weight: 2.7, fillOpacity: Math.min((styleFor(feature).fillOpacity || 0.5) + 0.14, 0.9)}}));
    layer.on("mouseout", () => layer.setStyle(styleFor(feature)));
  }}
}}).addTo(map);
const labelGroup = L.layerGroup().addTo(map);
const cityGroup = L.layerGroup().addTo(map);
const battleGroup = L.layerGroup().addTo(map);
const campaignGroup = L.layerGroup().addTo(map);

function cityIcon() {{
  return L.divIcon({{className: "", html: '<span class="city-marker"></span>', iconSize: [14, 14], iconAnchor: [7, 7]}});
}}

function battleIcon(kind) {{
  const isNaval = kind === "naval";
  const isTreaty = kind === "treaty";
  let iconGlyph = "⚔";
  let cssClass = "";
  if (isNaval) {{
    iconGlyph = "⚓";
    cssClass = "naval";
  }} else if (isTreaty) {{
    iconGlyph = "📜";
    cssClass = "treaty";
  }}
  return L.divIcon({{
    className: "", 
    html: '<span class="battle-marker ' + cssClass + '">' + iconGlyph + '</span>', 
    iconSize: [12, 12], 
    iconAnchor: [6, 6]
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
    if (p.relation === "neighbour" && !["Habsburg Monarchy", "Polish-Lithuanian Commonwealth", "Venetian Republic", "Kingdom of Croatia"].includes(p.name)) return;
    const center = featureCenter(feature);
    const className = `territory-label ${{p.relation}}`;
    L.marker(center, {{
      icon: L.divIcon({{className: "", html: `<div class="${{className}}">${{p.name}}</div>`, iconSize: [132, 40], iconAnchor: [66, 20]}}),
      interactive: false
    }}).addTo(labelGroup);
  }});
}}

function renderPoints(year) {{
  cityGroup.clearLayers();
  battleGroup.clearLayers();
  campaignGroup.clearLayers();

  ATLAS.cities.forEach(([name, lat, lon, start, note]) => {{
    if (start === null || start <= year) {{
      L.marker([lat, lon], {{icon: cityIcon()}})
        .bindTooltip(`<div class="atlas-tooltip"><b>${{name}}</b><br>${{note}}</div>`, {{sticky: true}})
        .addTo(cityGroup);
    }}
  }});

  ATLAS.battles.forEach(battle => {{
    if (battle.year <= year) {{
      L.marker([battle.lat, battle.lon], {{icon: battleIcon(battle.kind)}})
        .bindTooltip(`<div class="atlas-tooltip"><b>${{battle.name}}</b><br>${{battle.date}} · ${{battle.kind}}<br><em>${{battle.commanders}}</em><br><b>Result:</b> ${{battle.result}}<br><b>Importance:</b> ${{battle.importance}}<br><b>Casualties:</b> ${{battle.casualties}}</div>`, {{sticky: true}})
        .addTo(battleGroup);
    }}
  }});

  ATLAS.campaigns.forEach(route => {{
    if (route.start <= year) {{
      const latlngs = route.points.map(([lon, lat]) => [lat, lon]);
      const visiblePoints = route.end <= year ? latlngs : latlngs.slice(0, Math.max(2, Math.ceil(latlngs.length * 0.55)));
      L.polyline(visiblePoints, {{
        color: route.name.includes("Aegean") ? "#1f5b6d" : "#642016",
        weight: 3,
        opacity: 0.78,
        dashArray: "10 8"
      }}).bindTooltip(`<div class="atlas-tooltip"><b>${{route.name}}</b><br>${{route.summary}}</div>`, {{sticky: true}}).addTo(campaignGroup);
    }}
  }});
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
  statSultan.textContent = event.sultan || "Unknown";
  statTerritory.textContent = `${{activeFeatures.length}} layers`;
  statPopulation.textContent = event.population || "Historical estimate varies";
  statProvinces.textContent = provinces;
  statVassals.textContent = vassals;
  statRival.textContent = event.largest_rival || "Regional rivals";
}}

function setYear(year) {{
  currentYear = Math.max(ATLAS.start, Math.min(ATLAS.end, Number(year)));
  slider.value = currentYear;
  yearEl.textContent = currentYear;
  const event = eventFor(currentYear);
  eventTitle.textContent = `${{event.year}} · ${{event.title}}`;
  eventBody.textContent = event.body;
  const activeFeatures = ATLAS.territories.features.filter(feature => activeInYear(feature, currentYear));
  territoryLayer.clearLayers();
  territoryLayer.addData({{
    type: "FeatureCollection",
    features: activeFeatures
  }});
  renderTerritoryLabels(activeFeatures);
  renderPoints(currentYear);
  updateStats(currentYear, event, activeFeatures);
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
  minBtn.textContent = isMin ? "▲" : "▼";
  minBtn.title = isMin ? "Expand Panel" : "Minimize Panel";
}});

// Standalone horizontal text label for Anatolia
L.marker([39.20, 34.50], {{
  icon: L.divIcon({{
    className: "",
    html: '<div class="anatolia-map-label">Anatolia</div>',
    iconSize: [200, 30],
    iconAnchor: [100, 15]
  }}),
  interactive: false
}}).addTo(map);

const searchItems = [
  ...ATLAS.territories.features.map(feature => ({{label: feature.properties.name, year: feature.properties.start, latlng: null}})),
  ...ATLAS.cities.map(([name, lat, lon, start]) => ({{label: name, year: start || currentYear, latlng: [lat, lon]}})),
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
}});

L.control.layers(null, {{
  "Territories and neighbours": territoryLayer,
  "Territory labels": labelGroup,
  "Cities": cityGroup,
  "Battles": battleGroup,
  "Campaign routes": campaignGroup
}}, {{collapsed: false, position: "topright"}}).addTo(map);

setYear(currentYear);
\"\"\"


def build_atlas(output_path="ottoman_europe_atlas.html"):
    \"\"\"Build and save the interactive atlas.\"\"\"
    output = Path(output_path)
    html = f\"\"\"<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Ottoman Europe Historical Atlas</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
  <style>{{_css()}}</style>
</head>
<body>
  {{_shell()}}
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script>{{_script()}}</script>
</body>
</html>
\"\"\"
    output.write_text(html, encoding="utf-8")
    print(f"Atlas saved to {output.resolve()}")
    return output
"""

# Completely overwrite with verified structural template code
builder_path.write_text(pristine_code, encoding="utf-8")
print("✓ map_builder.py fully restored with comprehensive and clean syntax.")

print("\nCompiling clean production atlas layout...")
try:
    from atlas.map_builder import build_atlas
    build_atlas("ottoman_europe_atlas.html")
    print("✓ Complete! Clear your browser cache and refresh 'ottoman_europe_atlas.html' to review.")
except Exception as e:
    print(f"X Compilation failed: {e}")