from flask import render_template, flash, redirect, url_for, session
from app import app
from app import models as mdl
from .forms import InputForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = InputForm()
    if form.validate_on_submit():
        session['last_name'] = form.last_name._value()
        flash('Will search for First Name: %s, Last Name: %s, \
               Case Number: %s, remember_me= %s' %
              (form.first_name._value(), form.last_name._value(),
               form.case_num._value(), str(form.remember_me.data)))

        return redirect(url_for('results'))

    return render_template('index.html',
                           title='When Is My Court Date',
                           form=form)

@app.route('/results')
def results():
    df = mdl.search_last(session['last_name'].replace(' ', ''))
    return render_template('results.html',
                           data=df.to_html(),
                           title='My Court Date Is',
                           )


# http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-unit-testing
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
