import pymongo
from flask import Blueprint, current_app, render_template

from app.models import Experience, Project, Skill


pages = Blueprint(
    'pages', __name__, template_folder='templates', static_folder='static'
)


@pages.route('/')
def index():
    skill_data = current_app.db.skill.find({})
    skills = [Skill(**skill) for skill in skill_data]

    project_data = current_app.db.project.find({'visible_index': {'$eq': True}}).sort('added', pymongo.DESCENDING)
    projects = [Project(**project) for project in project_data]
    
    return render_template('index.html', skills=skills, projects=projects)


@pages.route('/portfolio')
def portfolio():
    project_data = current_app.db.project.find({'visible': {'$eq': True}}).sort('added', pymongo.DESCENDING)
    projects = [Project(**project) for project in project_data]

    return render_template('portfolio.html', projects=projects)


@pages.route('/resume')
def resume():
    return render_template('resume.html')


@pages.route('/resume/<string:lang>')
def resume_sheet(lang):
    experience_data = current_app.db.experience.find({}).sort('date_from', pymongo.DESCENDING)
    experiences = [Experience(**data) for data in experience_data]

    skill_data = current_app.db.skill.find({})
    skills = [Skill(**data) for data in skill_data]

    return render_template(
        f'resume/resume-{lang}.html',
        experiences=experiences,
        skills=skills
    )


@pages.route('/contact')
def contact():
    return render_template('contact.html')


@pages.route('/img/<string:image_id>')
def get_image(image_id):
    image = current_app.fs.get(image_id)
    return image