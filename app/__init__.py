from flask_wtf import CSRFProtect
from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config
from flask import Flask, render_template

login_manager = LoginManager()
bcrypt = Bcrypt()
csrf = CSRFProtect()

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager.init_app(app)
    bcrypt.init_app(app)

    csrf.init_app(app)

    login_manager.login_view = 'auth.connexion'
    login_manager.login_message = 'Connecte-toi pour accéder à cette page.'

    from app.auth.routes import auth
    app.register_blueprint(auth)

    from app.profil.routes import profil
    app.register_blueprint(profil)

    from app.decouverte.routes import decouverte
    app.register_blueprint(decouverte)
    
    from app.publication.routes import publication
    app.register_blueprint(publication)

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.get_by_id(int(user_id))

    @app.errorhandler(404)
    def page_non_trouvee(e):
        return render_template('404.html'); 404

    @app.errorhandler(500)
    def page_non_trouvee(e):
        return render_template('500.html'); 500
        
    return app