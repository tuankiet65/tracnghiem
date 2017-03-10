from flask import render_template
from raven.contrib.flask import Sentry
from flask_wtf.csrf import CSRFProtect
from flask_babel import Babel

from .database import Announcement, create_all_tables
from .admin.database import create_all_tables as admin_create_all_tables
from .admin.database import AdminUser
from .admin import admin
from .authentication import load_session_token, authentication
from .participate import participate
from .exam import exam
from .stats import generate_stats
from . import app

app.register_blueprint(admin)
app.register_blueprint(authentication)
app.register_blueprint(participate)
app.register_blueprint(exam)
csrf = CSRFProtect(app)
babel = Babel(app)

if app.config['IS_PRODUCTION']:
    print("In production, enabling Sentry")
    sentry = Sentry(app, dsn = app.config['SENTRY_BACKEND_DSN'])


@babel.localeselector
def get_locale():
    return "vi"


app.before_request(load_session_token)


@app.route("/")
def index():
    announcements = (Announcement
                     .select()
                     .order_by(-Announcement.time))
    stats = generate_stats()
    return render_template("index.html", announcements = announcements, stats = stats)

@app.route("/rules")
def rules():
    return render_template("rules.html")


if app.config["DEBUG"]:
    @app.route("/create_tables")
    def burn():
        create_all_tables()
        admin_create_all_tables()
        AdminUser.create(username = "tuankiet65", password = "123456")
        return 'ok'


@app.route("/login")
def login_page():
    return render_template("login.html")
