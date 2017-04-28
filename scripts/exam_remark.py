from tracnghiem.database import database, Exam
from tracnghiem.exam import mark_exam
from tracnghiem.utils.datetime import get_current_local_dt


class Logging:
    fmt = "{prefix}[{time}] {message}{suffix}"
    time_format = "%Y-%m-%d %H:%M:%S"

    def log(self, message, line_feed = False, new_line = True):
        time = get_current_local_dt().strftime(self.time_format)
        print(self.fmt.format(prefix = "\r" if line_feed else "",
                              time = time,
                              message = message,
                              suffix = "\n" if new_line else ""), end = "")


log = Logging()

log.log("Opening database")
database.connect()

log.log("Remarking {} exams in database".format(Exam.select().count()))

count = 0

for exam in Exam.select():
    score = mark_exam(exam, force_remark = True)
    if exam.score != score:
        log.log("Exam id {} score is {}, should be {}".format(exam.id, exam.score, score))

    count += 1
    log.log("Remarked {} exams".format(count), line_feed = True, new_line = False)
