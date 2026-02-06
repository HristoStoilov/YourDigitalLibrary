from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def index():
    return render_template("index.html")

@main_bp.route("/<username>/welcome")
@login_required
def user_welcome(username):
    if current_user.username != username:
        return redirect(url_for('main.user_welcome', username=current_user.username))
    return render_template("welcome.html")
