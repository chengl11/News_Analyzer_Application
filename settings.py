class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:1997chengCHENG@127.0.0.1:3306/newsanalyzer"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

class DevelopmentConfig(Config):
    ENV = "development"

class ProductionConfig(Config):
    ENV = "production"
    DEBUG = False
