from flask import Blueprint, current_app, flash, redirect, render_template, url_for

from app.blueprints.pages.forms import ContactForm

from app.models.experience import Experience
from app.models.image import Image
from app.models.project import Project
from app.models.skill import Skill

pages = Blueprint('pages', __name__, template_folder='templates')


@pages.route('/')
def index():
    skills = Skill.get_all()
    projects = [project for project in Project.get_all() if project.visible_index]

    return render_template('views/index.j2', skills=skills, projects=projects)


@pages.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        email = form.email.data
        message = form.message.data

        response = current_app.webhook.send(text=f'*{email}*\n\n{message}')
        if response.status_code == 200:
            flash('Your message has been sent. I\'m going to reach you as soon as possible.', 'success')
            return redirect(url_for('pages.contact'))

        flash('Something went wrong. Please try again later.', 'danger')

    if len(form.errors) > 0:
        flash('Some form fields are not properly filled.', 'warning')

    return render_template('views/contact.j2', form=form)


@pages.route('/img/<string:image_id>')
def get_image(image_id):
    image = Image.get_image_by_id(image_id)
    return image


@pages.route('/portfolio')
def portfolio():
    projects = Project.get_all()

    return render_template('views/portfolio.j2', projects=projects)


@pages.route('/resume')
def resume():
    return render_template('views/resume.j2')

