import re
import unicodedata


# Palabras que no ayudan a identificar el juego base
STOPWORDS = {
    "edition",
    "ed",
    "goty",
    "game",
    "year",
    "ultimate",
    "deluxe",
    "complete",
    "collection",
    "bundle",
    "pack",
    "definitive",
    "special",
    "premium",
    "standard",
    "anniversary",
    "remastered",
    "remake",
    "director",
    "cut",
    "gold",
    "platinum",
    "enhanced",
    "soundtrack",
    "ost",
    "artbook",
    "expansion",
    "season",
    "pass",
    "upgrade",
}


ROMAN_MAP = {
    " i ": " 1 ",
    " ii ": " 2 ",
    " iii ": " 3 ",
    " iv ": " 4 ",
    " v ": " 5 ",
    " vi ": " 6 ",
    " vii ": " 7 ",
    " viii ": " 8 ",
    " ix ": " 9 ",
    " x ": " 10 ",
    " xi ": " 11 ",
    " xii ": " 12 ",
    " xiii ": " 13 ",
    " xiv ": " 14 ",
    " xv ": " 15 ",
    " xvi ": " 16 ",
}


def remove_accents(text: str) -> str:

    text = unicodedata.normalize("NFKD", text)
    return text.encode("ascii", "ignore").decode("utf-8")


def normalize_roman_numbers(text: str) -> str:

    text = f" {text} "
    for roman, arabic in ROMAN_MAP.items():
        text = text.replace(roman, arabic)
    return text.strip()


def remove_special_characters(text: str) -> str:

    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return text


def remove_stopwords(text: str) -> str:

    words = text.split()
    filtered = [w for w in words if w not in STOPWORDS]
    return " ".join(filtered)


def normalize_spaces(text: str) -> str:

    return re.sub(r"\s+", " ", text).strip()


def normalize_game_name(name: str) -> str:

    name = name.lower()
    name = remove_accents(name)
    name = remove_special_characters(name)
    name = normalize_roman_numbers(name)
    name = remove_stopwords(name)
    name = normalize_spaces(name)

    return name