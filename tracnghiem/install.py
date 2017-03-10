from flask import Blueprint, render_template, url_for, redirect
import os.path
from flask_wtf import FlaskForm
from wtforms import *

from .database import create_all_tables
from .admin.database import create_all_tables as admin_create_all_tables, AdminUser

install = Blueprint("install", __name__, url_prefix = "/install")


@install.route("/", methods = ["GET", "POST"], endpoint = "index")
def install_route():
    class FirstAdminForm(FlaskForm):
        username = StringField(validators = [validators.DataRequired()])
        password = PasswordField(validators = [validators.DataRequired()])

    if os.path.isfile(".installed"):
        return redirect(url_for("index"))

    form = FirstAdminForm()
    if form.validate_on_submit():
        create_all_tables()
        admin_create_all_tables()
        AdminUser.create(username = form.username.data,
                         password = form.password.data)
        with open(".installed", "w") as f:
            f.write("installed")
        return redirect(url_for("index"))
    else:
        return render_template("install.html")
