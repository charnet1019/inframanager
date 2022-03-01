from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, ValidationError, HiddenField, \
    BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional, URL


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 128)])
    remember = BooleanField('记住我')
    submit = SubmitField('登  录')


class AssetForm(FlaskForm):
    hostname = StringField('主机名', validators=[DataRequired(), Length(1, 20)])
    ip = StringField('内网ip', validators=[DataRequired(), Length(1, 15)])
    public_ip = StringField('公网ip', validators=[DataRequired(), Length(1, 15)])
    port = StringField('端口', default=22)
    protocol = StringField('协议', default='ssh')
