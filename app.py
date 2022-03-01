from flask import Flask, request, render_template
from werkzeug.security import generate_password_hash

from apps import create_app
import click
from apps.user.models import User
from apps.asset.models import Asset
from common.exts import db

app = create_app()

# @app.cli.command()
# @click.option('--username', default='admin', help='Administrator username')
# @click.option('--password', default='Wimj@$1209', help='Administrator password')
# @click.option('--fullname', default='administrator', help='Administrator full name')
# @click.option('--is_active', default=True, help='is active by default')
# @click.option('--is_admin', default=True, help='is administrator by default')
# def createsuperuser(username, password, fullname='administrator', is_active=True, is_admin=True):
#     # def createsuperuser(username, password):
#     user = User.query.first()
#     if user:
#         click.echo('Updating user ...')
#         user.username = username
#         user.password = generate_password_hash(password)
#         user.fullname = fullname
#         user.is_active = is_active
#         user.is_admin = is_admin
#     else:
#         click.echo('Add user ...')
#         user = User()
#         user.username = username
#         user.password = generate_password_hash(password)
#         print(user.password)
#         user.fullname = fullname
#         user.is_active = is_active
#         user.is_admin = is_admin
#         db.session.add(user)
#
#     db.session.commit()
#     click.echo('Done.....')


if __name__ == '__main__':
    print(app.url_map)
    app.run(host='192.168.60.3')
