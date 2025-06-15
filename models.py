from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), default='Attorney')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Case(db.Model):
    __tablename__ = 'cases'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    case_number = db.Column(db.String(100), unique=True)
    practice_area = db.Column(db.String(100))
    stage = db.Column(db.String(100))
    date_opened = db.Column(db.Date)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='Active')
    office = db.Column(db.String(100))
    statute_of_limitations = db.Column(db.Date)
    conflict_check = db.Column(db.Boolean, default=False)
    conflict_check_notes = db.Column(db.Text)
    billing_method = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Contact(db.Model):
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    address2 = db.Column(db.Text)
    city = db.Column(db.String(100))
    state = db.Column(db.String(50))
    zip_code = db.Column(db.String(20))
    country = db.Column(db.String(100))
    contact_type = db.Column(db.String(50))  # Client, Opposing Party, etc.
    company_name = db.Column(db.String(255))
    website = db.Column(db.String(255))
    main_phone = db.Column(db.String(20))
    fax_number = db.Column(db.String(20))
    private_notes = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Document(db.Model):
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500))
    file_type = db.Column(db.String(50))
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'))
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TimeEntry(db.Model):
    __tablename__ = 'time_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'))
    user = db.Column(db.String(100))
    activity = db.Column(db.String(255))
    description = db.Column(db.Text)
    date = db.Column(db.Date)
    duration = db.Column(db.Float)  # in hours
    rate = db.Column(db.Numeric(10, 2))
    billable = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Expense(db.Model):
    __tablename__ = 'expenses'
    
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'))
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    date = db.Column(db.Date)
    category = db.Column(db.String(100))
    activity = db.Column(db.String(255))
    cost = db.Column(db.Numeric(10, 2))
    quantity = db.Column(db.Integer, default=1)
    billable = db.Column(db.Boolean, default=True)
    receipt_path = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'))
    event_type = db.Column(db.String(100))
    location = db.Column(db.String(255))
    all_day = db.Column(db.Boolean, default=False)
    repeats = db.Column(db.Boolean, default=False)
    is_private = db.Column(db.Boolean, default=False)
    not_linked_to_case = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Bill(db.Model):
    __tablename__ = 'bills'
    
    id = db.Column(db.Integer, primary_key=True)
    bill_number = db.Column(db.String(100), unique=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'))
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    due_date = db.Column(db.Date)
    status = db.Column(db.String(50), default='Pending')
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Invoice(db.Model):
    __tablename__ = 'invoices'
    
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(100), unique=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'))
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    due_date = db.Column(db.Date)
    status = db.Column(db.String(50), default='Draft')
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'))
    assigned_to = db.Column(db.String(100))
    due_date = db.Column(db.Date)
    priority = db.Column(db.String(20), default='Medium')
    status = db.Column(db.String(50), default='Pending')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TrustAccount(db.Model):
    __tablename__ = 'trust_accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    account_name = db.Column(db.String(255), nullable=False)
    account_number = db.Column(db.String(100), unique=True)
    balance = db.Column(db.Numeric(15, 2), default=0.00)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'))
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Collaboration(db.Model):
    __tablename__ = 'collaboration'
    
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'))
    message = db.Column(db.Text, nullable=False)
    sender = db.Column(db.String(100), nullable=False)
    visibility = db.Column(db.String(20), default='Internal')  # Internal, External
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'))
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'))
    appointment_date = db.Column(db.DateTime)
    duration = db.Column(db.Integer)  # in minutes
    location = db.Column(db.String(255))
    meeting_type = db.Column(db.String(50))  # In-person, Video, Phone
    status = db.Column(db.String(50), default='Scheduled')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

