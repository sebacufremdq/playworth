import json
from pathlib import Path


CATALOG_PATH = Path("data/steam_catalog.json")
INDEX_PATH = Path("data/steam_index.json")


def main():

    print("[INFO] Loading normalized catalog")

    with open(CATALOG_PATH, encoding="utf-8") as f:
        catalog = json.load(f)

    index = {}

    for game in catalog:

        key = game["normalized"]

        if key not in index:
            index[key] = []

        index[key].append({
            "appid": game["appid"],
            "name": game["name"]
        })

    print(f"[INFO] Indexed {len(index)} normalized titles")

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print(f"[INFO] Saved index to {INDEX_PATH}")


if __name__ == "__main__":
    main()