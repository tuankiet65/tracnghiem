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

container = $("#announcement-container")
AnnouncementList = DataList("announcement", container, html_template, true);

AnnouncementList.load();

function add_announcement(){
    input_data = {
        title: $("#title").val(),
        content: $("#content").val(),
        time: parseInt((new Date().getTime())/1000)
    }

    AnnouncementList.add(input_data, function(){
        $("#announcement-add-form")[0].reset();
    });

    // to inhibit default behaviour (submit the form)
    return false;
}

function remove_announcement(){

}