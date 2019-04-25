from peewee import *

from ..database import BaseModel, PasswordField
from ..utils.random import generate_random_string


class AdminUser(BaseModel):
    username = CharField(index = True)
    password = PasswordField()


class AdminSessionToken(BaseModel):
    token = CharField(default = lambda: generate_random_string())
    user = ForeignKeyField(AdminUser)


__all__ = ['AdminUser', 'AdminSessionToken']
