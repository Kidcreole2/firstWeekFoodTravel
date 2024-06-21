from flask import Flask
from flask_login import LoginManager
from flask_simple_captcha import CAPTCHA

app = Flask(
    __name__, template_folder="../templates", static_folder="../templates/static"
)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "abc"

DEFAULT_CONFIG = {
    'SECRET_CAPTCHA_KEY': 'LONGKEY',  # use for JWT encoding/decoding

    'EXPIRE_SECONDS': 60 * 10,  # takes precedence over EXPIRE_MINUTES
    'CAPTCHA_IMG_FORMAT': 'JPEG',  # 'PNG' or 'JPEG' (JPEG is 3X faster)

    'CAPTCHA_LENGTH': 6,  # Length of the generated CAPTCHA text
    'CAPTCHA_DIGITS': False,  # Should digits be added to the character pool?
    'EXCLUDE_VISUALLY_SIMILAR': True,  # Exclude visually similar characters
    'BACKGROUND_COLOR': (0, 0, 0),  # RGB(A?) background color (default black)
    'TEXT_COLOR': (255, 255, 255),  # RGB(A?) text color (default white)

    'ONLY_UPPERCASE': True, # Only use uppercase characters
    #'CHARACTER_POOL': 'AaBb',  # Use a custom character pool
}

SIMPLE_CAPTCHA = CAPTCHA(config=DEFAULT_CONFIG)
SIMPLE_CAPTCHA.init_app(app=app)

login_manager = LoginManager()
login_manager.init_app(app)

import routes
import models
import views
