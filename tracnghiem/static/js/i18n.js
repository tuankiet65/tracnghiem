gettext = function(i18n_json){

    this.i18n_json_link = i18n_json;
    this.dictionary = {};

    _ = function(str){
        return this.dictionary[str];
    }

    init = function(callback){
        $.getJSON(this.i18n_json_link, function(data){
            this.dictionary = data;
            callback();
        }.bind(this))
    }

    return this;
}