"""empty message

Revision ID: df8acde46fbb
Revises: 6d0fb511f9c3
Create Date: 2021-03-27 16:50:26.558190

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df8acde46fbb'
down_revision = '6d0fb511f9c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('rdatetime', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'rdatetime')
    # ### end Alembic commands ###
