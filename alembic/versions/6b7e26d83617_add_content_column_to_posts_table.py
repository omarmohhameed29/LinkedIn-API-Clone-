"""add content column to posts table

Revision ID: 6b7e26d83617
Revises: bfa726104fc4
Create Date: 2024-02-27 09:31:07.204919

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b7e26d83617'
down_revision: Union[str, None] = 'bfa726104fc4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass 


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
