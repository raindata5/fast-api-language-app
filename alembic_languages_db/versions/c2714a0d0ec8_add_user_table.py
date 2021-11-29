"""add user table

Revision ID: c2714a0d0ec8
Revises: f2adabe8421a
Create Date: 2021-11-26 19:29:56.461769

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text


# revision identifiers, used by Alembic.
revision = 'c2714a0d0ec8'
down_revision = 'f2adabe8421a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("User", sa.Column("UserID", sa.Integer, primary_key=True, nullable=False),
    sa.Column("email", sa.String(40), unique=True, nullable=False ),
    sa.Column("password", sa.String(300), nullable=False),
    sa.Column("created_at", sa.DATETIME(timezone=True), nullable= False, server_default=text('SYSUTCDATETIME()'))
    )
    pass


def downgrade():
    op.drop_table("User")
    pass
