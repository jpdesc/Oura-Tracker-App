"""empty message

Revision ID: e22f1dccbb61
Revises: dc51f3b9cef1
Create Date: 2022-04-27 15:57:08.261184

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e22f1dccbb61'
down_revision = 'dc51f3b9cef1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('log', 'id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('log', 'focus',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=True)
    op.alter_column('log', 'mood',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=True)
    op.alter_column('log', 'energy',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=True)
    op.alter_column('log', 'journal',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               existing_nullable=True)
    op.alter_column('readiness', 'id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('readiness', 'readiness_score',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=True)
    op.alter_column('readiness', 'hrv_balance',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=True)
    op.alter_column('readiness', 'recovery_index',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=True)
    op.alter_column('readiness', 'resting_hr',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=True)
    op.alter_column('readiness', 'temperature',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=True)
    op.alter_column('sleep', 'id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('sleep', 'sleep_score',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=True)
    op.alter_column('sleep', 'total_rem_sleep',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               existing_nullable=True)
    op.alter_column('sleep', 'total_deep_sleep',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               existing_nullable=True)
    op.alter_column('sleep', 'sleep_efficiency',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=True)
    op.alter_column('sleep', 'restlessness',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=True)
    op.alter_column('sleep', 'rem_score',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=True)
    op.alter_column('sleep', 'deep_score',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=True)
    op.alter_column('sleep', 'total_sleep',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               existing_nullable=True)
    op.alter_column('weights', 'id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('weights', 'workout_id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=True)
    op.alter_column('weights', 'workout_week',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=True)
    op.alter_column('workout', 'id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('workout', 'type',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               existing_nullable=True)
    op.alter_column('workout', 'soreness',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=True)
    op.alter_column('workout', 'intensity',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=True)
    op.alter_column('workout', 'filename',
               existing_type=sa.TEXT(),
               type_=sa.String(length=50),
               existing_nullable=True)
    op.alter_column('workout', 'workout_log',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('workout', 'workout_log',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               existing_nullable=True)
    op.alter_column('workout', 'filename',
               existing_type=sa.String(length=50),
               type_=sa.TEXT(),
               existing_nullable=True)
    op.alter_column('workout', 'intensity',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=True)
    op.alter_column('workout', 'soreness',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=True)
    op.alter_column('workout', 'type',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               existing_nullable=True)
    op.alter_column('workout', 'id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('weights', 'workout_week',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=True)
    op.alter_column('weights', 'workout_id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=True)
    op.alter_column('weights', 'id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('sleep', 'total_sleep',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               existing_nullable=True)
    op.alter_column('sleep', 'deep_score',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=True)
    op.alter_column('sleep', 'rem_score',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=True)
    op.alter_column('sleep', 'restlessness',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=True)
    op.alter_column('sleep', 'sleep_efficiency',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=True)
    op.alter_column('sleep', 'total_deep_sleep',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               existing_nullable=True)
    op.alter_column('sleep', 'total_rem_sleep',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               existing_nullable=True)
    op.alter_column('sleep', 'sleep_score',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=True)
    op.alter_column('sleep', 'id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('readiness', 'temperature',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=True)
    op.alter_column('readiness', 'resting_hr',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=True)
    op.alter_column('readiness', 'recovery_index',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=True)
    op.alter_column('readiness', 'hrv_balance',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=True)
    op.alter_column('readiness', 'readiness_score',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=True)
    op.alter_column('readiness', 'id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('log', 'journal',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               existing_nullable=True)
    op.alter_column('log', 'energy',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=True)
    op.alter_column('log', 'mood',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=True)
    op.alter_column('log', 'focus',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=True)
    op.alter_column('log', 'id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False,
               autoincrement=True)
    # ### end Alembic commands ###
