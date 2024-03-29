"""create table ConfirmationKeys

Revision ID: 380bb3f1d9fe
Revises: 6d95c13baeea
Create Date: 2024-02-19 09:45:05.253470

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "380bb3f1d9fe"
down_revision: Union[str, None] = "6d95c13baeea"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "confirmation_keys",
        sa.Column("email_confirmation_code", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("confirmation_keys")
    # ### end Alembic commands ###
