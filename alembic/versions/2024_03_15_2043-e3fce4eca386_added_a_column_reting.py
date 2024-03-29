"""added a column reting

Revision ID: e3fce4eca386
Revises: 380bb3f1d9fe
Create Date: 2024-03-15 20:43:41.448795

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e3fce4eca386"
down_revision: Union[str, None] = "380bb3f1d9fe"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "profile", sa.Column("rating", sa.Float(), server_default="5", nullable=False)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("profile", "rating")
    # ### end Alembic commands ###
