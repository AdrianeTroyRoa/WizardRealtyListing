from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import Property, Address

views = Blueprint('views', __name__)

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

        print(property_status)
        new_address = Address(loc_number = property_locnum, street_name= property_street, barangay=property_brgy, city=property_city, province=property_province, postal_code=property_pcode)
        
        db.session.add(new_address)
        db.session.commit()
        
        address_id = new_address.id

        if(property_status == "Available"):
            new_property = Property(name=property_name, property_type="estate", is_available=True, addr=address_id)
        else:
            new_property = Property(name=property_name, property_type="estate", is_available=False, addr=address_id)


        db.session.add(new_property)
        db.session.commit()
        
        return redirect(url_for('views.home'))

    return render_template('index.html')
