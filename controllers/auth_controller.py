
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from services.auth_service import (
    register_user,
    authenticate_user,
    get_user_dashboard_data,
    change_user_password
)

auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        success, result = register_user(username, email, password)
        if not success:
            flash(result)
            return redirect(url_for('auth.register'))

        flash('Registration successful!')
        return redirect(url_for('auth.login'))

    return render_template("register.html")


@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = authenticate_user(username, password)
        if user:
            if user.is_banned:
                flash('Your account has been banned. Please contact the administrator.')
                return redirect(url_for('auth.login'))

            login_user(user)

            # Redirect based on user role
            if user.is_admin():
                return redirect(url_for('admin.admin_dashboard'))
            return redirect(url_for('auth.dashboard'))

        flash('Invalid username or password')
    
    return render_template("login.html")


@auth_bp.route("/user/logout")
@login_required
def user_logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth_bp.route("/profile")
@login_required
def profile():
    return redirect(url_for('auth.user_profile'))


@auth_bp.route("/user/profile")
@login_required
def user_profile():
    return render_template("profile.html", user=current_user)


@auth_bp.route("/user/dashboard")
@login_required
def dashboard():
    stats = get_user_dashboard_data(current_user.id)

    return render_template("dashboard.html", 
                         user=current_user,
                         total_books_added=stats['total_books_added'],
                         total_reviews_written=stats['total_reviews_written'],
                         recent_books=stats['recent_books'],
                         recent_reviews=stats['recent_reviews'])


@auth_bp.route("/user/change-password", methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        success, message = change_user_password(
            current_user,
            current_password,
            new_password,
            confirm_password
        )

        if not success:
            flash(message)
            return redirect(url_for('auth.change_password'))

        flash(message)
        return redirect(url_for('auth.dashboard'))

    return render_template("change_password.html")
