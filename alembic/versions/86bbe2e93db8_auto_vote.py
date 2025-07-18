"""auto_vote

Revision ID: 86bbe2e93db8
Revises: aa7237e7ad4c
Create Date: 2025-06-28 19:03:27.350007

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86bbe2e93db8'
down_revision: Union[str, Sequence[str], None] = 'aa7237e7ad4c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    # alembic revision --autogenerate -m "auto_vote"
    op.create_table('votes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.create_unique_constraint(None, 'users', ['email'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.drop_table('votes')
    # ### end Alembic commands ###
