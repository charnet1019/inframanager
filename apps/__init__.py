from flask import Flask
from flask_migrate import Migrate

import settings
from apps.asset.views import asset_bp
from common.exts import db, bootstrap, csrf, login_manager
from apps.user.views import user_bp

bp_list = [user_bp, asset_bp]


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(settings)
    db.init_app(app)
    migrate = Migrate(app, db, render_as_batch=True, compare_type=True, compare_server_default=True)
    bootstrap.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    for bp in bp_list:
        app.register_blueprint(bp)

    return app
