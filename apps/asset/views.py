from flask import Blueprint, session, render_template, redirect, request, url_for, make_response, jsonify

from apps.asset.models import Asset
from apps.user.models import User
from common.exts import db
from common.utils import encrypt, decrypt

asset_bp = Blueprint('asset', '__name__', url_prefix='/asset')


@asset_bp.route('/list', methods=['GET', 'POST'])
def index():
    uid = session.get('uid')
    if uid:
        user = User.query.get(uid)
        assets = Asset.query.all()
        return render_template('asset/index.html', user=user, assets=assets)

    return redirect(url_for('user.login'))


@asset_bp.route('/add', methods=['GET', 'POST'])
def add_asset():
    uid = session.get('uid', None)

    if uid is None:
        return redirect(url_for('user.login'))

    print('@@@@@@@@@@@@@@ request.form @@@@@@@@', request.headers)

    if request.method == 'POST':
        user = User.query.get(uid)
        username = user.username

        print('********* request.form ****', request.headers)
        env = request.form.get('env', 'test')
        hostname = request.form.get('hostname')
        ip = request.form.get('ip')
        if request.form.get('public_ip'):
            public_ip = request.form.get('public_ip')
        else:
            public_ip = None
        host_username = request.form.get('username')
        host_password = request.form.get('password')
        port = request.form.get('port')
        protocol = request.form.get('protocol', default=0, type=int)
        auth_type = request.form.get('auth_type', default=0, type=int)
        if request.form.get('use'):
            use = request.form.get('use')
        else:
            use = None
        if request.form.get('vendor'):
            vendor = request.form.get('vendor')
        else:
            vendor = None
        if request.form.get('model'):
            model = request.form.get('model')
        else:
            model = None
        if request.form.get('cpu_model'):
            cpu_model = request.form.get('cpu_model')
        else:
            cpu_model = None
        cpu_cores = request.form.get('cpu_cores', default=None, type=int)
        sys_hdd = request.form.get('sys_hdd', default=None, type=int)
        data_hdd = request.form.get('data_hdd', default=None, type=int)
        memory = request.form.get('memory', default=None, type=int)
        if request.form.get('os_type'):
            os_type = request.form.get('os_type')
        else:
            os_type = None
        if request.form.get('os_arch'):
            os_arch = request.form.get('os_arch')
        else:
            os_arch = None
        if request.form.get('sn'):
            sn = request.form.get('sn')
        else:
            sn = None
        if request.form.get('comment'):
            comment = request.form.get('comment')
        else:
            comment = None

        # 写入数据
        asset = Asset()
        asset.user_id = uid
        asset.env = env
        asset.hostname = hostname
        asset.ip = ip
        asset.public_ip = public_ip
        asset.username = host_username
        asset.password = encrypt(host_password)
        asset.port = port
        asset.protocol = int(protocol)
        asset.auth_type = auth_type
        asset.create_by = username
        asset.use = use
        asset.vendor = vendor
        asset.model = model
        asset.cpu_model = cpu_model
        asset.cpu_cores = cpu_cores
        asset.sys_hdd = sys_hdd
        asset.data_hdd = data_hdd
        asset.memory = memory
        asset.os_type = os_type
        asset.os_arch = os_arch
        asset.sn = sn
        asset.comment = comment

        db.session.add(asset)
        db.session.commit()

        assets = Asset.query.all()
        # return render_template('asset/index.html', user=user, assets=assets)
        return redirect(url_for('asset.index'))

    return render_template('asset/add.html')


@asset_bp.route('/edit', methods=['POST', 'GET'])
def edit():
    uid = session.get('uid', None)
    if uid is None:
        return redirect(url_for('user.login'))

    asset_id = request.args.get('asset_id')
    asset = Asset.query.get(asset_id)

    if request.method == 'POST':
        env = request.form.get('env')
        hostname = request.form.get('hostname')
        ip = request.form.get('ip')
        if request.form.get('public_ip'):
            public_ip = request.form.get('public_ip')
        else:
            public_ip = None
        port = request.form.get('port')
        username = request.form.get('username')
        password = request.form.get('password')
        auth_type = request.form.get('auth_type')
        if request.form.get('use'):
            use = request.form.get('use')
        else:
            use = None
        if request.form.get('cpu_model'):
            cpu_model = request.form.get('cpu_model')
        else:
            cpu_model = None
        cpu_cores = request.form.get('cpu_cores', default=None, type=int)
        memory = request.form.get('memory', default=None, type=int)
        sys_hdd = request.form.get('sys_hdd', default=None, type=int)
        data_hdd = request.form.get('data_hdd', default=None, type=int)
        if request.form.get('vendor'):
            vendor = request.form.get('vendor')
        else:
            vendor = None
        print('++++++++++', data_hdd)
        if request.form.get('comment'):
            comment = request.form.get('comment')
        else:
            comment = None
        if request.form.get('sn'):
            sn = request.form.get('sn')
        else:
            sn = None

        # update data
        asset_id = request.form.get('asset_id')
        asset = Asset.query.get(asset_id)
        asset.env = env
        asset.vendor = vendor
        asset.hostname = hostname
        asset.ip = ip
        asset.public_ip = public_ip
        asset.username = username
        asset.password = password
        asset.port = port
        asset.auth_type = int(auth_type)
        asset.use = use
        asset.cpu_model = cpu_model
        asset.cpu_cores = cpu_cores
        asset.memory = memory
        asset.sys_hdd = sys_hdd
        asset.data_hdd = data_hdd
        asset.comment = comment
        asset.sn = sn
        db.session.commit()
        return redirect(url_for('asset.index'))

    return render_template('asset/edit.html', asset=asset)


@asset_bp.route('/delete', methods=['GET', 'POST'])
def delete():
    uid = session.get('uid')

    if uid is None:
        return redirect(url_for('user.login'))

    asset_id = request.args.get('aid')
    asset = Asset.query.get(asset_id)

    if asset:
        db.session.delete(asset)
        db.session.commit()

        return redirect(url_for('asset.index'))


@asset_bp.route('/decrypt')
def decrypt_pwd():
    uid = session.get('uid')

    if uid is None:
        return redirect(url_for('user.login'))

    asset_id = request.args.get('aid')
    asset = Asset.query.get(asset_id)

    password = decrypt(asset.password)
    # print('++++++++++', password)

    # resp = make_response()
    return jsonify({'password': password})
    # return password
