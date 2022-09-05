"""empty message

Revision ID: b7fce7a277a4
Revises: af0fb3a0d827
Create Date: 2022-04-14 21:37:41.384975

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7fce7a277a4'
down_revision = 'af0fb3a0d827'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('workout', sa.Column('soreness', sa.Integer(), nullable=True))
    op.add_column('workout', sa.Column('intensity', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('workout', 'intensity')
    op.drop_column('workout', 'soreness')
    # ### end Alembic commands ###