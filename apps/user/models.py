from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from common.exts import db


class User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='用户id')
    fullname = db.Column(db.String(20), nullable=False, comment='用户命名')
    username = db.Column(db.String(16), nullable=False, unique=True, comment='用户名')
    password = db.Column(db.String(102), nullable=False, comment='用户密码')
    create_datetime = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    update_datetime = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    avatar = db.Column(db.String(50), comment='用户头像')
    wechat = db.Column(db.String(15), comment='用户微信')
    phone = db.Column(db.String(11), comment='用户手机号')
    email = db.Column(db.String(30), comment='用户邮箱')
    is_active = db.Column(db.Boolean, default=False, nullable=False, comment='用户状态 0:禁用  1:启用')
    is_admin = db.Column(db.Boolean, default=False, nullable=False, comment='是否是管理员 0: 普通用户  1: 管理员')

    def __str__(self):
        return self.username

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password, password)
