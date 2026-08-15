"""Visual design tokens for the historical atlas."""

print("Styles file successfully loaded!")

DIRECT = "#0f5b44"
DIRECT_DARK = "#12362d"
VASSAL = "#68b684"
INK = "#241b18"
PAPER = "#fbf6ea"

POWER_COLORS = {
    # Core Ottoman & Direct Rulers
    "Ottoman Province": DIRECT,
    "Ottoman Vassal": VASSAL,
    "Current Conquest":  "#d4c04f",
   "Michael the Braves Dominion of the Lower Danube": "#d4af37",
    "Wallachian Principality": "#d00258",
    "Moldavian Principality": "#8b2500",
    "Crown of Castile": "#f1c40f",
    "Crown of Aragon": "#e74c3c",
    "Spainish Empire": "#F4C430",
   "Dutch Republic": "#4169E1",
   "Swiss Confederacy": "#b19cd9",
   "Duchy of Naxos": "#85e5eb",
   "Papal States": "#f39c12",
   "Golden Horde": "#C89B3C",
   "Nogai Horde": "#1B365D",
   
    # Regional Powers & Monarchies
    "Upper Hungary": "#86cfa0",
    "Habsburg Monarchy": "#f30707",
    "Royal Hungary": "#d97706",
    "Kingdom of Hungary": "#d97706",
    "Kingdom of Croatia": "#1e61e6",
    "Holy Roman Empire": "#0FF507",
    "HRE": "#e25379",
    "Tsardom of Russia": "#123228",
    "Kingdom of France": "#002366",
    "House of Wettin":"#800031",
  "House of Wettin (Albertine branch)":"#800031",
"House of Wettin (Ernestine branch)":"#800031",
"House of Ascania":"#800031",
"House of Jagiellon":"#d97706",
    
    # Italian & Mediterranean States
    "Venetian Republic": "#8f2f2a",
    "Republic of Ragusa": "#c7a06a",
    "Republic of Genoa": "#18D8BB",
    "Kingdom of England": "#df07f3",
    "Kingdom of Denmark": "#ffff55",
    "Kingdom of Denmark (union crown)": "#e5f931",
    "House of Hohenzollern": "#9c07f3",
    "House of Wittelsbach":"#07f3bc",
    "House of Luxembourg / Wittelsbach":"#9c07f3",
    "House of Hohenzollern / Luxembourg":"#9c07f3",
    "vassal of Polish-Lithuanian Commonwealth":"#9B3918", 
    "Sibir Khanate":"#09D57D", 
    
    # Eastern Europe & Rus Principalities
    "Grand Duchy of Muscovy": "#1a7894",
    "Kingdom of Poland": "#4cc6ef",
    "Fief of Poland": "#3ebee9",
    "Grand Duchy of Lithuania": "#4112cd",
    "Vassal of the Grand Duchy of Lithuania": "#4112cd",
    "Polish-Lithuanian Commonwealth": "#952500", 
    "Cossack Hetmanate": "#C8F72D",
    "Kingdom of Sweden":"#C1EE45",
    "Teutonic Order":"#0F0045",
    "House of Luxembourg":"#0086ED",
    # Steppe Khanates & Hordes (Added Great Horde & Kazan Khanate)
    "Crimean Khanate": "#68b684",
    "Great Horde": "#8b7355",      
    "Kazan Khanate": "#cc6600",     
    "Independent Khanate": "#168ECA",
    "Don Cossacks": "#17bda7",
    "Timurid Empire": "#b93e65",
    "Livonian Order": "#0066b5",
    
    # Balkans & Southeast Europe
    "Albanian Lords": "#a5a58d",
    "Serbian Empire": "#6b705c",
    "Serbian Despotate": "#84a59d",
    "Bulgarian Tsardom": "#b7b7a4",
    "Byzantine Empire": "#7b0000",
    "Kingdom of Bosnia": "#4682B4",
    "Principality of Moravian Serbia": "#CD5C5C",
    "Serbian Uprising": "#CE1754",
    "Duchy of Saint Sava (Herzegovina)": "#13CACA",  
    "Principality of Transylvania": "#002AE7",
    "Independent (Kosača Family)": "#8B4513",
    "Habsburg vassal": "#D7473C",
     "Habsburg Personal Union": "#D7473C",
     "House of Griffin": "#72545B",
    
    # Middle East, North Africa & Rivals
    "Mamluk Sultanate": "#c19a6b",
    "Zápolya Dynasty": "#D2691E",
    "Crown of Bohemia": "#6A5ACD",
    "Alaouite Dynasty": "#b87d4b",
    "Saadian Sultanate": "#a66c3d",
    "Saadian Empire (Timbuktu)": "#945b2f",
    "Wattasid Sultanate": "#824a21",
    "Marinid Sultanate": "#703913",
    "Guarded Domains - Safavid Iran": "#04C6C3"
}


def css_palette_vars():
    """
    Dynamically converts all POWER_COLORS into CSS variables (--power-name),
    ensuring map styles load correctly without fallback grey render states.
    """
    pairs = {
        "paper": PAPER,
        "ink": INK,
        "direct": DIRECT,
        "direct-dark": DIRECT_DARK,
        "vassal": VASSAL,
    }
    
    # Automatically generate CSS variables for every power color
    for power_name, color_hex in POWER_COLORS.items():
        slug = power_name.lower().replace(" ", "-").replace("(", "").replace(")", "").replace("/", "-")
        pairs[f"power-{slug}"] = color_hex

    return "\n".join(f"--{key}: {value};" for key, value in pairs.items())