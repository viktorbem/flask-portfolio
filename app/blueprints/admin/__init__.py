from datetime import datetime
from io import BytesIO

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from werkzeug.utils import secure_filename

from app.blueprints.admin.forms import ExperienceForm, ProjectForm, ProjectImageForm, SkillForm

from app.models.experience import Experience
from app.models.image import Image
from app.models.project import Project
from app.models.skill import Skill

admin = Blueprint('admin', __name__, template_folder='templates')


def convert_date(date):
    return datetime.combine(date, datetime.min.time())


@admin.route('/')
@login_required
def home():
    return render_template('views/admin-home.j2')


@admin.route('/experience/add', methods=['GET', 'POST'])
@login_required
def add_experience():
    form = ExperienceForm()
    if form.validate_on_submit():
        payload = {
            'date_from': convert_date(form.date_from.data),
            'company': form.company.data,
            'title_cs': form.title_cs.data,
            'title_en': form.title_en.data,
            'description_cs': form.description_cs.data,
            'description_en': form.description_en.data,
            'visible': False
        }

        if form.date_to.data:
            payload['date_to'] = convert_date(form.date_to.date)

        new_experience = Experience.create_one(payload)
        if new_experience:
            flash('New experience has been added.', 'success')

        return redirect(url_for('admin.experiences'))

    return render_template('views/admin-edit-form.j2', form=form, title='Add experience')


@admin.route('/experience/edit/<string:object_id>', methods=['GET', 'POST'])
@login_required
def edit_experience(object_id):
    experience = Experience.get_one_by_id(object_id)
    if not experience:
        flash('Requested experience was not found', 'warning')
        return redirect(url_for('admin.experiences'))

    form = ExperienceForm()
    if form.validate_on_submit():
        payload = {
            'date_from': convert_date(form.date_from.data),
            'company': form.company.data,
            'title_cs': form.title_cs.data,
            'title_en': form.title_en.data,
            'description_cs': form.description_cs.data,
            'description_en': form.description_en.data,
        }

        if form.date_to.data:
            payload['date_to'] = convert_date(form.date_to.date)

        result = Experience.update_one(object_id, payload)
        if result.modified_count > 0:
            flash('The experience was successfully updated.', 'success')

        return redirect(url_for('admin.experiences'))

    form.date_from.data = experience.date_from
    form.date_to.data = experience.date_to
    form.company.data = experience.company
    form.title_cs.data = experience.title_cs
    form.title_en.data = experience.title_en
    form.description_cs.data = experience.description_cs
    form.description_en.data = experience.description_en

    return render_template('views/admin-edit-form.j2', form=form, title='Edit experience')


@admin.route('/experience/toggle/<string:object_id>', methods=['POST'])
@login_required
def toggle_experience(object_id):
    if request.method == 'POST':
        visible = request.form.get('visible') == 'True'
        result = Experience.update_one(object_id, {'visible': visible})
        if result.modified_count > 0:
            flash('The experience was successfully updated.', 'success')

    return redirect(url_for('admin.experiences'))


@admin.route('/experiences')
@login_required
def experiences():
    all_experiences = Experience.get_all(False)

    return render_template('views/admin-experiences.j2', experiences=all_experiences)


@admin.route('/project/add', methods=['GET', 'POST'])
@login_required
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        payload = {
            'title': form.title.data,
            'description': form.description.data,
            'visible_index': form.visible_index.data,
            'added': datetime.now(),
            'visible': False
        }

        if form.github_link.data:
            payload['github_link'] = form.github_link.data

        if form.project_link.data:
            payload['project_link'] = form.project_link.data

        new_project = Project.create_one(payload)
        if new_project:
            flash('New project has been added.', 'success')
            return redirect(url_for('admin.upload_project_image', object_id=new_project.id))

        flash('Something went wrong. Try again later.', 'danger')
        return redirect(url_for('admin.projects'))

    return render_template('views/admin-edit-form.j2', form=form, title='Add project')


