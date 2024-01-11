from flask import Flask
from .views import blue

def create_app():
    app = Flask(__name__)

    app.register_blueprint(blueprint=blue)
    # from . import routes
    # app.register_blueprint(routes.bp)

    # 防止报错
    # The session is unavailable because no secret key was set.
    # Set the secret_key on the application to something unique and secret.
    app.secret_key = 'this is my secret_key'
    return app
