from flask import Blueprint, render_template

error_views = Blueprint('error', __name__)

@error_views.app_errorhandler(404)
def not_found_error_404(error):
    return render_template('pages/error/error404.html')

@error_views.app_errorhandler(403)
def not_found_error_403(error):
    return render_template('pages/error/error403.html')