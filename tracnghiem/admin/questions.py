from flask import abort, render_template
from playhouse.shortcuts import model_to_dict
from wtforms import *

from tracnghiem.database import Question, QuestionSet
from .data_list import DataList

QuestionList = DataList("question", "questionset/<int:qset_id>")
QuestionList.set_template("")


@QuestionList.main_func
def main_func(qset_id):
    try:
        qset = QuestionSet.get(id = qset_id)
    except QuestionSet.DoesNotExist:
        return abort(404)
    return render_template("admin_question.html", qset = qset)


@QuestionList.get_func
def get_func(qset_id):
    query = Question.select().where(Question.set == qset_id)
    return [{
                'id'   : entry.id,
                'value': model_to_dict(entry, exclude = [Question.id, Question.set], recurse = False)
            } for entry in query]


class QuestionAddForm(Form):
    question = StringField(validators = [validators.DataRequired()])
    answer_a = StringField(validators = [validators.DataRequired()])
    answer_b = StringField(validators = [validators.DataRequired()])
    answer_c = StringField(validators = [validators.DataRequired()])
    correct_answer = IntegerField(validators = [validators.DataRequired(), validators.NumberRange(min = 1, max = 3)])


@QuestionList.add_func
def add_func(value, qset_id):
    form = QuestionAddForm(formdata = value)
    try:
        qset = QuestionSet.get(id = qset_id)
    except QuestionSet.DoesNotExist:
        return None
    if form.validate():
        entry = Question.create(question = form.question.data,
                                answer_a = form.answer_a.data,
                                answer_b = form.answer_b.data,
                                answer_c = form.answer_c.data,
                                correct_answer = form.correct_answer.data,
                                set = qset)
        return entry.id
    else:
        return None


@QuestionList.remove_func
def remove_func(id, qset_id):
    try:
        entry = Question.get(id = id)
    except Question.DoesNotExist:
        return False
    entry.delete_instance()
    return True
