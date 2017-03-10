from flask import Blueprint, g, render_template
from .database import Contest, Exam, Account
from .authentication import need_to_login

participate = Blueprint("participate", __name__, url_prefix = "/participate")

def get_contests():
    return Contest.select()

def get_exams(contest):
    return Exam.select().where(Exam.contest == contest)

@participate.route("/", methods = ["GET"], endpoint = "index")
@need_to_login()
def render_participate_page():
    contests = get_contests()
    contest_exam_map = {}
    for contest in contests:
        contest_exam_map[contest.id] = get_exams(contest)
    return render_template("participate.html", contests = contests, exams = contest_exam_map)