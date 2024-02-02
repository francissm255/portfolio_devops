import os
from portfolio import Flask
from flask_migrate import Migrate

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    from yourapplication.model import db
    db.init_app(app)

    from yourapplication.views.admin import admin
    from yourapplication.views.frontend import frontend
    app.register_blueprint(admin)
    app.register_blueprint(frontend)

    return app

# def create_app(test_config=None):
#     app = Flask(__name__, instance_relative_config=True)
#     app.config.from_mapping(
#         SECRET_KEY='dev',
#         SQLALCHEMY_DATABASE_URI='postgresql://postgres@localhost:5432/tr_speedrunning2',
#         SQLALCHEMY_TRACK_MODIFICATIONS=False,
#         SQLALCHEMY_ECHO=True
#     )