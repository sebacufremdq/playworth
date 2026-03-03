import pandas as pd
from database import Session, Game
from clients.steam_client import search_steam_app, get_steam_reviews
from datetime import datetime
from pathlib import Path


def process_games(input_file: str):
    df = pd.read_excel(input_file)

    session = Session()

    for _, row in df.iterrows():
        game_name = row["game_name"].strip()

        existing_game = session.query(Game).filter_by(input_name=game_name).first()

        if existing_game:
            print(f"[INFO] {game_name} already exists. Updating...")
            game = existing_game
        else:
            print(f"[INFO] Creating entry for {game_name}")
            game = Game(input_name=game_name)
            session.add(game)
            session.commit()

        appid = search_steam_app(game_name)

        if not appid:
            print(f"[WARNING] No Steam AppID found for {game_name}")
            continue

        steam_pct, steam_count = get_steam_reviews(appid)

        game.steam_appid = appid
        game.steam_positive_pct = steam_pct
        game.steam_review_count = steam_count
        game.updated_at = datetime.utcnow()

        session.commit()

        print(f"[SUCCESS] {game_name} → {steam_pct}% ({steam_count} reviews)")

    session.close()


if __name__ == "__main__":
    base_path = Path(__file__).resolve().parent
    input_path = base_path / "data" / "input.xlsx"
    process_games(input_path)
