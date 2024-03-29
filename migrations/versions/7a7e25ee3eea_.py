"""empty message

Revision ID: 7a7e25ee3eea
Revises: 707bcb2ca0dc
Create Date: 2022-09-29 14:46:31.210763

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a7e25ee3eea'
down_revision = '707bcb2ca0dc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('base_workout', sa.Column('template_id', sa.Integer(), nullable=True))
    op.alter_column('base_workout', 'template_name',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=True)
    op.drop_constraint('base_workout_template_name_fkey', 'base_workout', type_='foreignkey')
    op.create_foreign_key(None, 'base_workout', 'template', ['template_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'base_workout', type_='foreignkey')
    op.create_foreign_key('base_workout_template_name_fkey', 'base_workout', 'template', ['template_name'], ['id'])
    op.alter_column('base_workout', 'template_name',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.drop_column('base_workout', 'template_id')
    # ### end Alembic commands ###
