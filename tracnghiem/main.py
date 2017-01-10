from flask import Flask, render_template

from .database import Announcement, create_all_tables

app = Flask(__name__)

@app.route("/")
def index():
    announcements = (Announcement
                     .select()
                     .order_by(- Announcement.time))
    return render_template("index.html", announcements = announcements)

# TODO: This should only run when debug is True
@app.route("/create_tables")
def burn():
    create_all_tables()
    return 'ok'