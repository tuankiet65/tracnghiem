function Question(question_count, question, answer_a, answer_b, answer_c, answer_d, change_callback, id){
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
            <h4>Question {{question_count}}: {{question}}</h4> \
            <div class="question-choices"> \
                <p> \
                    <input type="radio" name="{{element_name}}" id="{{element_name}}_1" class="with-gap" value="1"> \
                    <label for="{{element_name}}_1"> \
                        {{answer_a}} \
                    </label> \
                </p> \
                <p> \
                    <input type="radio" name="{{element_name}}" id="{{element_name}}_2" class="with-gap" value="2"> \
                    <label for="{{element_name}}_2"> \
                        {{answer_b}} \
                    </label> \
                </p> \
                <p> \
                    <input type="radio" name="{{element_name}}" id="{{element_name}}_3" class="with-gap" value="3"> \
                    <label for="{{element_name}}_3"> \
                        {{answer_c}} \
                    </label> \
                </p> \
                <p> \
                    <input type="radio" name="{{element_name}}" id="{{element_name}}_4" class="with-gap" value="4"> \
                    <label for="{{element_name}}_4"> \
                        {{answer_d}} \
                    </label> \
                </p> \
            </div> \
        </div> \
    ')

    this.render_to = function(container){
        data = {
            question: this.question,
            answer_a: this.answer_a,
            answer_b: this.answer_b,
            answer_c: this.answer_c,
            answer_d: this.answer_d,
            question_count: this.question_count,
            element_name: this.element_name
        }
        render_data = this.template(data);
        $(container).append(render_data);

        $("input[type=radio][name="+this.element_name+"]").change(function(){
            this.change_callback(this.question_count);
        }.bind(this))
    }.bind(this);

    this.load_answer = function(answer){
        $("input[type=radio][name="+this.element_name+"]").prop("checked", false);
        if (answer != 0){
            console.log("input[type=radio][id="+this.element_name+"_"+answer.toString()+"]");
            $("input[type=radio][id="+this.element_name+"_"+answer.toString()+"]").prop("checked", true);
            this.change_callback(this.question_count);
        }
    }.bind(this);

    this.get_answer = function(){
        answer = parseInt($("input[type=radio][name="+this.element_name+"]:checked").val());
        if (isNaN(answer)){
            return 0;
        } else {
            return answer;
        }
    }

    return this;
}

function Exam(exam, contest, questions){
    this.exam = $.parseJSON(exam);
    this.contest = $.parseJSON(contest);
    this.questions = $.parseJSON(questions);
    this.question_container = $("#exam_container");
    this.question_answered = new Set();
    this.answers_modified = false;

    $("#total-questions").text(this.questions.length);
    $("#questions-answered").text(0);

    this.question_checked_callback = function(question_count){
        this.question_answered.add(question_count);
        $("#questions-answered").text(this.question_answered.size);
        this.answers_modified = true;
    }.bind(this);

    this._tmp = $.parseJSON(this.exam.answers);
    for (q = 0; q < this.questions.length; q++){
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

    this._time_pad = function(value){
        if (value <= 9){
            value = '0'+value.toString();
        } else {
            value = value.toString();
        }

        return value;
    }

    this.update_time_remaining = function(remaining){
        var minute = parseInt(remaining / 60);
        var second = (remaining % 60);

        minute = this._time_pad(minute);
        second = this._time_pad(second);

        $("#countdown-minute").text(minute);
        $("#countdown-second").text(second);

    }

    this.get_answers = function(){
        answers = [];
        for (q = 0; q < this.questions.length; q++){
            answers.push(this.questions[q].get_answer());
        }
        return answers;
    }.bind(this);

    this.save_answers = function(){
        $("#sync-done").css("display", "none");
        $("#sync-inprogress").css("display", "inline");
        answers = JSON.stringify(this.get_answers());
        $.post("/exam/save_answers", {
            exam_id: this.exam.secret_key,
            answer: answers,
            close_exam: false
        }, function(){
            $("#sync-inprogress").css("display", "none");
            $("#sync-done").css("display", "inline");
            this.answers_modified = false;
        }.bind(this))
    }.bind(this);

    this.close_exam = function(){
        answers = JSON.stringify(this.get_answers());
        $("#modal-submitting").modal("open");
        $.post("/exam/save_answers", {
            exam_id: this.exam.secret_key,
            answer: answers,
            close_exam: true
        }, function(data){
            $("#modal-submitting").modal("close");
            score = data.score;
            swal({
                titleText: "Congratulations",
                text: "You have finished your exam with score of " + score.toString() + "/" + this.questions.length,
                type: "success",
            }).then(function(){
                window.location.replace("/participate");
            })
        }.bind(this))
    }

    this.tick = function(remaining){
        this.update_time_remaining(remaining);
        if (remaining <= 0){
            this.close_exam();
        }
    }.bind(this);

    this.countdown = new Countdown(moment.utc(this.exam.finish_date, "ddd, DD MMM YYYY HH:mm:ss"),
                                   this.tick);

    this.autosave = function(){
        if (this.answers_modified){
            this.save_answers();
        }
    }.bind(this);

    this.autosave_id = setInterval(this.autosave, 5000);

    return this;
}

exam = new Exam(exam, "{}", questions);

$("#close-exam-button").click(function(){
    if (exam.question_answered.size < exam.questions.length){
        warning_text = "Do you want to close the exam? You still have time and you have ";
        warning_text += (exam.questions.length - exam.question_answered.size).toString();
        warning_text += " questions unanswered";
    } else {
        warning_text = "Do you want to close the exam? You still have time";
    }
    swal({
        titleText: "Warning",
        text: warning_text,
        type: "warning",
        showCloseButton: true,
        showCancelButton: true,
        focusCancel: true
    }).then(function(){
        exam.close_exam();
    })
})