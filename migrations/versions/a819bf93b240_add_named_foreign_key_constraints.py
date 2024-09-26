"""Add named foreign key constraints

Revision ID: a819bf93b240
Revises: 
Create Date: 2024-09-25 10:29:52.243818

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a819bf93b240'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_crop')
    with op.batch_alter_table('crop', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(),server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False))
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(),server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False))
        batch_op.drop_column('expected_harvest_date')
        batch_op.drop_column('crop_rotation_history')
        batch_op.drop_column('planting_date')

    with op.batch_alter_table('crop_management', schema=None) as batch_op:
        batch_op.add_column(sa.Column('crop_cycle_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('created_at', sa.DateTime(),server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False))
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(),server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False))
        #batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('fk_cropmanagement_crop_cycle_id', 'cropcycle', ['crop_cycle_id'], ['id'])
        batch_op.drop_column('crop_id')

    with op.batch_alter_table('financial_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('crop_cycle_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('created_at', sa.DateTime(),server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False))
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(),server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False))
        #batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('fk_financialdata_crop_cycle_id', 'cropcycle', ['crop_cycle_id'], ['id'])
        batch_op.drop_column('crop_id')

    with op.batch_alter_table('users1', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(),server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False))
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(),server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False))

    with op.batch_alter_table('yield_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('crop_cycle_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('harvest_dates', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('created_at', sa.DateTime(),server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False))
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(),server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False))
        #batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('fk_yielddata_crop_cycle_id', 'cropcycle', ['crop_cycle_id'], ['id'])
        batch_op.drop_column('post_harvest_loss')
        batch_op.drop_column('harvest_date')
        batch_op.drop_column('crop_id')
        batch_op.drop_column('factors_affecting_yield')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('yield_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('factors_affecting_yield', sa.TEXT(), nullable=True))
        batch_op.add_column(sa.Column('crop_id', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('harvest_date', sa.DATE(), nullable=True))
        batch_op.add_column(sa.Column('post_harvest_loss', sa.FLOAT(), nullable=True))
        #batch_op.drop_constraint('crop_id', type_='foreignkey')
        batch_op.create_foreign_key('fk_yielddata_crop_cycle_id', 'crop', ['crop_id'], ['id'])
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')
        batch_op.drop_column('harvest_dates')
        batch_op.drop_column('crop_cycle_id')

    with op.batch_alter_table('users1', schema=None) as batch_op:
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')

    with op.batch_alter_table('financial_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('crop_id', sa.INTEGER(), nullable=True))
        #batch_op.drop_constraint('crop_id', type_='foreignkey')
        batch_op.create_foreign_key('fk_financialdata_crop_cycle_id', 'crop', ['crop_id'], ['id'])
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')
        batch_op.drop_column('crop_cycle_id')

    with op.batch_alter_table('crop_management', schema=None) as batch_op:
        batch_op.add_column(sa.Column('crop_id', sa.INTEGER(), nullable=True))
        #batch_op.drop_constraint('crop_id', type_='foreignkey')
        batch_op.create_foreign_key('fk_cropmanagement_crop_cycle_id', 'crop', ['crop_id'], ['id'])
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')
        batch_op.drop_column('crop_cycle_id')

    with op.batch_alter_table('crop', schema=None) as batch_op:
        batch_op.add_column(sa.Column('planting_date', sa.DATE(), nullable=True))
        batch_op.add_column(sa.Column('crop_rotation_history', sa.TEXT(), nullable=True))
        batch_op.add_column(sa.Column('expected_harvest_date', sa.DATE(), nullable=True))
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')

    op.create_table('_alembic_tmp_crop',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), nullable=False),
    sa.Column('crop_variety', sa.VARCHAR(length=100), nullable=True),
    sa.Column('acreage', sa.FLOAT(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('created_at', sa.DATETIME(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.DATETIME(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users1.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
