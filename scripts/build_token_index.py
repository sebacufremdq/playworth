import json
from collections import defaultdict
from pathlib import Path


CATALOG_PATH = Path("data/steam_catalog.json")
OUT_PATH = Path("data/token_index.json")


def main():

    with open(CATALOG_PATH, encoding="utf-8") as f:
        catalog = json.load(f)

    token_index = defaultdict(set)

    for game in catalog:

        normalized = game["normalized"]
        tokens = normalized.split()

        for token in tokens:

            if len(token) < 3:
                continue

            token_index[token].add(normalized)

    token_index = {k: list(v) for k, v in token_index.items()}

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(token_index, f, ensure_ascii=False)

    print(f"[INFO] Token index built with {len(token_index)} tokens")


if __name__ == "__main__":
    main()