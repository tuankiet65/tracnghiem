from .database import Account, Exam, Contest

def generate_stats():
    account_count = Account.select().count()
    exam_count = Exam.select().count()
    contest_count = Contest.select().count()

    return {
        "account_count": account_count,
        "exam_count": exam_count,
        "contest_count": contest_count
    }