from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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

#    from .models import Person, Client, Employee, Property, Address, PersonAddress, PropertyAddress 
#    with app.app_context():
#        db.create_all()
#        db.session.commit()

    return app
