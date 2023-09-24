from bson import ObjectId
from flask import current_app
from flask_login import UserMixin, login_user


class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data.get('_id'))
        self.email = user_data.get('email')
        self.password = user_data.get('password')

    def get_id(self):
        return self.id

    def login(self):
        login_user(self)

    @classmethod
    def create_one(cls, email, password):
        user_data = {
            'email': email,
            'password': password,
        }

        new_user = current_app.db.users.insert_one(user_data)
        if new_user:
            user_data['_id'] = new_user.inserted_id
            return cls(user_data)

        return None

    @classmethod
    def get_one_by_email(cls, email):
        user_data = current_app.db.users.find_one({'email': email})
        if user_data:
            return cls(user_data)

        return None

    @classmethod
    def get_one_by_id(cls, user_id):
        user_data = current_app.db.users.find_one({'_id': ObjectId(user_id)})
        if user_data:
            return cls(user_data)

        return None
