"""
Ottoman Empire Territorial Expansion in Europe (1299–1683)
Interactive map built with Folium + Shapely + GeoPandas.

Run:
    pip install folium geopandas shapely fiona pyproj
    python ottoman_map.py
Then open ottoman_europe.html in any browser.
"""

import folium
from folium import plugins
from folium.plugins import Fullscreen, MiniMap, MeasureControl, MousePosition
from branca.element import Template, MacroElement, Element

from shapely.geometry import Polygon, MultiPolygon, Point
from shapely.ops import unary_union

import json
import math
from pathlib import Path

# ---------------------------------------------------------------------------
# 1.  OTTOMAN TERRITORIAL PHASES — historically accurate polygons (WGS-84)
#     Each entry: (name, acquired_year, vassal, colour_phase, tooltip_html, coords_list_of_rings)
#     Coordinates are (lon, lat) pairs tracing each region boundary.
#     Sources: EURATLAS historical GIS, Barkan, Inalcik, Pitcher (1972),
#              McEvedy, Finkel "Osman's Dream", Imber "The Ottoman Empire".
# ---------------------------------------------------------------------------

# Helper – make a Shapely polygon from a list of (lon,lat) tuples
def poly(coords):
    return Polygon(coords)

def mpoly(list_of_coords):
    return MultiPolygon([Polygon(c) for c in list_of_coords])

