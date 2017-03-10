function DataList(url, name, container, render_data_func, prepend){
    this.html_content_render = render_data_func;
    this.container = $(container);
    this.name = name;
    this.url = url;
    this.prepend = prepend;

    this.ajax_get = "/admin/ajax/" + this.url + "/get";
    this.ajax_add = "/admin/ajax/" + this.url + "/add";
    this.ajax_remove = "/admin/ajax/" + this.url + "/remove";

    this.wrapper = Handlebars.compile("<div class='"+ this.name + "-entry-wrapper' data-id='{{{id}}}'> {{{html}}} </div>");

    this.render = function(id, value){
        value["_id"] = id;
        content_html = this.html_content_render(value);
        complete_html = this.wrapper({
            id: id,
            html: content_html
        });
        if (!prepend) {
            this.container.append(complete_html);
        } else {
            this.container.prepend(complete_html);
        }
        element = $("."+this.name+"-entry-wrapper[data-id=\""+id+"\"]");
        edit_button = element.find("."+this.name+"-button-edit");

        remove_button = element.find("."+this.name+"-button-remove");
        console.log(remove_button);
        edit_button.click(this.edit);
        remove_button.click(this.remove);
    }

    this.load = function(){
        $.getJSON(this.ajax_get, $.proxy(function(data){
            console.log(data);
            for (i = 0; i < data.entries.length; i++){
                id = data.entries[i].id;
                value = data.entries[i].value;

                this.render(id, value);
            }
        }, this))
    }

    this.add = $.proxy(function(value, callback){
        $.post(this.ajax_add, {data: JSON.stringify(value)}, $.proxy(function(response){
            this.render(response.id, value);
            callback();
        }, this))
    }, this);

    this.remove = function(id){
        element = $(".entry-wrapper[data-id=\"" + id + "\"]");
        element.remove();
    }

    this.edit = function(){
        return true;
    }

    this.remove = $.proxy(function(event){
        console.log("remove button pressed");
        button = $(event.currentTarget);

        offending_entry = button.closest("."+this.name+"-entry-wrapper");
        id = offending_entry.data("id");

        // TODO: i18n
        swal({
            title: "Delete this?",
            text: "Are you sure want to delete this?",
            type: "warning",
            showCancelButton: true,
            confirmButtonText: 'Yes'
        }).then(
            $.proxy(function(){
                $.post(this.ajax_remove, {id: id}, function(){
                    offending_entry.remove();
                })
            }, this),
            function(){}
        );
    }, this);

    return this;
}