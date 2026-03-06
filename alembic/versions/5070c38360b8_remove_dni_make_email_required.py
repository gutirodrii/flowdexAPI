"""remove_dni_make_email_required

Revision ID: 5070c38360b8
Revises:
Create Date: 2026-03-06 17:20:35.948850

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '5070c38360b8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('usuarios', 'dni', if_exists=True)
    op.alter_column('usuarios', 'email',
                    existing_type=sa.String(),
                    nullable=False)


def downgrade() -> None:
    op.alter_column('usuarios', 'email',
                    existing_type=sa.String(),
                    nullable=True)
    op.add_column('usuarios',
                  sa.Column('dni', sa.String(), nullable=True))
