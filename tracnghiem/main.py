from flask import render_template
from raven.contrib.flask import Sentry
from flask_wtf.csrf import CSRFProtect
from flask_babel import Babel

from .database import Announcement
from .admin import admin
from .authentication import load_session_token, authentication
from .participate import participate
from .exam import exam
from .stats import generate_stats
from .install import install
from .yourself import yourself
from . import app

app.register_blueprint(admin)
app.register_blueprint(authentication)
app.register_blueprint(participate)
app.register_blueprint(exam)
app.register_blueprint(install)
app.register_blueprint(yourself)
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
