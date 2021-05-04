from applications.views.admin.index import admin_index
from applications.views.admin.user import admin_user
from applications.views.admin.file import admin_file
from applications.views.admin.newsIngester import admin_news_ingester
from applications.views.admin.monitor import admin_Monitor

def init_adminViews(app):

    app.register_blueprint(admin_index)
    app.register_blueprint(admin_user)
    app.register_blueprint(admin_file)
    app.register_blueprint(admin_Monitor)
    app.register_blueprint(admin_news_ingester)