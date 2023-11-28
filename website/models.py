from . import db
from sqlalchemy.sql import func
from flask_login import UserMixin

class Person(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    middle_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20), nullable=False)
    name_append = db.Column(db.String(20))
    email_address = db.Column(db.String(20), nullable=False, unique=True)
    date_of_birth = db.Column(db.Date)
    date_account = db.Column(db.DateTime(timezone=True), default=func.now())
    is_male = db.Column(db.Boolean)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), unique=True)
    employee = db.relationship('Employee')
    employee_client_assignment = db.relationship('Employee_Client_Assignment')

class Employee(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    employee_number = db.Column(db.String(8), unique=True)
    date_employed = db.Column(db.Date)
    password = db.Column(db.String(200), nullable=False)
    is_senior = db.Column(db.Boolean)

class Employee_Client_Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('person.id'), unique=True)

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    property_type = db.Column(db.String(20), nullable=False)
    date_listing = db.Column(db.DateTime(timezone=True), default=func.now())
    is_available = db.Column(db.Boolean)
    addr = db.Column(db.Integer, db.ForeignKey('address.id'), unique=True)

class Address(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    loc_number = db.Column(db.String(20))
    street_name = db.Column(db.String(20), nullable=False)
    barangay = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    province = db.Column(db.String(20), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    person_addr = db.relationship('Person')
    property_addr = db.relationship('Property')
