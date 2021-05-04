# db config
DATABASE = 'applications/database/myweb.sqlite3'

DB_URI = "sqlite:///{db}".format(db=DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = True


