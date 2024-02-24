"""added columm balance  in table profile

Revision ID: 6d95c13baeea
Revises: b2a17a368aac
Create Date: 2024-02-17 18:23:02.292025

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6d95c13baeea"
down_revision: Union[str, None] = "b2a17a368aac"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("profile", sa.Column("balance", sa.Float(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("profile", "balance")
    # ### end Alembic commands ###