import json
from pathlib import Path

from clients.steam_client import SteamClient


DATA_PATH = Path("data")
CATALOG_FILE = DATA_PATH / "steam_catalog_raw.json"


def main():

    steam = SteamClient()

    print("[INFO] Downloading Steam catalog...")

    apps = steam.get_app_list()

    if not apps:
        print("[ERROR] Failed to download catalog")
        return

    print(f"[INFO] Downloaded {len(apps)} apps")

    # asegurar que exista la carpeta data
    DATA_PATH.mkdir(exist_ok=True)

    with open(CATALOG_FILE, "w", encoding="utf-8") as f:
        json.dump(apps, f)

    print(f"[INFO] Catalog saved to {CATALOG_FILE}")


if __name__ == "__main__":
    main()