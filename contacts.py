from flask import Blueprint, request, jsonify
from src.models import db, Contact
from datetime import datetime

contacts_bp = Blueprint("contacts", __name__)

@contacts_bp.route("/contacts", methods=["GET"])
def get_contacts():
    try:
        contacts = Contact.query.all()
        contacts_list = []
        for contact in contacts:
            contacts_list.append({
                "id": contact.id,
                "first_name": contact.first_name,
                "last_name": contact.last_name,
                "email": contact.email,
                "phone": contact.phone,
                "address": contact.address,
                "address2": contact.address2,
                "city": contact.city,
                "state": contact.state,
                "zip_code": contact.zip_code,
                "country": contact.country,
                "contact_type": contact.contact_type,
                "company_name": contact.company_name,
                "website": contact.website,
                "main_phone": contact.main_phone,
                "fax_number": contact.fax_number,
                "private_notes": contact.private_notes,
                "user_id": contact.user_id,
                "created_at": contact.created_at.isoformat() if contact.created_at else None,
                "updated_at": contact.updated_at.isoformat() if contact.updated_at else None
            })
        return jsonify(contacts_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@contacts_bp.route("/contacts", methods=["POST"])
def create_contact():
    try:
        data = request.get_json()
        
        new_contact = Contact(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            phone=data.get('phone'),
            address=data.get('address'),
            address2=data.get('address2'),
            city=data.get('city'),
            state=data.get('state'),
            zip_code=data.get('zip_code'),
            country=data.get('country'),
            contact_type=data.get('contact_type'),
            company_name=data.get('company_name'),
            website=data.get('website'),
            main_phone=data.get('main_phone'),
            fax_number=data.get('fax_number'),
            private_notes=data.get('private_notes'),
            user_id=data.get('user_id', 1)  # Default user for now
        )
        
        db.session.add(new_contact)
        db.session.commit()
        
        return jsonify({
            "id": new_contact.id,
            "first_name": new_contact.first_name,
            "last_name": new_contact.last_name,
            "email": new_contact.email,
            "phone": new_contact.phone,
            "address": new_contact.address,
            "address2": new_contact.address2,
            "city": new_contact.city,
            "state": new_contact.state,
            "zip_code": new_contact.zip_code,
            "country": new_contact.country,
            "contact_type": new_contact.contact_type,
            "company_name": new_contact.company_name,
            "website": new_contact.website,
            "main_phone": new_contact.main_phone,
            "fax_number": new_contact.fax_number,
            "private_notes": new_contact.private_notes,
            "user_id": new_contact.user_id,
            "created_at": new_contact.created_at.isoformat() if new_contact.created_at else None,
            "updated_at": new_contact.updated_at.isoformat() if new_contact.updated_at else None
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@contacts_bp.route("/contacts/<int:contact_id>", methods=["GET"])
def get_contact(contact_id):
    try:
        contact = Contact.query.get_or_404(contact_id)
        return jsonify({
            "id": contact.id,
            "first_name": contact.first_name,
            "last_name": contact.last_name,
            "email": contact.email,
            "phone": contact.phone,
            "address": contact.address,
            "address2": contact.address2,
            "city": contact.city,
            "state": contact.state,
            "zip_code": contact.zip_code,
            "country": contact.country,
            "contact_type": contact.contact_type,
            "company_name": contact.company_name,
            "website": contact.website,
            "main_phone": contact.main_phone,
            "fax_number": contact.fax_number,
            "private_notes": contact.private_notes,
            "user_id": contact.user_id,
            "created_at": contact.created_at.isoformat() if contact.created_at else None,
            "updated_at": contact.updated_at.isoformat() if contact.updated_at else None
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@contacts_bp.route("/contacts/<int:contact_id>", methods=["PUT"])
def update_contact(contact_id):
    try:
        contact = Contact.query.get_or_404(contact_id)
        data = request.get_json()
        
        contact.first_name = data.get('first_name', contact.first_name)
        contact.last_name = data.get('last_name', contact.last_name)
        contact.email = data.get('email', contact.email)
        contact.phone = data.get('phone', contact.phone)
        contact.address = data.get('address', contact.address)
        contact.address2 = data.get('address2', contact.address2)
        contact.city = data.get('city', contact.city)
        contact.state = data.get('state', contact.state)
        contact.zip_code = data.get('zip_code', contact.zip_code)
        contact.country = data.get('country', contact.country)
        contact.contact_type = data.get('contact_type', contact.contact_type)
        contact.company_name = data.get('company_name', contact.company_name)
        contact.website = data.get('website', contact.website)
        contact.main_phone = data.get('main_phone', contact.main_phone)
        contact.fax_number = data.get('fax_number', contact.fax_number)
        contact.private_notes = data.get('private_notes', contact.private_notes)
        contact.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            "id": contact.id,
            "first_name": contact.first_name,
            "last_name": contact.last_name,
            "email": contact.email,
            "phone": contact.phone,
            "address": contact.address,
            "address2": contact.address2,
            "city": contact.city,
            "state": contact.state,
            "zip_code": contact.zip_code,
            "country": contact.country,
            "contact_type": contact.contact_type,
            "company_name": contact.company_name,
            "website": contact.website,
            "main_phone": contact.main_phone,
            "fax_number": contact.fax_number,
            "private_notes": contact.private_notes,
            "user_id": contact.user_id,
            "created_at": contact.created_at.isoformat() if contact.created_at else None,
            "updated_at": contact.updated_at.isoformat() if contact.updated_at else None
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@contacts_bp.route("/contacts/<int:contact_id>", methods=["DELETE"])
def delete_contact(contact_id):
    try:
        contact = Contact.query.get_or_404(contact_id)
        db.session.delete(contact)
        db.session.commit()
        return jsonify({"message": "Contact deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

