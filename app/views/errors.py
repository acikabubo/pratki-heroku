from flask import render_template, make_response, jsonify
from app import app


@app.errorhandler(429)
def ratelimit_handler(e):
    return render_template('errors/too_many_requests.html', e=str(e)[4:])


@app.errorhandler(500)
def internal_server_error_handler(e):
    return render_template('errors/internal_server_error.html')
    