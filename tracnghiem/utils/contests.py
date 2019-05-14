from ..database import Contest

def get_contests():
    query = Contest.select()

    return [(contest.id, contest.title) for contest in query]
