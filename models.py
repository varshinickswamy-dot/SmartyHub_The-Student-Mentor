from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# -----------------------------
# USER TABLE
# -----------------------------

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(20), default="student")

    # relationship
    resumes = db.relationship(
        "Resume",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

# -----------------------------
# RESUME TABLE
# -----------------------------

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    skills = db.Column(db.Text)
    education = db.Column(db.Text)
    projects = db.Column(db.Text)