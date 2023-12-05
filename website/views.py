from datetime import datetime
from flask import Blueprint, flash, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from . import db
from werkzeug.utils import secure_filename
from .models import ClientLikesProperty, Property, Address, Person, Client
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
    properties = Property.query.order_by(Property.id.desc()).all()
    list_addr = []

    for property in properties:
        list_addr.append(property.addr)

    addresses = Address.query.filter(Address.id.in_(list_addr)).order_by(Address.id.desc()).all()


    return render_template('index.html', properties=properties, property_address=zip(properties,addresses), property_address_edit=zip(properties,addresses))

@views.route('/interested/<int:prop_id>',methods=['GET','POST'])
@login_required
def client_interest(prop_id):
    if request.method=='POST':
        client_id = request.form.get('client_id')
        property = Property.query.filter_by(id=prop_id).first()
        unique_ent = ClientLikesProperty.query.filter_by(property_id=prop_id).all()
        client_ids = [result.client_id for result in unique_ent]

        clients = Client.query.filter(Client.client_id==client_id).first()
        
        if unique_ent:
            if (client_id in client_ids or property.client_id == client_id or not client_id or not clients):
                flash('Error: Client likely associated with the property or not found in database', category='error')
            else:
                client_property = ClientLikesProperty(client_id=client_id, property_id=prop_id) 
                db.session.add(client_property)
                db.session.commit()
                flash('Client enlisted the property as interest', category='success')
        else:
            if (property.client_id == client_id or not client_id or not clients):
                flash('Error: Client likely associated with the property or not found in database', category='error')
            else:
                client_property = ClientLikesProperty(client_id=client_id, property_id=prop_id) 
                db.session.add(client_property)
                db.session.commit()
                flash('Client enlisted the property as interest', category='success')

        return redirect(url_for('views.home'))

@views.route('/addproperty',methods=['GET','POST'])
@login_required
def addprop():
    if request.method=='POST':
        property_name = request.form.get('propertyName')
        property_locnum = request.form.get('propertyLoc')
        property_street = request.form.get('propertyStreet')
        property_brgy = request.form.get('propertyBrgy')
        property_city = request.form.get('propertyCity')
        property_province = request.form.get('propertyProv')
        property_pcode = request.form.get('propertyPostal')
        property_status = request.form.get('propertyStat')
        property_client = request.form.get('propertyCD')
        property_type = request.form.get('propertyType')

        new_address = Address(loc_number = property_locnum, street_name= property_street, barangay=property_brgy, city=property_city, province=property_province, postal_code=property_pcode)
        
        db.session.add(new_address)
        db.session.commit()
        
        address_id = new_address.id


        if 'file' not in request.files:
            return "no image detected"
        
        file = request.files['file']
        
        if file.filename == '':
            return "empty file name of image"
        print(property_type)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(UPLOAD_FOLDER+filename)
            if(property_status == "Available"):
                new_property = Property(name=property_name, is_available=True, addr=address_id, bg_image=filename, client_id=property_client, property_type=property_type)
            else:
                new_property = Property(name=property_name, is_available=False, addr=address_id, bg_image=filename, client_id=property_client, property_type=property_type)


            db.session.add(new_property)
            db.session.commit()
        
        return redirect(url_for('views.home'))

@views.route('/editproperty/<int:prop_id>',methods=['GET','POST'])
@login_required
def editprop(prop_id):
    if request.method=='POST':
        property_name = request.form.get('propertyName')
        property_locnum = request.form.get('propertyLoc')
        property_street = request.form.get('propertyStreet')
        property_brgy = request.form.get('propertyBrgy')
        property_city = request.form.get('propertyCity')
        property_province = request.form.get('propertyProv')
        property_pcode = request.form.get('propertyPostal')
        property_status = request.form.get('propertyStat')
        property_type = request.form.get('propertyType')

        
        property = Property.query.filter_by(id=prop_id).first()
        property.name = property_name
        property.property_type = property_type
        property.is_available = property_status
        if(property_status == "Available"):
            property.is_available = True
        else:
            property.is_available = False

        address = Address.query.filter_by(id=property.addr).first()
        address.loc_number = property_locnum
        address.street_name = property_street
        address.barangay = property_brgy
        address.city = property_city
        address.province = property_province
        address.postal_code = property_pcode

        db.session.commit()
        
        return redirect(url_for('views.home'))