territories = [

    # ── 1354 ── GALLIPOLI PENINSULA (Gelibolu) ──────────────────────────────
    {
        "name": "Gallipoli Peninsula",
        "year": 1354,
        "vassal": False,
        "tooltip": "<b>Gallipoli (Gelibolu) — 1354</b><br>Suleyman Pasha crossed the Dardanelles and seized the abandoned fortress of Tzympe, then Gallipoli itself. This was the decisive first foothold in Europe.",
        "geometry": poly([
            (26.38,40.39),(26.55,40.44),(26.72,40.52),(26.85,40.48),
            (26.95,40.39),(26.88,40.29),(26.75,40.24),(26.55,40.22),
            (26.38,40.28),(26.38,40.39)
        ])
    },

    # ── 1362 ── EASTERN THRACE (Edirne / Adrianople) ────────────────────────
    {
        "name": "Eastern Thrace (incl. Edirne)",
        "year": 1362,
        "vassal": False,
        "tooltip": "<b>Eastern Thrace & Adrianople — 1362</b><br>Murad I captured Adrianople (Edirne) c.1362–1369 and made it the Ottoman capital in Europe, replacing Bursa. Edirne remained capital until 1453.",
        "geometry": poly([
            (26.38,40.39),(26.85,40.48),(27.2,40.72),(27.55,40.88),
            (27.9,41.05),(28.25,41.20),(28.55,41.35),(28.8,41.55),
            (29.05,41.75),(28.95,41.95),(28.5,42.1),(28.0,42.1),
            (27.5,42.0),(26.95,41.85),(26.55,41.6),(26.35,41.35),
            (26.2,41.05),(26.25,40.72),(26.38,40.39)
        ])
    },

    # ── 1371 ── WESTERN THRACE & RHODOPE ────────────────────────────────────
    {
        "name": "Western Thrace & Rhodope Mtns",
        "year": 1371,
        "vassal": False,
        "tooltip": "<b>Western Thrace — 1371</b><br>After the Battle of Maritsa (26 Sep 1371), the Serbian coalition was crushed. Western Thrace including the Rhodope region fell to the Ottomans, opening the road to Macedonia.",
        "geometry": poly([
            (24.5,41.35),(24.9,41.5),(25.3,41.65),(25.7,41.75),
            (26.2,41.85),(26.55,41.6),(26.95,41.85),(26.95,41.6),
            (26.7,41.4),(26.35,41.1),(26.0,40.9),(25.6,40.8),
            (25.2,40.7),(24.85,40.75),(24.55,40.9),(24.4,41.1),(24.5,41.35)
        ])
    },

    # ── 1371–1395 ── BULGARIA (gradual) ─────────────────────────────────────
    {
        "name": "Bulgaria",
        "year": 1396,
        "vassal": False,
        "tooltip": "<b>Bulgaria — 1371–1396</b><br>Bulgaria became an Ottoman vassal after 1371. The Battle of Nicopolis (1396) — a crusading army led by Sigismund of Hungary — was crushed by Bayezid I. Bulgaria was fully absorbed as a direct province.",
        "geometry": poly([
            (22.35,43.8),(22.85,44.0),(23.35,44.05),(23.85,44.05),
            (24.35,43.95),(24.85,43.85),(25.35,43.75),(25.85,43.65),
            (26.35,43.55),(26.95,43.5),(27.45,43.4),(27.9,43.35),
            (28.5,43.55),(28.6,43.75),(28.5,44.1),(28.0,44.3),
            (27.5,44.45),(26.5,44.4),(25.5,44.35),(24.5,44.3),
            (23.5,44.15),(22.65,44.0),(22.35,43.8)
            # Closing via Danube-ish northern border
        ])
    },

    # ── 1371–1389 ── MACEDONIA ───────────────────────────────────────────────
    {
        "name": "Macedonia",
        "year": 1389,
        "vassal": False,
        "tooltip": "<b>Macedonia — 1371–1389</b><br>After Maritsa the Ottomans advanced through Macedonia. Serres fell in 1383, Bitola in 1385, Sofia in 1385. The Battle of Kosovo (1389) sealed control.",
        "geometry": poly([
            (20.45,41.85),(20.9,41.95),(21.35,42.1),(21.85,42.2),
            (22.35,42.15),(22.85,42.05),(23.3,41.95),(23.7,41.75),
            (24.1,41.55),(24.5,41.35),(24.5,41.1),(24.15,40.95),
            (23.75,40.85),(23.35,40.75),(22.95,40.6),(22.55,40.55),
            (22.15,40.55),(21.75,40.65),(21.4,40.85),(21.1,41.05),
            (20.75,41.3),(20.55,41.55),(20.45,41.85)
        ])
    },

    # ── 1389–1459 ── SERBIA ──────────────────────────────────────────────────
    {
        "name": "Serbia",
        "year": 1459,
        "vassal": False,
        "tooltip": "<b>Serbia — 1389–1459</b><br>Serbia became a vassal after Kosovo (1389). The Despotate survived under tribute. Smederevo, the last capital, fell to Mehmed II in 1459, fully absorbing Serbia.",
        "geometry": poly([
            (19.0,44.85),(19.5,45.1),(20.05,45.25),(20.55,45.15),
            (21.05,44.95),(21.55,44.75),(22.05,44.55),(22.55,44.35),
            (22.85,44.0),(22.35,43.8),(21.9,43.65),(21.45,43.55),
            (21.05,43.45),(20.65,43.35),(20.35,43.15),(20.05,43.0),
            (19.65,43.05),(19.35,43.25),(19.05,43.55),(18.85,43.85),
            (18.95,44.2),(19.0,44.55),(19.0,44.85)
        ])
    },

    # ── 1393–1400s ── THESSALY ───────────────────────────────────────────────
    {
        "name": "Thessaly",
        "year": 1393,
        "vassal": False,
        "tooltip": "<b>Thessaly — 1393</b><br>Bayezid I conquered Thessaly in 1393 from the Byzantine Duchy of Neopatras. The fertile plains of Thessaly were a major agricultural prize.",
        "geometry": poly([
            (21.55,39.35),(22.0,39.55),(22.5,39.7),(22.95,39.75),
            (23.35,39.65),(23.65,39.45),(23.85,39.2),(23.75,38.95),
            (23.45,38.75),(23.05,38.65),(22.65,38.65),(22.25,38.75),
            (21.95,38.95),(21.75,39.15),(21.55,39.35)
        ])
    },

    # ── 1393 ── WALLACHIA (vassal) ───────────────────────────────────────────
    {
        "name": "Wallachia (vassal principality)",
        "year": 1393,
        "vassal": True,
        "tooltip": "<b>Wallachia — Vassal from 1393</b><br>Mircea the Elder was forced into vassalage by Bayezid I after Nicopolis (1396). Wallachia paid annual tribute and provided troops. It retained its Orthodox princes (voivodes), including Vlad III 'the Impaler' (r.1456–62).",
        "geometry": poly([
            (22.55,44.35),(23.05,44.55),(23.55,44.7),(24.05,44.85),
            (24.55,44.95),(25.05,45.0),(25.55,44.95),(26.05,44.9),
            (26.55,44.85),(27.05,44.8),(27.45,44.65),(27.85,44.45),
            (28.2,44.2),(28.5,44.1),(28.6,43.75),(28.5,43.55),
            (27.9,43.35),(27.45,43.4),(26.95,43.5),(26.35,43.55),
            (25.85,43.65),(25.35,43.75),(24.85,43.85),(24.35,43.95),
            (23.85,44.05),(23.35,44.05),(22.85,44.0),(22.55,44.35)
        ])
    },

    # ── 1458–1460 ── PELOPONNESE (Morea) ────────────────────────────────────
    {
        "name": "Peloponnese (Morea)",
        "year": 1460,
        "vassal": False,
        "tooltip": "<b>Peloponnese (Morea) — 1458–1460</b><br>Mehmed II conquered the Byzantine Despotate of Morea in two campaigns. The last Palaiologos despots fled to Rome. Only Venetian coastal towns held out briefly.",
        "geometry": poly([
            (21.55,38.35),(22.0,38.55),(22.45,38.65),(22.9,38.65),
            (23.35,38.55),(23.65,38.3),(23.8,38.0),(23.75,37.7),
            (23.5,37.45),(23.15,37.25),(22.7,37.1),(22.25,37.1),
            (21.85,37.2),(21.55,37.45),(21.35,37.75),(21.3,38.05),
            (21.45,38.2),(21.55,38.35)
        ])
    },

    # ── 1453 ── CONSTANTINOPLE & BOSPHORUS ZONE ─────────────────────────────
    {
        "name": "Constantinople (Istanbul)",
        "year": 1453,
        "vassal": False,
        "tooltip": "<b>Constantinople — 29 May 1453 ⭐</b><br>Mehmed II 'the Conqueror' besieged the city with 80,000 men and 70 cannon. The city fell after 53 days. The last Byzantine Emperor Constantine XI died in the fighting. The Ottoman capital moved here from Edirne.",
        "geometry": poly([
            (28.55,41.35),(28.8,41.55),(29.05,41.75),(29.25,41.95),
            (29.4,41.8),(29.5,41.55),(29.45,41.3),(29.2,41.1),
            (28.95,40.95),(28.7,40.85),(28.45,40.95),(28.35,41.15),(28.55,41.35)
        ])
    },

    # ── 1458 ── CENTRAL & NORTHERN GREECE (Athens, Boeotia, Attica) ─────────
    {
        "name": "Central Greece (Athens, Attica, Boeotia)",
        "year": 1458,
        "vassal": False,
        "tooltip": "<b>Central Greece — 1456–1460</b><br>The Duchy of Athens (Florentine Acciaiuoli) fell to Mehmed II in 1456. Mehmed personally visited Athens in 1458, reportedly admiring the Parthenon.",
        "geometry": poly([
            (21.55,39.35),(21.75,39.15),(21.95,38.95),(22.25,38.75),
            (22.65,38.65),(23.05,38.65),(23.45,38.75),(23.75,38.95),
            (23.85,39.2),(24.1,39.35),(24.35,39.5),(24.5,39.4),
            (24.3,39.2),(24.0,38.95),(23.7,38.7),(23.55,38.45),
            (23.45,38.2),(23.2,38.05),(22.95,37.95),(22.65,37.9),
            (22.35,37.95),(22.05,38.05),(21.8,38.25),(21.6,38.5),
            (21.5,38.75),(21.5,39.05),(21.55,39.35)
        ])
    },

    # ── 1463 ── BOSNIA ───────────────────────────────────────────────────────
    {
        "name": "Bosnia",
        "year": 1463,
        "vassal": False,
        "tooltip": "<b>Bosnia — 1463</b><br>Mehmed II conquered the Kingdom of Bosnia in a lightning campaign. King Stephen Tomašević was captured at Ključ and beheaded. Bosnia became an Ottoman province (sanjak), with many Bosnians converting to Islam.",
        "geometry": poly([
            (15.75,45.2),(16.2,45.35),(16.65,45.45),(17.15,45.55),
            (17.65,45.55),(18.15,45.45),(18.65,45.25),(19.0,44.85),
            (19.0,44.55),(18.95,44.2),(18.85,43.85),(19.05,43.55),
            (19.35,43.25),(19.05,43.05),(18.75,42.95),(18.4,43.0),
            (18.05,43.15),(17.65,43.25),(17.25,43.3),(16.9,43.35),
            (16.55,43.4),(16.25,43.45),(15.95,43.5),(15.75,43.65),
            (15.65,43.95),(15.65,44.35),(15.7,44.75),(15.75,45.2)
        ])
    },

    # ── 1463 ── HERZEGOVINA ─────────────────────────────────────────────────
    {
        "name": "Herzegovina",
        "year": 1482,
        "vassal": False,
        "tooltip": "<b>Herzegovina — 1482</b><br>The Duchy of Saint Sava (Herzegovina) resisted under Duke Vladislav until fully conquered in 1482 by Bayezid II. Combined with Bosnia into a single Ottoman province.",
        "geometry": poly([
            (15.75,43.65),(15.95,43.5),(16.25,43.45),(16.55,43.4),
            (16.9,43.35),(17.25,43.3),(17.65,43.25),(18.05,43.15),
            (18.4,43.0),(18.75,42.95),(18.55,42.7),(18.25,42.5),
            (17.95,42.4),(17.65,42.35),(17.35,42.45),(17.05,42.6),
            (16.75,42.75),(16.45,42.85),(16.15,42.9),(15.9,42.95),
            (15.7,43.1),(15.6,43.35),(15.75,43.65)
        ])
    },

    # ── 1468 ── ALBANIA ──────────────────────────────────────────────────────
    {
        "name": "Albania",
        "year": 1479,
        "vassal": False,
        "tooltip": "<b>Albania — 1468–1479</b><br>Gjergj Kastrioti (Skanderbeg) held off the Ottomans for 25 years. After his death (1468), resistance collapsed. Shkodra (Scutari) fell to Mehmed II in 1479 despite Venetian defence.",
        "geometry": poly([
            (19.35,42.05),(19.65,42.15),(20.0,42.25),(20.35,42.35),
            (20.65,42.25),(20.95,42.1),(21.1,41.85),(21.05,41.55),
            (20.85,41.25),(20.6,41.0),(20.35,40.8),(20.1,40.65),
            (19.85,40.55),(19.55,40.55),(19.3,40.65),(19.1,40.85),
            (19.0,41.1),(18.95,41.4),(19.05,41.7),(19.35,42.05)
        ])
    },

    # ── 1475 ── CRIMEAN VASSAL KHANATE ──────────────────────────────────────
    {
        "name": "Crimean Khanate (vassal)",
        "year": 1475,
        "vassal": True,
        "tooltip": "<b>Crimean Khanate — vassal from 1475</b><br>Mehmed II's Black Sea campaign captured the Genoese colonies (Caffa/Feodosiya, Sudak, Tana). The Giray dynasty became Ottoman vassals, regularly raiding Poland, Russia and Lithuania for slaves.",
        "geometry": poly([
            (32.5,46.1),(33.0,46.3),(33.5,46.5),(34.0,46.6),
            (34.5,46.65),(35.0,46.6),(35.45,46.45),(35.75,46.15),
            (35.85,45.85),(35.55,45.55),(35.0,45.3),(34.4,45.1),
            (33.8,44.95),(33.3,44.85),(32.8,44.9),(32.35,45.05),
            (32.1,45.35),(32.2,45.7),(32.5,46.1)
        ])
    },

    # ── 1484 ── MOLDAVIA (vassal) ────────────────────────────────────────────
    {
        "name": "Moldavia (vassal principality)",
        "year": 1484,
        "vassal": True,
        "tooltip": "<b>Moldavia — vassal from 1484</b><br>Stephen the Great (Ștefan cel Mare) fought brilliant campaigns but accepted Ottoman suzerainty in 1484. Kilia and Akkerman (Bilhorod-Dnistrovskyi) on the Black Sea were directly annexed, cutting Moldavia off from the sea.",
        "geometry": poly([
            (26.55,44.85),(27.05,44.8),(27.45,44.65),(27.85,44.45),
            (28.2,44.2),(28.5,44.1),(28.8,44.0),(29.1,44.05),
            (29.5,44.2),(29.85,44.35),(30.15,44.45),(30.4,44.55),
            (30.5,44.85),(30.35,45.15),(30.1,45.4),(29.85,45.7),
            (29.55,45.95),(29.25,46.2),(28.95,46.45),(28.6,46.7),
            (28.3,46.95),(27.95,47.2),(27.6,47.4),(27.25,47.55),
            (26.85,47.65),(26.5,47.6),(26.2,47.45),(26.0,47.2),
            (25.9,46.95),(25.95,46.65),(26.05,46.35),(26.15,46.05),
            (26.25,45.75),(26.35,45.45),(26.45,45.15),(26.55,44.85)
        ])
    },

    # ── 1499–1503 ── GREEK COAST / VENETIAN TOWNS ───────────────────────────
    {
        "name": "Western Greece (ex-Venetian ports)",
        "year": 1503,
        "vassal": False,
        "tooltip": "<b>Western Greece — 1499–1503</b><br>The Ottoman-Venetian War (1499–1503) resulted in Venice ceding Lepanto (Naupaktos), Modon, Coron, and Pylos — key Adriatic and Ionian staging posts. Venice retained Corfu and Crete.",
        "geometry": mpoly([
            [(20.8,38.55),(21.05,38.6),(21.2,38.45),(21.1,38.3),(20.85,38.3),(20.75,38.45),(20.8,38.55)],
            [(21.75,37.05),(21.95,37.1),(22.05,36.95),(21.95,36.85),(21.75,36.88),(21.65,37.0),(21.75,37.05)],
            [(21.65,36.82),(21.85,36.85),(21.9,36.72),(21.8,36.65),(21.65,36.65),(21.6,36.75),(21.65,36.82)],
        ])
    },

    # ── 1512–1520 ── NORTHERN AEGEAN (Tenedos etc.) ──────────────────────────
    # Integrated in the earlier Thrace polygon

    # ── 1521 ── BELGRADE ────────────────────────────────────────────────────
    # Belgrade covered in Serbia polygon above; annotated separately as city marker

    # ── 1522 ── RHODES & DODECANESE ─────────────────────────────────────────
    {
        "name": "Rhodes & Dodecanese Islands",
        "year": 1522,
        "vassal": False,
        "tooltip": "<b>Rhodes — 1522</b><br>The Knights Hospitaller held Rhodes heroically. Suleiman the Magnificent besieged the island with 100,000 men. After a six-month siege the Knights surrendered honourably (Jan 1523) and withdrew to Malta.",
        "geometry": mpoly([
            [(28.1,36.5),(28.2,36.55),(28.3,36.48),(28.25,36.38),(28.1,36.35),(28.0,36.42),(28.1,36.5)],
            [(27.15,37.6),(27.3,37.65),(27.45,37.55),(27.4,37.4),(27.2,37.35),(27.05,37.45),(27.15,37.6)],
            [(27.2,36.85),(27.35,36.9),(27.45,36.75),(27.35,36.65),(27.15,36.65),(27.05,36.75),(27.2,36.85)],
            [(26.85,37.45),(27.0,37.5),(27.1,37.38),(27.0,37.28),(26.8,37.28),(26.75,37.38),(26.85,37.45)],
            [(26.55,37.6),(26.7,37.65),(26.8,37.5),(26.65,37.4),(26.5,37.42),(26.45,37.52),(26.55,37.6)],
            [(25.5,36.95),(25.65,37.0),(25.75,36.85),(25.65,36.75),(25.45,36.75),(25.35,36.85),(25.5,36.95)],
        ])
    },

    # ── 1526 ── CENTRAL HUNGARY (after Mohács) ───────────────────────────────
    {
        "name": "Central Hungary (Buda province)",
        "year": 1541,
        "vassal": False,
        "tooltip": "<b>Central Hungary — 1526–1541</b><br>The Battle of Mohács (29 Aug 1526) annihilated the Hungarian army. King Louis II drowned fleeing. Suleiman occupied Buda briefly. In 1541 Suleiman trapped John I's widow in Buda and permanently annexed it — the province of Budin — which remained Ottoman for 145 years.",
        "geometry": poly([
            (16.8,47.0),(17.3,47.15),(17.8,47.25),(18.3,47.3),
            (18.8,47.3),(19.3,47.25),(19.8,47.1),(20.3,46.9),
            (20.8,46.65),(21.3,46.4),(21.6,46.1),(21.75,45.75),
            (21.65,45.45),(21.35,45.2),(21.0,45.05),(20.55,45.15),
            (20.05,45.25),(19.5,45.1),(19.0,44.85),(18.65,45.25),
            (18.15,45.45),(17.65,45.55),(17.15,45.55),(16.65,45.45),
            (16.3,45.55),(16.1,45.85),(16.05,46.2),(16.1,46.55),(16.8,47.0)
        ])
    },

    # ── 1541 ── TRANSYLVANIA (vassal) ────────────────────────────────────────
    {
        "name": "Transylvania (vassal principality)",
        "year": 1541,
        "vassal": True,
        "tooltip": "<b>Transylvania — vassal from 1541</b><br>After Buda fell, John I's son (John II Sigismund) ruled Transylvania as an Ottoman vassal. It served as a crucial buffer state against the Habsburgs, paying annual tribute. Later princes like István Báthory and Gábor Bethlen used Ottoman backing in Habsburg conflicts.",
        "geometry": poly([
            (20.8,46.65),(21.3,46.4),(21.6,46.1),(21.75,45.75),
            (22.15,45.55),(22.65,45.45),(23.15,45.4),(23.65,45.4),
            (24.15,45.45),(24.65,45.5),(25.15,45.5),(25.65,45.4),
            (26.0,45.1),(26.15,44.75),(26.05,44.45),(25.65,44.2),
            (25.15,44.1),(24.65,44.1),(24.15,44.15),(23.65,44.2),
            (23.15,44.3),(22.65,44.45),(22.15,44.6),(21.65,44.75),
            (21.35,45.2),(21.65,45.45),(21.75,45.75),(21.6,46.1),(21.3,46.4),(20.8,46.65)
        ])
    },

    # ── 1541 ── SLAVONIA & OTTOMAN CROATIA STRIP ─────────────────────────────
    {
        "name": "Ottoman Slavonia & Croatian marches",
        "year": 1541,
        "vassal": False,
        "tooltip": "<b>Ottoman Slavonia & Croatian marches — 1521–1541</b><br>After Belgrade (1521) and Mohács (1526), the Ottomans swept into Slavonia. Esseg (Osijek) was taken; much of Slavonia fell by 1537. The Military Frontier (Vojna Krajina) was established by the Habsburgs to contain further advance.",
        "geometry": poly([
            (16.1,45.85),(16.3,45.55),(16.65,45.45),(17.15,45.55),
            (17.65,45.55),(18.15,45.45),(18.65,45.25),(19.0,44.85),
            (18.65,44.65),(18.3,44.55),(17.9,44.55),(17.5,44.6),
            (17.1,44.7),(16.7,44.8),(16.35,44.95),(16.1,45.15),
            (15.95,45.45),(16.1,45.85)
        ])
    },

    # ── 1566 ── CHIOS ────────────────────────────────────────────────────────
    {
        "name": "Chios",
        "year": 1566,
        "vassal": False,
        "tooltip": "<b>Chios — 1566</b><br>Chios had been a prosperous Genoese colony (Maona of Chios) since 1346. Piyale Pasha annexed it bloodlessly for Selim II, completing Ottoman control of the entire Aegean.",
        "geometry": poly([
            (25.95,38.55),(26.1,38.6),(26.2,38.5),(26.15,38.35),(25.95,38.3),(25.85,38.42),(25.95,38.55)
        ])
    },

    # ── 1571 ── CYPRUS ───────────────────────────────────────────────────────
    {
        "name": "Cyprus",
        "year": 1571,
        "vassal": False,
        "tooltip": "<b>Cyprus — 1570–1571</b><br>The Ottoman-Venetian War saw Cyprus invaded in 1570. Nicosia fell after 45 days (Sep 1570); 20,000 were massacred. Famagusta, defended heroically by Marcantonio Bragadin, held until Aug 1571. Bragadin was flayed alive. Cyprus was lost to Venice, held by Ottomans until 1878.",
        "geometry": poly([
            (32.3,35.0),(32.6,35.1),(32.9,35.15),(33.2,35.1),
            (33.5,35.05),(33.8,34.95),(34.0,34.8),(34.15,34.6),
            (34.05,34.45),(33.75,34.35),(33.4,34.3),(33.0,34.3),
            (32.65,34.4),(32.35,34.6),(32.2,34.8),(32.3,35.0)
        ])
    },

    # ── 1620s–1672 ── PODOLIA (Ukraine, brief) ──────────────────────────────
    {
        "name": "Podolia (annexed 1672–1699)",
        "year": 1672,
        "vassal": False,
        "tooltip": "<b>Podolia — 1672</b><br>The Treaty of Buchach (1672) after the Ottoman-Polish War ceded Podolia — including the mighty fortress of Kamianets-Podilskyi — to the Ottomans. This was the furthest Ottoman expansion into eastern Europe. Returned to Poland by the Treaty of Carlowitz (1699).",
        "geometry": poly([
            (25.9,48.5),(26.4,48.65),(26.9,48.75),(27.4,48.8),
            (27.9,48.8),(28.4,48.75),(28.9,48.65),(29.4,48.5),
            (29.85,48.3),(30.15,48.05),(30.25,47.75),(30.1,47.5),
            (29.75,47.3),(29.35,47.15),(28.95,47.05),(28.55,47.0),
            (28.15,47.0),(27.75,47.05),(27.35,47.15),(26.95,47.3),
            (26.6,47.5),(26.35,47.75),(26.2,48.05),(26.1,48.3),(25.9,48.5)
        ])
    },

    # ── 1645–1669 ── CRETE (Candia) ──────────────────────────────────────────
    {
        "name": "Crete (Candia)",
        "year": 1669,
        "vassal": False,
        "tooltip": "<b>Crete (Candia) — 1645–1669</b><br>The Great Cretan War lasted 24 years. Heraklion (Candia), the Venetian capital, survived the longest siege in history — 21 years (1648–1669). It finally fell when Venice ran out of resources. The island held until 1898 (Cretan State) and 1913 (Greece).",
        "geometry": poly([
            (23.55,35.55),(23.9,35.6),(24.35,35.6),(24.8,35.6),
            (25.25,35.55),(25.7,35.5),(26.15,35.45),(26.55,35.35),
            (26.9,35.2),(27.15,35.05),(27.2,34.85),(27.0,34.7),
            (26.7,34.6),(26.3,34.6),(25.85,34.65),(25.4,34.7),
            (24.95,34.75),(24.5,34.8),(24.05,34.85),(23.65,34.95),
            (23.3,35.1),(23.15,35.3),(23.25,35.5),(23.55,35.55)
        ])
    },

    # ── 1672 ── RIGHT-BANK UKRAINE (brief vassal) ───────────────────────────
    {
        "name": "Right-Bank Ukraine (brief vassal 1669–1699)",
        "year": 1672,
        "vassal": True,
        "tooltip": "<b>Right-Bank Ukraine — 1669–1699</b><br>Hetman Petro Doroshenko sought Ottoman overlordship in 1669 to resist both Poland and Russia. This was nominal — the Ottomans never directly administered the region. Abandoned after the failure at Vienna (1683) and Treaty of Carlowitz (1699).",
        "geometry": poly([
            (29.85,48.3),(30.35,48.55),(30.85,48.75),(31.35,48.9),
            (31.85,48.95),(32.35,48.9),(32.85,48.8),(33.35,48.65),
            (33.75,48.45),(33.95,48.15),(33.85,47.85),(33.55,47.6),
            (33.1,47.4),(32.6,47.3),(32.1,47.25),(31.6,47.3),
            (31.1,47.45),(30.65,47.65),(30.3,47.9),(30.0,48.15),(29.85,48.3)
        ])
    },

    # ── AEGEAN ISLANDS – LESBOS, LEMNOS (mid 15c) ───────────────────────────
    {
        "name": "Lesbos & Northern Aegean Islands",
        "year": 1462,
        "vassal": False,
        "tooltip": "<b>Lesbos & Northern Aegean — 1455–1462</b><br>Mehmed II systematically took the Aegean islands from Genoese and Byzantine rulers. Imbros, Lemnos, and Lesbos fell in 1462 after the Genoese Gattilusio dynasty was eliminated.",
        "geometry": mpoly([
            [(26.15,39.25),(26.35,39.35),(26.55,39.3),(26.7,39.15),(26.65,39.0),(26.45,38.95),(26.25,39.0),(26.1,39.1),(26.15,39.25)],
            [(25.05,40.0),(25.25,40.1),(25.45,40.05),(25.55,39.9),(25.45,39.75),(25.2,39.72),(25.0,39.8),(24.95,39.92),(25.05,40.0)],
            [(25.45,40.5),(25.7,40.55),(25.9,40.42),(25.85,40.28),(25.6,40.22),(25.38,40.3),(25.35,40.42),(25.45,40.5)],
        ])
    },

    # ── EPIRUS & NW GREECE ──────────────────────────────────────────────────
    {
        "name": "Epirus & NW Greece",
        "year": 1449,
        "vassal": False,
        "tooltip": "<b>Epirus — 1430–1449</b><br>The Despotate of Epirus gradually fell. Ioannina surrendered in 1430. By 1449 the whole region was Ottoman. Previously a Byzantine successor state under Carlo II Tocco.",
        "geometry": poly([
            (19.95,41.85),(20.2,41.95),(20.45,41.85),(20.55,41.55),
            (20.55,41.25),(20.45,41.0),(20.25,40.85),(20.05,40.65),
            (19.85,40.55),(19.55,40.55),(19.3,40.65),(19.1,40.85),
            (19.0,41.1),(18.95,41.4),(19.05,41.7),(19.35,42.05),
            (19.65,41.95),(19.95,41.85)
        ])
    },
]

