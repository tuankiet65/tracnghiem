html_template = Handlebars.compile(
    '<div class="card-panel blue-grey lighten-5">'+
        '<div class="action-buttons right">' +
            '<button class="announcement-button-edit waves-effect waves-teal btn-flat"><i class="material-icons">edit</i></button>' +
            '<button class="announcement-button-remove waves-effect waves-teal btn-flat"><i class="material-icons">delete</i></button>' +
        '</div>' +
        '<div class="black-text">'+
            '<h5>{{title}}</h5>' +
            '<p>{{content}}</p>' +
            '<small class="announcement-time">Thong bao duoc dang vao luc {{time}}</small>'+
        '</div>' +
    '</div>');

container = $("#announcement-container");
AnnouncementList = new DataList("announcement", "announcement", container, html_template, true);

AnnouncementList.load();

function add_announcement(){
    form.disable_button();

    var input_data = form.get_form_data();

    if (!input_data){
        form.enable_button();
        return false;
    }

    input_data.time = parseInt((new Date().getTime())/1000);

    AnnouncementList.add(input_data, function(){
        form.clear_form();
        form.enable_button();
    });

    // to inhibit default behaviour (submit the form)
    return false;
}

form = new Form();
form.set_button($("#submit-button"));
form.add_field("title", $("#title"), [FormValidation.NotEmpty], "Xin hay nhap tieu de");
form.add_field("content", $("#content"), [FormValidation.NotEmpty], "Xin hay nhap noi dung");