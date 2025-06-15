import os
from flask import Flask
from flask_cors import CORS
from src.models import db

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins="https://friendly-monstera-afca26.netlify.app/")

# Supabase PostgreSQL configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:jbgbaCDhGfw52GNT@db.kdczlvudghomhjwzeuwe.supabase.co:5432/postgres"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "your-secret-key-here"

# Initialize SQLAlchemy with app
db.init_app(app)

# Import and register blueprints
from src.routes.cases import cases_bp
from src.routes.contacts import contacts_bp
from src.routes.documents import documents_bp
from src.routes.tasks import tasks_bp
from src.routes.events import events_bp
from src.routes.time_entries import time_entries_bp
from src.routes.expenses import expenses_bp
from src.routes.bills import bills_bp
from src.routes.invoices import invoices_bp
from src.routes.trust_accounts import trust_accounts_bp
from src.routes.collaboration import collaboration_bp
from src.routes.appointments import appointments_bp
from src.routes.users import users_bp

app.register_blueprint(cases_bp, url_prefix="/api")
app.register_blueprint(contacts_bp, url_prefix="/api")
app.register_blueprint(documents_bp, url_prefix="/api")
app.register_blueprint(tasks_bp, url_prefix="/api")
app.register_blueprint(events_bp, url_prefix="/api")
app.register_blueprint(time_entries_bp, url_prefix="/api")
app.register_blueprint(expenses_bp, url_prefix="/api")
app.register_blueprint(bills_bp, url_prefix="/api")
app.register_blueprint(invoices_bp, url_prefix="/api")
app.register_blueprint(trust_accounts_bp, url_prefix="/api")
app.register_blueprint(collaboration_bp, url_prefix="/api")
app.register_blueprint(appointments_bp, url_prefix="/api")
app.register_blueprint(users_bp, url_prefix="/api")

@app.route("/")
def index():
    return {"message": "Eviction CRM API", "status": "running"}

@app.route("/health")
def health():
    return {"status": "healthy", "database": "supabase"}

@app.before_request
def create_tables():
    """Create database tables on first request"""
    if not hasattr(create_tables, 'done'):
        try:
            db.create_all()
            create_tables.done = True
        except Exception as e:
            print(f"Database connection error: {e}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

