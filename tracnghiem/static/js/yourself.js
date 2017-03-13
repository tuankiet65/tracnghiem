var ChangePasswordForm = new Form();
function SamePassword(value){
    pwd = $("#new_password").val();
    pwd_repeat = $("#new_password_repeat").val();

    return (pwd == pwd_repeat) && (FormValidation.StrongPassword(pwd));
}
ChangePasswordForm.add_field("old_password",
                             $("#old_password"),
                             [FormValidation.NotEmpty],
                             i18n.translate("Please enter your old password").fetch());
ChangePasswordForm.add_field("new_password",
                             $("#new_password"),
                             [FormValidation.NotEmpty, FormValidation.StrongPassword],
                             i18n.translate("Your password is too weak ").fetch());
ChangePasswordForm.add_field("new_password_repeat",
                             $("#new_password_repeat"),
                             [FormValidation.NotEmpty, FormValidation.StrongPassword],
                             i18n.translate("Password either is not the same or too weak").fetch());
ChangePasswordForm.set_button($("#password-change-button"));
function change_password(){
    ChangePasswordForm.disable_button();

    input_data = ChangePasswordForm.get_form_data();

    if (!input_data){
        ChangePasswordForm.enable_button();
        return false;
    }

    $.post("/yourself/change_password", input_data, function(data){
        if (data.error == "incorrect old password"){
            Materialize.toast(i18n.translate("Incorrect old password").fetch(), 5000);
        } else {
            Materialize.toast(i18n.translate("Password changed successfully. You'll be logged out...").fetch(), 5000);
            setTimeout(function(){
                location.reload();
            }, 2000);
        }
        ChangePasswordForm.enable_button();
    })

    return false;
}

var EditProfileForm = new Form();
EditProfileForm.add_field("name",
                          $("#edit_name"),
                          [FormValidation.NotEmpty],
                          i18n.translate("Please fill in your name").fetch());
EditProfileForm.add_field("school",
                          $("#edit_school"),
                          [FormValidation.NotEmpty],
                          i18n.translate("Please choose your school").fetch());
EditProfileForm.add_field("klass",
                          $("#edit_klass"),
                          [FormValidation.NotEmpty],
                          i18n.translate("Please fill in your class").fetch());
EditProfileForm.set_button($("#edit-profile-button"));
function edit_profile(){
    EditProfileForm.disable_button();

    input_data = EditProfileForm.get_form_data();

    if (!input_data){
        EditProfileForm.enable_button();
        return false;
    }

    $.post("/yourself/edit_profile", input_data, function(data){
        Materialize.toast(i18n.translate("Profile edited successfully").fetch(), 5000);
        EditProfileForm.enable_button();
        location.reload();
    })

    return false;
}