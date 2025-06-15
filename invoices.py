from flask import Blueprint, request, jsonify
from src.models import db, Invoice
from datetime import datetime

invoices_bp = Blueprint("invoices", __name__)

@invoices_bp.route("/invoices", methods=["GET"])
def get_invoices():
    try:
        invoices = Invoice.query.all()
        invoices_list = []
        for invoice in invoices:
            invoices_list.append({
                "id": invoice.id,
                "invoice_number": invoice.invoice_number,
                "case_id": invoice.case_id,
                "amount": float(invoice.amount) if invoice.amount else None,
                "due_date": invoice.due_date.isoformat() if invoice.due_date else None,
                "status": invoice.status,
                "description": invoice.description,
                "user_id": invoice.user_id,
                "created_at": invoice.created_at.isoformat() if invoice.created_at else None,
                "updated_at": invoice.updated_at.isoformat() if invoice.updated_at else None
            })
        return jsonify(invoices_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@invoices_bp.route("/invoices", methods=["POST"])
def create_invoice():
    try:
        data = request.get_json()
        
        new_invoice = Invoice(
            invoice_number=data.get('invoice_number'),
            case_id=data.get('case_id'),
            amount=float(data.get('amount')) if data.get('amount') else None,
            due_date=datetime.strptime(data.get('due_date'), '%Y-%m-%d').date() if data.get('due_date') else None,
            status=data.get('status', 'Draft'),
            description=data.get('description'),
            user_id=data.get('user_id', 1)  # Default user for now
        )
        
        db.session.add(new_invoice)
        db.session.commit()
        
        return jsonify({
            "id": new_invoice.id,
            "invoice_number": new_invoice.invoice_number,
            "case_id": new_invoice.case_id,
            "amount": float(new_invoice.amount) if new_invoice.amount else None,
            "due_date": new_invoice.due_date.isoformat() if new_invoice.due_date else None,
            "status": new_invoice.status,
            "description": new_invoice.description,
            "user_id": new_invoice.user_id,
            "created_at": new_invoice.created_at.isoformat() if new_invoice.created_at else None,
            "updated_at": new_invoice.updated_at.isoformat() if new_invoice.updated_at else None
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@invoices_bp.route("/invoices/<int:invoice_id>", methods=["GET"])
def get_invoice(invoice_id):
    try:
        invoice = Invoice.query.get_or_404(invoice_id)
        return jsonify({
            "id": invoice.id,
            "invoice_number": invoice.invoice_number,
            "case_id": invoice.case_id,
            "amount": float(invoice.amount) if invoice.amount else None,
            "due_date": invoice.due_date.isoformat() if invoice.due_date else None,
            "status": invoice.status,
            "description": invoice.description,
            "user_id": invoice.user_id,
            "created_at": invoice.created_at.isoformat() if invoice.created_at else None,
            "updated_at": invoice.updated_at.isoformat() if invoice.updated_at else None
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@invoices_bp.route("/invoices/<int:invoice_id>", methods=["PUT"])
def update_invoice(invoice_id):
    try:
        invoice = Invoice.query.get_or_404(invoice_id)
        data = request.get_json()
        
        invoice.invoice_number = data.get('invoice_number', invoice.invoice_number)
        invoice.case_id = data.get('case_id', invoice.case_id)
        if data.get('amount'):
            invoice.amount = float(data.get('amount'))
        if data.get('due_date'):
            invoice.due_date = datetime.strptime(data.get('due_date'), '%Y-%m-%d').date()
        invoice.status = data.get('status', invoice.status)
        invoice.description = data.get('description', invoice.description)
        invoice.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            "id": invoice.id,
            "invoice_number": invoice.invoice_number,
            "case_id": invoice.case_id,
            "amount": float(invoice.amount) if invoice.amount else None,
            "due_date": invoice.due_date.isoformat() if invoice.due_date else None,
            "status": invoice.status,
            "description": invoice.description,
            "user_id": invoice.user_id,
            "created_at": invoice.created_at.isoformat() if invoice.created_at else None,
            "updated_at": invoice.updated_at.isoformat() if invoice.updated_at else None
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@invoices_bp.route("/invoices/<int:invoice_id>", methods=["DELETE"])
def delete_invoice(invoice_id):
    try:
        invoice = Invoice.query.get_or_404(invoice_id)
        db.session.delete(invoice)
        db.session.commit()
        return jsonify({"message": "Invoice deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

