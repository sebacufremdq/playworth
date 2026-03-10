import requests
from typing import Dict, List, Optional
import time


class SteamClient:

    STEAMSPY_ALL_URL = "https://steamspy.com/api.php"
    APP_DETAILS_URL = "https://store.steampowered.com/api/appdetails"

    def __init__(self):

        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        })

    # -----------------------------
    # Get catalog (appid + name)
    # -----------------------------
    def get_catalog(self) -> List[Dict]:

        catalog = []
        page = 0

        try:

            while True:

                params = {
                    "request": "all",
                    "page": page
                }

                response = self.session.get(
                    self.STEAMSPY_ALL_URL,
                    params=params,
                    timeout=60
                )

                response.raise_for_status()

                data = response.json()

                # SteamSpy devuelve dict vacío cuando no hay más páginas
                if not data:
                    break

                for appid, game in data.items():
                    catalog.append({
                        "appid": int(appid),
                        "name": game.get("name")
                    })

                print(f"[INFO] Page {page} downloaded ({len(data)} apps)")

                page += 1

                time.sleep(1)  # evitar rate limit

            return catalog

        except Exception as e:

            print(f"[ERROR] Failed to download Steam catalog: {e}")
            return catalog
    # -----------------------------
    # Get detailed game metadata
    # -----------------------------
    def get_app_details(self, appid: int) -> Optional[Dict]:

        try:

            params = {"appids": appid}

            response = self.session.get(
                self.APP_DETAILS_URL,
                params=params,
                timeout=30
            )

            response.raise_for_status()

            data = response.json()

            if not data[str(appid)]["success"]:
                return None

            return data[str(appid)]["data"]

        except Exception as e:

            print(f"[ERROR] Failed to fetch app {appid}: {e}")
            return None

    # -----------------------------
    # Get review score
    # -----------------------------
    def get_reviews(self, appid: int):

        try:

            url = f"https://store.steampowered.com/appreviews/{appid}"

            params = {"json": 1}

            response = self.session.get(url, params=params, timeout=30)

            response.raise_for_status()

            data = response.json()

            summary = data.get("query_summary", {})

            total = summary.get("total_reviews", 0)
            positive = summary.get("total_positive", 0)

            if total == 0:
                return None, 0

            pct = round((positive / total) * 100, 2)

            return pct, total

        except Exception as e:

            print(f"[ERROR] Failed to fetch reviews for {appid}: {e}")
            return None, None