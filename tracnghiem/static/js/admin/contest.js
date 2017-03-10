begin_date = $("#begin-date").pickadate({
    format: "dd/mm/yyyy"
})

end_date = $("#end-date").pickadate({
    format: "dd/mm/yyyy"
})

html_template = Handlebars.compile(
    '<div class="card-panel blue-grey lighten-5">'+
        '<div class="action-buttons right">' +
            '<a class="contest-button-edit waves-effect waves-teal btn-flat">' +
                '<i class="material-icons">edit</i>' +
            '</a>' +
            '<button class="contest-button-remove waves-effect waves-teal btn-flat"><i class="material-icons">delete</i></button>' +
        '</div>' +
        '<div class="black-text">'+
            '<h5>{{title}}</h5>' +
        '</div>' +
    '</div>');

ContestList = DataList("contest", "contest", $("#contest-container"), html_template);

ContestList.load();

function add_contest(){
    form.disable_button();

    data = form.get_form_data();
    if (!data){
        form.enable_button();
        return false;
    }

    ContestList.add(data, function(){
        form.enable_button();
        form.clear_form();
    });

    return false;
}

form = Form();
form.set_button($("#submit-button"));
form.add_field("title", $("#title"), [FormValidation.NotEmpty], "Hay nhap ten cuoc thi");
form.add_field("begin_date", $("#begin-date"), [FormValidation.NotEmpty], "Hay nhap ngay bat dau cuoc thi");
form.add_field("end_date", $("#end-date"), [FormValidation.NotEmpty], "Hay nhap ngay ket thuc cuoc thi");
form.add_field("duration", $("#duration"), [FormValidation.NotEmpty, FormValidation.IsInt], "Hay nhap thoi gian thi (phut)");
form.add_field("question_count", $("#question-count"), [FormValidation.NotEmpty, FormValidation.IsInt], "Hay nhap so luong cau hoi");
form.add_field("question_set", $("#question-set"), [FormValidation.NotEmpty, FormValidation.ValidJSON], "give me question set");

