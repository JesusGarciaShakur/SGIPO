from flask import Blueprint, render_template, redirect

admin_views = Blueprint('admin', __name__)

@admin_views.route('/')
def admin():
    return render_template('pages/admin.html')