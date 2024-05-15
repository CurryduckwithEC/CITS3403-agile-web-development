"""Add join_date to User model

Revision ID: a08f036caed3
Revises: 89472fd72ba1
Create Date: 2024-05-15 09:09:11.493514

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a08f036caed3'
down_revision = '89472fd72ba1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('join_date', sa.DateTime(), nullable=True))
        batch_op.alter_column('hashedPassword',
               existing_type=sa.VARCHAR(length=30),
               type_=sa.String(length=128),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('hashedPassword',
               existing_type=sa.String(length=128),
               type_=sa.VARCHAR(length=30),
               existing_nullable=False)
        batch_op.drop_column('join_date')

    # ### end Alembic commands ###
