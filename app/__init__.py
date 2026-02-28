from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config

login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager.init_app(app)
    bcrypt.init_app(app)

    login_manager.login_view = 'auth.connexion'
    login_manager.login_message = 'Connecte-toi pour accéder à cette page.'

    from app.auth.routes import auth
    app.register_blueprint(auth)

    from app.profil.routes import profil
    app.register_blueprint(profil)


    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.get_by_id(int(user_id))
    return app