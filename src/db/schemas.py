from pydantic import BaseModel

import uuid


class GameRoomBase(BaseModel):
    id: uuid.UUID
    code: str
    deck_name: str
    player_names: list[str]
    curr_player_idx: int
    levels_card_cnt: list[int]
    curr_card_idx: int
    levels_cnt: int
    curr_level: int
    is_game_started: bool
    is_game_over: bool

    class Config:
        from_attributes = True


class GameRoomRequest(BaseModel):
    deck_name: str
    levels_card_cnt: list[int]
    levels_cnt: int
