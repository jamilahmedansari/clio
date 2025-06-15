from flask import Blueprint, request, jsonify
from src.models import db, Collaboration
from datetime import datetime

collaboration_bp = Blueprint("collaboration", __name__)

@collaboration_bp.route("/collaboration", methods=["GET"])
def get_collaboration():
    try:
        collaborations = Collaboration.query.all()
        collaborations_list = []
        for collab in collaborations:
            collaborations_list.append({
                "id": collab.id,
                "case_id": collab.case_id,
                "message": collab.message,
                "sender": collab.sender,
                "visibility": collab.visibility,
                "user_id": collab.user_id,
                "created_at": collab.created_at.isoformat() if collab.created_at else None,
                "updated_at": collab.updated_at.isoformat() if collab.updated_at else None
            })
        return jsonify(collaborations_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@collaboration_bp.route("/collaboration", methods=["POST"])
def create_collaboration():
    try:
        data = request.get_json()
        
        new_collaboration = Collaboration(
            case_id=data.get('case_id'),
            message=data.get('message'),
            sender=data.get('sender'),
            visibility=data.get('visibility', 'Internal'),
            user_id=data.get('user_id', 1)  # Default user for now
        )
        
        db.session.add(new_collaboration)
        db.session.commit()
        
        return jsonify({
            "id": new_collaboration.id,
            "case_id": new_collaboration.case_id,
            "message": new_collaboration.message,
            "sender": new_collaboration.sender,
            "visibility": new_collaboration.visibility,
            "user_id": new_collaboration.user_id,
            "created_at": new_collaboration.created_at.isoformat() if new_collaboration.created_at else None,
            "updated_at": new_collaboration.updated_at.isoformat() if new_collaboration.updated_at else None
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@collaboration_bp.route("/collaboration/<int:collaboration_id>", methods=["GET"])
def get_collaboration_item(collaboration_id):
    try:
        collaboration = Collaboration.query.get_or_404(collaboration_id)
        return jsonify({
            "id": collaboration.id,
            "case_id": collaboration.case_id,
            "message": collaboration.message,
            "sender": collaboration.sender,
            "visibility": collaboration.visibility,
            "user_id": collaboration.user_id,
            "created_at": collaboration.created_at.isoformat() if collaboration.created_at else None,
            "updated_at": collaboration.updated_at.isoformat() if collaboration.updated_at else None
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@collaboration_bp.route("/collaboration/<int:collaboration_id>", methods=["PUT"])
def update_collaboration(collaboration_id):
    try:
        collaboration = Collaboration.query.get_or_404(collaboration_id)
        data = request.get_json()
        
        collaboration.case_id = data.get('case_id', collaboration.case_id)
        collaboration.message = data.get('message', collaboration.message)
        collaboration.sender = data.get('sender', collaboration.sender)
        collaboration.visibility = data.get('visibility', collaboration.visibility)
        collaboration.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            "id": collaboration.id,
            "case_id": collaboration.case_id,
            "message": collaboration.message,
            "sender": collaboration.sender,
            "visibility": collaboration.visibility,
            "user_id": collaboration.user_id,
            "created_at": collaboration.created_at.isoformat() if collaboration.created_at else None,
            "updated_at": collaboration.updated_at.isoformat() if collaboration.updated_at else None
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@collaboration_bp.route("/collaboration/<int:collaboration_id>", methods=["DELETE"])
def delete_collaboration(collaboration_id):
    try:
        collaboration = Collaboration.query.get_or_404(collaboration_id)
        db.session.delete(collaboration)
        db.session.commit()
        return jsonify({"message": "Collaboration deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

