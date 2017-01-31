from peewee import *
from playhouse.fields import PasswordField
from .common import get_current_utc

# TODO: This should be replaced with a config file
database = MySQLDatabase(host = "localhost",
                         user = "root",
                         password = "BOINCTuanKiet",
                         database = "tracnghiem")


def create_all_tables():
    database.create_tables([Announcement, School, Account, SessionToken, Contest, Question])


class BaseModel(Model):
    class Meta:
        database = database


class Announcement(BaseModel):
    # auto id field
    title = CharField()
    content = TextField()
    time = DateTimeField(default = get_current_utc)


class School(BaseModel):
    # auto id field
    name = CharField()


class Account(BaseModel):
    # auto id field
    username = CharField(index = True)
    password = PasswordField()
    name = CharField()
    email = CharField()
    school = ForeignKeyField(School)


class SessionToken(BaseModel):
    id = CharField()


class Contest(BaseModel):
    # auto id field
    title = CharField()
    start_time = DateTimeField()
    end_time = DateTimeField()


class Question(BaseModel):
    # auto id field
    contest = ForeignKeyField(Contest)
    question = CharField()
    answer_a = CharField()
    answer_b = CharField()
    answer_c = CharField()
    answer_d = CharField()
    correct_answer = CharField()
