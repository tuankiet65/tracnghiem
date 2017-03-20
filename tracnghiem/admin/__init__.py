from flask import Blueprint, g, session, redirect, url_for, request

from .authentication import get_user_from_token
from .routes import index

admin = Blueprint("admin", __name__,
                  template_folder = "templates",
                  url_prefix = "/admin")

from .authentication import login_page
from .routes import index
from .announcement import AnnouncementList
from .school import SchoolList
from .contest import ContestList
from .questions import QuestionList
from .question_set import QuestionSetList

admin.add_url_rule("/login", view_func = login_page, methods = ["GET", "POST"])
admin.add_url_rule("/", view_func = index)
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


@admin.route("/logout")
def logout():
    try:
        del session['admin_token']
    except KeyError:
        pass
    return redirect(url_for("admin.index"))
