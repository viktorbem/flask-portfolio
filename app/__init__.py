import gridfs
import os

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from pymongo import MongoClient

from app.blueprints.admin import admin
from app.blueprints.pages import pages
from app.blueprints.user import user

from app.models.user import User

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    # MongoDB initialization and configuration
    app.config['MONGODB_URI'] = os.environ.get('MONGODB_URI')
    app.db = MongoClient(app.config['MONGODB_URI']).get_default_database()
    app.fs = gridfs.GridFS(app.db)

    # LoginManager initialization and configuration
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'pages.index'

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_one_by_id(user_id)

    # Blueprints
    app.register_blueprint(pages)
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(user, url_prefix='/auth')

    return app
