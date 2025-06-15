from flask import Blueprint, request, jsonify
from src.models import db, Task
from datetime import datetime

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/tasks", methods=["GET"])
def get_tasks():
    try:
        tasks = Task.query.all()
        tasks_list = []
        for task in tasks:
            tasks_list.append({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "case_id": task.case_id,
                "assigned_to": task.assigned_to,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "priority": task.priority,
                "status": task.status,
                "user_id": task.user_id,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "updated_at": task.updated_at.isoformat() if task.updated_at else None
            })
        return jsonify(tasks_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tasks_bp.route("/tasks", methods=["POST"])
def create_task():
    try:
        data = request.get_json()
        
        new_task = Task(
            title=data.get('title'),
            description=data.get('description'),
            case_id=data.get('case_id'),
            assigned_to=data.get('assigned_to'),
            due_date=datetime.strptime(data.get('due_date'), '%Y-%m-%d').date() if data.get('due_date') else None,
            priority=data.get('priority', 'Medium'),
            status=data.get('status', 'Pending'),
            user_id=data.get('user_id', 1)  # Default user for now
        )
        
        db.session.add(new_task)
        db.session.commit()
        
        return jsonify({
            "id": new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            "case_id": new_task.case_id,
            "assigned_to": new_task.assigned_to,
            "due_date": new_task.due_date.isoformat() if new_task.due_date else None,
            "priority": new_task.priority,
            "status": new_task.status,
            "user_id": new_task.user_id,
            "created_at": new_task.created_at.isoformat() if new_task.created_at else None,
            "updated_at": new_task.updated_at.isoformat() if new_task.updated_at else None
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@tasks_bp.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    try:
        task = Task.query.get_or_404(task_id)
        return jsonify({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "case_id": task.case_id,
            "assigned_to": task.assigned_to,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "priority": task.priority,
            "status": task.status,
            "user_id": task.user_id,
            "created_at": task.created_at.isoformat() if task.created_at else None,
            "updated_at": task.updated_at.isoformat() if task.updated_at else None
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tasks_bp.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    try:
        task = Task.query.get_or_404(task_id)
        data = request.get_json()
        
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.case_id = data.get('case_id', task.case_id)
        task.assigned_to = data.get('assigned_to', task.assigned_to)
        if data.get('due_date'):
            task.due_date = datetime.strptime(data.get('due_date'), '%Y-%m-%d').date()
        task.priority = data.get('priority', task.priority)
        task.status = data.get('status', task.status)
        task.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "case_id": task.case_id,
            "assigned_to": task.assigned_to,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "priority": task.priority,
            "status": task.status,
            "user_id": task.user_id,
            "created_at": task.created_at.isoformat() if task.created_at else None,
            "updated_at": task.updated_at.isoformat() if task.updated_at else None
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@tasks_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    try:
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