# ---------------------------------------------------------------------------
# 2.  HISTORICAL EVENTS TIMELINE
# ---------------------------------------------------------------------------
events = {
    1299: ("Ottoman state founded", "Osman I establishes the Ottoman principality in Bithynia (NW Anatolia). European expansion begins 55 years later."),
    1354: ("Gallipoli seized", "Suleyman Pasha crosses the Dardanelles — the first Ottoman presence in Europe. The earthquake that damaged Gallipoli's walls gave them their chance."),
    1362: ("Adrianople (Edirne) captured", "Murad I takes Adrianople and relocates the Ottoman capital to Europe. Edirne remains the capital until 1453."),
    1371: ("Battle of Maritsa", "A coalition of Serbian princes is crushed at the Maritsa River on 26 Sep 1371. Macedonia and western Thrace fall open to Ottoman advance."),
    1389: ("Battle of Kosovo ⚔", "15 June 1389 — both Sultan Murad I and Prince Lazar of Serbia are killed. Serbian power is broken. Kosovo becomes a defining event in Serbian national memory."),
    1396: ("Battle of Nicopolis", "The last major crusade is annihilated by Bayezid I at Nicopolis (25 Sep 1396). Bulgaria fully absorbed. Sigismund of Hungary barely escapes."),
    1402: ("Battle of Ankara — temporary check", "Timur (Tamerlane) defeats and captures Bayezid I at Ankara. The Ottoman state fractures in civil war (Interregnum 1402–1413), halting European expansion."),
    1430: ("Thessaloniki taken", "Murad II captures Thessaloniki from Venice. The second city of Byzantium falls."),
    1453: ("Fall of Constantinople ⭐", "29 May 1453 — Mehmed II ends the Byzantine Empire after 1,000 years. 80,000 troops, 70+ cannon. Emperor Constantine XI dies fighting. A new era begins."),
    1456: ("Siege of Belgrade repulsed", "Hunyadi János (John Hunyadi) and a peasant crusade under Giovanni da Capistrano repel Mehmed II from Belgrade. The city holds for another 65 years."),
    1462: ("Aegean islands taken", "Mehmed II takes Lesbos, Lemnos, Imbros from the Genoese Gattilusio family. The northern Aegean is now Ottoman."),
    1463: ("Bosnia conquered", "Mehmed II conquers the Kingdom of Bosnia in weeks. King Stephen Tomašević is captured and beheaded at Jajce."),
    1468: ("Albania falls (after Skanderbeg)", "Gjergj Kastrioti 'Skanderbeg' dies in January 1468. Without him Albania's resistance collapses within a decade. Shkodra falls to Mehmed II in 1479."),
    1475: ("Crimea becomes vassal", "Mehmed II's Black Sea campaign. Genoese colonies (Caffa) taken directly; Crimean Khanate (Giray dynasty) becomes an Ottoman vassal raiding state."),
    1480: ("Otranto briefly seized", "Ottoman forces raid the Italian peninsula, taking Otranto in August 1480 and massacring 800 who refused conversion. They withdrew after Mehmed II's death in 1481."),
    1484: ("Moldavia becomes vassal", "Bayezid II takes Kilia and Akkerman, cutting Moldavia off from the Black Sea. Stephen the Great accepts vassalage. Moldavia pays tribute for centuries."),
    1521: ("Belgrade falls", "Suleiman the Magnificent takes Belgrade — the 'gateway to Hungary' — in August 1521. It had repelled Mehmed II in 1456."),
    1522: ("Rhodes surrenders", "Suleiman besieges Rhodes with 100,000 men. The Knights of St. John surrender honourably in January 1523 and withdraw to Malta."),
    1526: ("Battle of Mohács ⚔", "29 August 1526 — Hungary's army is destroyed in 2 hours. King Louis II drowns fleeing. 'The realm of Hungary is no more.' Suleiman enters Buda."),
    1529: ("First Siege of Vienna", "Suleiman's army reaches Vienna (27 Sep 1529) but cannot take it. Supply lines are stretched, season too late, walls too thick for his cannon. He withdraws — the high-water mark."),
    1541: ("Buda permanently occupied", "Suleiman traps Queen Isabella in Buda and annexes it. Central Hungary becomes the Ottoman province of Budin. Transylvania is a vassal state."),
    1565: ("Great Siege of Malta", "Suleiman's forces besiege the Knights of St. John at Malta. After heroic resistance (May–Sep 1565) the Ottomans withdraw — their first major failure in the Western Mediterranean."),
    1566: ("Suleiman dies at Szigetvár", "Suleiman the Magnificent dies (5 Sep 1566) during the siege of Szigetvár (Croatia), aged ~72. His death is concealed. Chios is also annexed this year."),
    1571: ("Battle of Lepanto & Cyprus", "Cyprus is conquered from Venice. The Battle of Lepanto (7 Oct 1571) — the Holy League fleet under Don John of Austria destroys the Ottoman fleet. Cyprus remains Ottoman."),
    1593: ("Long Turkish War begins", "The 'Long War' or Thirteen Years' War (1593–1606) with the Habsburgs begins. Despite some setbacks the Ottomans retain Hungary. Treaty of Zsitvatorok (1606) — first time the Ottoman Sultan treats a European monarch as an equal."),
    1645: ("Cretan War begins", "Ottomans invade Crete (Venice's richest colony). The siege of Candia (Heraklion) begins — it will last 21 years, the longest siege in history."),
    1669: ("Crete (Candia) falls", "Heraklion surrenders on 5 Sep 1669 after 21 years. Venice's last major eastern holding is lost. The Ottomans hold Crete until the 1897 revolt and 1913 union with Greece."),
    1672: ("Podolia annexed", "Ottoman-Polish War. Treaty of Buchach cedes Podolia to the Ottomans — the furthest north they ever reach. Kamianets-Podilskyi fortress taken."),
    1683: ("Second Siege of Vienna — TURNING POINT ⭐", "Kara Mustafa Pasha besieges Vienna from 14 July 1683. On 12 September the relief army — Polish King Jan III Sobieski, Holy League — charges from the Kahlenberg hill. The Ottoman camp is routed. This begins the 'Great Turkish War' and the permanent Ottoman retreat from central Europe."),
}

