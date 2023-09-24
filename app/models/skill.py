from bson import ObjectId
from flask import current_app


class Skill:
    def __init__(self, skill_data):
        self.id = str(skill_data.get('_id'))
        self.title = skill_data.get('title')
        self.icons = [icon for icon in skill_data.get('icons')]
        self.description = skill_data.get('description')
        self.visible = skill_data.get('visible', True)

    @classmethod
    def create_one(cls, skill_data):
        new_skill = current_app.db.skill.insert_one(skill_data)
        if new_skill:
            skill_data['_id'] = new_skill.inserted_id
            return cls(skill_data)

        return None

    @classmethod
    def get_all(cls, visible_only=True):
        query = {'visible': {'$eq': True}} if visible_only else {}
        skill_data = current_app.db.skill.find(query)
        return [cls(data) for data in skill_data]

    @classmethod
    def get_one_by_id(cls, skill_id):
        skill_data = current_app.db.skill.find_one({'_id': ObjectId(skill_id)})
        if skill_data:
            return cls(skill_data)

        return None

    @staticmethod
    def update_one(skill_id, payload):
        return current_app.db.skill.update_one(
            {'_id': ObjectId(skill_id)},
            {'$set': payload}
        )
