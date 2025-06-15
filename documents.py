from flask import Blueprint, request, jsonify
from src.models import db, Document
from datetime import datetime

documents_bp = Blueprint("documents", __name__)

@documents_bp.route("/documents", methods=["GET"])
def get_documents():
    try:
        documents = Document.query.all()
        documents_list = []
        for doc in documents:
            documents_list.append({
                "id": doc.id,
                "name": doc.name,
                "file_path": doc.file_path,
                "file_type": doc.file_type,
                "case_id": doc.case_id,
                "description": doc.description,
                "user_id": doc.user_id,
                "created_at": doc.created_at.isoformat() if doc.created_at else None,
                "updated_at": doc.updated_at.isoformat() if doc.updated_at else None
            })
        return jsonify(documents_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@documents_bp.route("/documents", methods=["POST"])
def create_document():
    try:
        data = request.get_json()
        
        new_document = Document(
            name=data.get('name'),
            file_path=data.get('file_path'),
            file_type=data.get('file_type'),
            case_id=data.get('case_id'),
            description=data.get('description'),
            user_id=data.get('user_id', 1)  # Default user for now
        )
        
        db.session.add(new_document)
        db.session.commit()
        
        return jsonify({
            "id": new_document.id,
            "name": new_document.name,
            "file_path": new_document.file_path,
            "file_type": new_document.file_type,
            "case_id": new_document.case_id,
            "description": new_document.description,
            "user_id": new_document.user_id,
            "created_at": new_document.created_at.isoformat() if new_document.created_at else None,
            "updated_at": new_document.updated_at.isoformat() if new_document.updated_at else None
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@documents_bp.route("/documents/<int:document_id>", methods=["GET"])
def get_document(document_id):
    try:
        document = Document.query.get_or_404(document_id)
        return jsonify({
            "id": document.id,
            "name": document.name,
            "file_path": document.file_path,
            "file_type": document.file_type,
            "case_id": document.case_id,
            "description": document.description,
            "user_id": document.user_id,
            "created_at": document.created_at.isoformat() if document.created_at else None,
            "updated_at": document.updated_at.isoformat() if document.updated_at else None
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@documents_bp.route("/documents/<int:document_id>", methods=["PUT"])
def update_document(document_id):
    try:
        document = Document.query.get_or_404(document_id)
        data = request.get_json()
        
        document.name = data.get('name', document.name)
        document.file_path = data.get('file_path', document.file_path)
        document.file_type = data.get('file_type', document.file_type)
        document.case_id = data.get('case_id', document.case_id)
        document.description = data.get('description', document.description)
        document.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            "id": document.id,
            "name": document.name,
            "file_path": document.file_path,
            "file_type": document.file_type,
            "case_id": document.case_id,
            "description": document.description,
            "user_id": document.user_id,
            "created_at": document.created_at.isoformat() if document.created_at else None,
            "updated_at": document.updated_at.isoformat() if document.updated_at else None
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@documents_bp.route("/documents/<int:document_id>", methods=["DELETE"])
def delete_document(document_id):
    try:
        document = Document.query.get_or_404(document_id)
        db.session.delete(document)
        db.session.commit()
        return jsonify({"message": "Document deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