@views.route('/editpropertyinclient/<int:prop_id>/<string:client_id>',methods=['GET','POST'])
@login_required
def editprop_in_client(prop_id, client_id):
    if request.method=='POST':
        property_name = request.form.get('propertyName')
        property_locnum = request.form.get('propertyLoc')
        property_street = request.form.get('propertyStreet')
        property_brgy = request.form.get('propertyBrgy')
        property_city = request.form.get('propertyCity')
        property_province = request.form.get('propertyProv')
        property_pcode = request.form.get('propertyPostal')
        property_status = request.form.get('propertyStat')
        property_type = request.form.get('propertyType')

        
        property = Property.query.filter_by(id=prop_id).first()
        property.name = property_name
        property.property_type = property_type
        property.is_available = property_status
        if(property_status == "Available"):
            property.is_available = True
        else:
            property.is_available = False

        address = Address.query.filter_by(id=property.addr).first()
        address.loc_number = property_locnum
        address.street_name = property_street
        address.barangay = property_brgy
        address.city = property_city
        address.province = property_province
        address.postal_code = property_pcode

        db.session.commit()
        
        return redirect(url_for('views.interested', client_id=client_id))

@views.route('/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('query', '')
    properties = Property.query.filter(Property.name.ilike(f"%{query}%")).order_by(Property.id.desc()).all()

    property_list = []
    for property in properties:
        property_list.append({
            'id':property.id,
            'bg_image' : property.bg_image,
            'name': property.name,
            'seller': property.client.person.first_name + ' '+ property.client.person.last_name, #will change if connected to db
            'is_available': property.is_available
        })

    return jsonify({'properties': property_list})


@views.route('/delete/<int:prop_id>')
@login_required
def delete(prop_id):
    property = Property.query.filter_by(id=prop_id).first()
    db.session.delete(property)
    db.session.commit()
    
    return redirect(url_for('views.home'))

@views.route('/deleteinclientview/<int:prop_id>/<string:client_id>')
@login_required
def delete_in_clientview(prop_id, client_id):
    property = Property.query.filter_by(id=prop_id).first()
    db.session.delete(property)
    db.session.commit()
    
    return redirect(url_for('views.interested', client_id=client_id))

@views.route('/deleteclientlikes/<int:prop_id>/<string:client_id>')
@login_required
def delete_client_interest(prop_id, client_id):
    property = ClientLikesProperty.query.filter_by(property_id=prop_id).filter_by(client_id=client_id).first()
    db.session.delete(property)
    db.session.commit()
    
    return redirect(url_for('views.interested', client_id=client_id))

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



@views.route('/interest_properties/<string:client_id>')
def interested(client_id):
    properties = Property.query.order_by(Property.id.desc()).all()
    properties_owned = Property.query.filter(Property.client_id==client_id).order_by(Property.id.desc()).all()
    properties_interest_0 = ClientLikesProperty.query.filter(ClientLikesProperty.client_id==client_id).order_by(ClientLikesProperty.id.desc()).all()
    list_addr = []
    list_likes = []

    for like in properties_interest_0:
        list_likes.append(like.property_id)

    for property in properties:
        list_addr.append(property.addr)
        prop = property

    for property in properties_owned:
        prop = property
        break

    properties_liked = Property.query.filter(Property.id.in_(list_likes)).order_by(Property.id.desc()).all()
    addresses = Address.query.filter(Address.id.in_(list_addr)).order_by(Address.id.desc()).all()
    return render_template('interested.html', owner=prop, properties_owned=properties_owned, properties_liked=properties_liked, property_address=zip(properties,addresses), property_address_edit=zip(properties,addresses), client_id=client_id, properties=properties)
