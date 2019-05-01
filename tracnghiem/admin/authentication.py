from flask import render_template, redirect, url_for, g, session
from flask_wtf import FlaskForm
from wtforms import *

from tracnghiem.admin.database import AdminUser, AdminSessionToken


def get_user_from_token(token: str):
    try:
        token_entry = AdminSessionToken.get(token = token)
    except AdminSessionToken.DoesNotExist:
        return None
    return token_entry.user


class LoginForm(FlaskForm):
    username = StringField("Username", [
        validators.InputRequired()
    ])
    password = PasswordField("password", [
        validators.InputRequired()
    ])


def create_login_token(user: AdminUser) -> str:
    entry = AdminSessionToken.create(user = user)
    return entry.token


def do_login(username: str, password: str) -> bool:
    try:
        user = AdminUser.get(username = username)
    except AdminUser.DoesNotExist:
        return False
    if not user.password.check_password(password):
        return False
    session['admin_token'] = create_login_token(user)
    return True


# route "/login"
# methods GET POST
def login_page():
    if g.user is not None:
        return redirect(url_for("admin.index"))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if do_login(login_form.data['username'], login_form.data['password']):
            return redirect(url_for("admin.index"))
        else:
            return render_template("admin_login.html", has_error = True)
    else:
        return render_template("admin_login.html", has_error = False)
