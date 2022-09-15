"""empty message

Revision ID: a80044a087de
Revises: 8f2390895bb9
Create Date: 2022-09-13 12:36:01.670702

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a80044a087de'
down_revision = '8f2390895bb9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'username',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'username',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
