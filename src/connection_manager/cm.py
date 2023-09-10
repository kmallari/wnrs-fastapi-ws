import json

from fastapi import WebSocket
from sqlalchemy.orm import Session

from ..db import repo
from ..errors import error_factory


class ConnectionManager:
    def __init__(self):
        self.active_connections = {}
        self.controller = {
            "add_player": self.add_player,
            "remove_player": self.remove_player,
            "start_game": self.start_game,
            "next_card": self.next_card,
            "prev_card": self.prev_card,
        }

    async def connect(self, websocket: WebSocket, room_id: str):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

    def disconnect(self, websocket: WebSocket, room_id: str):
        self.active_connections[room_id].remove(websocket)

    async def send(self, websocket: WebSocket, data: dict):
        try:
            await websocket.send_json(data)
        except Exception as e:
            print(e)

    async def broadcast(self, room_id: str, res):
        try:
            if room_id in self.active_connections:
                for connection in self.active_connections[room_id]:
                    await connection.send_json(res)
        except Exception as e:
            print(e)

    async def add_player(self, db: Session, room_id: str, player_name: str):
        game_room = repo.add_player(db, room_id, player_name)
        if game_room in error_factory:
            return error_factory[game_room]
        return {"type": "add_player", "res": player_name}

    async def remove_player(self, db: Session, room_id: str, player_name: str):
        game_room = repo.remove_player(db, room_id, player_name)
        if game_room in error_factory:
            return error_factory[game_room]
        return {"type": "remove_player", "res": player_name}

    async def start_game(self, db: Session, room_id: str, _):
        game_room = repo.start_game(db, room_id)
        print(str(game_room.to_dict()))
        if game_room in error_factory:
            return error_factory[game_room]
        game_room_copy = game_room.to_dict().copy()
        game_room_copy["id"] = str(game_room_copy["id"])
        return {
            "type": "start_game",
            "res": json.dumps(game_room_copy, separators=(",", ":")),
        }

    async def next_card(self, db: Session, room_id: str, _):
        game_room = repo.next_card(db, room_id)
        if game_room in error_factory:
            return error_factory[game_room]
        game_room_copy = game_room.to_dict().copy()
        game_room_copy["id"] = str(game_room_copy["id"])
        return {
            "type": "next_card",
            "res": json.dumps(game_room_copy, separators=(",", ":")),
        }

    async def prev_card(self, db: Session, room_id: str, _):
        game_room = repo.prev_card(db, room_id)
        if game_room in error_factory:
            return error_factory[game_room]
        game_room_copy = game_room.to_dict().copy()
        game_room_copy["id"] = str(game_room_copy["id"])
        return {
            "type": "prev_card",
            "res": json.dumps(game_room_copy, separators=(",", ":")),
        }
