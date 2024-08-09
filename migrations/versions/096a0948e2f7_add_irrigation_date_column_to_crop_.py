"""Add irrigation_date column to crop_management

Revision ID: 096a0948e2f7
Revises: 8bfed1e49192
Create Date: 2024-08-07 14:07:58.601751

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '096a0948e2f7'
down_revision = '8bfed1e49192'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('crop_management', schema=None) as batch_op:
        batch_op.add_column(sa.Column('irrigation_date', sa.Date(), nullable=True))
        batch_op.alter_column('irrigation_amount',
               existing_type=sa.DATE(),
               type_=sa.Float(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('crop_management', schema=None) as batch_op:
        batch_op.alter_column('irrigation_amount',
               existing_type=sa.Float(),
               type_=sa.DATE(),
               existing_nullable=True)
        batch_op.drop_column('irrigation_date')

    # ### end Alembic commands ###