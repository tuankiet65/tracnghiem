from flask import render_template, request, g
from flask_babel import Babel
from flask_wtf.csrf import CSRFProtect
from raven.contrib.flask import Sentry

from . import app
from .admin import admin
from .authentication import load_session_token, authentication, get_schools
from .database import Announcement, database
from .exam import exam
from .install import install
from .participate import participate
from .stats import generate_stats
from .yourself import yourself

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


@app.before_request
def _db_connect():
    database.connect()


@app.teardown_request
def _db_close(exc):
    if not database.is_closed():
        database.close()


app.before_request(load_session_token)


@app.before_request
def determine_workaround():
    g.workaround = {}
    user_agent = request.user_agent
    if user_agent.platform in ("ipad", "iphone"):
        g.workaround['ios_select'] = True
    else:
        g.workaround['ios_select'] = False


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
