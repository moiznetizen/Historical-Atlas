"""Load atlas content from JSON data files."""

from .utils import load_json

BOUNDS = [[0, -15.0], [55.0, 65.0]]
TIMELINE_START = 1354
TIMELINE_END = 1685

TERRITORIES = load_json("territories.json")
EVENTS = load_json("events.json")
CITIES = load_json("cities.json")
BATTLES = load_json("battles.json")
CAMPAIGNS = load_json("campaigns.json")
