import os

from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

from api.database import db
from api.views import bp as app_blueprint


def create_app():
    flask_app = Flask(__name__)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URLDATABASE_URLDATABASE_URLDATABASE_URLDATABASE_URL", "sqlite://")
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.app_context().push()
    db.init_app(flask_app)
    db.create_all()

    swaggerui_blueprint = get_swaggerui_blueprint(
        '/swagger',
        '/static/swagger.yml',
        config={
            'app_name': "Fizzbuzz web server"
        }
    )
    flask_app.register_blueprint(swaggerui_blueprint, url_prefix='/swagger')
    flask_app.register_blueprint(app_blueprint)

    return flask_app


