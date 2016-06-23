from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class InputForm(Form):
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    case_num = StringField('case_num', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

    def validate(self):
        if not Form.validate(self):
            print "not form validate"
            if self.first_name.data or \
                    self.last_name.data or \
                    self.case_num.data:
                print "Should return True"
                return True
        print "Should return False"

        return False