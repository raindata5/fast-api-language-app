"""create language table

Revision ID: f2adabe8421a
Revises: 
Create Date: 2021-11-25 16:50:51.531576

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2adabe8421a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("Language", sa.Column("languageid", sa.Integer, primary_key=True, nullable=True),
    sa.Column("name", sa.String(50), unique=True))


def downgrade():
    op.drop_table("dbo.Language")
