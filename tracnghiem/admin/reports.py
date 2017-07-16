import csv

from flask import render_template, Response, stream_with_context
from flask_wtf import FlaskForm
from wtforms import *

from ..database import Exam, Account, School, Contest
from ..utils.contests import get_contests
from ..utils.datetime import d_to_local_dt, dt_to_local_dt, get_current_local_dt
from ..utils.schools import get_schools


def exam_to_object(exam: Exam) -> object:
    return {
        'id'               : exam.id,
        'secret_key'       : exam.secret_key,
        'contestant_name'  : exam.contestant.name,
        'contestant_school': exam.contestant.school.name,
        'begin_date'       : dt_to_local_dt(exam.begin_date).isoformat(),
        'end_date'         : dt_to_local_dt(exam.finish_date).isoformat(),
        'duration'         : exam.elapsed_time,
        'score'            : exam.score,
        'finished'         : 1 if exam.finished else 0,
        'contest'          : exam.contest.title
    }


CSV_FIELDS = ['id', 'secret_key', 'contestant_name', 'contestant_school',
              'contest', 'begin_date', 'end_date', 'duration', 'score', 'finished']


class LineIO:
    line = ""

    def write(self, line):
        self.line = line

    def read(self):
        return self.line


# admin.route("/reports", methods=["GET", "POST"])
def reports():
    class GenerateReportsForm(FlaskForm):
        begin_date = DateField(validators = [validators.DataRequired()], format = "%d/%m/%Y")
        end_date = DateField(validators = [validators.DataRequired()], format = "%d/%m/%Y")
        contests = SelectMultipleField(validators = [validators.DataRequired()], choices = get_contests(), coerce = int)
        schools = SelectMultipleField(validators = [validators.DataRequired()], choices = get_schools(), coerce = int)
        include_unfinished = BooleanField(validators = [validators.Optional()], false_values = ('false', ''))

    form = GenerateReportsForm()
    if form.validate_on_submit():
        begin_date = d_to_local_dt(form.begin_date.data, min_time = True)
        end_date = d_to_local_dt(form.end_date.data, min_time = False)

        query = (Exam
                 .select(Exam.id,
                         Account.name, School.name,
                         Exam.begin_date, Exam.finish_date, Exam.elapsed_time, Exam.score, Exam.finished, Exam.contest)
                 .join(Contest)
                 .switch(Exam)
                 .join(Account)
                 .join(School)
                 .where((Exam.begin_date >= begin_date) & (Exam.finish_date <= end_date))
                 .where(School.id << form.schools.data)
                 .where(Contest.id << form.contests.data))

        if not form.include_unfinished.data:
            query = (query
                     .where(Exam.finished))

        now = get_current_local_dt()
        filename = "reports_{}.csv".format(now.isoformat())

        @stream_with_context
        def generate_request(query):
            lineio = LineIO()
            csv_writer = csv.DictWriter(f = lineio, fieldnames = CSV_FIELDS, extrasaction = "raise")

            csv_writer.writeheader()
            yield lineio.read()

            for exam in query:
                csv_writer.writerow(exam_to_object(exam))
                yield lineio.read()

                # For whatever reasons custom-made Response doesn't trigger

        response = Response(generate_request(query), mimetype = 'text/csv', content_type = "text/csv")
        response.headers['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

        return response
    else:
        if form.errors:
            return render_template("admin_reports.html", schools = get_schools(), contests = get_contests(),
                                   fail = True)
        else:
            return render_template("admin_reports.html", schools = get_schools(), contests = get_contests())
