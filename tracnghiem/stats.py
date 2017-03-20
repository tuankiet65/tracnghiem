from .database import Account, Exam, School


def generate_stats():
    result = {}
    schools = School.select()

    for school in schools:
        result[school.id] = {}
        result[school.id]['account_count'] = Account.select().join(School).where(Account.school == school).count()
        result[school.id]['exam_count'] = Exam.select().join(Account).where(Account.school == school).count()

    return result
