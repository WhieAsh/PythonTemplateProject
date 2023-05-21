"""Creating first tables

Revision ID: 04e53f6bf8ef
Revises: 
Create Date: 2023-04-02 23:43:48.455328

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04e53f6bf8ef'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('create_at', sa.TIMESTAMP(), nullable=True, server_default=sa.func.now()),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('short_description', sa.String(), nullable=True),
    sa.Column('long_bio', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username', name='unique_username')
    )
    op.create_table('liked_post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('create_at', sa.TIMESTAMP(), nullable=True, server_default=sa.func.now()),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='FK_USER_ID'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'post_id', name='unique_user_id_post_id')
    )
    op.create_index('user_id_idx', 'liked_post', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('user_id_idx', table_name='liked_post')
    op.drop_table('liked_post')
    op.drop_table('user')
    # ### end Alembic commands ###