import re
from datetime import datetime
import platform
import psutil
from flask import Blueprint, request, render_template, jsonify, current_app
from flask_marshmallow import Marshmallow

ma = Marshmallow()
admin_Monitor = Blueprint('adminMonitor', __name__, url_prefix='/admin/monitor')

# def StrOfSize(size):
#     def strofsize(integer, remainder, level):
#         if integer >= 1024:
#             remainder = integer % 1024
#             integer //= 1024
#             level += 1
#             return strofsize(integer, remainder, level)
#         else:
#             return integer, remainder, level
#
#     units = ['B', 'K', 'M', 'G', 'T', 'P']
#     integer, remainder, level = strofsize(size, 0, 0)
#     if level+1 > len(units):
#         level = -1
#     return ( '{}.{:>03d} {}'.format(integer, remainder, units[level]) )

@admin_Monitor.route('/')
def index():
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
