from flask import Blueprint, render_template

from app.models.experience import Experience
from app.models.image import Image
from app.models.project import Project
from app.models.skill import Skill

pages = Blueprint('pages', __name__, template_folder='templates')


@pages.route('/')
def index():
    skills = Skill.get_all()
    projects = [project for project in Project.get_all() if project.visible_index]

    return render_template('index.j2', skills=skills, projects=projects)


@pages.route('/portfolio')
def portfolio():
    projects = Project.get_all()

    return render_template('portfolio.j2', projects=projects)


@pages.route('/resume')
def resume():
    return render_template('resume.j2')


@pages.route('/resume/<string:lang>')
def resume_sheet(lang):
    experiences = Experience.get_all()
    skills = Skill.get_all()

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
    image = Image.get_image_by_id(image_id)
    return image
