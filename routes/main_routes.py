from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        # Redirect admin to admin dashboard
        if current_user.is_admin():
            return redirect(url_for('admin.admin_dashboard'))
        # Redirect regular users to their dashboard
        return redirect(url_for('auth.dashboard'))
    return render_template("index.html")

@main_bp.route("/user/welcome")
@login_required
def user_welcome():
    return render_template("welcome.html")
