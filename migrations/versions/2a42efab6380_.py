"""empty message

Revision ID: 2a42efab6380
Revises: 747efaa21d63
Create Date: 2022-08-13 19:30:36.699111

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a42efab6380'
down_revision = '747efaa21d63'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Shows', schema=None) as batch_op:
        batch_op.add_column(sa.Column('venue_name', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('artist_name', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('artist_image_link', sa.String(), nullable=True))
        batch_op.drop_column('name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Shows', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.drop_column('artist_image_link')
        batch_op.drop_column('artist_name')
        batch_op.drop_column('venue_name')

    # ### end Alembic commands ###
