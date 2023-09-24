from bson import ObjectId
from flask import current_app


class Image:
    def __init__(self):
        pass

    @classmethod
    def create_one(cls, image_name, image_data):
        file_id = current_app.fs.put(image_data, filename=image_name)
        return file_id

    @classmethod
    def get_image_by_id(cls, image_id):
        # TODO: This should be refactored in database to single data type
        if len(image_id) == 24:
            image_id = ObjectId(image_id)

        return current_app.fs.get(image_id)

    @staticmethod
    def delete_one(image_id):
        # TODO: This should be refactored in database to single data type
        if len(image_id) == 24:
            image_id = ObjectId(image_id)

        return current_app.fs.delete(image_id)
