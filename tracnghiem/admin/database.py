from tracnghiem.database import BaseModel, database
from peewee import *
from playhouse.fields import PasswordField
from tracnghiem.common import gen_random_string

class AdminUser(BaseModel):
    username = CharField(index = True)
    password = PasswordField()

class AdminSessionToken(BaseModel):
    token = CharField(default = lambda: gen_random_string())
    user = ForeignKeyField(rel_model = AdminUser)

def create_all_tables():
    database.create_tables([AdminUser, AdminSessionToken])