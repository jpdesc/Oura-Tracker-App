"""empty message

Revision ID: a26a4cfb9f3f
Revises: 5f204e2b605a
Create Date: 2022-04-09 16:18:55.469897

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a26a4cfb9f3f'
down_revision = '5f204e2b605a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('log', sa.Column('date', sa.Date(), nullable=True))
    op.add_column('sleep', sa.Column('date', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sleep', 'date')
    op.drop_column('log', 'date')
    # ### end Alembic commands ###