import pymongo
from bson import ObjectId
from flask import current_app


class Project:
    def __init__(self, project_data):
        self.id = str(project_data.get('_id'))
        self.title = project_data.get('title')
        self.description = project_data.get('description')
        self.added = project_data.get('added')
        self.image_id = str(project_data.get('image_id'))
        self.github_link = project_data.get('github_link')
        self.project_link = project_data.get('project_link')
        self.visible = project_data.get('visible', True)
        self.visible_index = project_data.get('visible_index', False)

    @classmethod
    def create_one(cls, project_data):
        new_project = current_app.db.project.insert_one(project_data)
        if new_project:
            project_data['_id'] = new_project.inserted_id
            return cls(project_data)

        return None

    @classmethod
    def get_all(cls, visible_only=True):
        query = {'visible': {'$eq': True}} if visible_only else {}
        project_data = current_app.db.project.find(query).sort('added', pymongo.DESCENDING)

        return [cls(data) for data in project_data]

    @classmethod
    def get_one_by_id(cls, project_id):
        project_data = current_app.db.project.find_one({'_id': ObjectId(project_id)})
        if project_data:
            return cls(project_data)

        return None

    @staticmethod
    def update_one(project_id, payload):
        return current_app.db.project.update_one(
            {'_id': ObjectId(project_id)},
            {'$set': payload}
        )
