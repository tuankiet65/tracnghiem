from flask import json
from playhouse.shortcuts import model_to_dict
from wtforms import *

from tracnghiem.database import Contest, QuestionSet, Question
from .data_list import DataList

ContestList = DataList("contest")

ContestList.set_template("admin_contest.html")


@ContestList.get_func
def get():
    query = Contest.select()
    return [{
                "id"   : entry.id,
                "value": model_to_dict(entry, exclude = [Contest.id])
            } for entry in query]


@ContestList.remove_func
def remove(id: int):
    try:
        entry = Contest.get(id = id)
    except Contest.DoesNotExist:
        return False
    entry.delete_instance()
    return True


class ContestAddForm(Form):
    title = StringField(validators = [validators.DataRequired()])
    begin_date = DateField(validators = [validators.DataRequired()], format = "%d/%m/%Y")
    end_date = DateField(validators = [validators.DataRequired()], format = "%d/%m/%Y")
    duration = IntegerField(validators = [validators.DataRequired()])
    question_set = StringField(validators = [validators.DataRequired()])


def get_question_set_count(param):
    question_sets = json.loads(param)

    question_count = 0

    for set in question_sets:
        qset = QuestionSet.get(id = set['id'])

        if set['count'] > Question.select().where(Question.set == qset).count():
            raise ValueError

        question_count += set['count']

    return question_count

@ContestList.add_func
def add(value):
    form = ContestAddForm(formdata = value)
    if form.validate():
        question_count = get_question_set_count(form.question_set.data)

        entry = Contest.create(title = form.title.data,
                               begin_date = form.begin_date.data,
                               end_date = form.end_date.data,
                               duration = form.duration.data,
                               question_count = question_count,
                               question_set = form.question_set.data)

        return entry.id
    else:
        return None
