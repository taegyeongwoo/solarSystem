"""empty message

Revision ID: fcee47230388
Revises: 25a5773e1d33
Create Date: 2024-08-25 10:55:47.618031

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fcee47230388'
down_revision = '25a5773e1d33'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('property',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('property_id', sa.String(length=50), nullable=False),
    sa.Column('capacity_type', sa.String(length=50), nullable=False),
    sa.Column('current_status', sa.String(length=50), nullable=False),
    sa.Column('remaining_sections', sa.Integer(), nullable=False),
    sa.Column('land_contract', sa.String(length=50), nullable=False),
    sa.Column('observation_point', sa.String(length=50), nullable=False),
    sa.Column('annual_production', sa.Float(), nullable=False),
    sa.Column('power_sale_price', sa.Float(), nullable=False),
    sa.Column('annual_revenue', sa.Float(), nullable=False),
    sa.Column('remaining_revenue', sa.Float(), nullable=False),
    sa.Column('accumulated_revenue', sa.Float(), nullable=False),
    sa.Column('land_price', sa.Float(), nullable=False),
    sa.Column('system_price', sa.Float(), nullable=False),
    sa.Column('available_finance', sa.String(length=200), nullable=True),
    sa.Column('manufacturer', sa.String(length=100), nullable=True),
    sa.Column('system_capacity', sa.String(length=50), nullable=True),
    sa.Column('model_type', sa.String(length=50), nullable=True),
    sa.Column('max_output', sa.Float(), nullable=True),
    sa.Column('conversion_efficiency', sa.Float(), nullable=True),
    sa.Column('output_warranty', sa.Integer(), nullable=True),
    sa.Column('product_warranty', sa.Integer(), nullable=True),
    sa.Column('monitoring_system', sa.String(length=10), nullable=True),
    sa.Column('service_cost', sa.Float(), nullable=True),
    sa.Column('inverter_manufacturer', sa.String(length=100), nullable=True),
    sa.Column('inverter_type', sa.String(length=50), nullable=True),
    sa.Column('max_capacity', sa.Float(), nullable=True),
    sa.Column('inverter_efficiency', sa.Float(), nullable=True),
    sa.Column('inverter_warranty', sa.Integer(), nullable=True),
    sa.Column('inverter_monitoring_system', sa.String(length=10), nullable=True),
    sa.Column('inverter_service_cost', sa.Float(), nullable=True),
    sa.Column('structure_manufacturer', sa.String(length=100), nullable=True),
    sa.Column('structure_type', sa.String(length=50), nullable=True),
    sa.Column('construction_method', sa.String(length=50), nullable=True),
    sa.Column('incident_angle', sa.Float(), nullable=True),
    sa.Column('fixing_type', sa.String(length=50), nullable=True),
    sa.Column('structure_warranty', sa.Integer(), nullable=True),
    sa.Column('included_in_price', sa.String(length=500), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_property_user_id_user'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_property'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('property')
    # ### end Alembic commands ###
