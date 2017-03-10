import requests
from urllib.parse import urlencode, urlunsplit

class FacebookLoginFlow:
    # https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow
    client_id = None
    client_secret = None
    redirect_uri = None

    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def build_facebook_login_url(self):
        # TODO
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            # "state": "<CSRF token here>"
            "response_type": "code",
            "scope": "public_profile"
        }
        params = urlencode(params)
        return urlunsplit(("https", "www.facebook.com", "v2.8/dialog/oauth", params, ""))

    def build_facebook_code_to_access_token_url(self, code):
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "code": code
        }
        params = urlencode(params)
        return urlunsplit(("https", "graph.facebook.com", "v2.8/oauth/access_token", params, ""))

    def code_to_user_id(self, code):
        access_token = self.code_to_access_token(code)
        req = requests.get("https://graph.facebook.com/me")
        return req.json()['id']

    def code_to_access_token(self, code):
        url = self.build_facebook_code_to_access_token_url(code)
        req = requests.get(url)
        return req.json()['access_token']
