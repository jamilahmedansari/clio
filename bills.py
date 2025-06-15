from flask import Blueprint, request, jsonify
from src.models import db, Bill
from datetime import datetime

bills_bp = Blueprint("bills", __name__)

@bills_bp.route("/bills", methods=["GET"])
def get_bills():
    try:
        bills = Bill.query.all()
        bills_list = []
        for bill in bills:
            bills_list.append({
                "id": bill.id,
                "bill_number": bill.bill_number,
                "case_id": bill.case_id,
                "amount": float(bill.amount) if bill.amount else None,
                "due_date": bill.due_date.isoformat() if bill.due_date else None,
                "status": bill.status,
                "description": bill.description,
                "user_id": bill.user_id,
                "created_at": bill.created_at.isoformat() if bill.created_at else None,
                "updated_at": bill.updated_at.isoformat() if bill.updated_at else None
            })
        return jsonify(bills_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bills_bp.route("/bills", methods=["POST"])
def create_bill():
    try:
        data = request.get_json()
        
        new_bill = Bill(
            bill_number=data.get('bill_number'),
            case_id=data.get('case_id'),
            amount=float(data.get('amount')) if data.get('amount') else None,
            due_date=datetime.strptime(data.get('due_date'), '%Y-%m-%d').date() if data.get('due_date') else None,
            status=data.get('status', 'Pending'),
            description=data.get('description'),
            user_id=data.get('user_id', 1)  # Default user for now
        )
        
        db.session.add(new_bill)
        db.session.commit()
        
        return jsonify({
            "id": new_bill.id,
            "bill_number": new_bill.bill_number,
            "case_id": new_bill.case_id,
            "amount": float(new_bill.amount) if new_bill.amount else None,
            "due_date": new_bill.due_date.isoformat() if new_bill.due_date else None,
            "status": new_bill.status,
            "description": new_bill.description,
            "user_id": new_bill.user_id,
            "created_at": new_bill.created_at.isoformat() if new_bill.created_at else None,
            "updated_at": new_bill.updated_at.isoformat() if new_bill.updated_at else None
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@bills_bp.route("/bills/<int:bill_id>", methods=["GET"])
def get_bill(bill_id):
    try:
        bill = Bill.query.get_or_404(bill_id)
        return jsonify({
            "id": bill.id,
            "bill_number": bill.bill_number,
            "case_id": bill.case_id,
            "amount": float(bill.amount) if bill.amount else None,
            "due_date": bill.due_date.isoformat() if bill.due_date else None,
            "status": bill.status,
            "description": bill.description,
            "user_id": bill.user_id,
            "created_at": bill.created_at.isoformat() if bill.created_at else None,
            "updated_at": bill.updated_at.isoformat() if bill.updated_at else None
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bills_bp.route("/bills/<int:bill_id>", methods=["PUT"])
def update_bill(bill_id):
    try:
        bill = Bill.query.get_or_404(bill_id)
        data = request.get_json()
        
        bill.bill_number = data.get('bill_number', bill.bill_number)
        bill.case_id = data.get('case_id', bill.case_id)
        if data.get('amount'):
            bill.amount = float(data.get('amount'))
        if data.get('due_date'):
            bill.due_date = datetime.strptime(data.get('due_date'), '%Y-%m-%d').date()
        bill.status = data.get('status', bill.status)
        bill.description = data.get('description', bill.description)
        bill.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            "id": bill.id,
            "bill_number": bill.bill_number,
            "case_id": bill.case_id,
            "amount": float(bill.amount) if bill.amount else None,
            "due_date": bill.due_date.isoformat() if bill.due_date else None,
            "status": bill.status,
            "description": bill.description,
            "user_id": bill.user_id,
            "created_at": bill.created_at.isoformat() if bill.created_at else None,
            "updated_at": bill.updated_at.isoformat() if bill.updated_at else None
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@bills_bp.route("/bills/<int:bill_id>", methods=["DELETE"])
def delete_bill(bill_id):
    try:
        bill = Bill.query.get_or_404(bill_id)
        db.session.delete(bill)
        db.session.commit()
        return jsonify({"message": "Bill deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

