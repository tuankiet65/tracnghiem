from .common import generate_random_string
import os
import subprocess
import dateutil.tz

class Config:
    WTF_CSRF_ENABLED = True

    RECAPTCHA_PUBLIC_KEY = "6LfWFRQUAAAAAEgmWWE8_AcZyt0tlJ4ns1v_GabY"
    RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY")

    SENTRY_FRONTEND_DSN = 'https://ef69ff9bf83c4f7a986986a467c5ef77@sentry.io/135701'
    SENTRY_BACKEND_DSN = 'https://55aef6867d17453282d5c8b951003976:457b1673dfd747fdbe94aa33e1e6fe18@sentry.io/135702'

    GIT_REVISION = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode("utf-8").strip()

    DB_HOST = os.environ.get("MYSQL_DB_HOST")
    DB_USERNAME = os.environ.get("MYSQL_DB_USERNAME")
    DB_PASSWORD = os.environ.get("MYSQL_DB_PASSWORD")
    DB_DATABASE = os.environ.get("MYSQL_DB_DATABASE")

    TIMEZONE = dateutil.tz.gettz("Asia/Ho_Chi_Minh")

class DevelopmentConfig(Config):
    IS_PRODUCTION = False
    SECRET_KEY = "lol"

    DEBUG = True
    SERVER_NAME = "dev.env:5000"


class ProductionConfig(Config):
    IS_PRODUCTION = True
    SECRET_KEY = generate_random_string()

    DEBUG = False
    SERVER_NAME = "thi.quandoansontra.com"
