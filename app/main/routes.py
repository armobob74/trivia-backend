from flask import session, redirect, url_for, render_template, request
import pdb
from . import main

@main.route('/', methods=['GET', 'POST'])
def index():
    """This screen is only accessed by testers and never by users"""
    if request.method == 'POST':
        session['name'] = request.form['name']
    name = 'default name'
    if 'name' in session:
        name = session['name']

    return render_template('index.html', name = name)
