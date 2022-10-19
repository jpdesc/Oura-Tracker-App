"""empty message

Revision ID: bfd7738c62d5
Revises: 55c93ddc63af
Create Date: 2022-10-18 12:57:48.526288

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'bfd7738c62d5'
down_revision = '55c93ddc63af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'day', ['id'])
    op.create_unique_constraint(None, 'events', ['id'])
    op.add_column('log', sa.Column('day_id', sa.Integer(), nullable=True))
    op.create_unique_constraint(None, 'log', ['id'])
    op.add_column('readiness', sa.Column('day_id', sa.Integer(), nullable=True))
    op.create_unique_constraint(None, 'readiness', ['id'])
    op.add_column('sleep', sa.Column('day_id', sa.Integer(), nullable=True))
    op.create_unique_constraint(None, 'sleep', ['id'])
    op.add_column('tag', sa.Column('day_id', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('oura_access_token', sa.String(length=50), nullable=True))
    op.add_column('user', sa.Column('join_date', sa.Date(), nullable=True))
    op.add_column('weights', sa.Column('exercises', sa.ARRAY(sa.String()), nullable=True))
    op.drop_column('weights', 'exercises_old')
    op.add_column('workout', sa.Column('day_id', sa.Integer(), nullable=True))
    op.create_unique_constraint(None, 'workout', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'workout', type_='unique')
    op.drop_column('workout', 'day_id')
    op.add_column('weights', sa.Column('exercises_old', postgresql.ARRAY(sa.VARCHAR()), autoincrement=False, nullable=True))
    op.drop_column('weights', 'exercises')
    op.drop_column('user', 'join_date')
    op.drop_column('user', 'oura_access_token')
    op.drop_column('tag', 'day_id')
    op.drop_constraint(None, 'sleep', type_='unique')
    op.drop_column('sleep', 'day_id')
    op.drop_constraint(None, 'readiness', type_='unique')
    op.drop_column('readiness', 'day_id')
    op.drop_constraint(None, 'log', type_='unique')
    op.drop_column('log', 'day_id')
    op.drop_constraint(None, 'events', type_='unique')
    op.drop_constraint(None, 'day', type_='unique')
    # ### end Alembic commands ###