from flask import Blueprint, g, session, redirect, url_for, request

from .authentication import get_user_from_token
from .routes import index

admin = Blueprint("admin", __name__,
                  template_folder = "templates",
                  url_prefix = "/admin")

from .authentication import login_page

admin.add_url_rule("/login", view_func = login_page, methods = ["GET", "POST"])

from .routes import index

admin.add_url_rule("/", view_func = index)

from .announcement import AnnouncementList

AnnouncementList.add_url_rule(admin)

from .school import SchoolList

SchoolList.add_url_rule(admin)

from .contest import ContestList

ContestList.add_url_rule(admin)

from .questions import QuestionList

QuestionList.add_url_rule(admin)

from .question_set import QuestionSetList

QuestionSetList.add_url_rule(admin)

@admin.before_request
def load_user_info():
    try:
        g.user = get_user_from_token(session['token'])
    except KeyError:
        g.user = None
    if g.user is None and request.path != url_for("admin.login_page"):
        # TODO: Enable this in production
        redirect(url_for("admin.login_page"))

