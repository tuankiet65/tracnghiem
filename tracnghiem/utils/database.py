from ..database import *
from ..admin.database import *

def create_all_tables():
    database.create_tables([Announcement, School, Account, SessionToken,
                            Contest, Question, Exam, QuestionSet,
                            AdminUser, AdminSessionToken])
