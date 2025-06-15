from flask import Blueprint, request, jsonify
from src.models import db, TimeEntry
from datetime import datetime

time_entries_bp = Blueprint("time_entries", __name__)

@time_entries_bp.route("/time-entries", methods=["GET"])
def get_time_entries():
    try:
        time_entries = TimeEntry.query.all()
        time_entries_list = []
        for entry in time_entries:
            time_entries_list.append({
                "id": entry.id,
                "case_id": entry.case_id,
                "user": entry.user,
                "activity": entry.activity,
                "description": entry.description,
                "date": entry.date.isoformat() if entry.date else None,
                "duration": float(entry.duration) if entry.duration else None,
                "rate": float(entry.rate) if entry.rate else None,
                "billable": entry.billable,
                "user_id": entry.user_id,
                "created_at": entry.created_at.isoformat() if entry.created_at else None,
                "updated_at": entry.updated_at.isoformat() if entry.updated_at else None
            })
        return jsonify(time_entries_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@time_entries_bp.route("/time-entries", methods=["POST"])
def create_time_entry():
    try:
        data = request.get_json()
        
        new_time_entry = TimeEntry(
            case_id=data.get('case_id'),
            user=data.get('user'),
            activity=data.get('activity'),
            description=data.get('description'),
            date=datetime.strptime(data.get('date'), '%Y-%m-%d').date() if data.get('date') else None,
            duration=float(data.get('duration')) if data.get('duration') else None,
            rate=float(data.get('rate')) if data.get('rate') else None,
            billable=data.get('billable', True),
            user_id=data.get('user_id', 1)  # Default user for now
        )
        
        db.session.add(new_time_entry)
        db.session.commit()
        
        return jsonify({
            "id": new_time_entry.id,
            "case_id": new_time_entry.case_id,
            "user": new_time_entry.user,
            "activity": new_time_entry.activity,
            "description": new_time_entry.description,
            "date": new_time_entry.date.isoformat() if new_time_entry.date else None,
            "duration": float(new_time_entry.duration) if new_time_entry.duration else None,
            "rate": float(new_time_entry.rate) if new_time_entry.rate else None,
            "billable": new_time_entry.billable,
            "user_id": new_time_entry.user_id,
            "created_at": new_time_entry.created_at.isoformat() if new_time_entry.created_at else None,
            "updated_at": new_time_entry.updated_at.isoformat() if new_time_entry.updated_at else None
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@time_entries_bp.route("/time-entries/<int:time_entry_id>", methods=["GET"])
def get_time_entry(time_entry_id):
    try:
        time_entry = TimeEntry.query.get_or_404(time_entry_id)
        return jsonify({
            "id": time_entry.id,
            "case_id": time_entry.case_id,
            "user": time_entry.user,
            "activity": time_entry.activity,
            "description": time_entry.description,
            "date": time_entry.date.isoformat() if time_entry.date else None,
            "duration": float(time_entry.duration) if time_entry.duration else None,
            "rate": float(time_entry.rate) if time_entry.rate else None,
            "billable": time_entry.billable,
            "user_id": time_entry.user_id,
            "created_at": time_entry.created_at.isoformat() if time_entry.created_at else None,
            "updated_at": time_entry.updated_at.isoformat() if time_entry.updated_at else None
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@time_entries_bp.route("/time-entries/<int:time_entry_id>", methods=["PUT"])
def update_time_entry(time_entry_id):
    try:
        time_entry = TimeEntry.query.get_or_404(time_entry_id)
        data = request.get_json()
        
        time_entry.case_id = data.get('case_id', time_entry.case_id)
        time_entry.user = data.get('user', time_entry.user)
        time_entry.activity = data.get('activity', time_entry.activity)
        time_entry.description = data.get('description', time_entry.description)
        if data.get('date'):
            time_entry.date = datetime.strptime(data.get('date'), '%Y-%m-%d').date()
        if data.get('duration'):
            time_entry.duration = float(data.get('duration'))
        if data.get('rate'):
            time_entry.rate = float(data.get('rate'))
        time_entry.billable = data.get('billable', time_entry.billable)
        time_entry.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            "id": time_entry.id,
            "case_id": time_entry.case_id,
            "user": time_entry.user,
            "activity": time_entry.activity,
            "description": time_entry.description,
            "date": time_entry.date.isoformat() if time_entry.date else None,
            "duration": float(time_entry.duration) if time_entry.duration else None,
            "rate": float(time_entry.rate) if time_entry.rate else None,
            "billable": time_entry.billable,
            "user_id": time_entry.user_id,
            "created_at": time_entry.created_at.isoformat() if time_entry.created_at else None,
            "updated_at": time_entry.updated_at.isoformat() if time_entry.updated_at else None
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@time_entries_bp.route("/time-entries/<int:time_entry_id>", methods=["DELETE"])
def delete_time_entry(time_entry_id):
    try:
        time_entry = TimeEntry.query.get_or_404(time_entry_id)
        db.session.delete(time_entry)
        db.session.commit()
        return jsonify({"message": "Time entry deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

