from .database import School, Account, Exam


def generate_stats():
    result = {}

    # The below SQL + Python code should be equivalent to this
    # schools = School.select()
    # for school in schools:
    #     result[school.id] = {}
    #     result[school.id]['account_count'] = Account.select().join(School).where(Account.school == school).count()
    #     result[school.id]['exam_count'] = Exam.select().join(Account).where(Account.school == school).count()

    query = School.raw("""SELECT
        t1.school_id,
        account_count,
        exam_count
    FROM
        ((SELECT
            account.school_id AS school_id, COUNT(*) AS account_count
        FROM
            account
        GROUP BY account.school_id) AS t1)
            INNER JOIN
        ((SELECT
            school.id AS school_id, COUNT(*) AS exam_count
        FROM
            ((exam
        INNER JOIN account ON exam.contestant_id = account.id)
        INNER JOIN school ON account.school_id = school.id)
        GROUP BY school.id) AS t2) ON t1.school_id = t2.school_id
    """).dicts().execute()

    for row in query:
        school_id = int(row['school_id'])

        result[school_id] = {
            'account_count': int(row['account_count']),
            'exam_count': int(row['exam_count'])
        }

    return result
