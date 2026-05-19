from sqlalchemy.orm import Session
from app.models import Game


def create_game(db: Session, data):
    game = Game(
        title=data.title,
        genre=data.genre,
        platform=data.platform,
        release_year=data.release_year,
        cover_url=data.cover_url
    )

    db.add(game)
    db.commit()
    db.refresh(game)

    return game


def get_game(db: Session, game_id: str):
    return db.query(Game).filter(Game.id == game_id).first()


def list_games(db: Session):
    return db.query(Game).all()


def search_games(db: Session, q: str):
    return db.query(Game).filter(Game.title.ilike(f"%{q}%")).all()