from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.blueprints.user.forms import LoginForm, RegisterForm
from app.models.user import User

user = Blueprint('user', __name__, template_folder='templates')


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        stored_user = User.get_one_by_email(email)
        if stored_user and check_password_hash(stored_user.password, password):
            stored_user.login()
            flash('Successfully logged in.', 'success')
            return redirect(url_for('admin.home'))
        else:
            flash('Unable to log in. Please try again.', 'danger')

    if len(form.errors) > 0:
        flash('Some of the form fields are not properly filled.', 'danger')

    return render_template('views/user-login.j2', form=form)


@user.route('/logout')
def logout():
    logout_user()
    flash('Successfully logged out.', 'success')

    return redirect(url_for('pages.index'))


# @user.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         email = form.email.data
#         password = form.password.data
#
#         stored_user = User.get_user_by_email(email)
#         if stored_user:
#             flash('Email already exists. Please log in instead.', 'danger')
#         else:
#             hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
#             new_user = User.create_user(email, hashed_password)
#             new_user.login()
#             flash('Your account has been created.', 'success')
#             return redirect(url_for('admin.home'))
#
#     if len(form.errors) > 0:
#         flash('Some of the form fields are not properly filled.', 'danger')
#
#     return render_template('views/user-register.j2', form=form)
