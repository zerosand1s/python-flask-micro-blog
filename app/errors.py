from flask import render_template
from app import flask_app, db


@flask_app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', title='Not Found'), 404


@flask_app.errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return render_template('500.html', title='Internal Server Error'), 500

