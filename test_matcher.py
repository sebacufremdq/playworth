from utils.matching.steam_matcher import SteamMatcher


matcher = SteamMatcher()

tests = [
    "Call of Duty Modern Warfare II",
    "COD Modern Warfare 2",
    "Dark Souls III",
    "Resident Evil VII Biohazard",
    "The Witcher 3 Wild Hunt"
]


for t in tests:

    result = matcher.match(t)

    print("\nINPUT:", t)
    print("RESULT:", result)