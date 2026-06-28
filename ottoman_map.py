"""Build the Ottoman Europe historical atlas.

Run:
    pip install -r requirements.txt
    python ottoman_map.py
"""

from atlas.map_builder import build_atlas


if __name__ == "__main__":
    build_atlas("ottoman_europe_atlas.html")
