import requests
from typing import Optional, Tuple

BASE_SEARCH_URL = "https://store.steampowered.com/api/storesearch"
BASE_REVIEW_URL = "https://store.steampowered.com/appreviews"


def search_steam_app(game_name: str) -> Optional[int]:
    try:
        response = requests.get(
            BASE_SEARCH_URL,
            params={"term": game_name, "l": "english", "cc": "US"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        if data["total"] == 0:
            return None

        return data["items"][0]["id"]

    except Exception as e:
        print(f"[ERROR] Steam search failed for {game_name}: {e}")
        return None


def get_steam_reviews(appid: int) -> Tuple[Optional[float], Optional[int]]:
    try:
        response = requests.get(
            f"{BASE_REVIEW_URL}/{appid}",
            params={"json": 1},
            timeout=10
        )
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
        print(f"[ERROR] Steam reviews failed for {appid}: {e}")
        return None, None