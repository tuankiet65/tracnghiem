from wtforms import *
from playhouse.shortcuts import model_to_dict

from .data_list import DataList
from tracnghiem.database import Question, QuestionSet

QuestionSetList = DataList("questionset", "questionset")
QuestionSetList.set_template("admin_question_set.html")


@QuestionSetList.get_func
def get_func():
    query = QuestionSet.select()
    return [{
                'id'   : entry.id,
                'value': model_to_dict(entry, recurse = False)
            } for entry in query]


class QuestionSetAddForm(Form):
    name = StringField(validators = [validators.DataRequired()])


@QuestionSetList.add_func
def add_func(value):
    form = QuestionSetAddForm(formdata = value)
    if form.validate():
        entry = QuestionSet.create(name = form.name.data)
        return entry.id
    else:
        return None


@QuestionSetList.remove_func
def remove_func(id):
    try:
        entry = QuestionSet.get(id = id)
    except Question.DoesNotExist:
        return False
    entry.delete_instance()
    return True
