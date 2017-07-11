from flask import Blueprint, g, session, redirect, url_for, request, render_template

from .announcement import AnnouncementList
from .authentication import login_page, get_user_from_token
from .contest import ContestList
from .question_set import QuestionSetList
from .questions import QuestionList
from .reports import reports
from .school import SchoolList
from .utils import login_as

admin = Blueprint("admin", __name__,
                  template_folder = "templates",
                  url_prefix = "/admin")

AnnouncementList.add_url_rule(admin)
SchoolList.add_url_rule(admin)
ContestList.add_url_rule(admin)
QuestionList.add_url_rule(admin)
QuestionSetList.add_url_rule(admin)


@admin.before_request
def load_user_info():
    try:
        g.user = get_user_from_token(session['admin_token'])
    except KeyError:
        g.user = None
    if g.user is None and request.path != url_for("admin.login_page"):
        return redirect(url_for("admin.login_page"))


@admin.route("/")
def index():
    return render_template("admin_index.html")


@admin.route("/logout")
def logout():
    try:
        del session['admin_token']
    except KeyError:
        pass
    return redirect(url_for("admin.index"))


admin.add_url_rule("/login", view_func = login_page, methods = ["GET", "POST"])
admin.add_url_rule("/reports", endpoint = "reports", view_func = reports, methods = ["GET", "POST"])
admin.add_url_rule("/utils/login_as", endpoint = "utils_login_as", view_func = login_as, methods = ["POST"])
