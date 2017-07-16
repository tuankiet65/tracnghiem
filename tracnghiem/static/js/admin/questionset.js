html_template = Handlebars.compile(
    '<div class="card-panel blue-grey lighten-5">' +
        '<div class="action-buttons right">' +
            '<a class="questionset-button-edit waves-effect waves-teal btn-flat" href="/admin/questionset/{{_id}}"><i class="material-icons">edit</i></a>' +
            '<button class="questionset-button-remove waves-effect waves-teal btn-flat"><i class="material-icons">delete</i></button>' +
        '</div>' +
        '<div class="black-text">' +
            '<h5>{{name}}</h5>' +
        '</div>' +
    '</div>');

container = $("#questionset-container");
QuestionSetList = new DataList("questionset", "questionset", container, html_template, true);

QuestionSetList.load();

function add_questionset(){
    form.disable_button();

    var input_data = form.get_form_data();

    if (!input_data) {
        form.enable_button();
        return false;
    }

    input_data.time = parseInt((new Date().getTime()) / 1000);

    QuestionSetList.add(input_data, function (){
        form.clear_form();
        form.enable_button();
    });

    // to inhibit default behaviour (submit the form)
    return false;
}

form = new Form();
form.set_button($("#submit-button"));
form.add_field("name", $("#name"), [FormValidation.NotEmpty], "Xin hay nhap tieu de");