html_template = Handlebars.compile(
    '<div class="card-panel blue-grey lighten-5">'+
        '<div class="action-buttons right">' +
            '<button class="question-button-edit waves-effect waves-teal btn-flat"><i class="material-icons">edit</i></button>' +
            '<button class="question-button-remove waves-effect waves-teal btn-flat"><i class="material-icons">delete</i></button>' +
        '</div>' +
        '<div class="black-text">'+
            '<h5>{{question}}</h5>' +
            '<p>{{answer_a}}</p>' +
            '<p>{{answer_b}}</p>' +
            '<p>{{answer_c}}</p>' +
            '<p>{{answer_d}}</p>' +
            '<p>{{correct_answer}}</p>' +
        '</div>' +
    '</div>');

container = $("#question-container")
QuestionList = DataList("questionset/" + qset_id.toString(), "question", container, html_template, true);

QuestionList.load();

function add_question(){
    form.disable_button();

    data = form.get_form_data();

    if (!data){
        form.enable_button();
        return false;
    }

    data.correct_answer = parseInt($("input[type=radio][name=correct_answer]:checked").val());

    QuestionList.add(data, function(){
        form.enable_button();
        form.clear_form();
    });

    // to inhibit default behaviour (submit the form)
    return false;
}

form = Form();
form.set_button($("#submit-button"));
form.add_field("question", $("#question"), [FormValidation.NotEmpty], "Xin nhap cau hoi");
form.add_field("answer_a", $("#answer_a"), [FormValidation.NotEmpty], "Xin nhap cau tra loi");
form.add_field("answer_b", $("#answer_b"), [FormValidation.NotEmpty], "Xin nhap cau tra loi");
form.add_field("answer_c", $("#answer_c"), [FormValidation.NotEmpty], "Xin nhap cau tra loi");
form.add_field("answer_d", $("#answer_d"), [FormValidation.NotEmpty], "Xin nhap cau tra loi");