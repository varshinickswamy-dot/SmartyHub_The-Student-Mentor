from flask import Flask, render_template, request, redirect, jsonify, flash, send_file
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from models import db, User, Resume

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image,
    Table, TableStyle, ListFlowable, ListItem
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch

import os
from ai.chatbot import reply

# --------------------------------------------------
# APP SETUP
# --------------------------------------------------

app = Flask(__name__)
app.secret_key = "secret123"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "data.db")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
REPORT_FOLDER = os.path.join(BASE_DIR, "reports")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + DB_PATH
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# --------------------------------------------------
# LOGIN MANAGER
# --------------------------------------------------

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/"

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# --------------------------------------------------
# AUTH
# --------------------------------------------------

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form.get("email")).first()
        if user and check_password_hash(user.password, request.form.get("password")):
            login_user(user)
            return redirect("/dashboard")
        flash("Invalid Email or Password")
    return render_template("login.html")


@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        if User.query.filter_by(email=request.form.get("email")).first():
            flash("Email already exists")
            return redirect("/register")
        user = User(
            name=request.form.get("name"),
            email=request.form.get("email"),
            password=generate_password_hash(request.form.get("password"))
        )
        db.session.add(user)
        db.session.commit()
        flash("Registration Successful!")
        return redirect("/")
    return render_template("register.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

# --------------------------------------------------
# CAREER
# --------------------------------------------------

@app.route("/career", methods=["GET","POST"])
@login_required
def career():

    if request.method == "POST":

        stream = request.form.get("stream")
        marks = int(request.form.get("marks"))

        if stream == "science":
            if marks >= 85:
                data = {
                    "result":"Medical (MBBS)",
                    "fees":"₹1L - ₹10L",
                    "duration":"5.5 Years",
                    "subjects":["Biology"],
                    "careers":["Doctor"],
                    "higher":["MD","MS"]
                }
            elif marks >= 70:
                data = {
                    "result":"Engineering (B.Tech)",
                    "fees":"₹80k - ₹2.5L",
                    "duration":"4 Years",
                    "subjects":["Physics","Chemistry","Maths"],
                    "careers":["Software Engineer"],
                    "higher":["M.Tech","MS","PhD"]
                }
            else:
                data = {
                    "result":"B.Sc Science",
                    "fees":"₹30k - ₹80k",
                    "duration":"3 Years",
                    "subjects":["Physics","Chemistry"],
                    "careers":["Teacher"],
                    "higher":["M.Sc","B.Ed"]
                }

        elif stream == "commerce":
            if marks >= 80:
                data = {
                    "result":"Chartered Accountant",
                    "fees":"₹50k - ₹1L",
                    "duration":"4 Years",
                    "subjects":["Accounting"],
                    "careers":["CA"],
                    "higher":["CFA"]
                }
            elif marks >= 65:
                data = {
                    "result":"B.Com",
                    "fees":"₹40k - ₹1L",
                    "duration":"3 Years",
                    "subjects":["Accounts"],
                    "careers":["Accountant"],
                    "higher":["MBA"]
                }
            else:
                data = {
                    "result":"BBA",
                    "fees":"₹50k - ₹1.5L",
                    "duration":"3 Years",
                    "subjects":["Management"],
                    "careers":["HR"],
                    "higher":["MBA"]
                }

        elif stream == "arts":
            if marks >= 75:
                data = {
                    "result":"Journalism",
                    "fees":"₹60k - ₹2L",
                    "duration":"3 Years",
                    "subjects":["Media"],
                    "careers":["Journalist"],
                    "higher":["MA"]
                }
            elif marks >= 60:
                data = {
                    "result":"BA Psychology",
                    "fees":"₹40k - ₹1.2L",
                    "duration":"3 Years",
                    "subjects":["Psychology"],
                    "careers":["Counselor"],
                    "higher":["MA"]
                }
            else:
                data = {
                    "result":"BA General",
                    "fees":"₹30k - ₹80k",
                    "duration":"3 Years",
                    "subjects":["History"],
                    "careers":["Teacher"],
                    "higher":["MA"]
                }

        return render_template("career.html",
                               result=data["result"],
                               details=data)

    return render_template("career.html")

# --------------------------------------------------
# CHATBOT
# --------------------------------------------------

@app.route("/chatbot")
@login_required
def chatbot():
    return render_template("chatbot.html")

@app.route("/chat", methods=["POST"])
@login_required
def chat():
    return jsonify({"reply": reply(request.json.get("msg"))})
# --------------------------------------------------
# ✅ RESUME BUILDER (MODERN TWO COLUMN PDF)
# --------------------------------------------------

@app.route("/resume", methods=["GET", "POST"])
@login_required
def resume():

    if request.method == "POST":

        # ---------------- PHOTO ----------------
        photo_path = None
        photo = request.files.get("photo")

        if photo and photo.filename:
            filename = secure_filename(photo.filename)
            photo_path = os.path.join(UPLOAD_FOLDER, filename)
            photo.save(photo_path)

        # ---------------- FORM DATA ----------------
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        phone = request.form.get("phone", "")
        address = request.form.get("address", "")
        links = request.form.get("links", "")

        summary = request.form.get("summary", "")
        skills = request.form.get("skills", "")
        education = request.form.get("education", "")
        experience = request.form.get("experience", "")
        projects = request.form.get("projects", "")
        certifications = request.form.get("certifications", "")
        achievements = request.form.get("achievements", "")
        languages = request.form.get("languages", "")
        hobbies = request.form.get("hobbies", "")

        # ---------------- SAVE DB ----------------
        r = Resume(
            user_id=current_user.id,
            name=name,
            email=email,
            skills=skills,
            education=education,
            projects=projects
        )
        db.session.add(r)
        db.session.commit()

        # ---------------- PDF PATH ----------------
        pdf_path = os.path.join(REPORT_FOLDER, f"resume_{r.id}.pdf")

        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=A4,
            rightMargin=25,
            leftMargin=25,
            topMargin=25,
            bottomMargin=25
        )

        elements = []
        styles = getSampleStyleSheet()

        # ---------------- STYLES ----------------
        resume_heading = ParagraphStyle(
            "resume_heading",
            parent=styles["Heading1"],
            alignment=1,
            fontSize=24,
            textColor=colors.HexColor("#0f766e"),
            spaceAfter=10
        )

        name_style = ParagraphStyle(
            "name",
            fontSize=20,
            textColor=colors.white,
            spaceAfter=10
        )

        contact_style = ParagraphStyle(
            "contact",
            fontSize=9,
            textColor=colors.whitesmoke,
            spaceAfter=4
        )

        left_title = ParagraphStyle(
            "left_title",
            fontSize=11,
            textColor=colors.white,
            backColor=colors.HexColor("#0f766e"),
            leftIndent=6,
            spaceBefore=12,
            spaceAfter=6
        )

        left_text = ParagraphStyle(
            "left_text",
            fontSize=9,
            textColor=colors.white,
            spaceAfter=4
        )

        right_title = ParagraphStyle(
            "right_title",
            fontSize=13,
            textColor=colors.HexColor("#0f766e"),
            spaceBefore=12,
            spaceAfter=6
        )

        body = ParagraphStyle(
            "body",
            fontSize=10.5,
            spaceAfter=6
        )

        # ---------------- TOP HEADING ----------------
        elements.append(Paragraph("RESUME", resume_heading))
        elements.append(Spacer(1, 8))
        elements.append(HRFlowable(width="100%", thickness=1,
                                   color=colors.HexColor("#0f766e")))
        elements.append(Spacer(1, 12))

        # ---------------- LEFT COLUMN ----------------
        left = []

        if photo_path:
            left.append(Image(photo_path, 1.5 * inch, 1.5 * inch))
            left.append(Spacer(1, 12))

        left.append(Paragraph(name.upper(), name_style))

        if email:
            left.append(Paragraph(email, contact_style))
        if phone:
            left.append(Paragraph(phone, contact_style))
        if address:
            left.append(Paragraph(address, contact_style))
        if links:
            left.append(Paragraph(links, contact_style))

        # SUMMARY
        if summary:
            left.append(Paragraph("SUMMARY", left_title))
            left.append(Paragraph(summary, left_text))

        # LANGUAGES
        if languages:
            left.append(Paragraph("LANGUAGES", left_title))
            for l in languages.split(","):
                if l.strip():
                    left.append(Paragraph("• " + l.strip(), left_text))

        # HOBBIES
        if hobbies:
            left.append(Paragraph("HOBBIES", left_title))
            for h in hobbies.split(","):
                if h.strip():
                    left.append(Paragraph("• " + h.strip(), left_text))

        # ---------------- RIGHT COLUMN ----------------
        right = []

        if education:
            right.append(Paragraph("EDUCATION", right_title))
            right.append(Paragraph(education, body))

        if skills:
            right.append(Paragraph("SKILLS", right_title))
            right.append(ListFlowable(
                [ListItem(Paragraph(s.strip(), body))
                 for s in skills.split(",") if s.strip()],
                bulletType="bullet"
            ))

        if experience:
            right.append(Paragraph("EXPERIENCE", right_title))
            right.append(Paragraph(experience, body))

        if projects:
            right.append(Paragraph("PROJECTS", right_title))
            right.append(Paragraph(projects, body))

        if certifications:
            right.append(Paragraph("CERTIFICATIONS", right_title))
            right.append(Paragraph(certifications, body))

        if achievements:
            right.append(Paragraph("ACHIEVEMENTS", right_title))
            right.append(Paragraph(achievements, body))

        # ---------------- TWO COLUMN TABLE ----------------
        table = Table([[left, right]], colWidths=[200, 330])

        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#0f766e")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 18),
            ("RIGHTPADDING", (0, 0), (-1, -1), 18),
            ("TOPPADDING", (0, 0), (-1, -1), 18),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 18),
        ]))

        elements.append(table)

        # ---------------- BUILD PDF ----------------
        doc.build(elements)

        return send_file(pdf_path, as_attachment=True)

    return render_template("resume.html")
# --------------------------------------------------
# TIMETABLE
# --------------------------------------------------

@app.route("/timetable")
@login_required
def timetable():
    return render_template("timetable.html")

# --------------------------------------------------
# ADMIN
# --------------------------------------------------

@app.route("/admin")
@login_required
def admin():
    if current_user.role != "admin":
        return "Access Denied"
    return render_template("admin.html", users=User.query.all())

# --------------------------------------------------
# RUN
# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True) 