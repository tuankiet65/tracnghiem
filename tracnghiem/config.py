import datetime
import os
import subprocess

import dateutil.tz


class Config:
    WTF_CSRF_ENABLED = True

    RECAPTCHA_PUBLIC_KEY = "6LfWFRQUAAAAAEgmWWE8_AcZyt0tlJ4ns1v_GabY"
    RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY")

    SENTRY_FRONTEND_DSN = 'https://1b5f9102075941d3a42d3d5eb8ea6dd3@sentry.io/135701'
    SENTRY_BACKEND_DSN = 'https://6a249ba9277548ba9be632ea6fdb6359@sentry.io/135702'

    GIT_REVISION = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode("utf-8").strip()

    DB_HOST = os.environ.get("MYSQL_DB_HOST")
    DB_USERNAME = os.environ.get("MYSQL_DB_USERNAME")
    DB_PASSWORD = os.environ.get("MYSQL_DB_PASSWORD")
    DB_DATABASE = os.environ.get("MYSQL_DB_DATABASE")

    TIMEZONE = dateutil.tz.gettz("Asia/Ho_Chi_Minh")

    FRIENDLY_TIMEZONE = datetime.datetime.now(TIMEZONE).tzname()

    SECRET_KEY = os.environ.get("SECRET_KEY")

    LOCALE = "vi"


class DevelopmentConfig(Config):
    ENV = "development"


class ProductionConfig(Config):
    ENV = "production"
    SERVER_NAME = "thi.quandoansontra.org.vn"
