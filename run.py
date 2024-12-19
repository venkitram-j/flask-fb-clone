"""
Flask CLI/Application entry point.
"""
import os

from flask_fb_clone import create_app, db

app = create_app(os.getenv("APP_ENV", "testing"))
