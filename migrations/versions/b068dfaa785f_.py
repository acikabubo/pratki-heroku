"""empty message

Revision ID: b068dfaa785f
Revises: 2797a5107e69
Create Date: 2018-10-27 13:09:32.348730

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b068dfaa785f'
down_revision = '2797a5107e69'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('external_login', sa.Column('provider', sa.String(length=15), nullable=False))
    op.create_unique_constraint('unique_provider_user_id', 'external_login', ['provider', 'user_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('unique_provider_user_id', 'external_login', type_='unique')
    op.drop_column('external_login', 'provider')
    # ### end Alembic commands ###