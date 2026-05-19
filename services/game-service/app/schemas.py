from pydantic import BaseModel
from typing import List
from datetime import datetime
from uuid import UUID


class GameCreate(BaseModel):
    title: str
    genre: str
    platform: str
    release_year: int
    cover_url: str


class GameOut(BaseModel):
    id: UUID
    title: str
    genre: str
    platform: str
    release_year: int
    cover_url: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class GameList(BaseModel):
    items: List[GameOut]
    total: int
    limit: int
    offset: int