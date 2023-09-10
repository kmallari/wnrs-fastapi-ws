import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from ..db import repo, schemas
from ..db.db import SessionLocal

router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.rollback()
    finally:
        db.close()


@router.get("/game-room/", response_model=schemas.GameRoomBase)
def read_game_room(code: str, db: Session = Depends(get_db)):
    db_game_room = repo.get_game_room(db, code=code)
    if db_game_room is None:
        raise HTTPException(status_code=404, detail="Game Room not found")
    return db_game_room


@router.get("/game-room/id", response_model=schemas.GameRoomBase)
def read_game_room_by_id(id: str, db: Session = Depends(get_db)):
    db_game_room = repo.get_game_room_by_id(db, id=id)
    if db_game_room is None:
        raise HTTPException(status_code=404, detail="Game Room not found")
    return db_game_room


@router.post("/game-room/", response_model=schemas.GameRoomBase)
def create_game_room(game_room: schemas.GameRoomRequest, db: Session = Depends(get_db)):
    # generate 6 character alphanumeric code
    def generate_code():
        import random
        import string

        return "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

    print("1")
    code = generate_code()
    id = uuid.uuid4()
    print("2")
    db_game_room = repo.create_game_room(db, id, code, game_room=game_room)
    return db_game_room


@router.post("/game-room/:id/add-player")
async def add_player(id: str, player_name: str, db: Session = Depends(get_db)):
    repo.add_player(db, id, player_name)
    return {"ok": True}


# HEALTH CHECK


# if can connect to db, return "ok": True, else return "ok": False
@router.get("/health-db")
async def health_check_db(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1;"))
        return {"ok": True}
    except Exception as e:
        print(e)
        return {"ok": False, "detail": str(e)}


@router.get("/health-server")
async def health_check_server():
    return {"ok": True}
