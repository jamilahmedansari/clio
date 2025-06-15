from flask import Blueprint, request, jsonify
from src.models import db, TrustAccount
from datetime import datetime

trust_accounts_bp = Blueprint("trust_accounts", __name__)

@trust_accounts_bp.route("/trust-accounts", methods=["GET"])
def get_trust_accounts():
    try:
        trust_accounts = TrustAccount.query.all()
        trust_accounts_list = []
        for account in trust_accounts:
            trust_accounts_list.append({
                "id": account.id,
                "account_name": account.account_name,
                "account_number": account.account_number,
                "balance": float(account.balance) if account.balance else None,
                "case_id": account.case_id,
                "description": account.description,
                "user_id": account.user_id,
                "created_at": account.created_at.isoformat() if account.created_at else None,
                "updated_at": account.updated_at.isoformat() if account.updated_at else None
            })
        return jsonify(trust_accounts_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@trust_accounts_bp.route("/trust-accounts", methods=["POST"])
def create_trust_account():
    try:
        data = request.get_json()
        
        new_trust_account = TrustAccount(
            account_name=data.get('account_name'),
            account_number=data.get('account_number'),
            balance=float(data.get('balance', 0.00)),
            case_id=data.get('case_id'),
            description=data.get('description'),
            user_id=data.get('user_id', 1)  # Default user for now
        )
        
        db.session.add(new_trust_account)
        db.session.commit()
        
        return jsonify({
            "id": new_trust_account.id,
            "account_name": new_trust_account.account_name,
            "account_number": new_trust_account.account_number,
            "balance": float(new_trust_account.balance) if new_trust_account.balance else None,
            "case_id": new_trust_account.case_id,
            "description": new_trust_account.description,
            "user_id": new_trust_account.user_id,
            "created_at": new_trust_account.created_at.isoformat() if new_trust_account.created_at else None,
            "updated_at": new_trust_account.updated_at.isoformat() if new_trust_account.updated_at else None
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@trust_accounts_bp.route("/trust-accounts/<int:trust_account_id>", methods=["GET"])
def get_trust_account(trust_account_id):
    try:
        trust_account = TrustAccount.query.get_or_404(trust_account_id)
        return jsonify({
            "id": trust_account.id,
            "account_name": trust_account.account_name,
            "account_number": trust_account.account_number,
            "balance": float(trust_account.balance) if trust_account.balance else None,
            "case_id": trust_account.case_id,
            "description": trust_account.description,
            "user_id": trust_account.user_id,
            "created_at": trust_account.created_at.isoformat() if trust_account.created_at else None,
            "updated_at": trust_account.updated_at.isoformat() if trust_account.updated_at else None
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@trust_accounts_bp.route("/trust-accounts/<int:trust_account_id>", methods=["PUT"])
def update_trust_account(trust_account_id):
    try:
        trust_account = TrustAccount.query.get_or_404(trust_account_id)
        data = request.get_json()
        
        trust_account.account_name = data.get('account_name', trust_account.account_name)
        trust_account.account_number = data.get('account_number', trust_account.account_number)
        if data.get('balance'):
            trust_account.balance = float(data.get('balance'))
        trust_account.case_id = data.get('case_id', trust_account.case_id)
        trust_account.description = data.get('description', trust_account.description)
        trust_account.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            "id": trust_account.id,
            "account_name": trust_account.account_name,
            "account_number": trust_account.account_number,
            "balance": float(trust_account.balance) if trust_account.balance else None,
            "case_id": trust_account.case_id,
            "description": trust_account.description,
            "user_id": trust_account.user_id,
            "created_at": trust_account.created_at.isoformat() if trust_account.created_at else None,
            "updated_at": trust_account.updated_at.isoformat() if trust_account.updated_at else None
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@trust_accounts_bp.route("/trust-accounts/<int:trust_account_id>", methods=["DELETE"])
def delete_trust_account(trust_account_id):
    try:
        trust_account = TrustAccount.query.get_or_404(trust_account_id)
        db.session.delete(trust_account)
        db.session.commit()
        return jsonify({"message": "Trust account deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

