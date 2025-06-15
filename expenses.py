from flask import Blueprint, request, jsonify
from src.models import db, Expense
from datetime import datetime

expenses_bp = Blueprint("expenses", __name__)

@expenses_bp.route("/expenses", methods=["GET"])
def get_expenses():
    try:
        expenses = Expense.query.all()
        expenses_list = []
        for expense in expenses:
            expenses_list.append({
                "id": expense.id,
                "case_id": expense.case_id,
                "description": expense.description,
                "amount": float(expense.amount) if expense.amount else None,
                "date": expense.date.isoformat() if expense.date else None,
                "category": expense.category,
                "activity": expense.activity,
                "cost": float(expense.cost) if expense.cost else None,
                "quantity": expense.quantity,
                "billable": expense.billable,
                "receipt_path": expense.receipt_path,
                "user_id": expense.user_id,
                "created_at": expense.created_at.isoformat() if expense.created_at else None,
                "updated_at": expense.updated_at.isoformat() if expense.updated_at else None
            })
        return jsonify(expenses_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@expenses_bp.route("/expenses", methods=["POST"])
def create_expense():
    try:
        data = request.get_json()
        
        new_expense = Expense(
            case_id=data.get('case_id'),
            description=data.get('description'),
            amount=float(data.get('amount')) if data.get('amount') else None,
            date=datetime.strptime(data.get('date'), '%Y-%m-%d').date() if data.get('date') else None,
            category=data.get('category'),
            activity=data.get('activity'),
            cost=float(data.get('cost')) if data.get('cost') else None,
            quantity=int(data.get('quantity', 1)),
            billable=data.get('billable', True),
            receipt_path=data.get('receipt_path'),
            user_id=data.get('user_id', 1)  # Default user for now
        )
        
        db.session.add(new_expense)
        db.session.commit()
        
        return jsonify({
            "id": new_expense.id,
            "case_id": new_expense.case_id,
            "description": new_expense.description,
            "amount": float(new_expense.amount) if new_expense.amount else None,
            "date": new_expense.date.isoformat() if new_expense.date else None,
            "category": new_expense.category,
            "activity": new_expense.activity,
            "cost": float(new_expense.cost) if new_expense.cost else None,
            "quantity": new_expense.quantity,
            "billable": new_expense.billable,
            "receipt_path": new_expense.receipt_path,
            "user_id": new_expense.user_id,
            "created_at": new_expense.created_at.isoformat() if new_expense.created_at else None,
            "updated_at": new_expense.updated_at.isoformat() if new_expense.updated_at else None
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@expenses_bp.route("/expenses/<int:expense_id>", methods=["GET"])
def get_expense(expense_id):
    try:
        expense = Expense.query.get_or_404(expense_id)
        return jsonify({
            "id": expense.id,
            "case_id": expense.case_id,
            "description": expense.description,
            "amount": float(expense.amount) if expense.amount else None,
            "date": expense.date.isoformat() if expense.date else None,
            "category": expense.category,
            "activity": expense.activity,
            "cost": float(expense.cost) if expense.cost else None,
            "quantity": expense.quantity,
            "billable": expense.billable,
            "receipt_path": expense.receipt_path,
            "user_id": expense.user_id,
            "created_at": expense.created_at.isoformat() if expense.created_at else None,
            "updated_at": expense.updated_at.isoformat() if expense.updated_at else None
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@expenses_bp.route("/expenses/<int:expense_id>", methods=["PUT"])
def update_expense(expense_id):
    try:
        expense = Expense.query.get_or_404(expense_id)
        data = request.get_json()
        
        expense.case_id = data.get('case_id', expense.case_id)
        expense.description = data.get('description', expense.description)
        if data.get('amount'):
            expense.amount = float(data.get('amount'))
        if data.get('date'):
            expense.date = datetime.strptime(data.get('date'), '%Y-%m-%d').date()
        expense.category = data.get('category', expense.category)
        expense.activity = data.get('activity', expense.activity)
        if data.get('cost'):
            expense.cost = float(data.get('cost'))
        if data.get('quantity'):
            expense.quantity = int(data.get('quantity'))
        expense.billable = data.get('billable', expense.billable)
        expense.receipt_path = data.get('receipt_path', expense.receipt_path)
        expense.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            "id": expense.id,
            "case_id": expense.case_id,
            "description": expense.description,
            "amount": float(expense.amount) if expense.amount else None,
            "date": expense.date.isoformat() if expense.date else None,
            "category": expense.category,
            "activity": expense.activity,
            "cost": float(expense.cost) if expense.cost else None,
            "quantity": expense.quantity,
            "billable": expense.billable,
            "receipt_path": expense.receipt_path,
            "user_id": expense.user_id,
            "created_at": expense.created_at.isoformat() if expense.created_at else None,
            "updated_at": expense.updated_at.isoformat() if expense.updated_at else None
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@expenses_bp.route("/expenses/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    try:
        expense = Expense.query.get_or_404(expense_id)
        db.session.delete(expense)
        db.session.commit()
        return jsonify({"message": "Expense deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

