from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile("config.py")
    from app import routes

    app.register_blueprint(routes.book_api)
    db.init_app(app)
    migrate.init_app(app, db)
    from app import models

    return app
