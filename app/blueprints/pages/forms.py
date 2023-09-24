from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Email, DataRequired


class ContactForm(FlaskForm):
    email = StringField('Your email', validators=[Email(), DataRequired()])
    message = TextAreaField(
        'Your message',
        render_kw={'rows': 10},
        validators=[DataRequired()]
    )
    submit = SubmitField('Contact me')
