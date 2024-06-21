from flask import Flask
from flask_login import LoginManager

app = Flask(
    __name__, template_folder="../templates", static_folder="../templates/static"
)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "abc"

login_manager = LoginManager()
login_manager.init_app(app)

import routes
import models
import views
