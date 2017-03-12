from .data_list import DataList
from wtforms import *
from tracnghiem.database import Contest
from playhouse.shortcuts import model_to_dict

ContestList = DataList("contest")

ContestList.set_template("admin_contest.html")


@ContestList.get_func
def get():
    query = Contest.select()
    return [{
                "id": entry.id,
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
    question_count = IntegerField(validators = [validators.DataRequired()])
    question_set = StringField(validators = [validators.DataRequired()])

@ContestList.add_func
def add(value):
    form = ContestAddForm(formdata = value)
    if form.validate():
        print(form.begin_date.data)
        entry = Contest.create(title = form.title.data,
                               begin_date = form.begin_date.data,
                               end_date = form.end_date.data,
                               duration = form.duration.data,
                               question_count = form.question_count.data,
                               question_set = form.question_set.data)
        return entry.id
    else:
        print(form.errors)
        return None
