import pymongo
from flask import Blueprint, current_app, render_template
from app.pages.models import Experience, Project, Skill

pages = Blueprint(
    'pages', __name__, template_folder='templates', static_folder='static', static_url_path='/pages/static'
)


@pages.route('/')
def index():
    skill_data = current_app.db.skill.find({'visible': {'$eq': True}})
    skills = [Skill(**skill) for skill in skill_data]

    project_data = current_app.db.project.find({'visible_index': {'$eq': True}}).sort('added', pymongo.DESCENDING)
    projects = [Project(**project) for project in project_data]

    return render_template('index.j2', skills=skills, projects=projects)


@pages.route('/portfolio')
def portfolio():
    project_data = current_app.db.project.find({'visible': {'$eq': True}}).sort('added', pymongo.DESCENDING)
    projects = [Project(**project) for project in project_data]

    return render_template('portfolio.j2', projects=projects)


@pages.route('/resume')
def resume():
    return render_template('resume.j2')


@pages.route('/resume/<string:lang>')
def resume_sheet(lang):
    experience_data = current_app.db.experience.find({}).sort('date_from', pymongo.DESCENDING)
    experiences = [Experience(**data) for data in experience_data]

    skill_data = current_app.db.skill.find({})
    skills = [Skill(**data) for data in skill_data]

    return render_template(
        f'resume/resume-{lang}.j2',
        experiences=experiences,
        skills=skills
    )


@pages.route('/contact')
def contact():
    return render_template('contact.j2')


@pages.route('/img/<string:image_id>')
def get_image(image_id):
    image = current_app.fs.get(image_id)
    return image
