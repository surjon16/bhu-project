"""empty message

Revision ID: 50d243d20423
Revises: 4e4a06e65ef5
Create Date: 2021-05-14 01:52:40.135757

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50d243d20423'
down_revision = '4e4a06e65ef5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('inventory', sa.Column('item_code', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('inventory', 'item_code')
    # ### end Alembic commands ###
