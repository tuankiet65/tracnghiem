from ..database import School


def get_schools():
    query = School.select()
    return [(entry.id, entry.name) for entry in query]
