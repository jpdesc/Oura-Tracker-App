"""empty message

Revision ID: 5f204e2b605a
Revises: 253a6619ae8d
Create Date: 2022-04-04 09:35:59.500883

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f204e2b605a'
down_revision = '253a6619ae8d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sleep', sa.Column('rem_score', sa.Integer(), nullable=True))
    op.add_column('sleep', sa.Column('deep_score', sa.Integer(), nullable=True))
    op.add_column('sleep', sa.Column('total_sleep', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sleep', 'total_sleep')
    op.drop_column('sleep', 'deep_score')
    op.drop_column('sleep', 'rem_score')
    # ### end Alembic commands ###