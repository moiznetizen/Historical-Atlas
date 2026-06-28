"""Visual design tokens for the historical atlas."""

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
    "Habsburg Monarchy": "#8e918d",
    "Polish-Lithuanian Commonwealth": "#f1e2bb",
    "Tsardom of Russia": "#739bb5",
    "Venetian Republic": "#8f2f2a",
    "Republic of Ragusa": "#c7a06a",
    "Kingdom of Croatia": "#a9a9a4",
    "Holy Roman Empire": "#c0b8a2",
    "Crimean Khanate": "#68b684",
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
