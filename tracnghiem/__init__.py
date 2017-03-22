import os

from flask import Flask, render_template
from flask_babel import gettext as _
from werkzeug.exceptions import *

app = Flask(__name__)

#################
# Configuration #
#################

if os.environ.get("IS_PRODUCTION") is not None:
    print("Running in production, activating production configurations")
    from tracnghiem.config import ProductionConfig as Config
else:
    print("Running in development, activating development configurations")
    from tracnghiem.config import DevelopmentConfig as Config

app.config.from_object(Config)


################################
# Error handling configuration #
################################

@app.errorhandler(NotFound)
def error_404(e):
    return render_template("error_template.html",
                           error_code = 404,
                           error_name = _("Page not found"),
                           error_message = _("The page you're looking for does not exists."),
                           image_caption = _(
                               "Here's a cute Hatsune Miku because we like it.<br />Not really related, but whatever."),
                           image = "images/miku.jpg"), 404


@app.errorhandler(BadRequest)
def error_400(e):
    return render_template("error_template.html",
                           error_code = 400,
                           error_name = _("Bad request"),
                           error_message = _("Your request couldn't be understood by the server."),
                           image_caption = _(
                               "Patchouli Knowledge is not happy that you might be doing nasty things to the server."),
                           image = "images/patchouli.jpg"), 400


@app.errorhandler(Forbidden)
def error_403(e):
    return render_template("error_template.html",
                           error_code = 403,
                           error_name = _("Forbidden"),
                           error_message = _(
                               "You just tried to access something which you don't have the required permission to do so."),
                           image_caption = _(
                               "Patchouli Knowledge is not happy that you might be doing nasty things to the server."),
                           image = "images/patchouli.jpg"), 403


@app.errorhandler(InternalServerError)
def error_500(e):
    return render_template("error_template.html",
                           error_code = 500,
                           error_name = _("Internal Server Error"),
                           error_message = _(
                               "The server encountered an internal error and was unable to complete your request."),
                           image_caption = _("Flandre Scarlet is sad because she couldn't fulfill this request <br />"
                                             "(don't worry though, we have been notified of this issue and will "
                                             "try to fix this issue as soon as possible)"),
                           image = "images/sad_flandre.jpg"), 500
