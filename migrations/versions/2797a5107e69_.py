"""empty message

Revision ID: 2797a5107e69
Revises: 333585b7e4ef
Create Date: 2018-10-26 22:57:26.172150

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2797a5107e69'
down_revision = '333585b7e4ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password_hash', sa.String(length=255), nullable=False))
    op.drop_column('user', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    op.drop_column('user', 'password_hash')
    # ### end Alembic commands ###
