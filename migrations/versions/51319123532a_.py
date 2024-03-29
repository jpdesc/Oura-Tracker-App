"""empty message

Revision ID: 51319123532a
Revises: 8b8c5339a748
Create Date: 2022-09-15 13:35:13.025123

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51319123532a'
down_revision = '8b8c5339a748'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=50),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'email',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=20),
               existing_nullable=False)
    # ### end Alembic commands ###
