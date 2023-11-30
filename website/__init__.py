from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'asecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Cscc21.1Best@db.zjroulizdphmthxvcwnb.supabase.co:5432/postgres'

    db.init_app(app)


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Person, Employee, Property, Address
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    login_manager.login_message = ''

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
