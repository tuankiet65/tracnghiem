from peewee import *

# TODO: This should be replaced with a config file
database = MySQLDatabase(host = "localhost",
                         user = "tracnghiem",
                         password = "tracnghiem",
                         database = "tracnghiem")


def create_all_tables():
    database.create_tables([Announcement])


class BaseModel(Model):
    class Meta:
        database = database


class Announcement(BaseModel):
    # auto id field
    title = CharField()
    content = TextField()
    time = DateTimeField()
