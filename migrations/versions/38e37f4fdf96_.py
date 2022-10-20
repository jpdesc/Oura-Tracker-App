"""empty message

Revision ID: 38e37f4fdf96
Revises: bfd7738c62d5
Create Date: 2022-10-20 11:19:05.592095

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38e37f4fdf96'
down_revision = 'bfd7738c62d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('day_id', sa.Integer(), nullable=True))
    op.add_column('events', sa.Column('title', sa.String(), nullable=True))
    op.drop_constraint('user_email_key', 'user', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('user_email_key', 'user', ['email'])
    op.drop_column('events', 'title')
    op.drop_column('events', 'day_id')
    # ### end Alembic commands ###
