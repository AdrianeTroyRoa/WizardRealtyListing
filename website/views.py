from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from . import db
from werkzeug.utils import secure_filename
from .models import Property, Address
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
        property_street = request.form.get('propertySt')
        property_brgy = request.form.get('propertyBrgy')
        property_city = request.form.get('propertyCity')
        property_province = request.form.get('propertyProv')
        property_pcode = request.form.get('propertyPost')
        property_status = request.form.get('propertyStat')

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
                new_property = Property(name=property_name, property_type="estate", is_available=True, addr=address_id, bg_image=filename)
            else:
                new_property = Property(name=property_name, property_type="estate", is_available=False, addr=address_id, bg_image=filename)


            db.session.add(new_property)
            db.session.commit()

 
        return redirect(url_for('views.home'))

    properties = Property.query.order_by(Property.id.desc()).all()
    list_addr = []

    for property in properties:
        print(property.bg_image)
        list_addr.append(property.addr)

    addresses = Address.query.filter(Address.id.in_(list_addr)).order_by(Address.id.desc()).all()

    return render_template('index.html', properties=properties, addresses=addresses)

@views.route('/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('query', '')
    properties = Property.query.filter(Property.name.ilike(f"%{query}%")).all()

    property_list = []
    for property in properties:
        property_list.append({

            'name': property.name,
            'seller': 'Din Shane Magallanes', #will change if connected to db
            'is_available': property.is_available,
        })

    return jsonify({'properties': property_list})
