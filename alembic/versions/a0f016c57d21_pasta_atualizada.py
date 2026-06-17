"""Pasta atualizada

Revision ID: a0f016c57d21
Revises: ca0636b8ebe3
Create Date: 2026-06-14 22:21:02.425453
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision: str = 'a0f016c57d21'
down_revision: Union[str, Sequence[str], None] = 'ca0636b8ebe3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # UNIQUE constraint (SQLite safe)
    with op.batch_alter_table("categoria") as batch_op:
        batch_op.create_unique_constraint("uq_categoria_nome", ["nome"])

    # nova coluna
    op.add_column(
        'pasta',
        sa.Column('Estado', sa.String(), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column('pasta', 'Estado')

    with op.batch_alter_table("categoria") as batch_op:
        batch_op.drop_constraint("uq_categoria_nome", type_="unique")