// Thanks to this answer on StackOverflow http://stackoverflow.com/a/16315366 (this gave me inspiration)
// also this tutorial http://jaskokoyn.com/2013/08/08/custom-helpers-handlebars-js-tutorial/
Handlebars.registerHelper('boldIfCorrectAnswer', function (answer, answer_count, correct_answer){
    var escaped_answer = Handlebars.escapeExpression(answer);
    var result = '<li class="collection-item">' + escaped_answer + '</li>';
    if (answer_count === correct_answer) {
        result = '<li class="collection-item teal lighten-3"><strong>' + escaped_answer + '</strong></li>';
    }
    return new Handlebars.SafeString(result);
});

html_template = Handlebars.compile(
    '<div class="card-panel blue-grey lighten-5">' +
        '<div class="action-buttons right">' +
            '<button class="question-button-edit waves-effect waves-teal btn-flat"><i class="material-icons">edit</i></button>' +
            '<button class="question-button-remove waves-effect waves-teal btn-flat"><i class="material-icons">delete</i></button>' +
        '</div>' +
        '<div class="black-text">' +
            '<span class="question-statement">{{question}}</span>' +
            '<ul class="collection">' +
                '{{boldIfCorrectAnswer answer_a 1 correct_answer}}' +
                '{{boldIfCorrectAnswer answer_b 2 correct_answer}}' +
                '{{boldIfCorrectAnswer answer_c 3 correct_answer}}' +
                '{{boldIfCorrectAnswer answer_d 4 correct_answer}}' +
            '</ul>' +
        '</div>' +
    '</div>');

container = $("#question-container");
QuestionList = new DataList("questionset/" + qset_id.toString(), "question", container, html_template, true);

QuestionList.load();

function add_question(){
    form.disable_button();

    var data = form.get_form_data();

    if (!data) {
        form.enable_button();
        return false;
    }

    data.correct_answer = parseInt($("input[type=radio][name=correct_answer]:checked").val());

    QuestionList.add(data, function (){
        form.enable_button();
        form.clear_form();
    });

    // to inhibit default behaviour (submit the form)
    return false;
}

form = new Form();
form.set_button($("#submit-button"));
form.add_field("question", $("#question"), [FormValidation.NotEmpty], "Xin nhap cau hoi");
form.add_field("answer_a", $("#answer_a"), [FormValidation.NotEmpty], "Xin nhap cau tra loi");
form.add_field("answer_b", $("#answer_b"), [FormValidation.NotEmpty], "Xin nhap cau tra loi");
form.add_field("answer_c", $("#answer_c"), [FormValidation.NotEmpty], "Xin nhap cau tra loi");
form.add_field("answer_d", $("#answer_d"), [FormValidation.NotEmpty], "Xin nhap cau tra loi");