import json

from fastapi import APIRouter, Depends, WebSocket
from sqlalchemy.orm import Session

from ..connection_manager.cm import ConnectionManager
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


manager = ConnectionManager()


@router.websocket("/ws/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket, room_id: str, db: Session = Depends(get_db)
):
    await manager.connect(websocket, room_id)
    try:
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)
            type = data["type"]
            request = data["data"]
            print("req", type, request)
            res = await manager.controller[type](db, room_id, request)
            print("res", res)
            if res["type"] == "error":
                await manager.send(websocket, res)
            else:
                await manager.broadcast(room_id, res)
    except:
        manager.disconnect(websocket, room_id)
