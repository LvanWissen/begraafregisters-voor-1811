from flask import render_template
from app import app
from flask import render_template, redirect


@app.route('/login', methods=['GET', 'POST'])
def login():

    return "test"
