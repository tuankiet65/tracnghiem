begin_date = $("#begin-date").pickadate({
    format: "dd/mm/yyyy"
});

end_date = $("#end-date").pickadate({
    format: "dd/mm/yyyy"
});

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

form = new Form();
form.set_button($("#submit-button"));
form.add_field("title", $("#title"), [FormValidation.NotEmpty], "Hay nhap ten cuoc thi");
form.add_field("begin_date", $("#begin-date"), [FormValidation.NotEmpty], "Hay nhap ngay bat dau cuoc thi");
form.add_field("end_date", $("#end-date"), [FormValidation.NotEmpty], "Hay nhap ngay ket thuc cuoc thi");
form.add_field("duration", $("#duration"), [FormValidation.NotEmpty, FormValidation.IsInt], "Hay nhap thoi gian thi (phut)");

function QuestionSetsInput(question_sets, div){
    this.main_div = div;
    this.question_sets = question_sets;

    this.question_set_input_html = Handlebars.compile(
        "<div class='row'>" +
            "<div class='col m10'>" +
                "<div class='input-field'>" +
                    "<select class='question-sets-input-question-sets-select' data-input-id='{{id}}'>" +
                        "{{#each question_sets}}" +
                            "<option value='{{this.value.id}}'>{{this.value.name}}</option>" +
                        "{{/each}}" +
                    "</select>" +
                "</div>" +
            "</div>" +
            "<div class='col m2'>" +
                "<div class='input-field'>" +
                    "<input type='number' class='question-sets-input-question-sets-count' placeholder='Count'>" +
                "</div>" +
            "</div>"+
        "</div>"
    );

    this.return_value_textbox = $("<textbox class='question-sets-input-return-value'></textbox>").appendTo(this.main_div);
    this.set_input_div = $("<div class='question-sets-input-set-input'></div>").appendTo(this.main_div);
    this.add_set_button = $("<button class='question-sets-input-add-set waves-effect waves-light btn' type='button'>Them bo cau hoi</button>").appendTo(this.main_div);

    this.sets = [];
    this.sets_count = 0;

    this.add_set = function(){
        html = this.question_set_input_html({
            id: this.sets_count,
            question_sets: this.question_sets
        });

        element = $(html).appendTo(this.set_input_div);
        this.sets.push(element);
        this.sets_count++;

        $('select').material_select();
    }.bind(this);

    this.render_textbox = function(){
        value = [];
        for (i = 0; i < this.sets_count; i++){
            value.push({
                id: parseInt(this.sets[i].find('select.question-sets-input-question-sets-select').val()),
                count: parseInt(this.sets[i].find('input.question-sets-input-question-sets-count').val())
            })
        }

        this.return_value_textbox.val(JSON.stringify(value));
    };

    this.add_set_button.click(this.add_set);

    return this;
}

$.getJSON("/admin/ajax/questionset/get", function(data){
    this.qset_input = new QuestionSetsInput(data.entries, $("#question-sets-div"));

    form.add_field("question_set", this.qset_input.return_value_textbox, [FormValidation.NotEmpty, FormValidation.ValidJSON], "");

    this.add_contest = function() {
        qset_input.render_textbox();

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
}.bind(window));


