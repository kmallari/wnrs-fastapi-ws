from sqlalchemy import Boolean, Column, SmallInteger, ARRAY, CHAR, VARCHAR, UUID
from .db import Base


class GameRoom(Base):
    __tablename__ = "game_rooms"

    id = Column(UUID, primary_key=True, index=True)
    code = Column(CHAR(6), unique=True, index=True)
    deck_name = Column(VARCHAR(50))
    player_names = Column(ARRAY(VARCHAR(15)))
    curr_player_idx = Column(SmallInteger, default=0)
    levels_card_cnt = Column(ARRAY(SmallInteger))
    curr_card_idx = Column(SmallInteger, default=0)
    levels_cnt = Column(SmallInteger, default=0)
    curr_level = Column(SmallInteger, default=0)
    is_game_started = Column(Boolean, default=False)
    is_game_over = Column(Boolean, default=False)

    def to_dict(self):
        return {field.name: getattr(self, field.name) for field in self.__table__.c}
