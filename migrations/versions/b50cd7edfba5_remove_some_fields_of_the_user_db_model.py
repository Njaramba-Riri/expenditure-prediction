"""Remove some fields of the user db model.

Revision ID: b50cd7edfba5
Revises: fe65518b32c8
Create Date: 2024-01-27 15:37:11.520413

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b50cd7edfba5'
down_revision = 'fe65518b32c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('about',
               existing_type=mysql.TEXT(),
               type_=sa.String(length=200),
               existing_nullable=True)
        batch_op.drop_index('company_email')
        batch_op.drop_column('tour_company')
        batch_op.drop_column('company_address')
        batch_op.drop_column('company_email')
        batch_op.drop_column('mobile')
        batch_op.drop_column('company_mobile')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('company_mobile', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('mobile', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('company_email', mysql.VARCHAR(length=64), nullable=True))
        batch_op.add_column(sa.Column('company_address', mysql.VARCHAR(length=100), nullable=True))
        batch_op.add_column(sa.Column('tour_company', mysql.VARCHAR(length=64), nullable=True))
        batch_op.create_index('company_email', ['company_email'], unique=False)
        batch_op.alter_column('about',
               existing_type=sa.String(length=200),
               type_=mysql.TEXT(),
               existing_nullable=True)

    # ### end Alembic commands ###