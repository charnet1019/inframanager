from flask import Blueprint, session, render_template, redirect, request, url_for, make_response, jsonify, send_file

from apps.asset.models import Asset
from apps.user.models import User
from common.exts import db
from common.utils import decrypt_msg, encrypt_msg, export_data

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
        asset.password = encrypt_msg(host_password)
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
        asset.password = encrypt_msg(password)
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
def decrypt():
    uid = session.get('uid')

    if uid is None:
        return redirect(url_for('user.login'))

    asset_id = request.args.get('aid')
    asset = Asset.query.get(asset_id)

    password = decrypt_msg(asset.password)
    # print('++++++++++', password)

    # resp = make_response()
    return jsonify({'password': password})
    # return password


@asset_bp.route('/encrypt')
def encrypt():
    uid = session.get('uid')

    if uid is None:
        return redirect(url_for('user.login'))

    asset_id = request.args.get('aid')
    asset = Asset.query.get(asset_id)

    enc_password = asset.password

    return jsonify({'password': enc_password})


@asset_bp.route('/download')
def download():
    uid = session.get('uid')

    if uid is None:
        return redirect(url_for('user.login'))

    asset_list = []
    column_list = ['环境', '主机名', '内网IP', '外网IP', '端口', '协议', '用户名', '密码', '认证类型', '资产用途',
                   '制造商', '资产型号', 'CPU型号', 'CPU核数', '系统盘大小', '数据盘大小',
                   '内存大小', '系统类型', '系统位数', '序列号', '可连接性', '创建时间', '更新时间', '备注']

    assets = Asset.query.all()

    for asset in assets:
        temp_list = list()

        temp_list.append(asset.env)
        temp_list.append(asset.hostname)
        temp_list.append(asset.ip)
        temp_list.append(asset.public_ip)
        temp_list.append(asset.port)
        temp_list.append(asset.protocol)
        temp_list.append(asset.username)
        temp_list.append(decrypt_msg(asset.password))
        temp_list.append(asset.auth_type)
        temp_list.append(asset.use)
        temp_list.append(asset.vendor)
        temp_list.append(asset.model)
        temp_list.append(asset.cpu_model)
        temp_list.append(asset.cpu_cores)
        temp_list.append(asset.sys_hdd)
        temp_list.append(asset.data_hdd)
        temp_list.append(asset.memory)
        temp_list.append(asset.os_type)
        temp_list.append(asset.os_arch)
        temp_list.append(asset.sn)
        temp_list.append(asset.connectivity)
        temp_list.append(asset.create_datetime)
        temp_list.append(asset.update_datetime)
        temp_list.append(asset.comment)

        asset_list.append(temp_list)

    resp = export_data(column_list, asset_list)

    # return send_file(resp, attachment_filename='hostinfo.xlsx', as_attachment=True)
    return resp
