from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    if app.config['ENV'] == 'production':
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../development.db'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    from .models import db, init_db
    db.init_app(app)
    app.cli.add_command(init_db)

    from .views import root
    app.register_blueprint(root)

    return app
