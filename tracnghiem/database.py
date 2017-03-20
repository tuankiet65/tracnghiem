from peewee import *
from playhouse.fields import PasswordField

from . import app
from .common import get_current_local_dt, generate_random_string

database = MySQLDatabase(host = app.config["DB_HOST"],
                         user = app.config["DB_USERNAME"],
                         password = app.config["DB_PASSWORD"],
                         database = app.config["DB_DATABASE"])


def create_all_tables():
    database.create_tables([Announcement, School, Account, SessionToken, Contest, Question, Exam, QuestionSet],
                           safe = False)


class BaseModel(Model):
    class Meta:
        database = database


class Announcement(BaseModel):
    # auto id field
    title = CharField()
    content = TextField()
    time = DateTimeField(default = get_current_local_dt)


class School(BaseModel):
    # auto id field
    name = CharField(unique = True, max_length = 100)


class Account(BaseModel):
    # auto id field
    username = CharField(index = True, unique = True, max_length = 100)
    password = PasswordField()
    name = CharField()
    school = ForeignKeyField(School)
    klass = CharField()
    facebook_id = CharField(index = True, max_length = 100)


class SessionToken(BaseModel):
    id = CharField(default = lambda: generate_random_string(50), primary_key = True, max_length = 100)
    account = ForeignKeyField(Account)


class Contest(BaseModel):
    # auto id field
    title = CharField()
    begin_date = DateField(formats = "%d/%m/%Y")
    end_date = DateField(formats = "%d/%m/%Y")
    duration = IntegerField()
    question_count = IntegerField()
    minimum_percentage = IntegerField()
    question_set = CharField(default = "[]")


class QuestionSet(BaseModel):
    # auto id field
    name = CharField()


class Question(BaseModel):
    # auto id field
    set = ForeignKeyField(QuestionSet)
    question = CharField()
    answer_d = CharField()
    answer_c = CharField()
    answer_b = CharField()
    answer_a = CharField()
    correct_answer = IntegerField()  # 1=A 2=B 3=C 4=D


class Exam(BaseModel):
    # auto id field
    secret_key = CharField(default = lambda: generate_random_string(50))
    contestant = ForeignKeyField(Account)
    begin_date = DateTimeField(default = get_current_local_dt)
    finish_date = DateTimeField()
    elapsed_time = IntegerField(default = 0)
    finished = BooleanField(default = False)
    questions = TextField(default = "")
    answers = TextField(default = "")
    session_lock = ForeignKeyField(SessionToken)
    contest = ForeignKeyField(Contest)
    score = IntegerField(default = 0)
