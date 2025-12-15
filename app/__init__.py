from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Import blueprints here to avoid circular imports (blueprints import `app`/`db`)
    from app.auth import auth
    from app.inventory import inventory

    app.register_blueprint(auth)
    app.register_blueprint(inventory)

    return app

