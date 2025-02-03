from flask_wtf import FlaskForm
from flask_babel import _
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class MessageForm(FlaskForm):
    message = TextAreaField(_('Message'), validators=[DataRequired(), Length(min=0, max=140)])
    submit = SubmitField('<i data-acorn-icon="navigate-diagonal" class="icon" data-acorn-size="18"></i>')