@admin.route('/project/edit/<string:object_id>', methods=['GET', 'POST'])
@login_required
def edit_project(object_id):
    project = Project.get_one_by_id(object_id)
    if not project:
        flash('Requested project was not found', 'warning')
        return redirect(url_for('admin.projects'))

    form = ProjectForm()
    if form.validate_on_submit():
        payload = {
            'title': form.title.data,
            'description': form.description.data,
            'visible_index': form.visible_index.data,
        }

        if form.github_link.data:
            payload['github_link'] = form.github_link.data

        if form.project_link.data:
            payload['project_link'] = form.project_link.data

        result = Project.update_one(object_id, payload)
        if result.modified_count > 0:
            flash('The project was successfully updated.', 'success')

        return redirect(url_for('admin.projects'))

    form.title.data = project.title
    form.description.data = project.description
    form.github_link.data = project.github_link
    form.project_link.data = project.project_link
    form.visible_index.data = project.visible_index

    return render_template('views/admin-edit-form.j2', form=form, title='Edit project')


@admin.route('/project/upload-image/<string:object_id>', methods=['GET', 'POST'])
@login_required
def upload_project_image(object_id):
    form = ProjectImageForm()
    project = Project.get_one_by_id(object_id)
    if not project:
        flash('Requested project was not found', 'warning')
        return redirect(url_for('admin.projects'))

    if form.validate_on_submit():
        image_name = secure_filename(form.image.data.filename)
        image_data = BytesIO(form.image.data.read())

        image_id = Image.create_one(image_name, image_data)
        if image_id:
            Image.delete_one(project.image_id)
            Project.update_one(object_id, {'image_id': image_id})

        return redirect(url_for('admin.projects'))

    return render_template('views/admin-upload-form.j2', form=form, project=project)


@admin.route('/project/toggle/<string:object_id>', methods=['POST'])
@login_required
def toggle_project(object_id):
    if request.method == 'POST':
        visible = request.form.get('visible') == 'True'
        result = Project.update_one(object_id, {'visible': visible})
        if result.modified_count > 0:
            flash('The project was successfully updated.', 'success')

    return redirect(url_for('admin.projects'))


@admin.route('/projects')
@login_required
def projects():
    all_projects = Project.get_all(False)

    return render_template('views/admin-projects.j2', projects=all_projects)


@admin.route('/skill/add', methods=['GET', 'POST'])
@login_required
def add_skill():
    form = SkillForm()
    if form.validate_on_submit():
        new_skill = Skill.create_one({
            'title': form.title.data,
            'icons': [icon.strip() for icon in form.icons.data.split('\n')],
            'description': form.description.data,
            'visible': False
        })
        if new_skill:
            flash('New skill has been added.', 'success')

        return redirect(url_for('admin.skills'))

    return render_template('views/admin-edit-form.j2', form=form, title='Add skill')


@admin.route('/skill/edit/<string:object_id>', methods=['GET', 'POST'])
@login_required
def edit_skill(object_id):
    skill = Skill.get_one_by_id(object_id)
    if not skill:
        flash('Requested skill was not found', 'warning')
        return redirect(url_for('admin.skills'))

    form = SkillForm()
    if form.validate_on_submit():
        payload = {
            'title': form.title.data,
            'icons': [icon.strip() for icon in form.icons.data.split('\n')],
            'description': form.description.data
        }
        result = Skill.update_one(object_id, payload)
        if result.modified_count > 0:
            flash('The skill was successfully updated.', 'success')

        return redirect(url_for('admin.skills'))

    form.title.data = skill.title
    form.icons.data = '\n'.join(skill.icons)
    form.description.data = skill.description

    return render_template('views/admin-edit-form.j2', form=form, title='Edit skill')


@admin.route('/skill/toggle/<string:object_id>', methods=['POST'])
@login_required
def toggle_skill(object_id):
    if request.method == 'POST':
        visible = request.form.get('visible') == 'True'
        result = Skill.update_one(object_id, {'visible': visible})
        if result.modified_count > 0:
            flash('The skill was successfully updated.', 'success')

    return redirect(url_for('admin.skills'))


@admin.route('/skills')
@login_required
def skills():
    all_skills = Skill.get_all(False)

    return render_template('views/admin-skills.j2', skills=all_skills)
