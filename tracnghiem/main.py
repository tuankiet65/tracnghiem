from flask import Flask, render_template, session

from .database import Announcement, create_all_tables
from .admin.database import create_all_tables as admin_create_all_tables
from .admin.database import AdminUser
from .admin import admin
from .common import gen_random_string

app = Flask(__name__)
app.register_blueprint(admin)

# TODO: Implement CSRF
app.config['WTF_CSRF_ENABLED'] = False

# TODO: better way to set secret key?
app.config['SECRET_KEY'] = gen_random_string()

@app.before_request
def load_user_info():
    try:
        # TODO: load user info
        pass
    except KeyError:
        pass

@app.route("/")
def index():
    announcements = (Announcement
                     .select()
                     .order_by(-Announcement.time))
    return render_template("index.html", announcements = announcements)

# TODO: This should only run when debug is True
@app.route("/create_tables")
def burn():
    create_all_tables()
    admin_create_all_tables()
    AdminUser.create(username = "tuankiet65", password = "123456")
    return 'ok'

@app.route("/login")
def login_page():
    return render_template("login.html")