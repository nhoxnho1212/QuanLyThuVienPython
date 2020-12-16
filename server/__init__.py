from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(fileConfig = None):
    app = Flask(__name__)
    app.config.from_object(fileConfig)
    db.init_app(app)

    with app.app_context():
        # from . import routes  # Import routes
        from server.api.routes import user_route
        from server.api.routes import book_route

        # from server.webApp import view
        db.create_all()  # Create sql tables for our data models

    return app
