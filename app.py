import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import (
    create_student,
    get_student_by_email,
    add_grade,
    get_grades_by_student,
    delete_grade as delete_grade_db,
    clear_grades as clear_grades_db,
    update_user_password,
    get_user_profile,
    get_grade_count,
    init_db,
)
from ai_feedback import generate_ai_feedback, generate_chat_reply
from export import export_grades_csv, export_grades_pdf

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret")
init_db()

def get_grade_info(score):
    if score >= 90:
        return "A+", 4.0
    elif score >= 85:
        return "A", 4.0
    elif score >= 80:
        return "A-", 3.75
    elif score >= 75:
        return "B+", 3.5
    elif score >= 70:
        return "B", 3.0
    elif score >= 65:
        return "B-", 2.75
    elif score >= 60:
        return "C+", 2.5
    elif score >= 55:
        return "C", 2.0
    elif score >= 50:
        return "C-", 1.75
    elif score >= 40:
        return "D", 1.5
    else:
        return "F (NG)", 0.0

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        flash(
            "We've upgraded! Please register or log in to save your grades in the new v2.0 dashboard.",
            "warning",
        )
        return redirect(url_for("register"))
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        
        if not name or not email or not password:
            flash("All fields are required.", "danger")
            return redirect(url_for("register"))
            
        date_str = datetime.datetime.now().strftime("%B %d, %Y")
        if get_student_by_email(email):
            flash("Email already registered.", "danger")
            return redirect(url_for("register"))
        hashed_pw = generate_password_hash(password)
        create_student(name, email, hashed_pw, date_str)
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        
        if not email or not password:
            flash("Email and password are required.", "danger")
            return redirect(url_for("login"))
            
        user = get_student_by_email(email)
        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            return redirect(url_for("dashboard"))
        flash("Invalid email or password.", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    user_id = session["user_id"]
    if request.method == "POST":
        subject = request.form.get("subject", "General").strip()
        try:
            score = float(request.form["grade"])
            if score < 0 or score > 100:
                flash("Grade must be between 0 and 100.", "danger")
            else:
                letter_grade, gpa_points = get_grade_info(score)
                date_str = datetime.datetime.now().strftime("%B %d, %Y")
                ai_feedback = generate_ai_feedback(
                    session["user_name"], subject, score, letter_grade, gpa_points, date_str
                )
                add_grade(user_id, subject, score, letter_grade, gpa_points, ai_feedback)
                flash("Grade evaluated and saved!", "success")
        except ValueError:
            flash("Please enter a valid number.", "danger")
    grades = get_grades_by_student(user_id)
    return render_template("dashboard.html", grades=grades, name=session["user_name"])

@app.route("/history")
def history():
    if "user_id" not in session:
        return redirect(url_for("login"))
    user_id = session["user_id"]
    search = request.args.get("search", "")
    grades = get_grades_by_student(user_id)
    if search:
        grades = [
            g
            for g in grades
            if search.lower() in g["subject"].lower() or search.lower() in g["date"].lower()
        ]
    return render_template("history.html", grades=grades, search=search)

@app.route("/history/delete/<int:grade_id>", methods=["POST"])
def delete_grade(grade_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    delete_grade_db(grade_id, session["user_id"])
    flash("Grade deleted.", "info")
    return redirect(url_for("history"))

@app.route("/history/clear")
def clear_history():
    if "user_id" not in session:
        return redirect(url_for("login"))
    clear_grades_db(session["user_id"])
    flash("History cleared.", "info")
    return redirect(url_for("history"))

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))
    user_id = session["user_id"]
    if request.method == "POST":
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        if current_password and new_password:
            user = get_user_profile(user_id)
            if check_password_hash(user["password_hash"], current_password):
                hashed_pw = generate_password_hash(new_password)
                update_user_password(user_id, hashed_pw)
                flash("Password updated successfully.", "success")
            else:
                flash("Current password is incorrect.", "danger")
    user = get_user_profile(user_id)
    grade_count = get_grade_count(user_id)
    return render_template("profile.html", user=user, grade_count=grade_count)

@app.route("/export/csv")
def export_csv():
    if "user_id" not in session:
        return redirect(url_for("login"))
    grades = get_grades_by_student(session["user_id"])
    return export_grades_csv(grades)

@app.route("/export/pdf")
def export_pdf():
    if "user_id" not in session:
        return redirect(url_for("login"))
    grades = get_grades_by_student(session["user_id"])
    return export_grades_pdf(grades, session["user_name"])

if __name__ == "__main__":
    app.run(debug=True, port=5000)


