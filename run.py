"""Flask CLI/Application entry point."""
import os

from src.flask_fb_clone import create_app, db
from src.flask_fb_clone.models.user import User

app = create_app(os.getenv("APP_ENV", "development"))


@app.shell_context_processor
def shell():
    return {"db": db, "User": User}
