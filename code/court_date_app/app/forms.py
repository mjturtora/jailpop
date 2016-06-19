from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class InputForm(Form):
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    case_num = StringField('case_num', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
