"""empty message

Revision ID: 6f6af73b317f
Revises: 6a01ef2bc911
Create Date: 2022-05-28 11:50:47.341563

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6f6af73b317f'
down_revision = '6a01ef2bc911'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('template',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('start_id', sa.Integer(), nullable=True),
    sa.Column('template_name', sa.String(), nullable=True),
    sa.Column('num_days', sa.Integer(), nullable=True),
    sa.Column('row_nums', sa.ARRAY(sa.Integer()), nullable=True),
    sa.Column('num_excs', sa.ARRAY(sa.Integer()), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('weights', sa.Column('template_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'weights', 'template', ['template_id'], ['id'])
    op.drop_column('weights', 'template_name')
    op.drop_column('weights', 'row_nums')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('weights', sa.Column('row_nums', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.add_column('weights', sa.Column('template_name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'weights', type_='foreignkey')
    op.drop_column('weights', 'template_id')
    op.drop_table('template')
    # ### end Alembic commands ###
