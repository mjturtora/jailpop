from flask import render_template, flash, redirect
from app import app
from .forms import InputForm

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           title='Home')

@app.route('/input', methods=['GET', 'POST'])
def input():
    form = InputForm()
    return render_template('input.html',
                           title='Input Name',
                           form=form)