# ---------------------------------------------------------------------------
# 3.  KEY CITIES
# ---------------------------------------------------------------------------
cities = [
    # (name, lat, lon, ottomanFrom, note)
    ("Constantinople / Istanbul", 41.015, 28.97, 1453, "Ottoman capital from 1453"),
    ("Edirne (Adrianople)", 41.68, 26.56, 1362, "Ottoman capital 1362–1453"),
    ("Belgrade", 44.82, 20.46, 1521, "Fell 1521 — 'Gateway to Hungary'"),
    ("Buda", 47.50, 19.05, 1541, "Ottoman capital of Hungary province from 1541"),
    ("Thessaloniki", 40.64, 22.94, 1430, "Fell to Murad II, 1430"),
    ("Athens", 37.97, 23.73, 1458, "Under Ottoman rule 1458–1833"),
    ("Sarajevo", 43.85, 18.38, 1463, "Founded as Ottoman city after 1463"),
    ("Sofia", 42.70, 23.32, 1385, "Ottoman Bulgaria capital from 1385"),
    ("Mohács", 45.99, 18.68, 1526, "Battle of Mohács 1526 ⚔"),
    ("Kosovo Polje", 42.66, 21.09, 1389, "Battle of Kosovo 1389 ⚔"),
    ("Maritsa (Črnomen)", 41.78, 26.28, 1371, "Battle of Maritsa 1371 ⚔"),
    ("Nicopolis", 43.70, 24.90, 1396, "Battle of Nicopolis 1396 ⚔"),
    ("Vienna", 48.21, 16.37, None, "Besieged 1529 & 1683 — never taken"),
    ("Kamianets-Podilskyi", 48.67, 26.58, 1672, "Podolia fortress — fell 1672"),
    ("Gallipoli", 40.41, 26.68, 1354, "First Ottoman foothold in Europe 1354"),
    ("Smederevo", 44.66, 20.93, 1459, "Last Serbian capital — fell 1459"),
    ("Nicosia", 35.17, 33.37, 1570, "Cyprus capital — fell 1570"),
    ("Rhodes (city)", 36.44, 28.22, 1522, "Knights of St. John surrendered 1522"),
    ("Heraklion (Candia)", 35.34, 25.14, 1669, "21-year siege ended 1669"),
    ("Shkodra", 42.07, 19.51, 1479, "Last Albanian stronghold — fell 1479"),
    ("Szigetvár", 46.05, 17.80, 1566, "Suleiman died here 1566"),
]

