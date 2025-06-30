"""create users table

Revision ID: df3db6549bbe
Revises: 4cf791eb6f43
Create Date: 2025-06-28 18:38:26.554108

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'df3db6549bbe'
down_revision: Union[str, Sequence[str], None] = '4cf791eb6f43'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True, nullable=False),
        sa.Column('email', sa.String, unique=True, nullable=False, index=True),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

def downgrade() -> None:
    op.drop_table('users')
