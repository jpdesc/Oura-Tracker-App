"""empty message

Revision ID: 3758156ad41e
Revises: 0b082426d734
Create Date: 2022-09-29 08:27:16.603064

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3758156ad41e'
down_revision = '0b082426d734'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('weights', sa.Column('day_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('weights', 'day_id')
    # ### end Alembic commands ###
