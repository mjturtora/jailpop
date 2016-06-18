from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class InputForm(Form):
    search_name = StringField('search_name', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)