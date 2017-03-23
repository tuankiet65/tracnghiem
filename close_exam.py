import time

from tracnghiem.database import database, Exam
from tracnghiem.exam import close_exam
from tracnghiem.utils.datetime import get_current_local_dt, get_minutes_delta


def close_expired_exam():
    # allow for one minute grace period, read below
    deadline = get_current_local_dt() - get_minutes_delta(1)

    unfinished_exam = Exam.select().where(
        (~Exam.finished) & (Exam.finish_date < deadline))

    count = 0
    for exam in unfinished_exam:
        close_exam(exam)
        log.log("Closing exam {}...".format(exam.secret_key))
        count += 1

    return count

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

log.log("Closing exam every 10 seconds")

try:
    while True:
        # Because this will potentially modify a lot of exam,
        # and this operation is asynchronously run compared to the backend code
        # it's best to aggregate all changes into a transaction,
        # to prevent inconsistencies
        with database.atomic():
            count = close_expired_exam()
            if count == 0:
                log.log("No exam to close".format(count), line_feed = True, new_line = False)
            else:
                log.log("Closed {} exam".format(count))
        time.sleep(10)
except KeyboardInterrupt:
    log.log("Ctrl-C caught, exiting...")
    database.close()
