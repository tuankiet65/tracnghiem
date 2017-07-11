from flask import request, json as fjson
from tracnghiem.authentication import login
from tracnghiem.database import Account

# name    : admin.util_login_as
# endpoint: admin/util/login_as
def login_as():
    try:
        username = request.form['username']
    except KeyError:
        return fjson.jsonify({
            "result": False
        })
    try:
        account = Account.get(username = username)
    except Account.DoesNotExist:
        return fjson.jsonify({
            "result": False
        })
    login(account)
    return fjson.jsonify({
        "result": True
    })