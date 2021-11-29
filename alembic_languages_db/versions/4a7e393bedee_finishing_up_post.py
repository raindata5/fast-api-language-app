"""finishing up post

Revision ID: 4a7e393bedee
Revises: c2714a0d0ec8
Create Date: 2021-11-26 19:45:11.220672

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text

# revision identifiers, used by Alembic.
revision = '4a7e393bedee'
down_revision = 'c2714a0d0ec8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("Language", sa.Column("LanguageID", sa.Integer, primary_key=True, nullable=False),
    sa.Column("Name", sa.String(40), unique=True, nullable=False ),
    sa.Column("Origin", sa.String(40), nullable=False ),
    sa.Column("Description", sa.String(400), server_default="C\'est l\'une des meilleurs" ),
    sa.Column("created_at", sa.DATETIME(timezone=True), nullable= False, server_default=text('SYSUTCDATETIME()')),
    sa.Column("UserID", sa.Integer, nullable=False)
    )

    op.create_foreign_key(
            "fk_language_user", source_table="Language",
            referent_table = "User", local_cols=["UserID"], remote_cols = ["UserID"], ondelete="CASCADE")
   
    pass


def downgrade():
    op.drop_constraint("fk_language_user", table_name = "Language")
    op.drop_table("Language")
    pass
