"""empty message

Revision ID: 8def2538f8c7
Revises: d9ad9a916349
Create Date: 2022-08-11 18:00:20.525700

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8def2538f8c7'
down_revision = 'd9ad9a916349'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('city',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
        batch_op.alter_column('state',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
        batch_op.alter_column('phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
        batch_op.alter_column('genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)

    with op.batch_alter_table('Shows', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('start_time',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)

    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('city',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
        batch_op.alter_column('state',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
        batch_op.alter_column('address',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
        batch_op.alter_column('phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.alter_column('phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
        batch_op.alter_column('address',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
        batch_op.alter_column('state',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
        batch_op.alter_column('city',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=True)

    with op.batch_alter_table('Shows', schema=None) as batch_op:
        batch_op.alter_column('start_time',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=True)

    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.alter_column('genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
        batch_op.alter_column('phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
        batch_op.alter_column('state',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
        batch_op.alter_column('city',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=True)

    # ### end Alembic commands ###
