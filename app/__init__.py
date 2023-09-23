import gridfs
import os

from dotenv import load_dotenv
from flask import Flask
from pymongo import MongoClient

from app.pages import pages

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    # MongoDB initialization and configuration
    app.config['MONGODB_URI'] = os.environ.get('MONGODB_URI')
    app.db = MongoClient(app.config['MONGODB_URI']).get_default_database()
    app.fs = gridfs.GridFS(app.db)

    # Blueprints
    app.register_blueprint(pages)

    return app
