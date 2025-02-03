from flask import Blueprint, jsonify, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500

@errors.app_errorhandler(413)
def error_413(error):
    return render_template('errors/500.html'), 413

# Custom error message when the rate limit is exceeded
@errors.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({"success":False, "error": "Too many requests, please try again later."}), 429