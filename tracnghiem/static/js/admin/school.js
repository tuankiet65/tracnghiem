html_template = Handlebars.compile(
    '<div class="card-panel blue-grey lighten-5">' +
        '<div class="action-buttons right">' +
            '<button class="school-button-edit waves-effect waves-teal btn-flat"><i class="material-icons">edit</i></button>' +
            '<button class="school-button-remove waves-effect waves-teal btn-flat"><i class="material-icons">delete</i></button>' +
        '</div>' +
        '<div class="black-text">' +
            '<h5>{{name}}</h5>' +
        '</div>' +
    '</div>');

SchoolList = new DataList("school", "school", $("#school-container"), html_template);

SchoolList.load();

function add_school(){
    form.disable_button();

    var data = form.get_form_data();

    if (!data) {
        form.enable_button();
        return false;
    }

    SchoolList.add(data, function (){
        form.clear_form();
        form.enable_button();
    });

    return false;
}

form = new Form();
form.set_button($("#submit-button"));
form.add_field("name", $("#name"), [FormValidation.NotEmpty], "Xin hay nhap ten truong");
