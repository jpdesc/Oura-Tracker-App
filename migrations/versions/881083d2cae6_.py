"""empty message

Revision ID: 881083d2cae6
Revises: 4163eb641f1e
Create Date: 2023-01-30 16:36:14.611480

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '881083d2cae6'
down_revision = '4163eb641f1e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('weights', sa.Column('og_workout_week', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('weights', 'og_workout_week')
    # ### end Alembic commands ###
