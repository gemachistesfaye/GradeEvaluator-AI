import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db, init_db
from ai_feedback import generate_ai_feedback
from export import export_grades_csv

app = Flask(__name__)
app.secret_key = "super_secret_key_v2" # Should be random in production

# Ensure DB is initialized
if not os.path.exists("gradeevaluator.db"):
    init_db()

def get_grade_info(score):
    if score >= 90: return "A+", 4.0
    elif score >= 85: return "A", 4.0
    elif score >= 80: return "A-", 3.75
    elif score >= 75: return "B+", 3.5
    elif score >= 70: return "B", 3.0
    elif score >= 65: return "B-", 2.75
    elif score >= 60: return "C+", 2.5
    elif score >= 55: return "C", 2.0
    elif score >= 50: return "C-", 1.75
    elif score >= 40: return "D", 1.5
    else: return "F (NG)", 0.0

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        flash("We've upgraded! Please register or log in to save your grades in the new v2.0 dashboard.", "warning")
        return redirect(url_for("register"))
        
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip()
        password = request.form["password"]
        date_str = datetime.datetime.now().strftime("%B %d, %Y")
        
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT id FROM students WHERE email = ?", (email,))
        if cur.fetchone() is not None:
            flash("Email already registered.", "danger")
            return redirect(url_for("register"))
            
        hashed_pw = generate_password_hash(password)
        cur.execute("INSERT INTO students (name, email, password, joined_date) VALUES (?, ?, ?, ?)", (name, email, hashed_pw, date_str))
        db.commit()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"]
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM students WHERE email = ?", (email,))
        user = cur.fetchone()
        if user and check_password_hash(user["password"], password):
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
        
    db = get_db()
    cur = db.cursor()
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
                
                ai_feedback = generate_ai_feedback(session["user_name"], subject, score, letter_grade, gpa_points, date_str)
                
                cur.execute("INSERT INTO grades (student_id, subject, score, letter_grade, gpa_points, ai_feedback, date) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (user_id, subject, score, letter_grade, gpa_points, ai_feedback, date_str))
                db.commit()
                flash("Grade evaluated and saved!", "success")
        except ValueError:
            flash("Please enter a valid number.", "danger")
            
    cur.execute("SELECT * FROM grades WHERE student_id = ? ORDER BY id DESC", (user_id,))
    grades = cur.fetchall()
    
    return render_template("dashboard.html", grades=grades, name=session["user_name"])

@app.route("/history")
def history():
    if "user_id" not in session:
        return redirect(url_for("login"))
    db = get_db()
    cur = db.cursor()
    search = request.args.get("search", "")
    if search:
        cur.execute("SELECT * FROM grades WHERE student_id = ? AND (subject LIKE ? OR date LIKE ?) ORDER BY id DESC", (session["user_id"], f"%{search}%", f"%{search}%"))
    else:
        cur.execute("SELECT * FROM grades WHERE student_id = ? ORDER BY id DESC", (session["user_id"],))
    grades = cur.fetchall()
    return render_template("history.html", grades=grades, search=search)

@app.route("/history/delete/<int:grade_id>")
def delete_grade(grade_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM grades WHERE id = ? AND student_id = ?", (grade_id, session["user_id"]))
    db.commit()
    flash("Grade deleted.", "info")
    return redirect(url_for("history"))

@app.route("/history/clear")
def clear_history():
    if "user_id" not in session:
        return redirect(url_for("login"))
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM grades WHERE student_id = ?", (session["user_id"],))
    db.commit()
    flash("History cleared.", "info")
    return redirect(url_for("history"))

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))
    db = get_db()
    cur = db.cursor()
    
    if request.method == "POST":
        new_password = request.form["new_password"]
        if new_password:
            hashed_pw = generate_password_hash(new_password)
            cur.execute("UPDATE students SET password = ? WHERE id = ?", (hashed_pw, session["user_id"]))
            db.commit()
            flash("Password updated successfully.", "success")
            
    cur.execute("SELECT * FROM students WHERE id = ?", (session["user_id"],))
    user = cur.fetchone()
    cur.execute("SELECT COUNT(*) as count FROM grades WHERE student_id = ?", (session["user_id"],))
    grade_count = cur.fetchone()["count"]
    
    return render_template("profile.html", user=user, grade_count=grade_count)

@app.route("/export/csv")
def export_csv():
    if "user_id" not in session:
        return redirect(url_for("login"))
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM grades WHERE student_id = ? ORDER BY id DESC", (session["user_id"],))
    grades = cur.fetchall()
    return export_grades_csv(grades)

if __name__=="__main__":
    app.run(debug=True, port=5000)
