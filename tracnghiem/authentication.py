from flask import render_template, session, g, Blueprint, redirect, url_for, request
from wtforms import *
from flask_wtf import FlaskForm, RecaptchaField
from functools import wraps
import peewee

from .database import SessionToken, Account, School


####################
# Helper functions #
####################

def need_to_login():
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if g.user is None:
                session['redirect_uri'] = request.full_path
                return redirect(url_for("authentication.general", login_required = True))
            return f(*args, **kwargs)

        return wrapped

    return wrapper


def load_session_token():
    try:
        session_token = SessionToken.get(id = session['token'])
        user = session_token.account
    except (KeyError, SessionToken.DoesNotExist):
        user = None
        session_token = None
    g.session_token = session_token
    g.user = user


def get_account(username, password):
    try:
        account = Account.get(username = username)
    except Account.DoesNotExist:
        return None
    if account.password.check_password(password):
        return account
    else:
        return None


def login(account):
    if account is not None:
        session_token = SessionToken.create(account = account)
        session['token'] = session_token.id
        return True
    else:
        return False


def get_schools():
    query = School.select()
    return [(entry.id, entry.name) for entry in query]


def register(username, password, school, klass, name, *args, **kwargs):
    try:
        account = Account.create(username = username,
                                 password = password,
                                 school = school,
                                 klass = klass,
                                 name = name,
                                 facebook_id = 0,
                                 **kwargs)
        return account
    except peewee.IntegrityError:
        return None


def logout():
    try:
        del session['token']
    except KeyError:
        pass


###############
# Flask Views #
###############

authentication = Blueprint("authentication", __name__, url_prefix = "/auth")


@authentication.route("/", endpoint = "general")
def general_authentication_page():
    login_required = request.args.get("login_required", False)
    return render_template("authentication/general.html", schools = get_schools(), login_required = login_required)


class LoginForm(FlaskForm):
    username = StringField(validators = [validators.InputRequired()])
    password = PasswordField(validators = [validators.InputRequired()])


@authentication.route("/login", methods = ["GET", "POST"], endpoint = "login")
def login_view():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.data['username']
        password = form.data['password']
        if login(get_account(username, password)):
            try:
                return redirect(session['redirect_uri'])
            except KeyError:
                return redirect(url_for("index"))
        else:
            return render_template("authentication/login.html", login_failed = True, username = username)
    else:
        return render_template("authentication/login.html")


@authentication.route("/register", methods = ["GET", "POST"], endpoint = "register")
def register_page():
    class RegisterForm(FlaskForm):
        username = StringField("username", validators = [validators.DataRequired()])
        password = PasswordField("password", validators = [validators.DataRequired()])
        name = StringField("name", validators = [validators.DataRequired()])
        password_repeat = PasswordField("password_repeat", validators = [validators.DataRequired()])
        school = SelectField("school", validators = [validators.DataRequired()], choices = get_schools(), coerce = int)
        klass = StringField("klass", validators = [validators.DataRequired()])
        recaptcha = RecaptchaField()

    form = RegisterForm()
    if form.validate_on_submit():
        account = register(**form.data)
        if account is not None:
            login(account)
            try:
                return redirect(session['redirect_uri'])
            except KeyError:
                return redirect(url_for("index"))
        else:
            return render_template("authentication/register.html", schools = get_schools(), account_exists = True)
    else:
        return render_template("authentication/register.html", schools = get_schools(), registration_failed = True)


@authentication.route("/logout", methods = ["GET"])
def logout_page():
    logout()
    return redirect(url_for("index"))
