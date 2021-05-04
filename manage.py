from flask_script import Manager, Server

from main import app

manager = Manager(app)

manager.add_command('start', Server(port=8806, use_debugger=True))  # 创建启动命令


if __name__ == '__main__':
    manager.run()