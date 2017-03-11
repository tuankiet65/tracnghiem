import random
import json
from flask import g, Blueprint, request, render_template, redirect, url_for
from flask import json as fjson
from playhouse.shortcuts import model_to_dict
from datetime import timedelta
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, validators

from .database import Exam, Question, Contest
from .authentication import need_to_login
from .common import get_local_datetime, get_current_time


def get_exam(exam_id):
    try:
        exam = Exam.get(id = exam_id)
    except Exam.DoesNotExist:
        return None
    return exam


def generate_exam_questions(contest: Contest):
    result = []
    random.seed()

    for question_set in fjson.loads(contest.question_set):
        candidates = list(Question.select().where(Question.set == question_set['question_set']))
        result.extend([q.id for q in random.sample(candidates, k = question_set['count'])])

    random.shuffle(result)

    return result


def get_exam_question(exam: Exam):
    result = []
    for question_id in fjson.loads(exam.questions):
        result.append(Question.get(id = question_id))
    return result


def mark_exam(exam: Exam):
    if exam.finished:
        return exam.score

    questions = json.loads(exam.questions)
    answers = json.loads(exam.answers)

    score = 0

    for question, answer in zip(questions, answers):
        question = Question.get(id = question)
        if question.correct_answer == answer:
            score += 1

    return score


def check_valid_answer(exam: Exam, answers):
    try:
        answers = json.loads(answers)
    except json.JSONDecodeError:
        return False
    if not isinstance(answers, list):
        print("fail at check if list")
        return False
    if len(answers) != len(json.loads(exam.questions)):
        print("fail at check if length equal")
        return False
    for answer in answers:
        if not isinstance(answer, int):
            return False
        if (answer < 0) or (answer > 4):
            return False
    return True


####################
# Flask endpoints
####################

exam = Blueprint("exam", __name__, url_prefix = "/exam")


@exam.route("/create", methods = ["GET"], endpoint = "create")
@need_to_login()
def create_exam_route():
    try:
        contest = request.args['contest_id']
    except KeyError:
        return fjson.jsonify(error = "no contest id specified"), 400
    try:
        contest = Contest.get(id = contest)
    except Contest.DoesNotExist:
        return fjson.jsonify(error = "no contest found"), 404

    questions = generate_exam_questions(contest)
    exam = Exam.create(contestant = g.user,
                       session_lock = g.session_token,
                       contest = contest,
                       questions = json.dumps(questions))

    exam.answers = json.dumps([0 for _ in range(len(questions))])
    exam.finish_date = exam.begin_date + timedelta(minutes = contest.duration)
    exam.save()
    return redirect("/exam/" + exam.secret_key)


def exam_to_dict(exam: Exam):
    # special function because model_to_dict doesn't know how to handle time
    return {
        "secret_key": exam.secret_key,
        "begin_date": get_local_datetime(exam.begin_date).isoformat(),
        "finish_date"  : get_local_datetime(exam.finish_date).isoformat(),
        "finished"  : exam.finished,
        "answers"   : exam.answers
    }


@exam.route("/<secret_key>", methods = ["GET"])
@need_to_login()
def exam_page(secret_key):
    try:
        exam = Exam.get(secret_key = secret_key)
    except KeyError:
        # TODO replace with a proper 404 page
        return fjson.jsonify(error = "no exam found"), 404

    if exam.contestant != g.user:
        return fjson.jsonify(error = "this is not your exam"), 403

    if exam.finished:
        return redirect(url_for("participate.index"))

    questions = get_exam_question(exam)

    return render_template("exam_page.html",
                           questions = [model_to_dict(q,
                                                      recurse = False,
                                                      exclude = [Question.correct_answer,
                                                                 Question.set]) for q in questions
                                        ],
                           exam = exam_to_dict(exam))


@exam.route("/save_answers", methods = ["POST"])
@need_to_login()
def save_answers():
    class ExamSaveAnswersForm(FlaskForm):
        exam_id = StringField(validators = [validators.DataRequired()])
        answer = StringField(validators = [validators.DataRequired()])
        close_exam = BooleanField(validators = [validators.InputRequired()], false_values = ('false', ''))

    form = ExamSaveAnswersForm()
    if form.validate_on_submit():
        exam = Exam.get(secret_key = form.exam_id.data)
        if exam is None:
            return fjson.jsonify(error = "exam id not found"), 404

        if not check_valid_answer(exam, form.answer.data):
            return fjson.jsonify(error = "invalid data"), 400

        exam.answers = form.answer.data
        exam.save()
        if form.close_exam.data:
            exam.score = mark_exam(exam)
            exam.finished = True

            exam.finish_date = min(get_current_time(), get_local_datetime(exam.finish_date))
            exam.elapsed_time = (exam.finish_date - get_local_datetime(exam.begin_date)).total_seconds()

            exam.save()

        return fjson.jsonify(result = "ok", score = exam.score)
    else:
        print(form.errors)
        return fjson.jsonify(error = "invalid form"), 400
