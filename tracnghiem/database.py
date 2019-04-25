import bcrypt
import secrets

from peewee import *

from . import app
from .utils.datetime import get_current_local_dt
from .utils.random import generate_random_string, generate_random_int

database = MySQLDatabase(host = app.config["DB_HOST"],
                         user = app.config["DB_USERNAME"],
                         password = app.config["DB_PASSWORD"],
                         database = app.config["DB_DATABASE"])


# Original Peewee 2.x PasswordField
# Credit to juancarlospaco
# https://github.com/juancarlospaco/peewee-extra-fields
class PasswordHash(bytes):
    def check_password(self, password):
        password = password.encode('utf-8')
        return secrets.compare_digest(bcrypt.hashpw(password, self), self)


class PasswordField(BlobField):
    def __init__(self, *args, **kwargs):
        self.raw_password = None
        super(PasswordField, self).__init__(*args, **kwargs)

    def db_value(self, value):
        """Convert the python value for storage in the database."""
        if isinstance(value, PasswordHash):
            return bytes(value)
        if isinstance(value, str):
            value = value.encode('utf-8')
        return value if value is None else bcrypt.hashpw(value, bcrypt.gensalt())

    def python_value(self, value):
        """Convert the database value to a pythonic value."""
        if isinstance(value, str):
            value = value.encode('utf-8')
        return PasswordHash(value)


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
    question = TextField()
    answer_d = CharField()
    answer_c = CharField()
    answer_b = CharField()
    answer_a = CharField()
    correct_answer = IntegerField()  # 1=A 2=B 3=C 4=D


class Exam(BaseModel):
    # auto id field
    secret_key = CharField(default = lambda: generate_random_string(50), index = True)
    contestant = ForeignKeyField(Account)
    begin_date = DateTimeField(default = get_current_local_dt)
    finish_date = DateTimeField()
    elapsed_time = IntegerField(default = 0)
    finished = BooleanField(default = False)
    # questions = TextField(default = "")
    random_seed = BigIntegerField(default = generate_random_int)
    answers = TextField(default = "")
    contest = ForeignKeyField(Contest)
    score = IntegerField(default = 0)


__all__ = [
    'database',
    'PasswordHash',
    'PasswordField',
    'BaseModel',
    'Announcement',
    'School',
    'Account',
    'SessionToken',
    'Contest',
    'Question',
    'Exam',
    'QuestionSet'
]
