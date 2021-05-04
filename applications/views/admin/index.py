from io import BytesIO
from flask import Blueprint, render_template, jsonify, request, session, make_response
from flask_login import login_user, login_required, logout_user, current_user
from applications.models.admin import User
from applications.service.menuTreeYaml import make_tree
from flask_marshmallow import Marshmallow
from applications.service.route_auth import check_auth
import re
import platform
import psutil
from datetime import datetime

admin_index = Blueprint('adminIndex', __name__, url_prefix='/admin')

ma = Marshmallow()


# ----------------------------------------------------------
# -------------------------  home page --------------------------
# ----------------------------------------------------------

@admin_index.route('/')
@login_required
def index():
    if not current_user.is_authenticated:
        return render_template('admin/login.html')
    username = current_user.username
    return render_template('admin/index.html', username=username)


# ==========================================================
#                          login
# ==========================================================


@admin_index.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            res = {"msg": "username or password is required", "code": 0}
            return jsonify(res)

        user = User.query.filter_by(username=username).first()
        if user is None:
            res = {"msg": "user not fount", "code": 0}
            return jsonify(res)
        if user.status is 0:
            res = {"msg": "user is locked", "code": 0}
            return jsonify(res)

        if username == user.username and user.validate_password(password):
            login_user(user)
            res = {"msg": "login sucess", "code": 1}
            return jsonify(res)

        res = {"msg": "username or password error", "code": 0}
        return jsonify(res)

    return render_template('admin/login.html')


# ==========================================================
#                        logout
# ==========================================================


@admin_index.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    res = {"msg": "注销成功", "code": 200}
    return jsonify(res)


# ==========================================================
#                               menu
# ==========================================================


@admin_index.route('/menu')
@login_required
def menu():
    menu_yaml = admin_index.root_path + "/../../config/menu/*.yaml"
    res = make_tree(menu_yaml)
    return jsonify(res)


# ----------------------------------------------------------
# -------------------------  home page -----------------------
# ----------------------------------------------------------


@admin_index.route('/welcome')
@login_required
def welcome():
    # host name
    hostname = platform.node()
    # operation system version
    system_version = platform.platform()
    # python version
    python_version = platform.python_version()
    # Physical cpu core count
    cpu_Physical_count = psutil.cpu_count(logical=False)
    # logical cpu core count
    cpu_logical_count = psutil.cpu_count()
    # cups percent
    cpus_percent = psutil.cpu_percent(interval=0.1)
    # memory information
    memory_information = psutil.virtual_memory()
    # memory used
    memory_usage = memory_information.percent
    memory_used = str(round(memory_information.used / 1024 / 1024))
    memory_total = str(round(memory_information.total / 1024 / 1024))
    memory_free = str(round(memory_information.free / 1024 / 1024))
    # disk information
    disk_partitions = psutil.disk_partitions()
    disk_partitions_list = []

    for i in disk_partitions:
        a = psutil.disk_usage(i.device)
        disk_partitions_dict = {
            'device': i.device,
            'fstype': i.fstype,
            'total': str(round(a.total/ 1024 / 1024)),
            'used': str(round(a.used/ 1024 / 1024)),
            'free': str(round(a.free/ 1024 / 1024)),
            'percent': a.percent
        }
        disk_partitions_list.append(disk_partitions_dict)

    # 开机时间
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    up_time = datetime.now() - boot_time
    up_time_list = re.split(r':|\,', str(up_time))
    # up_time_format=str(up_time)
    up_time_format = "{}:{}:{}:{}".format(up_time.days, up_time_list[0], up_time_list[1], up_time_list[2])

    return render_template('admin/monitor.html',
                           hostname=hostname,
                           system_version=system_version,
                           python_version=python_version,
                           cpu_logical_count=cpu_logical_count,
                           cpu_Physical_count=cpu_Physical_count,
                           cpus_percent=cpus_percent,
                           memory_usage=memory_usage,
                           memory_used=memory_used,
                           memory_total=memory_total,
                           memory_free=memory_free,
                           boot_time=boot_time,
                           up_time_format=up_time_format,
                           disk_partitions_list=disk_partitions_list
                           )
