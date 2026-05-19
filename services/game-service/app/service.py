from sqlalchemy.orm import Session

from app import repository
from app.schemas import GameCreate


def add_game(db: Session, data: GameCreate):
    return repository.create_game(db, data)


def fetch_game(db: Session, game_id: str):
    return repository.get_game(db, game_id)


def fetch_all_games(db: Session):
    return repository.list_games(db)


def search_for_games(db: Session, q: str):
    return repository.search_games(db, q)