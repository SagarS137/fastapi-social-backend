"""add fk to post table

Revision ID: aa7237e7ad4c
Revises: df3db6549bbe
Create Date: 2025-06-28 18:46:48.730846

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa7237e7ad4c'
down_revision: Union[str, Sequence[str], None] = 'df3db6549bbe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer, nullable=False))
    op.create_foreign_key(
        'posts_users_fk',           # Constraint name
        'posts',                    # Source table
        'users',                    # Referent table
        ['owner_id'],               # Local columns
        ['id'],                     # Remote columns
        ondelete='CASCADE'
    )

def downgrade() -> None:
    op.drop_constraint('posts_users_fk', 'posts', type_='foreignkey')
    op.drop_column('posts', 'owner_id')
