from flask import render_template
from app import flask_app


@flask_app.route('/')
@flask_app.route('/index')
def index():
    user = {'username': 'Harshal'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)
