from flask import render_template, flash, redirect
from app import app
from .forms import InputForm

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = InputForm()
    if form.validate_on_submit():
        flash('Will search for First Name: %s, Last Name: %s, \
               Case Number: %s, remember_me= %s' %
              (form.first_name._value(), form.last_name._value(),
               form.case_num._value(), str(form.remember_me.data)))

        print form.first_name._value(),  form.last_name._value(), \
               form.case_num._value(), str(form.remember_me.data)
        # Call search from here.

        return redirect('/index')

    return render_template('index.html',
                           title='When Is My Court Date',
                           form=form)
