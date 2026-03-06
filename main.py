import pandas as pd
from database import Session, Game
from clients.steam_client import search_steam_app, get_steam_reviews
from datetime import datetime
from pathlib import Path
from utils.normalization import normalize_game_name

########################################################################
# FUNCIONES                                                            #
########################################################################


def process_games(input_file):

    df = pd.read_excel(input_file)

    session = Session()

    for index, row in df.iterrows():

        game_name = row["game_name"].strip()
        game_name_normalized = normalize_game_name(game_name)

        print(f"[DEBUG] raw: {game_name} | normalized: {game_name_normalized}")

        existing_game = session.query(Game).filter_by(normalized_name=game_name_normalized).first()

        if existing_game:
            print(f"[INFO] {game_name} already exists. Updating...")
            game = existing_game
        else:
            print(f"[INFO] Creating entry for {game_name}")
            game = Game(
                input_name=game_name,
                normalized_name=game_name_normalized
            )
            session.add(game)
            session.commit()

        # Buscar en Steam
        appid = search_steam_app(game_name_normalized)

        if not appid:
            print(f"[WARNING] No Steam AppID found for {game_name}")
            continue

        steam_pct, steam_count = get_steam_reviews(appid)

        game.steam_appid = appid
        game.steam_positive_pct = steam_pct
        game.steam_review_count = steam_count
        game.updated_at = datetime.now()

        session.commit()

        print(f"[SUCCESS] {game_name} → {steam_pct}% ({steam_count} reviews)")

    session.close()

########################################################################
# ENTRYPOINT
########################################################################

if __name__ == "__main__":

    base_path = Path(__file__).resolve().parent
    input_path = base_path / "data" / "input.xlsx"

    process_games(input_path)
