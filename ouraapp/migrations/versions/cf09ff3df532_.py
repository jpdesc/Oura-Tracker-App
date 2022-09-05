"""empty message

Revision ID: cf09ff3df532
Revises: 75762fdbb37b
Create Date: 2022-04-03 13:44:37.375368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf09ff3df532'
down_revision = '75762fdbb37b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('log',
    sa.Column('id', sa.Date(), nullable=False),
    sa.Column('focus', sa.Integer(), nullable=True),
    sa.Column('mood', sa.Integer(), nullable=True),
    sa.Column('energy', sa.Integer(), nullable=True),
    sa.Column('journal', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('day')
    op.drop_constraint(None, 'sleep', type_='foreignkey')
    op.drop_column('sleep', 'day_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sleep', sa.Column('day_id', sa.DATETIME(), nullable=True))
    op.create_foreign_key(None, 'sleep', 'day', ['day_id'], ['id'])
    op.create_table('day',
    sa.Column('id', sa.DATETIME(), nullable=False),
    sa.Column('focus', sa.INTEGER(), nullable=True),
    sa.Column('mood', sa.INTEGER(), nullable=True),
    sa.Column('energy', sa.INTEGER(), nullable=True),
    sa.Column('journal', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('log')
    # ### end Alembic commands ###