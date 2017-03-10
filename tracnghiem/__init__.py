from flask import Flask
import os

app = Flask(__name__)

if os.environ.get("IS_PRODUCTION") is not None:
    print("Running in production, activating production configurations")
    from tracnghiem.config import ProductionConfig as Config
else:
    print("Running in development, activating development configurations")
    from tracnghiem.config import DevelopmentConfig as Config

app.config.from_object(Config)