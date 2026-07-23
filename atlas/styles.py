"""Visual design tokens for the historical atlas."""

print("Styles file successfully loaded!")

DIRECT = "#0f5b44"
DIRECT_DARK = "#12362d"
VASSAL = "#68b684"
INK = "#241b18"
PAPER = "#fbf6ea"

POWER_COLORS = {
    "Ottoman Province": DIRECT,
    "Ottoman Vassal": VASSAL,
    "Current Conquest": "#c89b3c",
    "Upper Hungary": "#86cfa0",
    "Habsburg Monarchy": "#47e612",
    "Royal Hungary": "#d97706",
    "Venetian Republic": "#8f2f2a",
    "Republic of Ragusa": "#c7a06a",
    "Kingdom of Hungary": "#d97706",
    "Kingdom of Croatia": "#1e61e6",
    "Holy Roman Empire": "#c0b8a2",
    "Crimean Khanate": "#68b684",
    "Don Cossacks": "#17bda7",
    "Tsardom of Russia": "#16a2c9",
    "Albanian Lords": "#a5a58d",
    "Serbian Empire": "#6b705c",
    "Serbian Despotate": "#84a59d",
    "Bulgarian Tsardom": "#b7b7a4",
    "Byzantine Empire": "#7b0000"

}


def css_palette_vars():
    pairs = {
        "paper": PAPER,
        "ink": INK,
        "direct": DIRECT,
        "direct-dark": DIRECT_DARK,
        "vassal": VASSAL,
    }
    return "\n".join(f"--{key}: {value};" for key, value in pairs.items())

POWER_COLORS.update({

    "Mamluk Sultanate": "#c19a6b", 
    "Zápolya Dynasty": "#D2691E",
    "Crown of Bohemia": "#6A5ACD",
    "Grand Duchy of Muscovy": "#1a7894",
    "Kingdom of Poland": "#c3500e",
    "Grand Duchy of Lithuania": "#3c14b3",
    "Polish-Lithuanian Commonwealth": "#f22f53",
    "HRE": "#e25379",
    "Alaouite Dynasty": "#b87d4b",
    "Independent (Kosača Family)": "#8B4513", 
    "Kingdom of Bosnia": "#4682B4",
    "Saadian Sultanate": "#a66c3d",
    "Saadian Empire (Timbuktu)": "#945b2f",
    "Polish-Lithuanian Commonwealth": "#d3de09",
    "Wattasid Sultanate": "#824a21",
    "Independent Khanate": "#168ECA",
    "Principality of Moravian Serbia": "#CD5C5C",
    "Serbian Uprising": "#CE1754",
    "Marinid Sultanate": "#703913",
    "Guarded Domains - Safavid Iran": "#FF0000",
    "Duchy of Saint Sava (Herzegovina) ": "#13CACA",
    "Republic of Genoa": "#18D8BB",
    "Principality of Transylvania": "#002AE7",
    "Cossack Hetmanate": "#C8F72D"
    


    
})


