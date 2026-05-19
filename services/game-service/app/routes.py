from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import GameCreate, GameOut, GameList
from app import service

router = APIRouter(prefix="/v1/games", tags=["games"])


@router.post("/", response_model=GameOut)
def create_game(game: GameCreate, db: Session = Depends(get_db)):
    return service.add_game(db, game)


@router.get("/", response_model=GameList)
def list_games(db: Session = Depends(get_db)):
    games = service.fetch_all_games(db)

    return {
        "items": games,
        "total": len(games),
        "limit": 20,
        "offset": 0
    }


@router.get("/{game_id}", response_model=GameOut)
def get_game(game_id: str, db: Session = Depends(get_db)):
    game = service.fetch_game(db, game_id)

    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    return game


@router.get("/search/", response_model=GameList)
def search_games(q: str, db: Session = Depends(get_db)):
    games = service.search_for_games(db, q)

    return {
        "items": games,
        "total": len(games),
        "limit": 20,
        "offset": 0
    }