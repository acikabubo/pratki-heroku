"""empty message

Revision ID: c2627b5abb77
Revises: a9bd02536f0c
Create Date: 2018-10-26 22:43:11.912063

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2627b5abb77'
down_revision = 'a9bd02536f0c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('first_name', sa.String(length=64), nullable=False))
    op.add_column('user', sa.Column('last_name', sa.String(length=64), nullable=False))
    op.add_column('user', sa.Column('password', sa.String(length=255), nullable=False))
    op.add_column('user', sa.Column('username', sa.String(length=64), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'username')
    op.drop_column('user', 'password')
    op.drop_column('user', 'last_name')
    op.drop_column('user', 'first_name')
    # ### end Alembic commands ###