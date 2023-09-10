from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from . import models, schemas


def create_game_room(
    db: Session, id: str, code: str, game_room: schemas.GameRoomRequest
):
    try:
        db_game_room = models.GameRoom(
            id=id,
            code=code,
            deck_name=game_room.deck_name,
            levels_card_cnt=game_room.levels_card_cnt,
            levels_cnt=game_room.levels_cnt,
        )
        db.add(db_game_room)
        db.commit()
        db.refresh(db_game_room)
        return db_game_room
    except Exception as e:
        print(e)
        db.rollback()
        return None


def get_game_room(db: Session, code: str):
    return db.query(models.GameRoom).filter(models.GameRoom.code == code).first()


def get_game_room_by_id(db: Session, id: str):
    return db.query(models.GameRoom).filter(models.GameRoom.id == id).first()


def next_card(db: Session, id: str):
    # handle going to next card.
    # increment the player index and card index.

    game_room = get_game_room_by_id(db, id)
    # don't do anything if the game is over.
    if game_room.is_game_over:
        return game_room

    # handle game over if we're at the last card of the last level
    if (
        game_room.curr_level == game_room.levels_cnt - 1
        and game_room.curr_card_idx == game_room.levels_card_cnt[game_room.curr_level]
    ):
        game_room.is_game_over = True
        db.commit()
        db.refresh(game_room)
        return game_room

    # if we're at the last card of a level,
    # go to the next level and reset the card index to 0.
    if game_room.curr_card_idx == game_room.levels_card_cnt[game_room.curr_level]:
        game_room.curr_level += 1
        game_room.curr_card_idx = 0
        db.commit()
        db.refresh(game_room)
        return game_room

    game_room.curr_card_idx += 1
    if game_room.curr_card_idx != 0:
        game_room.curr_player_idx = game_room.curr_card_idx % len(
            game_room.player_names
        )
    try:
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()

    db.refresh(game_room)

    return game_room


def prev_card(db: Session, id: str):
    # handle going to prev card.
    # decrement the player index and card index.

    game_room = get_game_room_by_id(db, id)
    # don't do anything if the game is over.
    if game_room.is_game_over:
        return game_room

    # handle going back to the first card of the first level
    if game_room.curr_level == 0 and game_room.curr_card_idx == 0:
        return game_room

    # if we're at the first card of a level,
    # go to the prev level and reset the card index to the last card of the prev level.
    if game_room.curr_card_idx == 0:
        game_room.curr_level -= 1
        game_room.curr_card_idx = game_room.levels_card_cnt[game_room.curr_level]
        db.commit()
        db.refresh(game_room)
        return game_room

    game_room.curr_card_idx -= 1
    if game_room.curr_card_idx != 0:
        game_room.curr_player_idx = game_room.curr_card_idx % len(
            game_room.player_names
        )

    try:
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()

    db.refresh(game_room)

    return game_room


def next_level(db: Session, code: str):
    game_room = get_game_room(db, code)
    game_room.curr_level += 1
    game_room.curr_card_idx = 0
    # game_room.curr_player_idx = 0 # might wanna look into this
    db.commit()
    db.refresh(game_room)
    return game_room


def prev_game(db: Session, code: str):
    game_room = get_game_room(db, code)
    game_room.curr_level -= 1
    game_room.curr_card_idx = 0
    # game_room.curr_player_idx = 0 # might wanna look into this
    db.commit()
    db.refresh(game_room)
    return game_room


def start_game(db: Session, id: str):
    game_room = get_game_room_by_id(db, id)
    game_room.is_game_started = True
    db.commit()
    db.refresh(game_room)
    return game_room


def end_game(db: Session, code: str):
    game_room = get_game_room(db, code)
    game_room.is_game_over = True
    db.commit()
    db.refresh(game_room)
    return game_room


def add_player(db: Session, id: str, player_name: str):
    game_room = get_game_room_by_id(db, id)
    if not game_room.player_names:
        game_room.player_names = []
    if len(game_room.player_names) >= 4:
        return 5001
    if player_name in game_room.player_names:
        return 5002
    else:
        game_room.player_names = game_room.player_names + [player_name]
        print(game_room.player_names)
        db.commit()
        db.refresh(game_room)
        return game_room


def remove_player(db: Session, id: str, player_name: str):
    game_room = get_game_room_by_id(db, id)
    if not game_room.player_names:
        game_room.player_names = []
    print(game_room.player_names, player_name, player_name in game_room.player_names)
    if player_name in game_room.player_names:
        game_room.player_names = [
            name for name in game_room.player_names if name != player_name
        ]
        print(game_room.player_names)
        db.commit()
        db.refresh(game_room)
        return game_room
    else:
        return 5003
