from flask import Flask
from flask_uploads import configure_uploads, patch_request_class
from applications.config import database, common
from applications.service.upload import files
from applications.service.deBug import OpenDug
from applications.views import init_view
from applications.models import db
from applications.service.login import init_flask_login
from applications.views.admin.error import init_error

def create_app():
    app = Flask(__name__)
    # regist router
    init_view(app)
    # regist error page
    init_error(app)
    # import database config
    app.config.from_object(database)
    # import common config
    app.config.from_object(common)
    # sqlalchemy init
    db.init_app(app)
    # flask_login init
    init_flask_login(app)
    # config file upload
    configure_uploads(app, files)
    patch_request_class(app)
    # debug toolbar
    OpenDug(app)

    return app

app = create_app()