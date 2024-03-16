"""added a column price in table subject

Revision ID: 301aa1b4f785
Revises: e3fce4eca386
Create Date: 2024-03-16 13:14:34.552010

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "301aa1b4f785"
down_revision: Union[str, None] = "e3fce4eca386"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("subject", sa.Column("price", sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("subject", "price")
    # ### end Alembic commands ###