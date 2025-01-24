"""create game rooms table

Revision ID: xxxxxxxxxxxx
Revises: 
Create Date: 2024-xx-xx xx:xx:xx.xxxx

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'xxxxxxxxxxxx'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('game_rooms',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('code', sa.CHAR(length=6), nullable=True),
        sa.Column('deck_name', sa.VARCHAR(length=50), nullable=True),
        sa.Column('player_names', sa.ARRAY(sa.VARCHAR(length=15)), nullable=True),
        sa.Column('curr_player_idx', sa.SmallInteger(), nullable=True),
        sa.Column('levels_card_cnt', sa.ARRAY(sa.SmallInteger()), nullable=True),
        sa.Column('curr_card_idx', sa.SmallInteger(), nullable=True),
        sa.Column('levels_cnt', sa.SmallInteger(), nullable=True),
        sa.Column('curr_level', sa.SmallInteger(), nullable=True),
        sa.Column('is_game_started', sa.Boolean(), nullable=True),
        sa.Column('is_game_over', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_game_rooms_code'), 'game_rooms', ['code'], unique=True)
    op.create_index(op.f('ix_game_rooms_id'), 'game_rooms', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_game_rooms_id'), table_name='game_rooms')
    op.drop_index(op.f('ix_game_rooms_code'), table_name='game_rooms')
    op.drop_table('game_rooms') 
