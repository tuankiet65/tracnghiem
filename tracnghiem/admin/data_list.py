from json.decoder import JSONDecodeError

from flask import Flask, json, request, render_template
from werkzeug.datastructures import ImmutableMultiDict


class DataList:
    name = None

    template = None

    main = None
    get = None
    add = None
    remove = None

    def set_template(self, template):
        self.template = template

    def main_page(self):
        return render_template(self.template)

    def __init__(self, name, url = None):
        self.name = name
        if url is None:
            url = self.name
        self.main = {
            "url"     : "/{}".format(url),
            "name"    : "{}_main".format(name),
            "endpoint": self.main_page
        }
        self.get = {
            "url"     : "/ajax/{}/get".format(url),
            "name"    : "{}_get".format(name),
            "endpoint": None
        }
        self.add = {
            "url"     : "/ajax/{}/add".format(url),
            "name"    : "{}_add".format(name),
            "endpoint": None
        }
        self.remove = {
            "url"     : "/ajax/{}/remove".format(url),
            "name"    : "{}_remove".format(name),
            "endpoint": None
        }

    def main_func(self, func):
        self.main['endpoint'] = func
        return func

    # function signature:
    # def func(value) -> id of newly created id | None on error
    def add_func(self, func):
        def tmp(*args, **kwargs):
            try:
                value = request.form['data']
            except KeyError:
                return json.jsonify({
                    "status": "error, no data received"
                }), 400
            try:
                value = json.loads(value)
                value = ImmutableMultiDict(value)
            except JSONDecodeError:
                return json.jsonify({
                    "status": "invalid json data"
                }), 400
            id = func(value, *args, **kwargs)
            if id is not None:
                return json.jsonify({
                    "status": "ok",
                    "id"    : id
                })
            else:
                return json.jsonify({
                    "status": "error, can't add object"
                }), 500

        self.add['endpoint'] = tmp
        return tmp

    # function signature:
    # def func(): -> list of entries
    def get_func(self, func):
        def tmp(*args, **kwargs):
            entries = func(*args, **kwargs)
            return json.jsonify({
                "status" : "ok",
                "entries": [{"id": d['id'], "value": d['value']} for d in entries]
            })

        self.get['endpoint'] = tmp
        return tmp

    # function signature:
    # def func(): -> boolean
    def remove_func(self, func):
        def tmp(*args, **kwargs):
            try:
                id = int(request.form['id'])
            except ValueError:
                return json.jsonify({
                    "status": "id is not a number"
                }), 400
            except KeyError:
                return json.jsonify({
                    "status": "error, no id received"
                }), 404
            result = func(id, *args, **kwargs)
            if result:
                return json.jsonify({
                    "status": "ok"
                })
            else:
                return json.jsonify({
                    "status": "error, can't delete object"
                }), 500

        self.remove['endpoint'] = tmp
        return tmp

    def add_url_rule(self, f: Flask):
        if self.template is not None:
            f.add_url_rule(self.main['url'], endpoint = self.main['name'], view_func = self.main['endpoint'],
                           methods = ["GET"])
        if self.add['endpoint'] is not None:
            f.add_url_rule(self.add['url'], endpoint = self.add['name'], view_func = self.add['endpoint'],
                           methods = ["POST"])
        if self.get['endpoint'] is not None:
            f.add_url_rule(self.get['url'], endpoint = self.get['name'], view_func = self.get['endpoint'],
                           methods = ["GET"])
        if self.remove['endpoint'] is not None:
            f.add_url_rule(self.remove['url'], endpoint = self.remove['name'], view_func = self.remove['endpoint'],
                           methods = ["POST"])
