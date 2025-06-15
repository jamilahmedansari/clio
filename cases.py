from flask import Blueprint, request, jsonify
from src.models import db, Case
from datetime import datetime

cases_bp = Blueprint("cases", __name__)

@cases_bp.route("/cases", methods=["GET"])
def get_cases():
    try:
        cases = Case.query.all()
        cases_list = []
        for case in cases:
            cases_list.append({
                "id": case.id,
                "name": case.name,
                "case_number": case.case_number,
                "practice_area": case.practice_area,
                "stage": case.stage,
                "date_opened": case.date_opened.isoformat() if case.date_opened else None,
                "description": case.description,
                "status": case.status,
                "office": case.office,
                "statute_of_limitations": case.statute_of_limitations.isoformat() if case.statute_of_limitations else None,
                "conflict_check": case.conflict_check,
                "conflict_check_notes": case.conflict_check_notes,
                "billing_method": case.billing_method,
                "user_id": case.user_id,
                "created_at": case.created_at.isoformat() if case.created_at else None,
                "updated_at": case.updated_at.isoformat() if case.updated_at else None
            })
        return jsonify(cases_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cases_bp.route("/cases", methods=["POST"])
def create_case():
    try:
        data = request.get_json()
        
        new_case = Case(
            name=data.get('name'),
            case_number=data.get('case_number'),
            practice_area=data.get('practice_area'),
            stage=data.get('stage'),
            date_opened=datetime.strptime(data.get('date_opened'), '%Y-%m-%d').date() if data.get('date_opened') else None,
            description=data.get('description'),
            status=data.get('status', 'Active'),
            office=data.get('office'),
            statute_of_limitations=datetime.strptime(data.get('statute_of_limitations'), '%Y-%m-%d').date() if data.get('statute_of_limitations') else None,
            conflict_check=data.get('conflict_check', False),
            conflict_check_notes=data.get('conflict_check_notes'),
            billing_method=data.get('billing_method'),
            user_id=data.get('user_id', 1)  # Default user for now
        )
        
        db.session.add(new_case)
        db.session.commit()
        
        return jsonify({
            "id": new_case.id,
            "name": new_case.name,
            "case_number": new_case.case_number,
            "practice_area": new_case.practice_area,
            "stage": new_case.stage,
            "date_opened": new_case.date_opened.isoformat() if new_case.date_opened else None,
            "description": new_case.description,
            "status": new_case.status,
            "office": new_case.office,
            "statute_of_limitations": new_case.statute_of_limitations.isoformat() if new_case.statute_of_limitations else None,
            "conflict_check": new_case.conflict_check,
            "conflict_check_notes": new_case.conflict_check_notes,
            "billing_method": new_case.billing_method,
            "user_id": new_case.user_id,
            "created_at": new_case.created_at.isoformat() if new_case.created_at else None,
            "updated_at": new_case.updated_at.isoformat() if new_case.updated_at else None
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@cases_bp.route("/cases/<int:case_id>", methods=["GET"])
def get_case(case_id):
    try:
        case = Case.query.get_or_404(case_id)
        return jsonify({
            "id": case.id,
            "name": case.name,
            "case_number": case.case_number,
            "practice_area": case.practice_area,
            "stage": case.stage,
            "date_opened": case.date_opened.isoformat() if case.date_opened else None,
            "description": case.description,
            "status": case.status,
            "office": case.office,
            "statute_of_limitations": case.statute_of_limitations.isoformat() if case.statute_of_limitations else None,
            "conflict_check": case.conflict_check,
            "conflict_check_notes": case.conflict_check_notes,
            "billing_method": case.billing_method,
            "user_id": case.user_id,
            "created_at": case.created_at.isoformat() if case.created_at else None,
            "updated_at": case.updated_at.isoformat() if case.updated_at else None
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cases_bp.route("/cases/<int:case_id>", methods=["PUT"])
def update_case(case_id):
    try:
        case = Case.query.get_or_404(case_id)
        data = request.get_json()
        
        case.name = data.get('name', case.name)
        case.case_number = data.get('case_number', case.case_number)
        case.practice_area = data.get('practice_area', case.practice_area)
        case.stage = data.get('stage', case.stage)
        if data.get('date_opened'):
            case.date_opened = datetime.strptime(data.get('date_opened'), '%Y-%m-%d').date()
        case.description = data.get('description', case.description)
        case.status = data.get('status', case.status)
        case.office = data.get('office', case.office)
        if data.get('statute_of_limitations'):
            case.statute_of_limitations = datetime.strptime(data.get('statute_of_limitations'), '%Y-%m-%d').date()
        case.conflict_check = data.get('conflict_check', case.conflict_check)
        case.conflict_check_notes = data.get('conflict_check_notes', case.conflict_check_notes)
        case.billing_method = data.get('billing_method', case.billing_method)
        case.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            "id": case.id,
            "name": case.name,
            "case_number": case.case_number,
            "practice_area": case.practice_area,
            "stage": case.stage,
            "date_opened": case.date_opened.isoformat() if case.date_opened else None,
            "description": case.description,
            "status": case.status,
            "office": case.office,
            "statute_of_limitations": case.statute_of_limitations.isoformat() if case.statute_of_limitations else None,
            "conflict_check": case.conflict_check,
            "conflict_check_notes": case.conflict_check_notes,
            "billing_method": case.billing_method,
            "user_id": case.user_id,
            "created_at": case.created_at.isoformat() if case.created_at else None,
            "updated_at": case.updated_at.isoformat() if case.updated_at else None
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@cases_bp.route("/cases/<int:case_id>", methods=["DELETE"])
def delete_case(case_id):
    try:
        case = Case.query.get_or_404(case_id)
        db.session.delete(case)
        db.session.commit()
        return jsonify({"message": "Case deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

