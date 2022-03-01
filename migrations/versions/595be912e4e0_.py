"""empty message

Revision ID: 595be912e4e0
Revises: ec596126e7c9
Create Date: 2022-02-25 16:05:05.785348

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '595be912e4e0'
down_revision = 'ec596126e7c9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('asset', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=mysql.VARCHAR(length=102),
               type_=sa.String(length=345),
               existing_comment='主机密码',
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('asset', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.String(length=345),
               type_=mysql.VARCHAR(length=102),
               existing_comment='主机密码',
               existing_nullable=False)

    # ### end Alembic commands ###