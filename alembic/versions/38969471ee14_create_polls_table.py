"""create_polls_table

Revision ID: 38969471ee14
Revises: f087922ff907
Create Date: 2022-07-09 07:26:09.386252

"""
from alembic import op
import sqlalchemy as sa
import enum

class PollType(enum.Enum):
    text = 1
    image = 2

# revision identifiers, used by Alembic.
revision = '38969471ee14'
down_revision = 'f087922ff907'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'polls',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(30), nullable=False),
        sa.Column('type', sa.Enum(PollType), nullable=False),
        sa.Column('is_add_choices_active', sa.Boolean, nullable=False),
        sa.Column('is_voting_active', sa.Boolean, nullable=False),
        sa.Column('created_by', sa.Integer, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
    )

def downgrade() -> None:
    op.drop_table('polls')
    op.execute("DROP TYPE polltype")