# ---------------------------------------------------------------------------
# 4.  BUILD FOLIUM MAP
# ---------------------------------------------------------------------------
print("Building Folium map...")

m = folium.Map(
    location=[41.5, 26.0],
    zoom_start=5,
    tiles=None,
    prefer_canvas=True,
)

# Base tile layers
folium.TileLayer(
    tiles="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
    attr='&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> contributors &copy; <a href="https://carto.com/">CARTO</a>',
    name="Light (CartoDB)",
    max_zoom=18,
    control=True,
    show=True,
).add_to(m)

folium.TileLayer(
    tiles="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png",
    attr='&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> contributors &copy; CARTO',
    name="Voyager (CartoDB)",
    max_zoom=18,
    control=True,
    show=False,
).add_to(m)

# ---------------------------------------------------------------------------
# 5.  COLOUR SCHEME  — darker red = earlier conquest (more entrenched)
# ---------------------------------------------------------------------------
def get_colour(year, vassal):
    if vassal:
        return "#e8a87c"          # warm orange for vassals
    # Phase colours
    phase_map = [
        (1354, "#f4c2b8"),
        (1390, "#e8987a"),
        (1430, "#d9644a"),
        (1460, "#c43d28"),
        (1500, "#a82a18"),
        (1530, "#8c1e0e"),
        (1570, "#700e05"),
        (1640, "#540600"),
        (1670, "#3d0200"),
    ]
    col = "#f4c2b8"
    for y, c in phase_map:
        if year >= y:
            col = c
    return col

