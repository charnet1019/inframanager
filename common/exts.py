from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()
bootstrap = Bootstrap()
csrf = CSRFProtect()

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    from apps.user.models import User
    user = User.query.get(user_id)

    return user


login_manager.login_view = 'login'
