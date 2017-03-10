var FormValidation = {
    StrongPassword: function(value){
        result = zxcvbn(value);
        return (result.score >= 3)
    },

    NotEmpty: function(value){
        return (value.length > 0)
    },

    SelectNotDefault: function(value){
        return (value.length != "0")
    },

    IsInt: function(value){
        return !(Number.isNaN(parseInt(value, 10)))
    },

    ValidJSON: function(value){
        try {
            v = JSON.parse(value);
            return true;
        } catch (SyntaxError) {
            return false;
        }
    }
}

var Form = function(){
    fields = {};
    submit_button = null;

    add_field = function(field_name, element, validations, warning){
        if (!($.isArray(validations))){
            throw "[Form] 'validations' must be an array (even if it only includes one validation)";
        }

        if (!(element instanceof jQuery)){
            throw "[Form] 'element' must be a jQuery object"
        }

        this.fields[field_name] = {
            element: element,
            validations: validations,
            warning: warning
        }

        element.addClass("validate");
        element.siblings("label").attr("data-error", warning);
        element.focusout($.proxy(function(event){
            event.stopPropagation(); // prevent changes from Materialize js
            this._validate_field(this.fields[field_name], true, false);
        }, this));
        if (element.hasClass("datepicker")){
            element.change($.proxy(function(event){
                console.log("change date called");
                event.stopPropagation(); // prevent changes from Materialize js
                this._validate_field(this.fields[field_name], true, false);
            }, this));
        }
    }

    // Because validate_field conflicts with a function in Materialize.css
    _validate_field = function(field, toggle_html_error, focus){
        element = field.element;
        value = element.val();
        console.log(element);
        console.log(field.validations.length);
        for (i = 0; i < field.validations.length; i++){
            if (!(field.validations[i](value))){
                if (toggle_html_error){
                    console.log("change");
                    element.removeClass("invalid valid").addClass("invalid");
                    if (focus){
                        if (element.hasClass("datepicker")){
                            element.click();
                        } else {
                            element.focus();
                        }
                        $('html, body').animate({
                            scrollTop: element.offset().top-100
                        }, 100);
                    }
                }
                return false;
            }
        }
        console.log("passed");
        if (toggle_html_error){
            element.removeClass("invalid valid").addClass("valid");
        }
        return true;
    }

    validate_form = function(){
        console.log("called");
        console.log(this.fields);
        for (field_name in this.fields){
            console.log(field_name);
            field = this.fields[field_name];
            console.log(field);
            if (!this._validate_field(field, true, true)){
                return false;
            }
        }
        console.log("end");
        return true;
    };

    get_form_data = function(){
        data = null;
        if (this.validate_form()){
            data = {};
            for (field_name in this.fields){
                data[field_name] = this.fields[field_name].element.val();
            }
        }
        return data;
    }

    clear_form = function(){
        for (field_name in this.fields){
            this.fields[field_name].element.val("").removeClass("invalid valid");
        }
    }.bind(this);

    set_button = function(elem){
        this.submit_button = elem;
    }

    disable_button = function(){
        this.submit_button.prop("disabled", true);
    }

    enable_button = function(){
        this.submit_button.prop("disabled", false);
    }

    return this;
}