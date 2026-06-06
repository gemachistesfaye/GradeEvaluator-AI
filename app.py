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
    update_user_profile,
    get_user_profile,
    get_grade_count,
    init_db,
)
from ai_feedback import generate_ai_feedback, generate_chat_reply
from export import export_grades_csv, export_grades_pdf

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret")
init_db()

def calculate_cumulative_gpa(grades):
    if not grades:
        return 0.0
        
    for g in grades:
        if g["letter_grade"] == "F (NG)" or g["score"] < 40:
            return "NG"
            
    total_points = sum(
        g["gpa_points"] * g.get("credits", 3)
        for g in grades
    )
    total_credits = sum(g.get("credits", 3) for g in grades)
    if total_credits == 0:
        return 0.0
    return round(total_points / total_credits, 2)

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
    return render_template("index.html", current_cgpa=calculate_cumulative_gpa(get_grades_by_student(session.get('user_id'))) if "user_id" in session else None)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        university = request.form.get("university", "").strip()
        
        if not name or not email or not password:
            flash("All fields are required.", "danger")
            return redirect(url_for("register"))
            
        date_str = datetime.datetime.now().strftime("%B %d, %Y")
        if get_student_by_email(email):
            flash("Email already registered.", "danger")
            return redirect(url_for("register"))
        hashed_pw = generate_password_hash(password)
        create_student(name, email, hashed_pw, date_str, university)
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", current_cgpa=calculate_cumulative_gpa(get_grades_by_student(session.get('user_id'))) if "user_id" in session else None)

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
    return render_template("login.html", current_cgpa=calculate_cumulative_gpa(get_grades_by_student(session.get('user_id'))) if "user_id" in session else None)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    user_id = session["user_id"]
    # Fetch user profile to get university
    user_profile = get_user_profile(user_id)
    university = user_profile.get("university", "")
    if request.method == "POST":
        semester_name = request.form.get("semester_name", "Semester 1").strip()
        subjects = request.form.getlist("subject[]")
        scores = request.form.getlist("grade[]")
        credits_list = request.form.getlist("credits[]")
        
        # Fallback if no JS array used
        if not subjects:
            subjects = [request.form.get("subject", "General").strip()]
            scores = [request.form.get("grade")]
            credits_list = [request.form.get("credits", 3)]

        try:
            for i in range(len(subjects)):
                subject = subjects[i].strip()
                score = float(scores[i])
                credit = int(credits_list[i])
                
                if score < 0 or score > 100:
                    flash(f"Grade for {subject} must be between 0 and 100.", "danger")
                    continue
                    
                letter_grade, gpa_points = get_grade_info(score)
                # Save without AI feedback initially
                add_grade(user_id, subject, score, letter_grade, gpa_points, "", credits=credit, semester_name=semester_name)
                
            flash("Grades evaluated and saved! Click 'Analyze Semester' to get your AI report.", "success")
        except ValueError:
            flash("Please enter valid numbers.", "danger")
            
    grades = get_grades_by_student(user_id)
    
    # Group grades by semester
    from collections import OrderedDict
    semesters_dict = OrderedDict()
    for g in grades:
        sem_name = g.get('semester_name', 'Semester 1')
        if sem_name not in semesters_dict:
            semesters_dict[sem_name] = []
        semesters_dict[sem_name].append(g)
        
    semesters_data = []
    for sem_name, sem_grades in semesters_dict.items():
        semesters_data.append({
            'name': sem_name,
            'grades': sem_grades,
            'sgpa': calculate_cumulative_gpa(sem_grades)
        })
        
    return render_template("dashboard.html", grades=grades, semesters_data=semesters_data, name=session["user_name"], university=university, cumulative_gpa=calculate_cumulative_gpa(grades), current_cgpa=calculate_cumulative_gpa(grades))

@app.route("/generate_report", methods=["POST"])
def generate_report():
    if "user_id" not in session:
        return redirect(url_for("login"))
    user_id = session["user_id"]
    grades = get_grades_by_student(user_id)
    if not grades:
        flash("No grades to analyze.", "warning")
        return redirect(url_for("dashboard"))
        
    cumulative_gpa = calculate_cumulative_gpa(grades)
    grades_summary = f"Actual Cumulative GPA: {cumulative_gpa}\n" + "\n".join([f"- {g['subject']}: {g['score']}/100 ({g['letter_grade']}), {g.get('credits', 3)} credits" for g in grades])
    date_str = datetime.datetime.now().strftime("%B %d, %Y")
    
    from ai_feedback import generate_semester_report
    report = generate_semester_report(session["user_name"], grades_summary, date_str)
    
    # Save report to the most recent grade to persist it
    from database import get_db
    with get_db() as conn:
        conn.execute("UPDATE grades SET ai_feedback = ? WHERE id = ?", (report, grades[0]["id"]))
        conn.commit()
        
    flash("Semester report generated successfully!", "success")
    return redirect(url_for("dashboard"))

@app.route("/chat", methods=["POST"])
def chat():
    if "user_id" not in session:
        return {"reply": "Please log in first!"}, 403
    
    data = request.get_json()
    message = data.get("message")
    grade_id = data.get("grade_id")
    conversation = data.get("conversation", [])
    
    grades = get_grades_by_student(session["user_id"])
    target_grade = next((g for g in grades if g["id"] == grade_id), None)
    
    if not target_grade:
        return {"reply": "Grade not found."}, 404
        
    reply = generate_chat_reply(
        session["user_name"], target_grade["subject"],
        target_grade["score"], target_grade["letter_grade"],
        target_grade["gpa_points"], target_grade["date"],
        conversation, message
    )
    return {"reply": reply}

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
    return render_template("history.html", grades=grades, search=search, current_cgpa=calculate_cumulative_gpa(grades))

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
    flash("History cleared. You can now start from scratch!", "info")
    return redirect(request.referrer or url_for("dashboard"))

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))
    user_id = session["user_id"]
    if request.method == "POST":
        # Handle name/university updates
        new_name = request.form.get("name")
        new_university = request.form.get("university")
        if new_name or new_university:
            update_user_profile(user_id, name=new_name if new_name else None, university=new_university if new_university else None)
            flash("Profile updated successfully.", "success")
    user = get_user_profile(user_id)
    grade_count = get_grade_count(user_id)
    return render_template("profile.html", user=user, grade_count=grade_count, cumulative_gpa=calculate_cumulative_gpa(get_grades_by_student(user_id)), current_cgpa=calculate_cumulative_gpa(get_grades_by_student(user_id)))
@app.route('/settings')
def settings():
    if "user_id" not in session:
        return redirect(url_for('login'))
    # Placeholder settings page – you can extend with actual settings fields later
    return render_template('settings.html', name=session.get('user_name', 'User'), current_cgpa=calculate_cumulative_gpa(get_grades_by_student(session.get('user_id'))) if "user_id" in session else None)

@app.route('/notifications')
def notifications():
    if "user_id" not in session:
        return redirect(url_for('login'))
    # Placeholder for future notifications list
    notifications = []
    return render_template('notifications.html', notifications=notifications, current_cgpa=calculate_cumulative_gpa(get_grades_by_student(session.get('user_id'))) if "user_id" in session else None)

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


