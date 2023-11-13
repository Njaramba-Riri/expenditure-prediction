"""initial migration

Revision ID: d7d8f463ce72
Revises: 
Create Date: 2023-09-22 08:39:04.862392

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd7d8f463ce72'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Countries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Alpha_Code', sa.String(length=4), nullable=True),
    sa.Column('Country', sa.String(length=100), nullable=True),
    sa.Column('Region', sa.String(length=20), nullable=True),
    sa.Column('Sub_Region', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('Alpha_Code')
    )
    op.create_table('Reference_Features',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('country', sa.String(length=255), nullable=True),
    sa.Column('age_group', sa.String(length=255), nullable=True),
    sa.Column('travel_with', sa.String(length=255), nullable=True),
    sa.Column('total_male', sa.Integer(), nullable=True),
    sa.Column('total_female', sa.Integer(), nullable=True),
    sa.Column('purpose', sa.String(length=255), nullable=True),
    sa.Column('main_activity', sa.String(length=255), nullable=True),
    sa.Column('info_source', sa.String(length=255), nullable=True),
    sa.Column('tour_arrangement', sa.String(length=30), nullable=True),
    sa.Column('package_transport_int', sa.String(length=10), nullable=True),
    sa.Column('package_accomodation', sa.String(length=10), nullable=True),
    sa.Column('package_food', sa.String(length=10), nullable=True),
    sa.Column('package_transport_tz', sa.String(length=10), nullable=True),
    sa.Column('package_sightseeing', sa.String(length=10), nullable=True),
    sa.Column('package_guided_tour', sa.String(length=10), nullable=True),
    sa.Column('package_insurance', sa.String(length=10), nullable=True),
    sa.Column('night_mainland', sa.Integer(), nullable=True),
    sa.Column('night_zanzibar', sa.Integer(), nullable=True),
    sa.Column('first_trip_tz', sa.String(length=10), nullable=True),
    sa.Column('actual_category', sa.String(length=30), nullable=True),
    sa.Column('predicted_category', sa.String(length=30), nullable=True),
    sa.Column('probability', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('location', sa.String(length=255), nullable=True),
    sa.Column('about', sa.Text(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('destinations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dest', sa.String(length=100), nullable=False),
    sa.Column('found', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Features',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('country', sa.String(length=255), nullable=True),
    sa.Column('age_group', sa.String(length=255), nullable=True),
    sa.Column('travel_with', sa.String(length=255), nullable=True),
    sa.Column('total_male', sa.Integer(), nullable=True),
    sa.Column('total_female', sa.Integer(), nullable=True),
    sa.Column('purpose', sa.String(length=255), nullable=True),
    sa.Column('main_activity', sa.String(length=255), nullable=True),
    sa.Column('info_source', sa.String(length=255), nullable=True),
    sa.Column('tour_arrangement', sa.String(length=30), nullable=True),
    sa.Column('package_transport_int', sa.String(length=10), nullable=True),
    sa.Column('package_accomodation', sa.String(length=10), nullable=True),
    sa.Column('package_food', sa.String(length=10), nullable=True),
    sa.Column('package_transport_tz', sa.String(length=10), nullable=True),
    sa.Column('package_sightseeing', sa.String(length=10), nullable=True),
    sa.Column('package_guided_tour', sa.String(length=10), nullable=True),
    sa.Column('package_insurance', sa.String(length=10), nullable=True),
    sa.Column('night_mainland', sa.Integer(), nullable=True),
    sa.Column('night_zanzibar', sa.Integer(), nullable=True),
    sa.Column('first_trip_tz', sa.String(length=10), nullable=True),
    sa.Column('predicted_category', sa.String(length=30), nullable=True),
    sa.Column('probability', sa.Float(), nullable=True),
    sa.Column('total_cost', sa.Integer(), nullable=True),
    sa.Column('cost_probability', sa.Float(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('role_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], )
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index('email_UNIQUE')
        batch_op.drop_index('username_UNIQUE')

    op.drop_table('users')
    op.drop_table('features')
    with op.batch_alter_table('countries', schema=None) as batch_op:
        batch_op.drop_index('Alpha_Code')

    op.drop_table('countries')
    op.drop_table('reference_features')
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.alter_column('email',
               existing_type=mysql.VARCHAR(length=64),
               nullable=True)
        batch_op.drop_index('email_UNIQUE')
        batch_op.create_index(batch_op.f('ix_admin_email'), ['email'], unique=True)

    with op.batch_alter_table('feedback', schema=None) as batch_op:
        batch_op.alter_column('feed',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
        batch_op.drop_constraint('feedback_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'Users', ['user_id'], ['id'])
        batch_op.create_foreign_key(None, 'Features', ['feature_id'], ['id'])

    with op.batch_alter_table('search', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.Integer(), nullable=False))
        batch_op.alter_column('user_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
        batch_op.create_foreign_key(None, 'Users', ['user_id'], ['id'])
        batch_op.drop_column('ID')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('search', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ID', mysql.INTEGER(), autoincrement=True, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.alter_column('user_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
        batch_op.drop_column('id')

    with op.batch_alter_table('feedback', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('feedback_ibfk_1', 'features', ['feature_id'], ['id'])
        batch_op.alter_column('feed',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)

    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_admin_email'))
        batch_op.create_index('email_UNIQUE', ['email'], unique=False)
        batch_op.alter_column('email',
               existing_type=mysql.VARCHAR(length=64),
               nullable=False)

    op.create_table('reference_features',
    sa.Column('id', mysql.VARCHAR(length=20), nullable=False),
    sa.Column('country', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('age_group', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('travel_with', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('total_male', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('total_female', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('purpose', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('main_activity', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('info_source', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('tour_arrangement', mysql.VARCHAR(length=30), nullable=True),
    sa.Column('package_transport_int', mysql.VARCHAR(length=10), nullable=True),
    sa.Column('package_accomodation', mysql.VARCHAR(length=10), nullable=True),
    sa.Column('package_food', mysql.VARCHAR(length=10), nullable=True),
    sa.Column('package_transport_tz', mysql.VARCHAR(length=10), nullable=True),
    sa.Column('package_sightseeing', mysql.VARCHAR(length=10), nullable=True),
    sa.Column('package_guided_tour', mysql.VARCHAR(length=10), nullable=True),
    sa.Column('package_insurance', mysql.VARCHAR(length=10), nullable=True),
    sa.Column('night_mainland', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('night_zanzibar', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('first_trip_tz', mysql.VARCHAR(length=10), nullable=True),
    sa.Column('actual_category', mysql.VARCHAR(length=30), nullable=True),
    sa.Column('predicted_category', mysql.VARCHAR(length=30), nullable=True),
    sa.Column('probability', mysql.FLOAT(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('countries',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('Alpha_Code', mysql.VARCHAR(length=4), nullable=True),
    sa.Column('Country', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('Region', mysql.VARCHAR(length=20), nullable=True),
    sa.Column('Sub_Region', mysql.VARCHAR(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    with op.batch_alter_table('countries', schema=None) as batch_op:
        batch_op.create_index('Alpha_Code', ['Alpha_Code'], unique=False)

    op.create_table('features',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('country', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('age_group', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('travel_with', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('total_male', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('total_female', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('purpose', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('main_activity', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('info_source', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('tour_arrangement', mysql.VARCHAR(length=30), nullable=True),
    sa.Column('package_transport_int', mysql.VARCHAR(length=10), nullable=True),
    sa.Column('package_accomodation', mysql.VARCHAR(length=10), nullable=True),
    sa.Column('package_food', mysql.VARCHAR(length=10), nullable=True),
    sa.Column('package_transport_tz', mysql.VARCHAR(length=10), nullable=True),
    sa.Column('package_sightseeing', mysql.VARCHAR(length=10), nullable=True),
    sa.Column('package_guided_tour', mysql.VARCHAR(length=10), nullable=True),
    sa.Column('package_insurance', mysql.VARCHAR(length=10), nullable=True),
    sa.Column('night_mainland', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('night_zanzibar', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('first_trip_tz', mysql.VARCHAR(length=10), nullable=True),
    sa.Column('predicted_category', mysql.VARCHAR(length=30), nullable=True),
    sa.Column('probability', mysql.FLOAT(), nullable=True),
    sa.Column('total_cost', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('cost_probability', mysql.VARCHAR(length=45), nullable=True),
    sa.Column('date', mysql.DATETIME(), nullable=True),
    sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('users',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('email', mysql.VARCHAR(length=64), nullable=False),
    sa.Column('username', mysql.VARCHAR(length=64), nullable=False),
    sa.Column('password', mysql.VARCHAR(length=100), nullable=False),
    sa.Column('location', mysql.VARCHAR(length=45), nullable=True),
    sa.Column('about', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('date_created', mysql.DATETIME(), nullable=False),
    sa.Column('last_seen', mysql.DATETIME(), nullable=True),
    sa.Column('confirmed', mysql.TINYINT(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index('username_UNIQUE', ['username'], unique=False)
        batch_op.create_index('email_UNIQUE', ['email'], unique=False)

    op.drop_table('role_users')
    op.drop_table('Features')
    op.drop_table('destinations')
    op.drop_table('Users')
    op.drop_table('Reference_Features')
    op.drop_table('Countries')
    # ### end Alembic commands ###