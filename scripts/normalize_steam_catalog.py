import json
import re
from pathlib import Path
from utils.game_name_normalizer import normalize_game_name


RAW_PATH = Path("data/steam_catalog_raw.json")
OUT_PATH = Path("data/steam_catalog.json")

def main():

    print("[INFO] Loading raw Steam catalog")

    with open(RAW_PATH, encoding="utf-8") as f:
        data = json.load(f)

    normalized_catalog = []

    for game in data:

        normalized_catalog.append({
            "appid": game["appid"],
            "name": game["name"],
            "normalized": normalize_game_name(game["name"])
        })

    print(f"[INFO] Processed {len(normalized_catalog)} games")

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(normalized_catalog, f, ensure_ascii=False, indent=2)

    print(f"[INFO] Saved normalized catalog to {OUT_PATH}")


if __name__ == "__main__":
    main()