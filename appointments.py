from flask import Blueprint, request, jsonify
from src.models import db, Appointment
from datetime import datetime

appointments_bp = Blueprint("appointments", __name__)

@appointments_bp.route("/appointments", methods=["GET"])
def get_appointments():
    try:
        appointments = Appointment.query.all()
        appointments_list = []
        for appointment in appointments:
            appointments_list.append({
                "id": appointment.id,
                "title": appointment.title,
                "description": appointment.description,
                "case_id": appointment.case_id,
                "contact_id": appointment.contact_id,
                "appointment_date": appointment.appointment_date.isoformat() if appointment.appointment_date else None,
                "duration": appointment.duration,
                "location": appointment.location,
                "meeting_type": appointment.meeting_type,
                "status": appointment.status,
                "user_id": appointment.user_id,
                "created_at": appointment.created_at.isoformat() if appointment.created_at else None,
                "updated_at": appointment.updated_at.isoformat() if appointment.updated_at else None
            })
        return jsonify(appointments_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@appointments_bp.route("/appointments", methods=["POST"])
def create_appointment():
    try:
        data = request.get_json()
        
        new_appointment = Appointment(
            title=data.get('title'),
            description=data.get('description'),
            case_id=data.get('case_id'),
            contact_id=data.get('contact_id'),
            appointment_date=datetime.fromisoformat(data.get('appointment_date').replace('Z', '+00:00')) if data.get('appointment_date') else None,
            duration=int(data.get('duration')) if data.get('duration') else None,
            location=data.get('location'),
            meeting_type=data.get('meeting_type'),
            status=data.get('status', 'Scheduled'),
            user_id=data.get('user_id', 1)  # Default user for now
        )
        
        db.session.add(new_appointment)
        db.session.commit()
        
        return jsonify({
            "id": new_appointment.id,
            "title": new_appointment.title,
            "description": new_appointment.description,
            "case_id": new_appointment.case_id,
            "contact_id": new_appointment.contact_id,
            "appointment_date": new_appointment.appointment_date.isoformat() if new_appointment.appointment_date else None,
            "duration": new_appointment.duration,
            "location": new_appointment.location,
            "meeting_type": new_appointment.meeting_type,
            "status": new_appointment.status,
            "user_id": new_appointment.user_id,
            "created_at": new_appointment.created_at.isoformat() if new_appointment.created_at else None,
            "updated_at": new_appointment.updated_at.isoformat() if new_appointment.updated_at else None
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@appointments_bp.route("/appointments/<int:appointment_id>", methods=["GET"])
def get_appointment(appointment_id):
    try:
        appointment = Appointment.query.get_or_404(appointment_id)
        return jsonify({
            "id": appointment.id,
            "title": appointment.title,
            "description": appointment.description,
            "case_id": appointment.case_id,
            "contact_id": appointment.contact_id,
            "appointment_date": appointment.appointment_date.isoformat() if appointment.appointment_date else None,
            "duration": appointment.duration,
            "location": appointment.location,
            "meeting_type": appointment.meeting_type,
            "status": appointment.status,
            "user_id": appointment.user_id,
            "created_at": appointment.created_at.isoformat() if appointment.created_at else None,
            "updated_at": appointment.updated_at.isoformat() if appointment.updated_at else None
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@appointments_bp.route("/appointments/<int:appointment_id>", methods=["PUT"])
def update_appointment(appointment_id):
    try:
        appointment = Appointment.query.get_or_404(appointment_id)
        data = request.get_json()
        
        appointment.title = data.get('title', appointment.title)
        appointment.description = data.get('description', appointment.description)
        appointment.case_id = data.get('case_id', appointment.case_id)
        appointment.contact_id = data.get('contact_id', appointment.contact_id)
        if data.get('appointment_date'):
            appointment.appointment_date = datetime.fromisoformat(data.get('appointment_date').replace('Z', '+00:00'))
        if data.get('duration'):
            appointment.duration = int(data.get('duration'))
        appointment.location = data.get('location', appointment.location)
        appointment.meeting_type = data.get('meeting_type', appointment.meeting_type)
        appointment.status = data.get('status', appointment.status)
        appointment.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            "id": appointment.id,
            "title": appointment.title,
            "description": appointment.description,
            "case_id": appointment.case_id,
            "contact_id": appointment.contact_id,
            "appointment_date": appointment.appointment_date.isoformat() if appointment.appointment_date else None,
            "duration": appointment.duration,
            "location": appointment.location,
            "meeting_type": appointment.meeting_type,
            "status": appointment.status,
            "user_id": appointment.user_id,
            "created_at": appointment.created_at.isoformat() if appointment.created_at else None,
            "updated_at": appointment.updated_at.isoformat() if appointment.updated_at else None
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@appointments_bp.route("/appointments/<int:appointment_id>", methods=["DELETE"])
def delete_appointment(appointment_id):
    try:
        appointment = Appointment.query.get_or_404(appointment_id)
        db.session.delete(appointment)
        db.session.commit()
        return jsonify({"message": "Appointment deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

