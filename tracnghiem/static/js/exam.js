function Question(question_count, question, answer_a, answer_b, answer_c, answer_d, change_callback, id){
    this.question_i18n = i18n.translate("Question").fetch();
    this.question = question;
    this.answer_a = answer_a;
    this.answer_b = answer_b;
    this.answer_c = answer_c;
    this.answer_d = answer_d;
    this.question_count = question_count;
    this.element_name = "question_" + this.question_count.toString();
    this.element = null;
    this.change_callback = change_callback;
    this.id = id;

    this.template = Handlebars.compile(' \
        <div class="question" data-question="{{question_count}}"> \
            <span class="question-statement">{{question_i18n}} {{question_count}}: {{question}}</span> \
            <div class="question-choices"> \
                <p> \
                    <label> \
                        <input type="radio" name="{{element_name}}" id="{{element_name}}_1" class="with-gap" value="1"> \
                        <span>{{answer_a}}</span> \
                    </label> \
                </p> \
                <p> \
                    <label> \
                        <input type="radio" name="{{element_name}}" id="{{element_name}}_2" class="with-gap" value="2"> \
                        <span>{{answer_b}}</span> \
                    </label> \
                </p> \
                <p> \
                    <label> \
                        <input type="radio" name="{{element_name}}" id="{{element_name}}_3" class="with-gap" value="3"> \
                        <span>{{answer_c}}</span> \
                    </label> \
                </p> \
                <p> \
                    <label> \
                        <input type="radio" name="{{element_name}}" id="{{element_name}}_4" class="with-gap" value="4"> \
                        <span>{{answer_d}}</span> \
                    </label> \
                </p> \
            </div> \
        </div> \
    ');

    this.render_to = function (container){
        var data = {
            question: this.question,
            answer_a: this.answer_a,
            answer_b: this.answer_b,
            answer_c: this.answer_c,
            answer_d: this.answer_d,
            question_count: this.question_count,
            element_name: this.element_name,
            question_i18n: this.question_i18n
        };
        var render_data = this.template(data);
        $(container).append(render_data);

        $("input[type=radio][name=" + this.element_name + "]").change(function (){
            this.change_callback(this.question_count);
        }.bind(this))
    }.bind(this);

    this.load_answer = function (answer){
        $("input[type=radio][name=" + this.element_name + "]").prop("checked", false);
        if (answer !== 0) {
            $("input[type=radio][id=" + this.element_name + "_" + answer.toString() + "]").prop("checked", true);
            this.change_callback(this.question_count);
        }
    }.bind(this);

    this.get_answer = function (){
        var answer = parseInt($("input[type=radio][name=" + this.element_name + "]:checked").val());
        if (isNaN(answer)) {
            return 0;
        } else {
            return answer;
        }
    };

    return this;
}

function CustomSet(size){
    this.size = size + 1;
    this.set = new Array(this.size);

    for (var i = 0; i < this.size; i++) {
        this.set[i] = false;
    }

    this.add = function (n){
        this.set[n] = true;
    }.bind(this);

    this.count = function (){
        var count = 0;
        for (var i = 0; i < this.size; i++) {
            if (this.set[i]) {
                count++;
            }
        }
        return count;
    }
}

function Countdown(start_time, end_time, tick_callback){
    this.start_time = start_time;
    this.end_time = end_time;

    this.remaining = parseInt((this.end_time - this.start_time) / 1000);
    this.tick_callback = tick_callback;

    this.timer_callback = function(){
        this.remaining--;
        this.tick_callback(this.remaining);
        if (this.remaining < 0){
            this.stop();
        }
    }.bind(this);

    this.stop = function(){
        clearInterval(this.timer_id);
    }.bind(this);

    this.timer_id = setInterval(this.timer_callback, 1000);
    this.tick_callback(this.remaining);

    return this;
}

