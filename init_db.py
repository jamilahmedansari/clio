#!/usr/bin/env python3
"""
Database initialization script for Eviction CRM
Creates tables and sets up initial data
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from src.models import User, Case, Contact, Document, TimeEntry, Expense, Event, Bill, Invoice, Task, TrustAccount, Collaboration, Appointment

def init_database():
    """Initialize the database with tables and sample data"""
    with app.app_context():
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()
        
        # Create a default user
        default_user = User(
            email="admin@evictioncrm.com",
            first_name="Admin",
            last_name="User",
            role="Attorney",
            is_active=True
        )
        
        db.session.add(default_user)
        db.session.commit()
        
        print("Database initialized successfully!")
        print(f"Default user created: {default_user.email}")
        print(f"User ID: {default_user.id}")

if __name__ == "__main__":
    init_database()

