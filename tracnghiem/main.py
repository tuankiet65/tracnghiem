from flask import render_template, request, session
from flask_babel import Babel
from flask_wtf.csrf import CSRFProtect

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from tracnghiem import app
from tracnghiem.admin import admin
from tracnghiem.authentication import load_session_token, authentication
from tracnghiem.database import Announcement, database
from tracnghiem.exam import exam
from tracnghiem.install import install
from tracnghiem.participate import participate
from tracnghiem.stats import generate_stats
from tracnghiem.utils.schools import get_schools
from tracnghiem.yourself import yourself

app.register_blueprint(admin)
app.register_blueprint(authentication)
app.register_blueprint(participate)
app.register_blueprint(exam)
app.register_blueprint(install)
app.register_blueprint(yourself)

csrf = CSRFProtect(app)
babel = Babel(app)

if app.config['ENV'] == "production":
    print("Production environment, enabling Sentry")
    sentry_sdk.init(
        dsn = app.config['SENTRY_BACKEND_DSN'],
        integrations = [FlaskIntegration()]
    )


@babel.localeselector
def get_locale():
    return app.config["LOCALE"]


@app.before_request
def _db_connect():
    database.connect()


@app.teardown_request
def _db_close(exc):
    if not database.is_closed():
        database.close()


@app.before_request
def clear_redirect_uri():
    if ((request.blueprint != "authentication") or (request.endpoint == "authentication.logout")) and (
                request.endpoint != "static"):
        try:
            del session['redirect_uri']
        except KeyError:
            pass


app.before_request(load_session_token)


@app.route("/")
def index():
    announcements = (Announcement
                     .select()
                     .order_by(-Announcement.time))
    stats = generate_stats()
    schools = get_schools()
    return render_template("index.html", announcements = announcements, stats = stats, schools = schools)


@app.route("/rules")
def rules():
    return render_template("rules.html")
