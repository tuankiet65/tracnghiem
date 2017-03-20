from peewee import *
from playhouse.fields import PasswordField

from tracnghiem.common import generate_random_string
from tracnghiem.database import BaseModel, database


class AdminUser(BaseModel):
    username = CharField(index = True)
    password = PasswordField()


class AdminSessionToken(BaseModel):
    token = CharField(default = lambda: generate_random_string())
    user = ForeignKeyField(rel_model = AdminUser)


def create_all_tables():
    database.create_tables([AdminUser, AdminSessionToken])
