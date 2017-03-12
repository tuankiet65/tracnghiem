from flask import Blueprint, g, render_template, json
from flask_wtf import FlaskForm
from wtforms import *

from .database import School, Contest, Exam
from .authentication import need_to_login, logout

yourself = Blueprint("yourself", __name__, url_prefix = "/yourself")


def get_contests():
    return Contest.select()


def get_exams(contest):
    return Exam.select().where((Exam.contest == contest) & (Exam.contestant == g.user))


def get_contest_exam_map(contests):
    contest_exam_map = {}
    for contest in contests:
        contest_exam_map[contest.id] = get_exams(contest)
    return contest_exam_map


def get_schools():
    query = School.select()
    return [(entry.id, entry.name) for entry in query]


@yourself.route("/", methods = ["GET"], endpoint = "index")
@need_to_login()
def yourself_view():
    contests = get_contests()
    return render_template("yourself.html",
                           schools = get_schools(),
                           contests = contests,
                           exams = get_contest_exam_map(contests))


@yourself.route("/change_password", methods = ["POST"])
@need_to_login()
def change_password():
    class ChangePasswordForm(FlaskForm):
        old_password = PasswordField(validators = [validators.DataRequired()])
        new_password = PasswordField(validators = [validators.DataRequired()])
        new_password_repeat = PasswordField(validators = [validators.DataRequired()])

    form = ChangePasswordForm()
    if form.validate_on_submit():
        if form.new_password.data != form.new_password_repeat.data:
            return json.jsonify(error = "repeat password does not match"), 400
        if not g.user.password.check_password(form.old_password.data):
            return json.jsonify(error = "incorrect old password")
        g.user.password = form.new_password.data
        g.user.save()
        logout()
        return json.jsonify(result = "ok")
    else:
        return json.jsonify(error = "bad form data"), 400


@yourself.route("/edit_profile", methods = ["POST"])
@need_to_login()
def edit_profile():
    class EditProfile(FlaskForm):
        name = StringField("name", validators = [validators.DataRequired()])
        school = SelectField("school", validators = [validators.DataRequired()], choices = get_schools(), coerce = int)
        klass = StringField("klass", validators = [validators.DataRequired()])

    form = EditProfile()
    if form.validate_on_submit():
        g.user.name = form.name.data
        g.user.school = form.school.data
        g.user.klass = form.klass.data
        g.user.save()
        return json.jsonify(result = "ok")
    else:
        return json.jsonify(error = "bad form data"), 400
