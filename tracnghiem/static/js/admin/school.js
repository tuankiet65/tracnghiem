html_template = Handlebars.compile(
    '<div class="card-panel blue-grey lighten-5">'+
        '<div class="action-buttons right">' +
            '<button class="school-button-edit waves-effect waves-teal btn-flat"><i class="material-icons">edit</i></button>' +
            '<button class="school-button-remove waves-effect waves-teal btn-flat"><i class="material-icons">delete</i></button>' +
        '</div>' +
        '<div class="black-text">'+
            '<h5>{{name}}</h5>' +
        '</div>' +
    '</div>');

SchoolList = DataList("school", $("#school-container"), html_template);

SchoolList.load();

function add_school(){
    data = {
        name: $("#name").val()
    }

    SchoolList.add(data, function(){
        $("#school-add-form")[0].reset();
    });

    return false;
}