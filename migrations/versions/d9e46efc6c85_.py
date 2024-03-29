"""empty message

Revision ID: d9e46efc6c85
Revises: eaa58bd28cc6
Create Date: 2022-10-07 13:55:50.263447

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9e46efc6c85'
down_revision = 'eaa58bd28cc6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('exercise', 'sets',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=True)
    op.alter_column('exercise', 'reps',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=True)
    op.alter_column('exercise', 'weight',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('exercise', 'weight',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.alter_column('exercise', 'reps',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.alter_column('exercise', 'sets',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    # ### end Alembic commands ###
