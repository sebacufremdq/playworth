import json
from pathlib import Path

from rapidfuzz import process, fuzz

from utils.normalization.game_name_normalizer import normalize_game_name


INDEX_PATH = Path("data/steam_index.json")

ALIASES = {
    "cod": "call of duty",
    "mw": "modern warfare",
    "rdr": "red dead redemption",
    "gta": "grand theft auto",
    "bf": "battlefield",
}

TOKEN_INDEX_PATH = Path("data/token_index.json")

class SteamMatcher:

    def __init__(self):

        with open(INDEX_PATH, encoding="utf-8") as f:
            self.token_index = json.load(f)

        # filtrar títulos basura
        self.normalized_titles = [
            t for t in self.index.keys()
            if len(t) > 3 and not t.isdigit()
        ]

        print(f"[INFO] Loaded Steam index with {len(self.normalized_titles)} titles")


    def get_candidates(self, normalized):

        tokens = normalized.split()
        candidates = set()

        for token in tokens:
            if token in self.token_index:
                candidates.update(self.token_index[token])

        return list(candidates)

    def expand_aliases(self, text: str):

        tokens = text.split()
        expanded = []

        for t in tokens:
            if t in ALIASES:
                expanded.extend(ALIASES[t].split())
            else:
                expanded.append(t)

        return " ".join(expanded)

    def match(self, name: str, threshold: int = 85):

        normalized = normalize_game_name(name)

        normalized = self.expand_aliases(normalized)

        # EXACT MATCH
        if normalized in self.index:
            return {
                "match_type": "exact",
                "query": name,
                "normalized": normalized,
                "result": self.index[normalized]
            }

        # evitar fuzzy en queries basura
        if len(normalized.split()) < 2:
            return None

        best_match = process.extractOne(
            normalized,
            self.normalized_titles,
            scorer=fuzz.token_set_ratio,
            score_cutoff=threshold
        )

        if best_match is None:
            return None

        matched_name, score, _ = best_match

        return {
            "match_type": "fuzzy",
            "query": name,
            "normalized": normalized,
            "matched_normalized": matched_name,
            "score": score,
            "result": self.index[matched_name]
        }