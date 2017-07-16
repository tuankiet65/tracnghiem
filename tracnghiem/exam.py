import json
from random import Random

from flask import g, Blueprint, request, render_template, redirect, url_for, abort
from flask import json as fjson
from flask_wtf import FlaskForm
from playhouse.shortcuts import model_to_dict
from wtforms import StringField, BooleanField, validators

from .authentication import need_to_login
from .database import Exam, Question, Contest
from .utils.datetime import dt_to_local_dt, get_current_local_dt, d_to_local_dt, get_minutes_delta


def get_exam_question(exam: Exam, include_answers: bool):
    rng = Random(exam.random_seed)
    print("random seed: {}".format(exam.random_seed))
    contest = exam.contest

    exam_questions = []

    for question_set in fjson.loads(contest.question_set):
        question_candidates = list(Question.select().where(Question.set == question_set['id']))
        exam_questions.extend([model_to_dict(q, exclude = [Question.set, Question.id]) for q in
                               rng.sample(question_candidates, k = question_set['count'])])

    for question in exam_questions:
        tmp = [
            (question['answer_a'], (question['correct_answer'] == 1)),
            (question['answer_b'], (question['correct_answer'] == 2)),
            (question['answer_c'], (question['correct_answer'] == 3)),
        ]

        # Shuffling the list three times seems to yield better randomness
        # (not scientifically proven)
        rng.shuffle(tmp)
        rng.shuffle(tmp)
        rng.shuffle(tmp)

        question['answer_a'] = tmp[0][0]
        question['answer_b'] = tmp[1][0]
        question['answer_c'] = tmp[2][0]

        if include_answers:
            question['correct_answer'] = (1 if tmp[0][1] else 2 if tmp[1][1] else 3)
        else:
            del question['correct_answer']

    return exam_questions


def mark_exam(exam: Exam, force_remark: bool = False):
    if exam.finished and not force_remark:
        return exam.score

    questions = get_exam_question(exam, include_answers = True)
    answers = json.loads(exam.answers)

    score = 0

    for question, answer in zip(questions, answers):
        if question['correct_answer'] == answer:
            score += 1

    return score


def check_valid_answer(exam: Exam, answers):
    try:
        answers = json.loads(answers)
    except json.JSONDecodeError:
        return False
    if not isinstance(answers, list):
        return False
    if len(answers) != exam.contest.question_count:
        return False
    for answer in answers:
        if not isinstance(answer, int):
            return False
        if (answer < 0) or (answer > 3):
            return False
    return True


def in_contest_date(contest):
    begin_date = d_to_local_dt(contest.begin_date, min_time = True)
    end_date = d_to_local_dt(contest.end_date, min_time = False)
    current_date = get_current_local_dt()

    return (current_date >= begin_date) and (current_date <= end_date)


def close_exam(exam: Exam):
    exam.score = mark_exam(exam)
    exam.finished = True

    exam.finish_date = min(get_current_local_dt(), dt_to_local_dt(exam.finish_date))
    exam.elapsed_time = (dt_to_local_dt(exam.finish_date) - dt_to_local_dt(exam.begin_date)).total_seconds()

    exam.save()


####################
# Flask endpoints
####################

exam = Blueprint("exam", __name__, url_prefix = "/exam")


@exam.route("/create", methods = ["GET"], endpoint = "create")
@need_to_login()
def create_exam_route():
    # check if contest_id is specified
    try:
        contest = request.args['contest_id']
    except KeyError:
        return abort(400)

    # check if contest exists
    try:
        contest = Contest.get(id = contest)
    except Contest.DoesNotExist:
        return abort(404)

    # check if the contest has started/hasn't ended
    if not in_contest_date(contest):
        return abort(403)

    exam = Exam.create(contestant = g.user,
                       contest = contest)

    exam.answers = json.dumps([0] * contest.question_count)
    exam.finish_date = dt_to_local_dt(exam.begin_date) + get_minutes_delta(contest.duration)
    exam.save()

    return redirect("/exam/" + exam.secret_key)


def exam_to_dict(exam: Exam):
    # special function because model_to_dict doesn't know how to handle time
    return {
        "secret_key" : exam.secret_key,
        "begin_date" : dt_to_local_dt(exam.begin_date).isoformat(),
        "finish_date": dt_to_local_dt(exam.finish_date).isoformat(),
        "finished"   : exam.finished,
        "answers"    : exam.answers
    }


@exam.route("/<secret_key>", methods = ["GET"])
@need_to_login()
def exam_page(secret_key):
    try:
        exam = Exam.get(secret_key = secret_key)
    except Exam.DoesNotExist:
        return abort(404)

    if exam.contestant != g.user:
        return abort(403)

    if exam.finished:
        return redirect(url_for("participate.index"))

    if get_current_local_dt() > dt_to_local_dt(exam.finish_date):
        # force close the exam
        close_exam(exam)
        return redirect(url_for("participate.index"))

    return render_template("exam_page.html",
                           questions = get_exam_question(exam, include_answers = False),
                           exam = exam_to_dict(exam))


@exam.route("/save_answers", methods = ["POST"])
@need_to_login(api_endpoint = True)
def save_answers():
    class ExamSaveAnswersForm(FlaskForm):
        exam_id = StringField(validators = [validators.DataRequired()])
        answer = StringField(validators = [validators.DataRequired()])
        close_exam = BooleanField(validators = [validators.InputRequired()], false_values = ('false', ''))

    form = ExamSaveAnswersForm()
    if form.validate_on_submit():
        try:
            exam = Exam.get(secret_key = form.exam_id.data)
        except Exam.DoesNotExist:
            return fjson.jsonify(error = "exam id not found"), 404

        if exam.contestant != g.user:
            return fjson.jsonify(error = "you aren't the contestant of this exam"), 403

        if exam.finished:
            return fjson.jsonify(error = "exam has already finished"), 403

        # here exam.finished is false
        # (because of the above if)

        # Things get pretty complicated from this point
        # We allow a one minute grace period in which we will accept ONE final answer from user,
        # and then we close the exam
        # This is to compensate for transmission delay
        # (banana internet connection, cellular network, etc)

        # First we check if the one-minute grace period is over
        # If yes then we reject the final answer and forcibly close the exam
        # Maybe not necessary because the exam should be closed automatically
        # by the cleanup script, but whatever
        if get_current_local_dt() > (dt_to_local_dt(exam.finish_date) + get_minutes_delta(1)):
            close_exam(exam)
            return fjson.jsonify(result = "ok",
                                 note = "you submitted it so late so we reject your last answer and "
                                        "mark your exam using your last saved answer",
                                 score = exam.score)

        # Check if answer is valid first because we may potentially use
        # it in the next step (or not)
        if not check_valid_answer(exam, form.answer.data):
            return fjson.jsonify(error = "invalid answer"), 400

        # At this point get_current_time() - exam.finished_date <= 1 minute
        # So check if current time is more than finish_date ot not
        # If yes then we accept the answer and forcibly close the exam
        if get_current_local_dt() > dt_to_local_dt(exam.finish_date):
            exam.answers = form.answer.data
            close_exam(exam)
            return fjson.jsonify(result = "ok",
                                 note = "you submitted it in the grace period",
                                 score = exam.score)

        # still in time, do things as normal

        exam.answers = form.answer.data
        exam.save()
        if form.close_exam.data:
            close_exam(exam)
            return fjson.jsonify(result = "ok", score = exam.score)
        else:
            return fjson.jsonify(result = "ok")
    else:
        return fjson.jsonify(error = "invalid form"), 400
