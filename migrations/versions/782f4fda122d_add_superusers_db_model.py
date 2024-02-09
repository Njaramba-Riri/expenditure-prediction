"""Add superusers db model

Revision ID: 782f4fda122d
Revises: 30150f310e66
Create Date: 2024-02-07 11:10:51.817275

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '782f4fda122d'
down_revision = '30150f310e66'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('superusers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('mobile', sa.String(length=20), nullable=False),
    sa.Column('agency', sa.String(length=255), nullable=False),
    sa.Column('agency_email', sa.String(length=100), nullable=False),
    sa.Column('agency_mobile', sa.String(), nullable=False),
    sa.Column('agency_address', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('mobile'),
    sa.UniqueConstraint('username')
    )
    with op.batch_alter_table('superusers', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_superusers_email'), ['email'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('superusers', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_superusers_email'))

    op.drop_table('superusers')
    # ### end Alembic commands ###
