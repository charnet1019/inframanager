from datetime import datetime

from sqlalchemy.orm import backref

from common.exts import db


class Asset(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='资产id')
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'))
    users = db.relationship('User', backref=backref('asset', uselist=False))

    env = db.Column(db.String(5), default='测试', nullable=False, comment='环境')
    hostname = db.Column(db.String(30), nullable=False, unique=True, comment='主机名')
    ip = db.Column(db.String(15), nullable=False, unique=True, comment='内网ip')
    public_ip = db.Column(db.String(15), unique=True, comment='外网ip')
    username = db.Column(db.String(15), default='root', nullable=False, comment='主机用户名')
    password = db.Column(db.String(345), nullable=False, comment='主机密码')
    port = db.Column(db.Integer, default=22, comment='端口')
    # protocol = db.Column(db.String(6), default='ssh', comment='连接协议')
    protocol = db.Column(db.Boolean, nullable=False, default=False, comment='协议 0:ssh 1:rdp 2:telnet 3:vnc')
    auth_type = db.Column(db.Boolean, nullable=False, default=False, comment='认证类型 0: 密码认证  1: 密钥认证')
    use = db.Column(db.String(255), comment='资产用途')
    vendor = db.Column(db.String(10), comment='制造商')
    model = db.Column(db.String(10), default='CVM', comment='资产型号')
    cpu_model = db.Column(db.String(30), comment='CPU型号')
    cpu_cores = db.Column(db.Integer, comment='CPU核数')
    sys_hdd = db.Column(db.Integer, default=50, comment='系统盘大小')
    data_hdd = db.Column(db.Integer, comment='数据盘大小')
    memory = db.Column(db.Integer, comment='内存大小')
    os_type = db.Column(db.String(12), default='CentOS', comment='系统类型')
    os_arch = db.Column(db.String(6), default='AMD64', comment='系统位数')
    sn = db.Column(db.String(20), comment='序列号')
    connectivity = db.Column(db.Boolean, default=False, comment='可连接性 0: 不可连接   1: 可连接')
    create_datetime = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    update_datetime = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    create_by = db.Column(db.String(16), comment='创建者')
    comment = db.Column(db.String(255), comment='备注')

    def __str__(self):
        return self.ip
