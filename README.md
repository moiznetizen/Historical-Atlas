# 🌍 Reconstructing the Pax Ottomana: Interactive Ottoman Empire Historical Atlas

> A fully interactive, standalone digital historical atlas and spatial-temporal GIS framework reconstructing the geopolitical expansion of the Ottoman Empire and its peripheral theaters across Europe, North Africa, the Middle East, and the Kipchak Steppe from 1354 to 1685.

---

## 🏛️ Project Overview & Historiographical Context
Traditional historical atlases of the Ottoman Empire often suffer from severe static visualization limitations, reducing centuries of shifting borders, vassal dependencies, and fluid frontier zones into rigid, isolated snapshots (e.g., 1453, 1566, 1683). Furthermore, mainstream historical narratives frequently omit micro-level engagements, small-scale border skirmishes, pitched sieges, and the precise administrative demarcation of eyalets and sanjaks that defined early modern imperial statecraft.

Grounded in authoritative historical scholarship—specifically incorporating the scholarly paradigm established by **Marc David Baer** in *The Ottomans: Khans, Caesars, and Caliphs*—this project models imperial evolution not merely through geopolitical conquest, but through institutional, dynastic, and strategic consolidation.

---

## 🚀 Key Features & Map Capabilities
* **Synchronized Moving Timeline & Events:** Interactive timeline slider (1354–1685) featuring playback controls (`Play/Pause`, speed modifiers) that dynamically render territorial polygons while simultaneously displaying corresponding historical event summaries from `events.json`.
* **Dynamic Sultan / Imperial Court Marker:** Automatically tracks and displays the reigning Ottoman sovereign over Constantinople across different historical epochs.
* **Granular Layer Controls:** Independent DOM layer toggles for:
  * *Territories and neighbours* (direct control, vassals, and regional rivals)
  * *Territory labels* and *Regional Area Labels* (Anatolia, Balkans, Levant, Kipchak Steppe, etc.)
  * *Cities & Fortresses* (distinguishing unfortified administrative hubs from hard military bastions like Belgrade, Buda, and Kars)
  * *Battles* (land engagements, naval encounters, and treaties)
  * *Campaign routes* (polyline vectors of major military expeditions)
* **Advanced Search & Camera Panning:** Search datalist indexing all territories, cities, and battles with automated viewport translation via Leaflet's `map.flyTo()`.
* **Contextual Tooltips:** Rich historical metadata on hover, detailing commanders, garrison strengths, battle results, and casualty estimates.

---

## 🛠️ Software Architecture & Python-to-Leaflet Pipeline
Developed by **Muhammad Abdul Moiz** (Graduate of Electrical Engineering, LUMS), the backend infrastructure uses a robust static-site generation pattern housed within the `atlas/` package directory:
1. **`utils.py` & `historical_data.py`:** Ingests and abstracts raw JSON datasets (`territories.json`, `events.json`, `cities.json`, `battles.json`, `campaigns.json`) with UTF-8 encoding.
2. **`styles.py`:** Manages visual design tokens, compiling color palettes for over twenty distinct geopolitical entities (Ottoman Eyalets, Habsburg Monarchy, Venetian Republic, Safavid Iran, Crimean Khanate, etc.) into CSS custom properties.
3. **`map_builder.py`:** The primary compilation engine that transforms raw spatial polygon arrays into valid GeoJSON `FeatureCollection` objects, merges them with custom CSS styles, and renders a high-performance standalone HTML document (`index.html` / `ottoman_europe_atlas.html`).

---

## 🔄 Iterative Data Refinement via Modular Patch Scripts
To maintain absolute historical fidelity across centuries of shifting borders, the project workflow incorporates a suite of modular Python patch scripts for non-destructive updates:
* `patch_north_africa_provinces.py`: Injects precise provincial boundaries for Algiers, Tripoli, Tunis, and Egypt.
* `patch_anatolia_dynamic.py` & `patch_albania_dynamic.py`: Manages sequential Anatolian beylik annexations and Balkan territorial transitions.
* `patch_crimean_campaigns.py`: Appends Eurasian steppe military campaigns (e.g., Sack of Kyiv, Great Crimean Raid on Moscow).
* `align_hungary_to_budin.py`: Re-engineers spatial geometries for Royal Hungary to ensure clean borders alongside the Eyalet of Budin.
* `patch_porte.py` & `patch_map_view.py`: Injects UI tokens (Sublime Porte star marker `★` for Constantinople) and default viewport settings.
* `verify_territories.py`: Validates data integrity across regional entries.

---

## 📚 How to Use This Project to Learn About the Ottomans
1. **Chronological Exploration:** Set the timeline slider to 1354 to observe the initial Gallipoli bridgehead, then step forward year-by-year to witness the transformation into a transcontinental empire.
2. **Thematic Layer Filtering:** Isolate "Cities & Fortresses" alongside "Battles" to study military logistics, supply lines, and fortress warfare.
3. **Event Correlation:** Read the synchronized event ticker at each timeline step to connect political milestones (e.g., Fall of Constantinople in 1453) directly with their spatial consequences.
4. **Targeted Search:** Use the search bar to locate specific historical nodes (e.g., Vienna, Algiers, Kars) and examine their administrative status.

---

## 📦 Project Directory Structure
```text
updated/
├── atlas/
│   ├── __init__.py
│   ├── historical_data.py
│   ├── map_builder.py
│   └── styles.py
├── data/
│   ├── battles.json
│   ├── campaigns.json
│   ├── cities.json
│   ├── events.json
│   └── territories.json
├── patch_*.py            # Modular data refinement scripts
├── index.html            # Compiled production Leaflet map (GitHub Pages entry)
└── README.md****
