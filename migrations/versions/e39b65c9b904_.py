"""empty message

Revision ID: e39b65c9b904
Revises: 5adf8048cbfe
Create Date: 2022-04-25 22:49:47.759013

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e39b65c9b904'
down_revision = '5adf8048cbfe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('workout', 'workout_id')
    op.drop_column('workout', 'workout_week')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('workout', sa.Column('workout_week', sa.BIGINT(), autoincrement=False, nullable=True))
    op.add_column('workout', sa.Column('workout_id', sa.BIGINT(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
