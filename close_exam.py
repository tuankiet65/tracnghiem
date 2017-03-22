import time
import logging

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
        logging.info("Closing exam {}...".format(exam.secret_key))
        count += 1

    return count


logging.basicConfig(format="[%(asctime)s][%(funcName)s] %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    level=logging.INFO)

logging.info("Opening database")
database.connect()

logging.info("Closing exam every 10 seconds")

try:
    while True:
        # Because this will potentially modify a lot of exam,
        # and this operation is asynchronously run compared to the backend code
        # it's best to aggregate all changes into a transaction,
        # to prevent inconsistencies
        with database.atomic():
            logging.info("Closing exam...")
            count = close_expired_exam()
            logging.info("Closed {} exam".format(count))
        time.sleep(10)
except KeyboardInterrupt:
    logging.info("Exiting...")
    database.close()
