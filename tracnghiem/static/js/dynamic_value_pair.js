function ValuePair(id, select_values){
    this.id = id;

    this.html_template = Handlebars.compile(' \
        <div class="row" class="value-pair" data-id="{{id}}"> \
            <div class="col m3"> \
                <input type="number" class="value-pair-first" placeholder="No of questions"> \
            </div> \
            <div class="col m9"> \
                <select id="reg_school" name="value-pair-second"> \
                {{#each select_values}}
                    <option value="{{ school[0] }}">{{ school[1] }}</option>
                </select> \
            </div> \
        </div> \
    ")

    this.render = function(container){
        html = this.html_template(this.id);
        container.append(html);

        this.element = $(".value-pair[data-id=" + this.id.toString() + "]");
    }

    this.get = function(){
        return {
            "first": this.element.blah;
            "second": this.element.blah;
        }
    }

    return this;
}
function DynamicValuePair(container, select_values){
    this.container = $(container);
    this.value_pair_groups = []
    this.select_values = select_values;

    for (i = 0; i < 6; i++){
        this.value_pair_groups.append(new ValuePair(i, this.select_values))
    }

    this.get = function(){

    }
    return this;
}

