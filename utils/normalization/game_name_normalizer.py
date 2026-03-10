import re
import unicodedata


# Palabras que no ayudan a identificar el juego base
STOPWORDS = frozenset({
    "edition","ed","goty","game","year","ultimate","deluxe","complete",
    "collection","bundle","pack","definitive","special","premium",
    "standard","anniversary","remastered","remake","director","cut",
    "gold","platinum","enhanced","soundtrack","ost","artbook",
    "expansion","season","pass","upgrade","the"
})


ROMAN_MAP = {
    "xvi": "16",
    "xv": "15",
    "xiv": "14",
    "xiii": "13",
    "xii": "12",
    "xi": "11",
    "x": "10",
    "ix": "9",
    "viii": "8",
    "vii": "7",
    "vi": "6",
    "v": "5",
    "iv": "4",
    "iii": "3",
    "ii": "2",
    "i": "1",
}


ROMAN_PATTERNS = {
    re.compile(rf"\b{roman}\b"): arabic
    for roman, arabic in ROMAN_MAP.items()
}

def separate_punctuation(text: str) -> str:
    return re.sub(r"([^\w\s])", r" \1 ", text)

def remove_accents(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    return text.encode("ascii", "ignore").decode("utf-8")


def normalize_roman_numbers(text: str) -> str:

    tokens = text.split()
    converted = []

    for token in tokens:

        clean = token.strip(".,:-_()[]{}")

        if clean in ROMAN_MAP:
            token = token.replace(clean, ROMAN_MAP[clean])

        converted.append(token)

    return " ".join(converted)


def remove_special_characters(text: str) -> str:
    return re.sub(r"[^a-z0-9\s]", " ", text)


def remove_stopwords(text: str) -> str:
    return " ".join(word for word in text.split() if word not in STOPWORDS)


def normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def normalize_game_name(name: str) -> str:

    name = name.lower()
    name = remove_accents(name)
    name = normalize_roman_numbers(name)
    name = remove_special_characters(name)
    name = remove_stopwords(name)
    name = normalize_spaces(name)

    return name