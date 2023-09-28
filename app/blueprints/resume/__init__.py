from flask import Blueprint, render_template, Response, url_for
from weasyprint import HTML, CSS

from app.models.experience import Experience
from app.models.skill import Skill

resume = Blueprint('resume', __name__, template_folder='templates')


@resume.route('/<string:lang>')
def get_html(lang):
    experiences = Experience.get_all()
    skills = Skill.get_all()

    return render_template(
        f'views/resume-page.j2',
        experiences=experiences,
        skills=skills,
        lang=lang
    )


@resume.route('/pdf/<string:lang>')
def get_pdf(lang):
    html_content = HTML(url_for('resume.get_html', lang=lang, _external=True))
    pdf_data = html_content.write_pdf(
        stylesheets=[CSS(string='@page { size: A3; margin: 0; }')]
    )

    response = Response(pdf_data)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachement; filename=viktorbem-{lang}-resume.pdf'

    return response
