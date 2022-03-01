"""empty message

Revision ID: 43a3d6ff50cc
Revises: 
Create Date: 2022-02-17 04:04:56.452786

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '43a3d6ff50cc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False, comment='用户id'),
    sa.Column('fullname', sa.String(length=20), nullable=False, comment='用户命名'),
    sa.Column('username', sa.String(length=16), nullable=False, comment='用户名'),
    sa.Column('password', sa.String(length=80), nullable=False, comment='用户密码'),
    sa.Column('create_datetime', sa.DateTime(), nullable=True, comment='创建时间'),
    sa.Column('update_datetime', sa.DateTime(), nullable=True, comment='更新时间'),
    sa.Column('avatar', sa.String(length=50), nullable=True, comment='用户头像'),
    sa.Column('wechat', sa.String(length=15), nullable=True, comment='用户微信'),
    sa.Column('phone', sa.String(length=11), nullable=True, comment='用户手机号'),
    sa.Column('email', sa.String(length=30), nullable=True, comment='用户邮箱'),
    sa.Column('is_active', sa.Boolean(), nullable=False, comment='用户状态 0:禁用  1:启用'),
    sa.Column('is_admin', sa.Boolean(), nullable=False, comment='是否是管理员 0: 普通用户  1: 管理员'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('asset',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False, comment='资产id'),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('hostname', sa.String(length=30), nullable=True, comment='主机名'),
    sa.Column('ip', sa.String(length=15), nullable=True, comment='内网ip'),
    sa.Column('public_ip', sa.String(length=15), nullable=True, comment='外网ip'),
    sa.Column('port', sa.Integer(), nullable=True, comment='端口'),
    sa.Column('protocol', sa.String(length=6), nullable=True, comment='连接协议'),
    sa.Column('auth_type', sa.Boolean(), nullable=True, comment='认证类型 0: 密码认证  1: 密钥认证'),
    sa.Column('use', sa.String(length=255), nullable=True, comment='资产用途'),
    sa.Column('vendor', sa.String(length=10), nullable=True, comment='制造商'),
    sa.Column('model', sa.String(length=10), nullable=True, comment='资产型号'),
    sa.Column('cpu_model', sa.String(length=30), nullable=True, comment='CPU型号'),
    sa.Column('cpu_cores', sa.Integer(), nullable=True, comment='CPU核数'),
    sa.Column('sys_hdd', sa.Integer(), nullable=True, comment='系统盘大小'),
    sa.Column('data_hdd', sa.Integer(), nullable=True, comment='数据盘大小'),
    sa.Column('memory', sa.Integer(), nullable=True, comment='内存大小'),
    sa.Column('os_type', sa.String(length=12), nullable=True, comment='系统类型'),
    sa.Column('os_arch', sa.String(length=6), nullable=True, comment='系统位数'),
    sa.Column('sn', sa.String(length=20), nullable=True, comment='序列号'),
    sa.Column('connectivity', sa.Boolean(), nullable=True, comment='可连接性 0: 不可连接   1: 可连接'),
    sa.Column('create_datetime', sa.DateTime(), nullable=True, comment='创建时间'),
    sa.Column('update_datetime', sa.DateTime(), nullable=True, comment='更新时间'),
    sa.Column('create_by', sa.String(length=16), nullable=True, comment='创建者'),
    sa.Column('comment', sa.String(length=255), nullable=True, comment='备注'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('hostname'),
    sa.UniqueConstraint('ip'),
    sa.UniqueConstraint('public_ip')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('asset')
    op.drop_table('user')
    # ### end Alembic commands ###