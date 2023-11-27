from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import Person
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        contact = request.form.get('phoneNo')
        gender = request.form.get('gender')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('confirmPassword')
        birth_date = request.form.get('birthDate')
        house_no = request.form.get('houseNo')
        barangay = request.form.get('barangay')
        city = request.form.get('city')
        province = request.form.get('province')
        postal_code = request.form.get('postalCode')
        employment_date=request.form.get('employmentDate')
        employee_type=request.form.get('employeeType')

        if len(first_name)<2:
            flash('First Name must be greater than 1 character!', category='error')
        if not first_name.isalpha():
            flash('First Name must only contain letters in the alpabet', category='error')
        elif len(last_name)<2:
            flash('Last Name must be greater than 1 character!', category='error')
        elif not last_name.isalpha():
            flash('Last Name must be greater than 1 character!', category='error')
        elif gender=='Gender':
            flash('Please select a gender!', category='error')
        elif not contact.isdigit():
            flash('Contact number must be in digits!', category='error')
        elif not len(contact)==11:
            flash('Contact number must have 11 digits!', category='error')
        elif len(email)<3:
            flash('Email must be greater than 3 characters!', category='error')
        elif len(password)<8:
            flash('Password must be at least 8 characters!', category='error')
        elif password!=password2:
            flash('Password dont match!', category='error')
        elif birth_date=='':
            flash('Please enter Date of Birth!', category='error')
        elif len(house_no)>100:
            flash('House/Building Number length too long!', category='error')
        elif len(barangay)>100:
            flash('Barangay length too long!', category='error')
        elif len(city)>100:
            flash('City length too long!', category='error')
        elif len(province)>100:
            flash('Province length too long!', category='error')
        elif not postal_code.isdigit():
            flash('Postal code must be in digits!', category='error')
        elif employment_date == '':
            flash('Please enter Date of Birth!', category='error')
        elif employee_type=='Employment Status':
            flash('Please enter Employment Status!', category='error')
        else:
            new_person = Person(first_name=first_name, last_name=last_name, email_address=email,
                                date_of_birth=birth_date)
            return success()        
        
    
    return render_template('register.html')

@auth.route('/success')
def success():
    return render_template('success.html')