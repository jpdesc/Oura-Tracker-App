"""empty message

Revision ID: 9af784419065
Revises: c29738f02d99
Create Date: 2023-01-23 19:40:16.005349

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9af784419065'
down_revision = 'c29738f02d99'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('workout', sa.Column('workout_log', sa.String(length=250), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('workout', 'workout_log')
    # ### end Alembic commands ###
