// https://stackoverflow.com/questions/948172/password-strength-meter
function scorePassword(pass) {
    var score = 0;
    if (!pass)
        return score;

    // award every unique letter until 5 repetitions
    var letters = Object();
    for (var i=0; i<pass.length; i++) {
        letters[pass[i]] = (letters[pass[i]] || 0) + 1;
        score += 5.0 / letters[pass[i]];
    }

    // bonus points for mixing it up
    var variations = {
        digits: /\d/.test(pass),
        lower: /[a-z]/.test(pass),
        upper: /[A-Z]/.test(pass),
        nonWords: /\W/.test(pass)
    };

    variationCount = 0;
    for (var check in variations) {
        variationCount += (variations[check] === true) ? 1 : 0;
    }
    score += (variationCount - 1) * 10;

    return parseInt(score);
}

var FormValidation = {
    StrongPassword: function(value){
        if (!value){
            return false;
        }
        result = scorePassword(value)
        return (result >= 45)
    },

    NotEmpty: function(value){
        if (!value){
            return false;
        }
        return (value.length > 0)
    },

    SelectNotDefault: function(value){
        if (!value){
            return false;
        }
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

function Form(){
    this.fields = {};
    this.submit_button = null;

    this.add_field = function(field_name, element, validations, warning){
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
                event.stopPropagation(); // prevent changes from Materialize js
                this._validate_field(this.fields[field_name], true, false);
            }, this));
        }
    }

    // Because validate_field conflicts with a function in Materialize.css
    this._validate_field = function(field, toggle_html_error, focus){
        element = field.element;
        value = element.val();
        for (i = 0; i < field.validations.length; i++){
            if (!(field.validations[i](value))){
                if (toggle_html_error){
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
        if (toggle_html_error){
            element.removeClass("invalid valid").addClass("valid");
        }
        return true;
    }

    this.validate_form = function(){
        for (field_name in this.fields){
            field = this.fields[field_name];
            if (!this._validate_field(field, true, true)){
                return false;
            }
        }
        return true;
    };

    this.get_form_data = function(){
        data = null;
        if (this.validate_form()){
            data = {};
            for (field_name in this.fields){
                data[field_name] = this.fields[field_name].element.val();
            }
        }
        return data;
    }

    this.clear_form = function(){
        for (field_name in this.fields){
            this.fields[field_name].element.val("").removeClass("invalid valid");
        }
    }.bind(this);

    this.set_button = function(elem){
        this.submit_button = elem;
    }

    this.disable_button = function(){
        this.submit_button.prop("disabled", true);
    }

    this.enable_button = function(){
        this.submit_button.prop("disabled", false);
    }

    return this;
}