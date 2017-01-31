from flask import Flask, json, request, render_template
from json.decoder import JSONDecodeError

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

    def __init__(self, name):
        self.name = name
        self.main = {
            "url": "/{}".format(name),
            "name": "{}_main".format(name),
            "endpoint": self.main_page
        }
        self.get = {
            "url": "/ajax/{}/get".format(name),
            "name": "{}_get".format(name),
            "endpoint": None
        }
        self.add = {
            "url": "/ajax/{}/add".format(name),
            "name": "{}_add".format(name),
            "endpoint": None
        }
        self.remove = {
            "url": "/ajax/{}/remove".format(name),
            "name": "{}_remove".format(name),
            "endpoint": None
        }

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
            except JSONDecodeError:
                return json.jsonify({
                    "status": "invalid json data"
                }), 400
            id = func(value)
            if id is not None:
                return json.jsonify({
                    "status": "ok",
                    "id": id
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
                "status": "ok",
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
            result = func(id)
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
        f.add_url_rule(self.main['url'], endpoint = self.main['name'], view_func = self.main['endpoint'],
                       methods = ["GET"])
        f.add_url_rule(self.add['url'], endpoint = self.add['name'], view_func = self.add['endpoint'], methods=["POST"])
        f.add_url_rule(self.get['url'], endpoint = self.get['name'], view_func = self.get['endpoint'], methods=["GET"])
        f.add_url_rule(self.remove['url'], endpoint = self.remove['name'], view_func = self.remove['endpoint'], methods=["POST"])