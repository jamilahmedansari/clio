from flask import Blueprint, request, jsonify
from src.models import db, Event
from datetime import datetime

events_bp = Blueprint("events", __name__)

@events_bp.route("/events", methods=["GET"])
def get_events():
    try:
        events = Event.query.all()
        events_list = []
        for event in events:
            events_list.append({
                "id": event.id,
                "title": event.title,
                "description": event.description,
                "start_date": event.start_date.isoformat() if event.start_date else None,
                "end_date": event.end_date.isoformat() if event.end_date else None,
                "case_id": event.case_id,
                "event_type": event.event_type,
                "location": event.location,
                "all_day": event.all_day,
                "repeats": event.repeats,
                "is_private": event.is_private,
                "not_linked_to_case": event.not_linked_to_case,
                "user_id": event.user_id,
                "created_at": event.created_at.isoformat() if event.created_at else None,
                "updated_at": event.updated_at.isoformat() if event.updated_at else None
            })
        return jsonify(events_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@events_bp.route("/events", methods=["POST"])
def create_event():
    try:
        data = request.get_json()
        
        new_event = Event(
            title=data.get('title'),
            description=data.get('description'),
            start_date=datetime.fromisoformat(data.get('start_date').replace('Z', '+00:00')) if data.get('start_date') else None,
            end_date=datetime.fromisoformat(data.get('end_date').replace('Z', '+00:00')) if data.get('end_date') else None,
            case_id=data.get('case_id'),
            event_type=data.get('event_type'),
            location=data.get('location'),
            all_day=data.get('all_day', False),
            repeats=data.get('repeats', False),
            is_private=data.get('is_private', False),
            not_linked_to_case=data.get('not_linked_to_case', False),
            user_id=data.get('user_id', 1)  # Default user for now
        )
        
        db.session.add(new_event)
        db.session.commit()
        
        return jsonify({
            "id": new_event.id,
            "title": new_event.title,
            "description": new_event.description,
            "start_date": new_event.start_date.isoformat() if new_event.start_date else None,
            "end_date": new_event.end_date.isoformat() if new_event.end_date else None,
            "case_id": new_event.case_id,
            "event_type": new_event.event_type,
            "location": new_event.location,
            "all_day": new_event.all_day,
            "repeats": new_event.repeats,
            "is_private": new_event.is_private,
            "not_linked_to_case": new_event.not_linked_to_case,
            "user_id": new_event.user_id,
            "created_at": new_event.created_at.isoformat() if new_event.created_at else None,
            "updated_at": new_event.updated_at.isoformat() if new_event.updated_at else None
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@events_bp.route("/events/<int:event_id>", methods=["GET"])
def get_event(event_id):
    try:
        event = Event.query.get_or_404(event_id)
        return jsonify({
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "start_date": event.start_date.isoformat() if event.start_date else None,
            "end_date": event.end_date.isoformat() if event.end_date else None,
            "case_id": event.case_id,
            "event_type": event.event_type,
            "location": event.location,
            "all_day": event.all_day,
            "repeats": event.repeats,
            "is_private": event.is_private,
            "not_linked_to_case": event.not_linked_to_case,
            "user_id": event.user_id,
            "created_at": event.created_at.isoformat() if event.created_at else None,
            "updated_at": event.updated_at.isoformat() if event.updated_at else None
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@events_bp.route("/events/<int:event_id>", methods=["PUT"])
def update_event(event_id):
    try:
        event = Event.query.get_or_404(event_id)
        data = request.get_json()
        
        event.title = data.get('title', event.title)
        event.description = data.get('description', event.description)
        if data.get('start_date'):
            event.start_date = datetime.fromisoformat(data.get('start_date').replace('Z', '+00:00'))
        if data.get('end_date'):
            event.end_date = datetime.fromisoformat(data.get('end_date').replace('Z', '+00:00'))
        event.case_id = data.get('case_id', event.case_id)
        event.event_type = data.get('event_type', event.event_type)
        event.location = data.get('location', event.location)
        event.all_day = data.get('all_day', event.all_day)
        event.repeats = data.get('repeats', event.repeats)
        event.is_private = data.get('is_private', event.is_private)
        event.not_linked_to_case = data.get('not_linked_to_case', event.not_linked_to_case)
        event.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "start_date": event.start_date.isoformat() if event.start_date else None,
            "end_date": event.end_date.isoformat() if event.end_date else None,
            "case_id": event.case_id,
            "event_type": event.event_type,
            "location": event.location,
            "all_day": event.all_day,
            "repeats": event.repeats,
            "is_private": event.is_private,
            "not_linked_to_case": event.not_linked_to_case,
            "user_id": event.user_id,
            "created_at": event.created_at.isoformat() if event.created_at else None,
            "updated_at": event.updated_at.isoformat() if event.updated_at else None
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@events_bp.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    try:
        event = Event.query.get_or_404(event_id)
        db.session.delete(event)
        db.session.commit()
        return jsonify({"message": "Event deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