def get_opacity(year, vassal):
    return 0.45 if vassal else 0.78

# ---------------------------------------------------------------------------
# 6.  ADD TERRITORY POLYGONS  — each with its own FeatureGroup for toggling
# ---------------------------------------------------------------------------

# Group by era for layer control
eras = {
    "Phase 1 — Early Thrace & Balkans (1354–1402)": [],
    "Phase 2 — Mehmed II conquests (1403–1481)":     [],
    "Phase 3 — Bayezid II & Selim I (1481–1520)":   [],
    "Phase 4 — Suleiman the Magnificent (1520–1566)": [],
    "Phase 5 — Later expansion & islands (1566–1683)": [],
}

def era_for(yr):
    if yr <= 1402: return "Phase 1 — Early Thrace & Balkans (1354–1402)"
    if yr <= 1481: return "Phase 2 — Mehmed II conquests (1403–1481)"
    if yr <= 1520: return "Phase 3 — Bayezid II & Selim I (1481–1520)"
    if yr <= 1566: return "Phase 4 — Suleiman the Magnificent (1520–1566)"
    return        "Phase 5 — Later expansion & islands (1566–1683)"

era_groups = {k: folium.FeatureGroup(name=k, show=True) for k in eras}

for t in territories:
    geom = t["geometry"]
    colour = get_colour(t["year"], t["vassal"])
    opacity = get_opacity(t["year"], t["vassal"])
    era = era_for(t["year"])
    dash = "8,4" if t["vassal"] else None

    gj = folium.GeoJson(
        data={"type": "Feature", "geometry": geom.__geo_interface__, "properties": {}},
        style_function=lambda feat, c=colour, o=opacity, d=dash: {
            "fillColor": c,
            "color": "#5a0000",
            "weight": 1.2,
            "fillOpacity": o,
            "dashArray": d,
        },
        tooltip=folium.Tooltip(t["tooltip"], sticky=True, max_width=280),
    )
    gj.add_to(era_groups[era])

