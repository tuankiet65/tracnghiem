function DataList(url, name, container, render_data_func, prepend){
    this.html_content_render = render_data_func;
    this.container = $(container);
    this.name = name;
    this.url = url;
    this.prepend = prepend;

    this.ajax_get = "/admin/ajax/" + this.url + "/get";
    this.ajax_add = "/admin/ajax/" + this.url + "/add";
    this.ajax_remove = "/admin/ajax/" + this.url + "/remove";

    this.wrapper = Handlebars.compile("<div class='" + this.name + "-entry-wrapper' data-id='{{{id}}}'> {{{html}}} </div>");

    this.render = function (id, value){
        value["_id"] = id;
        var content_html = this.html_content_render(value);
        var complete_html = this.wrapper({
            id: id,
            html: content_html
        });
        if (!prepend) {
            this.container.append(complete_html);
        } else {
            this.container.prepend(complete_html);
        }
        var element = $("." + this.name + "-entry-wrapper[data-id=\"" + id + "\"]");
        var edit_button = element.find("." + this.name + "-button-edit");

        var remove_button = element.find("." + this.name + "-button-remove");
        edit_button.click(this.edit);
        remove_button.click(this.remove);
    };

    this.load = function (){
        $.getJSON(this.ajax_get, function (data){
            for (var i = 0; i < data.entries.length; i++) {
                var id = data.entries[i].id;
                var value = data.entries[i].value;

                this.render(id, value);
            }
        }.bind(this))
    };

    this.add = function (value, callback){
        $.post(this.ajax_add, {data: JSON.stringify(value)}, function (response){
            this.render(response.id, value);
            callback();
        }.bind(this))
    }.bind(this);

    this.remove = function (id){
        var element = $(".entry-wrapper[data-id=\"" + id + "\"]");
        element.remove();
    };

    this.edit = function (){
        return true;
    };

    this.remove = function (event){
        var button = $(event.currentTarget);

        var offending_entry = button.closest("." + this.name + "-entry-wrapper");
        var id = offending_entry.data("id");

        // TODO: i18n
        Swal.fire({
            title: "Delete this?",
            text: "Are you sure want to delete this?",
            type: "warning",
            showCancelButton: true,
            confirmButtonText: 'Yes'
        }).then(function (result) {
            if (result.value) {
                $.post(this.ajax_remove, {id: id}, function (){
                    offending_entry.remove();
                });
            }
        }.bind(this));
    }.bind(this);

    return this;
}
