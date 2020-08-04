from frontend import app
from flask import render_template, redirect, url_for, session, request


@app.route('/', methods=['GET', 'POST'])
@app.route('/plot', methods=['GET', 'POST'])
def index():
    return render_template('show_plots.html')
