import gridfs
import os
import uuid
from flask import Flask
from dotenv import load_dotenv
from pymongo import MongoClient

from app.pages import pages

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config['MONGODB_URI'] = os.environ.get('MONGODB_URI')
    app.config['SECRET_KEY'] = uuid.uuid4().hex
    app.db = MongoClient(app.config['MONGODB_URI']).get_default_database()
    app.fs = gridfs.GridFS(app.db)
    app.register_blueprint(pages)

    return app