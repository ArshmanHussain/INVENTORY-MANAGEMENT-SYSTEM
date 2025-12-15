import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    # Use DATABASE_URL env var (e.g. mysql) or fall back to a local sqlite file for development
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'inventory.db')
    
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://username:password@localhost:3306/your_databasename"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

