from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import current_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash

from apps.forms import LoginForm
from apps.user.models import User

user_bp = Blueprint('user', '__name__', template_folder='templates', static_folder='static')


@user_bp.route('/')
def index():
    return redirect(url_for('user.login'))


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    uid = session.get('uid', None)
    if uid:
        return redirect(url_for('asset.index'))

    user = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('用户名密码不能为空', 'warning')
            return redirect(url_for('user.login'))

        user = User.query.first()
        if user:
            if username == user.username and check_password_hash(user.password, password):
                flash('Welcome back.', 'info')
                session['uid'] = user.id
                return redirect(url_for('asset.index'))

            flash('Invalid username or password.', 'warning')
            return redirect(url_for('user.login'))
        else:
            flash('No account.', 'warning')
            return redirect(url_for('user.login'))

    return render_template('user/login.html', user=user)
    # return render_template('base.html')


@user_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('user.login'))
