import os

from flask import Flask

from views import bp as app_blueprint
from database import db


def create_app():
    flask_app = Flask(__name__)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite://")
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.app_context().push()
    db.init_app(flask_app)
    db.create_all()

    flask_app.register_blueprint(app_blueprint)

    return flask_app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
