import pymongo
from bson import ObjectId
from flask import current_app


class Experience:
    def __init__(self, experience_data):
        self.id = str(experience_data.get('_id'))
        self.date_from = experience_data.get('date_from')
        self.date_to = experience_data.get('date_to')
        self.company = experience_data.get('company')
        self.title_cs = experience_data.get('title_cs')
        self.title_en = experience_data.get('title_en')
        self.description_cs = experience_data.get('description_cs')
        self.description_en = experience_data.get('description_en')
        self.visible = experience_data.get('visible', True)

    @classmethod
    def create_one(cls, experience_data):
        new_experience = current_app.db.experience.insert_one(experience_data)
        if new_experience:
            experience_data['_id'] = new_experience.inserted_id
            return cls(experience_data)

        return None

    @classmethod
    def get_all(cls, visible_only=True):
        query = {'visible': {'$eq': True}} if visible_only else {}
        experience_data = current_app.db.experience.find(query).sort('date_from', pymongo.DESCENDING)
        return [Experience(data) for data in experience_data]

    @classmethod
    def get_one_by_id(cls, experience_id):
        experience_data = current_app.db.experience.find_one({'_id': ObjectId(experience_id)})
        if experience_data:
            return cls(experience_data)

        return None

    @staticmethod
    def update_one(experience_id, payload):
        return current_app.db.experience.update_one(
            {'_id': ObjectId(experience_id)},
            {'$set': payload}
        )
