from flask import Blueprint, request, jsonify
from src.models import db, User
from datetime import datetime

users_bp = Blueprint("users", __name__)

@users_bp.route("/users", methods=["GET"])
def get_users():
    try:
        users = User.query.all()
        users_list = []
        for user in users:
            users_list.append({
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "is_active": user.is_active,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "updated_at": user.updated_at.isoformat() if user.updated_at else None
            })
        return jsonify(users_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route("/users", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        
        new_user = User(
            email=data.get('email'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            role=data.get('role', 'Attorney'),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            "id": new_user.id,
            "email": new_user.email,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "role": new_user.role,
            "is_active": new_user.is_active,
            "created_at": new_user.created_at.isoformat() if new_user.created_at else None,
            "updated_at": new_user.updated_at.isoformat() if new_user.updated_at else None
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@users_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        return jsonify({
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        
        user.email = data.get('email', user.email)
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.role = data.get('role', user.role)
        user.is_active = data.get('is_active', user.is_active)
        user.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@users_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