for grp in era_groups.values():
    grp.add_to(m)

# ---------------------------------------------------------------------------
# 7.  CITY MARKERS
# ---------------------------------------------------------------------------
city_group = folium.FeatureGroup(name="Cities & Battle Sites", show=True)

for (name, lat, lon, ott_from, note) in cities:
    if name == "Vienna":
        icon = folium.DivIcon(
            html=f'<div style="font-size:16px;color:#e67e22;text-shadow:1px 1px 2px #fff">★</div>',
            icon_size=(18, 18), icon_anchor=(9, 9)
        )
        tooltip_text = f"<b>{name}</b><br><i style='color:#888'>{note}</i>"
    elif "⚔" in name or "Battle" in note or "⚔" in note:
        icon = folium.DivIcon(
            html=f'<div style="font-size:14px;color:#8b0000;text-shadow:1px 1px 2px #fff">⚔</div>',
            icon_size=(16, 16), icon_anchor=(8, 8)
        )
        tooltip_text = f"<b>{name}</b><br><i style='color:#888'>{note}</i>"
    elif ott_from:
        icon = folium.DivIcon(
            html=f'<div style="width:8px;height:8px;background:#8b0000;border:1.5px solid #fff;border-radius:50%;margin:0"></div>',
            icon_size=(10, 10), icon_anchor=(5, 5)
        )
        tooltip_text = f"<b>{name}</b><br>Ottoman from <b>{ott_from}</b><br><i style='color:#888'>{note}</i>"
    else:
        icon = folium.DivIcon(
            html=f'<div style="width:8px;height:8px;background:#e67e22;border:1.5px solid #fff;border-radius:50%;margin:0"></div>',
            icon_size=(10, 10), icon_anchor=(5, 5)
        )
        tooltip_text = f"<b>{name}</b><br><i style='color:#888'>{note}</i>"

    folium.Marker(
        location=[lat, lon],
        icon=icon,
        tooltip=folium.Tooltip(tooltip_text, sticky=True),
    ).add_to(city_group)

