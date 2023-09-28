from flask import Blueprint, render_template, Response, url_for
import pdfkit

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
    pdf_data = pdfkit.from_url(
        url_for('resume.get_html', lang=lang, _external=True),
        output_path=False,
        options={'page-size': 'A4'}
    )

    response = Response(pdf_data)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=resume-{lang}.pdf'

    return response
