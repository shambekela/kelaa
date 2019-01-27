"""empty message

Revision ID: 1cf93299a7ec
Revises: f079e14e2d85
Create Date: 2019-01-25 22:39:10.899324

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1cf93299a7ec'
down_revision = 'f079e14e2d85'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'activity', 'user', ['user_uuid'], ['uuid'])
    op.create_foreign_key(None, 'activity', 'question', ['current_question'], ['key'])
    op.create_foreign_key(None, 'activity', 'channel', ['channel_id'], ['key'])
    op.create_foreign_key(None, 'channel', 'user', ['created_by'], ['uuid'])
    op.create_foreign_key(None, 'question', 'channel', ['channel_key'], ['key'], ondelete='CASCADE')
    op.create_foreign_key(None, 'question', 'user', ['created_by'], ['uuid'])
    op.create_foreign_key(None, 'tracker', 'user', ['user_uuid'], ['uuid'])
    op.create_foreign_key(None, 'user_detail', 'user', ['user_uuid'], ['uuid'], ondelete='CASCADE')
    op.create_foreign_key(None, 'user_detail', 'login_type', ['login_type'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_detail', type_='foreignkey')
    op.drop_constraint(None, 'user_detail', type_='foreignkey')
    op.drop_constraint(None, 'tracker', type_='foreignkey')
    op.drop_constraint(None, 'question', type_='foreignkey')
    op.drop_constraint(None, 'question', type_='foreignkey')
    op.drop_constraint(None, 'channel', type_='foreignkey')
    op.drop_constraint(None, 'activity', type_='foreignkey')
    op.drop_constraint(None, 'activity', type_='foreignkey')
    op.drop_constraint(None, 'activity', type_='foreignkey')
    # ### end Alembic commands ###