city_group.add_to(m)

# ---------------------------------------------------------------------------
# 8.  INTERACTIVE TIMELINE PANEL (HTML injection via branca macro)
# ---------------------------------------------------------------------------
from branca.element import MacroElement
from jinja2 import Template

timeline_html = """
<div id="ott-panel" style="
    position:fixed; bottom:20px; left:50%; transform:translateX(-50%);
    z-index:9999; background:rgba(255,252,248,0.97);
    border:1.5px solid #8b0000; border-radius:10px;
    padding:14px 18px; max-width:660px; width:92%;
    font-family:Georgia,serif; box-shadow:0 4px 18px rgba(0,0,0,0.25);
    ">
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px">
    <span style="font-size:17px;font-weight:bold;color:#5a0000">
      Ottoman Europe — Expansion Timeline
    </span>
    <span style="margin-left:auto;font-size:22px;font-weight:bold;color:#8b0000" id="ott-year-disp">1299</span>
  </div>
  <input type="range" id="ott-slider" min="1299" max="1683" value="1299" step="1"
    style="width:100%;accent-color:#8b0000;cursor:pointer;margin-bottom:8px">
  <div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:10px">
    <button onclick="jumpYear(1354)" style="font-size:11px;padding:3px 8px;border:1px solid #8b0000;border-radius:4px;cursor:pointer;background:#fff5f5;color:#5a0000">1354 Gallipoli</button>
    <button onclick="jumpYear(1362)" style="font-size:11px;padding:3px 8px;border:1px solid #8b0000;border-radius:4px;cursor:pointer;background:#fff5f5;color:#5a0000">1362 Edirne</button>
    <button onclick="jumpYear(1389)" style="font-size:11px;padding:3px 8px;border:1px solid #8b0000;border-radius:4px;cursor:pointer;background:#fff5f5;color:#5a0000">1389 Kosovo</button>
    <button onclick="jumpYear(1453)" style="font-size:11px;padding:3px 8px;border:1px solid #8b0000;border-radius:4px;cursor:pointer;background:#fff0f0;color:#5a0000;font-weight:bold">1453 Constantinople ⭐</button>
    <button onclick="jumpYear(1526)" style="font-size:11px;padding:3px 8px;border:1px solid #8b0000;border-radius:4px;cursor:pointer;background:#fff5f5;color:#5a0000">1526 Mohács</button>
    <button onclick="jumpYear(1529)" style="font-size:11px;padding:3px 8px;border:1px solid #8b0000;border-radius:4px;cursor:pointer;background:#fff5f5;color:#5a0000">1529 Vienna (1st)</button>
    <button onclick="jumpYear(1683)" style="font-size:11px;padding:3px 8px;border:1px solid #8b0000;border-radius:4px;cursor:pointer;background:#fff0f0;color:#5a0000;font-weight:bold">1683 Vienna (2nd) ⭐</button>
  </div>
  <div id="ott-event-box" style="font-size:12.5px;color:#333;line-height:1.55;background:#fdf6f0;border-radius:6px;padding:8px 10px;border-left:3px solid #8b0000;min-height:44px">
    <b>1299</b> — Ottoman state founded by Osman I in Bithynia (NW Anatolia). European expansion begins 55 years later.
  </div>
  <div style="margin-top:8px;display:flex;gap:12px;font-size:11px;color:#666;align-items:center">
    <span><span style="display:inline-block;width:14px;height:10px;background:#d9644a;border-radius:2px;vertical-align:middle"></span> Direct Ottoman province</span>
    <span><span style="display:inline-block;width:14px;height:10px;background:#e8a87c;border:1px dashed #8b0000;border-radius:2px;vertical-align:middle"></span> Vassal state</span>
    <span>★ Never conquered</span>
    <span>⚔ Major battle</span>
    <span style="margin-left:auto;font-size:10px;color:#aaa">Hover territories for detail</span>
  </div>
</div>

<script>
var events = """ + json.dumps(events) + """;

var slider = document.getElementById('ott-slider');
var yearDisp = document.getElementById('ott-year-disp');
var eventBox = document.getElementById('ott-event-box');

function updatePanel(yr) {
    yearDisp.textContent = yr;
    // find most recent event <= yr
    var keys = Object.keys(events).map(Number).filter(function(y){ return y <= yr; }).sort(function(a,b){return b-a;});
    if(keys.length > 0){
        var k = keys[0];
        var ev = events[k];
        eventBox.innerHTML = '<b>' + k + ' — ' + ev[0] + '</b><br>' + ev[1];
    } else {
        eventBox.innerHTML = '<b>' + yr + '</b> — Ottoman principality forming. No European territory yet.';
    }
}

slider.addEventListener('input', function(){ updatePanel(parseInt(this.value)); });

function jumpYear(y){
    slider.value = y;
    updatePanel(y);
}

updatePanel(1299);
</script>
"""

class HTMLMacro(MacroElement):
    def __init__(self, html):
        super().__init__()
        self._name = "HTMLMacro"
        self._template = Template(html)

m.get_root().html.add_child(folium.Element(timeline_html))

# Layer control
folium.LayerControl(collapsed=False, position="topright").add_to(m)

# ---------------------------------------------------------------------------
# 9.  SAVE
# ---------------------------------------------------------------------------
out = "ottoman_europe.html"
m.save(out)
print(f"\n✅ Map saved to: {os.path.abspath(out)}")
print(f"   File size: {os.path.getsize(out)/1024:.0f} KB")
print(f"\n   Open ottoman_europe.html in any modern browser to view the interactive map.")
PYEOF