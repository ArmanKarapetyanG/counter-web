from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError

##WTForm
class CharCounter(FlaskForm):
    def validation_on_spaces(form, field):
        if ' ' in field.data:
            raise ValidationError('Please type a WORD not a sentences (no-spaces after word)')

    word = StringField("Input", validators=[DataRequired(), validation_on_spaces])
    submit = SubmitField("Submit")