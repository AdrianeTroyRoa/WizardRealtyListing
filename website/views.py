from datetime import datetime
from flask import Blueprint, flash, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from . import db
from werkzeug.utils import secure_filename
from .models import Property, Address, Person, Client
from werkzeug.utils import secure_filename


views = Blueprint('views', __name__)

UPLOAD_FOLDER = 'website/static/images/property_imgs/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/',methods=['GET','POST'])
@login_required
def home():
    if request.method=='POST':
        property_name = request.form.get('propertyName')
        property_locnum = request.form.get('propertyLoc')
        property_street = request.form.get('propertyStreet')
        property_brgy = request.form.get('propertyBrgy')
        property_city = request.form.get('propertyCity')
        property_province = request.form.get('propertyProv')
        property_pcode = request.form.get('propertyPostal')
        property_status = request.form.get('availability')
        property_type = request.form.get('propertyType')
        client_id=request.form.get('propertyClient')

        new_address = Address(loc_number = property_locnum, street_name= property_street, barangay=property_brgy, city=property_city, province=property_province, postal_code=property_pcode)
        
        db.session.add(new_address)
        db.session.commit()
        
        address_id = new_address.id


        if 'file' not in request.files:
            return "no image detected"
        
        file = request.files['file']
        
        if file.filename == '':
            return "empty file name of image"

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(UPLOAD_FOLDER+filename)
            if(property_status == "Available"):
                new_property = Property(name=property_name, property_type=property_type, is_available=True, addr=address_id, bg_image=filename)
            else:
                new_property = Property(name=property_name, property_type=property_type, is_available=False, addr=address_id, bg_image=filename)


            db.session.add(new_property)
            db.session.commit()
        
        return redirect(url_for('views.home'))

    properties = Property.query.order_by(Property.id.desc()).all()
    list_addr = []

    for property in properties:
        list_addr.append(property.addr)

    addresses = Address.query.filter(Address.id.in_(list_addr)).order_by(Address.id.desc()).all()

    return render_template('index.html', properties=properties, addresses=addresses)

@views.route('/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('query', '')
    properties = Property.query.filter(Property.name.ilike(f"%{query}%")).order_by(Property.id.desc()).all()

    property_list = []
    for property in properties:
        property_list.append({
            'bg_image' : property.bg_image,
            'name': property.name,
            'seller': 'Din Shane Magallanes', #will change if connected to db
            'is_available': property.is_available
        })

    return jsonify({'properties': property_list})

@views.route('/clients', methods=['GET', 'POST'])
@login_required
def clients():
    print("hello")
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        suffix=request.form.get('suffix')
        contact = request.form.get('phoneNo')
        gender = request.form.get('gender')
        email = request.form.get('email')
        birth_date = request.form.get('birthDate')
        house_no = request.form.get('houseNo')
        street = request.form.get('street')
        barangay = request.form.get('barangay')
        city = request.form.get('city')
        province = request.form.get('province')
        postal_code = request.form.get('postalCode')

        emailcheck= Person.query.filter_by(email_address=email).first()
        contactcheck=Person.query.filter_by(contact_number=contact).first()

        if emailcheck:
            flash('Email already exist!', category='error')
        if contactcheck:
            flash('Contact number already exist!', category='error')
        else:
            new_address = Address(loc_number = house_no, street_name=street, barangay=barangay, city=city, province=province, postal_code=postal_code)

            db.session.add(new_address)
            db.session.commit()
            
            address_id = new_address.id

            if gender=='1':
                new_person = Person(first_name=first_name, last_name=last_name, name_append=suffix, contact_number=contact, is_male=True, email_address=email,
                                date_of_birth=birth_date,address_id=address_id)
            else:
                new_person = Person(first_name=first_name, last_name=last_name, name_append=suffix, contact_number=contact, is_male=False,email_address=email,
                                date_of_birth=birth_date,address_id=address_id)
            
            db.session.add(new_person)
            db.session.commit()

            person_id  = new_person.id

            client_id = f"CWRL000{person_id}"

            new_client= Client(id=person_id,client_id=client_id)

            db.session.add(new_client)
            db.session.commit()
            
            return redirect(url_for('views.clients'))
        
    client = Client.query.order_by(Client.id.desc()).all()

    list_client = []

    for clients in client:
        list_client.append(clients.id)

    clients = Client.query.filter(Client.id.in_(list_client)).order_by(Client.id.desc()).all()

    return render_template('clients.html',clients=clients)
