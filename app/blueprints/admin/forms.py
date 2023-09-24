import datetime

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed, FileSize
from wtforms import StringField, TextAreaField, HiddenField, SubmitField, BooleanField, DateField
from wtforms.validators import DataRequired


class NullableDateField(DateField):
    def process_formdata(self, valuelist):
        if not valuelist:
            return

        date_str = ' '.join(valuelist)

        if date_str == '':
            self.data = None
            return

        for date_format in self.strptime_format:
            try:
                self.data = datetime.datetime.strptime(date_str, date_format).date()
                return
            except ValueError:
                self.data = None

        raise (ValueError(self.gettext('Not a valid date value')))


class ExperienceForm(FlaskForm):
    date_from = DateField('Date From', validators=[DataRequired()])
    date_to = NullableDateField('Date To')
    company = StringField('Company', validators=[DataRequired()])
    title_cs = StringField('Title CS', validators=[DataRequired()])
    title_en = StringField('Title EN', validators=[DataRequired()])
    description_cs = TextAreaField(
        'Description CS',
        render_kw={'rows': 10, 'style': 'min-height:200px;'},
        validators=[DataRequired()]
    )
    description_en = TextAreaField(
        'Description EN',
        render_kw={'rows': 10, 'style': 'min-height:200px;'},
        validators=[DataRequired()]
    )
    submit = SubmitField('Save experience')


class ProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField(
        'Description',
        render_kw={'rows': 10, 'style': 'min-height:200px;'},
        validators=[DataRequired()]
    )
    github_link = StringField('GitHub Link')
    project_link = StringField('Project Link')
    visible_index = BooleanField('Visible on Index Page', default=False)
    submit = SubmitField('Save project')


class ProjectImageForm(FlaskForm):
    image = FileField(
        'Image',
        validators=[
            FileRequired(),
            FileAllowed(['jpg', 'png', 'JPG', 'PNG'], message='Only JPG and PNG images allowed.'),
            FileSize(max_size=1048576, message='Image size is to big. Maximal size allowed is 1 MB.')
        ]
    )
    submit = SubmitField('Save image')


class SkillForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    icons = TextAreaField(
        'Icons',
        render_kw={'rows': 5, 'style': 'min-height:100px;'},
        validators=[DataRequired()]
    )
    description = TextAreaField(
        'Description',
        render_kw={'rows': 10, 'style': 'min-height:200px;'},
        validators=[DataRequired()]
    )
    submit = SubmitField('Save skill')
