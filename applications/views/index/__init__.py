from applications.views.index.index import index_index

def init_indexViews(app):
    app.register_blueprint(index_index)