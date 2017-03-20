from tracnghiem.database import School
from .data_list import DataList

SchoolList = DataList("school")

SchoolList.set_template("admin_school.html")


@SchoolList.get_func
def get():
    query = School.select()
    return [{
                "id"   : entry.id,
                "value": {
                    "name": entry.name
                }
            } for entry in query]


@SchoolList.remove_func
def remove(id: int):
    try:
        entry = School.get(id = id)
    except School.DoesNotExist:
        return False
    entry.delete_instance()
    return True


@SchoolList.add_func
def add(value):
    try:
        school_name = value['name']
    except KeyError:
        return None
    entry = School.create(name = school_name)
    return entry.id
