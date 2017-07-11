import datetime
import os
import subprocess

import dateutil.tz


class Config:
    WTF_CSRF_ENABLED = True

    RECAPTCHA_PUBLIC_KEY = "6LfosygUAAAAAOcX1BtG2ibi2ozRqokBpAct2JNQ"
    RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY")

    SENTRY_FRONTEND_DSN = 'https://bb61196bb09e40beaaedcc6d22487f96@sentry.io/190334'
    SENTRY_BACKEND_DSN = 'https://c3ebac7dea0440f59c042a47261f6183:86a80b3d4ae744988df78402e2479ea4@sentry.io/190335'

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
    IS_PRODUCTION = False

    DEBUG = True
    SERVER_NAME = "dev.env:5000"


class ProductionConfig(Config):
    IS_PRODUCTION = True

    DEBUG = False
    SERVER_NAME = "dtncatp.tuankiet65.moe"
