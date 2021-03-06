from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager, login_required, current_user
from flask_socketio import SocketIO
from dotenv import load_dotenv
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY") 
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    

    with app.app_context():
        db.init_app(app)

    socketio = SocketIO(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from restaurant_webapp.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from restaurant_webapp.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from restaurant_webapp.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app