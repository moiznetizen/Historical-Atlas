"""Load atlas content from JSON data files."""

from .utils import load_json

BOUNDS = [[34.0, 8.0], [52.0, 39.0]]
TIMELINE_START = 1354
TIMELINE_END = 1685

TERRITORIES = load_json("territories.json")
EVENTS = load_json("events.json")
CITIES = load_json("cities.json")
BATTLES = load_json("battles.json")
CAMPAIGNS = load_json("campaigns.json")
