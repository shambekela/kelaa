"""empty message

Revision ID: de3674cf5d98
Revises: 
Create Date: 2019-01-21 19:56:20.662105

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de3674cf5d98'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.Integer(), nullable=True),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('date_joined', sa.DateTime(), nullable=False),
    sa.Column('avatar', sa.String(length=200), nullable=True),
    sa.Column('tokens', sa.Text(), nullable=True),
    sa.Column('num_of_logins', sa.Integer(), nullable=True),
    sa.Column('receiveEmail', sa.Boolean(), nullable=True),
    sa.Column('password_hash', sa.String(length=255), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.Column('login_type', sa.Integer(), nullable=False),
    sa.Column('profile_type', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_user_uuid'), 'user', ['uuid'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_uuid'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
