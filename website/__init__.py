from flask import Flask
from .keys import CONFIG_KEY

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = CONFIG_KEY

    from .views import views
    from .model import model
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(model, url_prefix="/")

    return app