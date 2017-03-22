from peewee import *
from playhouse.fields import PasswordField

from ..utils.random import generate_random_string
from ..database import BaseModel, database


class AdminUser(BaseModel):
    username = CharField(index = True)
    password = PasswordField()


class AdminSessionToken(BaseModel):
    token = CharField(default = lambda: generate_random_string())
    user = ForeignKeyField(rel_model = AdminUser)

__all__ = ['AdminUser', 'AdminSessionToken']