function Exam(exam, questions){
    this.exam = exam;
    this.questions = questions;

    this.question_container = $("#exam_container");
    this.question_answered = new CustomSet(this.questions.length);
    this.answers_modified = false;

    $("#total-questions").text(this.questions.length);
    $("#questions-answered").text(0);

    this.question_checked_callback = function (question_count){
        this.question_answered.add(question_count);
        $("#questions-answered").text(this.question_answered.count());
        this.answers_modified = true;
    }.bind(this);

    this._tmp = $.parseJSON(this.exam.answers);
    for (var q = 0; q < this.questions.length; q++) {
        this.questions[q] = new Question(q + 1,
            this.questions[q].question,
            this.questions[q].answer_a,
            this.questions[q].answer_b,
            this.questions[q].answer_c,
            this.questions[q].answer_d,
            this.question_checked_callback);
        this.questions[q].render_to(this.question_container);
        this.questions[q].load_answer(this._tmp[q]);
    }

    this._time_pad = function (value){
        if (value <= 9) {
            value = '0' + value.toString();
        } else {
            value = value.toString();
        }

        return value;
    };

    this.update_time_remaining = function (remaining){
        var minute = parseInt(remaining / 60);
        var second = (remaining % 60);

        minute = this._time_pad(minute);
        second = this._time_pad(second);

        $("#countdown-minute").text(minute);
        $("#countdown-second").text(second);

    };

    this.tick = function (remaining){
        this.update_time_remaining(remaining);
        if (remaining <= 0) {
            this.close_exam();
        }
    }.bind(this);

    this.countdown = new Countdown(
        moment.parseZone(current_server_time),
        moment.parseZone(this.exam.finish_date),
        this.tick
    );

    this.autosave = function (){
        if (this.answers_modified) {
            this.save_answers();
        }
    }.bind(this);

    this.autosave_id = setInterval(this.autosave, 5000);

    this.get_answers = function (){
        var answers = [];
        for (q = 0; q < this.questions.length; q++) {
            answers.push(this.questions[q].get_answer());
        }
        return answers;
    }.bind(this);

    this.ajax_send_answer = function (answer, close_exam, success_callback, failure_callback){
        $.ajax("/exam/save_answers", {
            method: "POST",
            data: {
                exam_id: this.exam.secret_key,
                answer: answer,
                close_exam: close_exam
            },
            dataType: "json",
            timeout: 4000
        }).done(
            success_callback
        ).fail(function (xhr, textStatus, errorThrown){
            var error = null;
            if (typeof xhr.responseJSON === "undefined") {
                error = null;
            } else if (typeof xhr.responseJSON.error === "undefined") {
                error = null;
            } else {
                error = xhr.responseJSON.error;
            }
            if (!error) {
                M.toast({
                    html: i18n.translate("Unknown AJAX error: %(text_status)s %(error_thrown)s, please reload.").fetch({
                        text_status: textStatus,
                        error_thrown: errorThrown
                    })
                });
            } else {
                if (xhr.status === 403) {
                    clearInterval(this.autosave_id);
                    Swal.fire({
                        titleText: i18n.translate("Authentication failure").fetch(),
                        text: i18n.translate("Please login again").fetch(),
                        type: "error"
                    }).then(function (){
                        window.location.reload(true);
                    })
                } else {
                    M.toast({
                        html: i18n.translate("AJAX error: %(error)s, please reload.").fetch({
                            error: error
                        })
                    });
                }
            }
            failure_callback();
        }.bind(this))
    }.bind(this);

    this.save_answers = function (){
        $("#sync-done").css("display", "none");
        $("#sync-fail").css("display", "none");
        $("#sync-inprogress").css("display", "inline");
        var answers = JSON.stringify(this.get_answers());
        this.ajax_send_answer(answers, false, function (){
            $("#sync-inprogress").css("display", "none");
            $("#sync-done").css("display", "inline");
            this.answers_modified = false;
        }.bind(this), function (){
            $("#sync-inprogress").css("display", "none");
            $("#sync-fail").css("display", "inline");
        }.bind(this));
    }.bind(this);

    this.close_exam = function (){
        var answers = JSON.stringify(this.get_answers());
        $("#modal-submitting").modal("open");
        clearInterval(this.autosave_id);
        this.countdown.stop();
        this.ajax_send_answer(answers, true, function (data){
            $("#modal-submitting").modal("close");
            var score = data.score;
            var finish_text = i18n.translate("You have finished your exam with score of %(score)d/%(questions_count)d").fetch({
                score: score,
                questions_count: this.questions.length
            });
            Swal.fire({
                titleText: i18n.translate("Congratulation").fetch(),
                text: finish_text,
                type: "success"
            }).then(function (){
                window.location.replace("/participate");
            })
        }.bind(this), function (){
            $("#modal-submitting").modal("close");
            Swal.fire({
                titleText: i18n.translate("Error").fetch(),
                text: i18n.translate("We can't close your exam at the moment. Please try again in a few seconds.").fetch(),
                type: "error"
            }).then(function (){
                window.location.reload(true);
            })
        })
    };

    return this;
}

exam = new Exam(exam, questions);

$("#close-exam-button").click(function (){
    var warning_text = i18n.translate("Do you want to close the exam? You still have time").fetch();
    if (exam.question_answered.count() < exam.questions.length) {
        warning_text = i18n.translate("Do you want to close the exam? You still have time and you have %(question)d questions unanswered").fetch({
            question: exam.questions.length - exam.question_answered.count()
        })
    }
    Swal.fire({
        titleText: i18n.translate("Warning").fetch(),
        text: warning_text,
        type: "warning",
        showCloseButton: true,
        showCancelButton: true,
        focusCancel: true
    }).then(function (result){
        if (result.value) {
            exam.close_exam();
        }
    })
});
