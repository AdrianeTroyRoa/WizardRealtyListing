from .models import Person, Employee, Property, Address
   with app.app_context():
        db.create_all()
        db.session.commit()
