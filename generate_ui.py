import os

os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write('''<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grade Evaluator v2.0</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="{{ url_for('static', filename='charts.js') }}" defer></script>
</head>
<body>
    <nav class="sidebar">
        <div class="logo">🎓 GradeEvaluator</div>
        <ul>
            {% if session.user_id %}
            <li><a href="{{ url_for('dashboard') }}">Dashboard</a></li>
            <li><a href="{{ url_for('history') }}">History</a></li>
            <li><a href="{{ url_for('profile') }}">Profile</a></li>
            <li><a href="{{ url_for('logout') }}">Logout</a></li>
            {% else %}
            <li><a href="{{ url_for('index') }}">Home</a></li>
            <li><a href="{{ url_for('login') }}">Login</a></li>
            <li><a href="{{ url_for('register') }}">Register</a></li>
            {% endif %}
        </ul>
        <button id="theme-toggle">🌓 Toggle Theme</button>
    </nav>
    <main class="content">
        {% with messages = get_flashed_messages(with_categories=true) %}
          {% if messages %}
            {% for category, message in messages %}
              <div class="alert alert-{{ category }}">{{ message }}</div>
            {% endfor %}
          {% endif %}
        {% endwith %}
        {% block content %}{% endblock %}
    </main>
    <script>
        const themeBtn = document.getElementById('theme-toggle');
        themeBtn.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', newTheme);
        });
    </script>
</body>
</html>''')

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write('''{% extends "base.html" %}
{% block content %}
<div class="hero">
    <h1>Welcome to GradeEvaluator v2.0</h1>
    <p>Your AI-powered personal academic coach.</p>
    <a href="{{ url_for('register') }}" class="btn">Get Started</a>
</div>
{% endblock %}''')

with open('templates/register.html', 'w', encoding='utf-8') as f:
    f.write('''{% extends "base.html" %}
{% block content %}
<h2>Register</h2>
<form method="POST" class="auth-form">
    <input type="text" name="name" placeholder="Full Name" required>
    <input type="email" name="email" placeholder="Email" required>
    <input type="password" name="password" placeholder="Password" required>
    <button type="submit" class="btn">Register</button>
</form>
{% endblock %}''')

with open('templates/login.html', 'w', encoding='utf-8') as f:
    f.write('''{% extends "base.html" %}
{% block content %}
<h2>Login</h2>
<form method="POST" class="auth-form">
    <input type="email" name="email" placeholder="Email" required>
    <input type="password" name="password" placeholder="Password" required>
    <button type="submit" class="btn">Login</button>
</form>
{% endblock %}''')

with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write('''{% extends "base.html" %}
{% block content %}
<h2>Welcome back, {{ name }}!</h2>

<div class="charts-container">
    <canvas id="barChart"></canvas>
    <canvas id="pieChart"></canvas>
    <canvas id="lineChart"></canvas>
</div>

<div class="form-container">
    <h3>Evaluate New Grade</h3>
    <form method="POST">
        <input type="text" name="subject" placeholder="Subject" required>
        <input type="number" name="grade" step="0.1" min="0" max="100" placeholder="Score (0-100)" required>
        <button type="submit" class="btn">Evaluate</button>
    </form>
</div>

{% if grades and grades|length > 0 %}
<div class="latest-evaluation">
    <h3>Latest Evaluation</h3>
    <div class="report-box">
        {{ grades[0].ai_feedback | safe }}
    </div>
</div>
{% endif %}

<script>
    // Pass grades data to JS
    const gradesData = {{ grades | tojson | safe }};
</script>
{% endblock %}''')

with open('templates/history.html', 'w', encoding='utf-8') as f:
    f.write('''{% extends "base.html" %}
{% block content %}
<div style="display: flex; justify-content: space-between; align-items: center;">
    <h2>Grade History</h2>
    <div>
        <button onclick="window.print()" class="btn">📥 PDF Report</button>
        <a href="{{ url_for('export_csv') }}" class="btn">📥 CSV Export</a>
        <a href="{{ url_for('clear_history') }}" class="btn btn-danger" onclick="return confirm('Clear all history?')">🗑️ Clear All</a>
    </div>
</div>

<form method="GET" style="margin-bottom: 20px;">
    <input type="text" name="search" placeholder="Search by subject or date..." value="{{ search }}">
    <button type="submit" class="btn">Search</button>
</form>

<table class="history-table">
    <thead>
        <tr>
            <th>Date</th>
            <th>Subject</th>
            <th>Score</th>
            <th>Grade</th>
            <th>GPA</th>
            <th>Action</th>
        </tr>
    </thead>
    <tbody>
        {% for g in grades %}
        <tr>
            <td>{{ g.date }}</td>
            <td>{{ g.subject }}</td>
            <td>{{ g.score }}</td>
            <td><span class="badge badge-{{ g.letter_grade[0]|lower }}">{{ g.letter_grade }}</span></td>
            <td>{{ g.gpa_points }}</td>
            <td><a href="{{ url_for('delete_grade', grade_id=g.id) }}" class="btn btn-danger btn-sm">Delete</a></td>
        </tr>
        {% else %}
        <tr><td colspan="6">No grades found.</td></tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}''')

with open('templates/profile.html', 'w', encoding='utf-8') as f:
    f.write('''{% extends "base.html" %}
{% block content %}
<div class="profile-card">
    <div class="avatar">{{ user.name[0] | upper }}</div>
    <h2>{{ user.name }}</h2>
    <p>Email: {{ user.email }}</p>
    <p>Joined: {{ user.joined_date }}</p>
    <p>Total Grades Checked: {{ grade_count }}</p>
    
    <h3>Change Password</h3>
    <form method="POST">
        <input type="password" name="new_password" placeholder="New Password" required>
        <button type="submit" class="btn">Update Password</button>
    </form>
</div>
{% endblock %}''')

with open('static/style.css', 'w', encoding='utf-8') as f:
    f.write('''
:root {
    --bg-color: #f4f7f6;
    --text-color: #333;
    --sidebar-bg: #2c3e50;
    --sidebar-text: #fff;
    --card-bg: #fff;
    --primary: #3498db;
    --danger: #e74c3c;
    --success: #2ecc71;
    --warning: #f1c40f;
}
[data-theme="dark"] {
    --bg-color: #1a1a1a;
    --text-color: #f4f7f6;
    --sidebar-bg: #111;
    --card-bg: #2c2c2c;
}
body {
    margin: 0;
    font-family: Arial, sans-serif;
    display: flex;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
}
.sidebar {
    width: 250px;
    background-color: var(--sidebar-bg);
    color: var(--sidebar-text);
    padding: 20px;
    display: flex;
    flex-direction: column;
}
.sidebar .logo { font-size: 1.5em; font-weight: bold; margin-bottom: 30px; }
.sidebar ul { list-style: none; padding: 0; flex-grow: 1;}
.sidebar ul li { margin-bottom: 15px; }
.sidebar ul li a { color: var(--sidebar-text); text-decoration: none; font-size: 1.1em;}
.content {
    flex-grow: 1;
    padding: 30px;
    overflow-y: auto;
}
.btn {
    padding: 10px 15px; background: var(--primary); color: #fff; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block;
}
.btn-danger { background: var(--danger); }
.btn-sm { padding: 5px 10px; font-size: 0.9em; }
.charts-container {
    display: flex; gap: 20px; margin-bottom: 30px; flex-wrap: wrap;
}
.charts-container canvas {
    background: var(--card-bg); padding: 15px; border-radius: 8px; width: 30%; min-width: 300px;
}
.form-container, .report-box, .profile-card {
    background: var(--card-bg); padding: 20px; border-radius: 8px; margin-bottom: 20px;
}
.auth-form input, .form-container input {
    display: block; width: 100%; max-width: 400px; padding: 10px; margin-bottom: 15px; border-radius: 5px; border: 1px solid #ccc;
}
.history-table { width: 100%; border-collapse: collapse; background: var(--card-bg); }
.history-table th, .history-table td { padding: 12px; border-bottom: 1px solid #ddd; text-align: left; }
.badge { padding: 5px 10px; border-radius: 12px; color: #fff; font-weight: bold; }
.badge-a { background: var(--success); }
.badge-b { background: var(--warning); }
.badge-c { background: orange; }
.badge-d, .badge-f { background: var(--danger); }
.avatar { width: 60px; height: 60px; border-radius: 50%; background: var(--primary); color: white; display: flex; align-items: center; justify-content: center; font-size: 2em; margin-bottom: 10px; }
@media print {
    .sidebar, .form-container, .btn, #theme-toggle { display: none; }
    .content { padding: 0; }
}
''')

with open('static/charts.js', 'w', encoding='utf-8') as f:
    f.write('''
document.addEventListener("DOMContentLoaded", () => {
    if (typeof gradesData === 'undefined' || gradesData.length === 0) return;
    
    // Process data
    gradesData.reverse(); // oldest first for line chart
    const subjects = gradesData.map(g => g.subject);
    const scores = gradesData.map(g => g.score);
    const dates = gradesData.map(g => g.date);
    
    const dist = {A:0, B:0, C:0, D:0, F:0};
    gradesData.forEach(g => {
        const letter = g.letter_grade[0].toUpperCase();
        if(dist[letter] !== undefined) dist[letter]++;
    });

    // Bar Chart - Grades by subject
    new Chart(document.getElementById('barChart'), {
        type: 'bar',
        data: {
            labels: subjects,
            datasets: [{ label: 'Score', data: scores, backgroundColor: '#3498db' }]
        }
    });

    // Pie Chart - Distribution
    new Chart(document.getElementById('pieChart'), {
        type: 'pie',
        data: {
            labels: Object.keys(dist),
            datasets: [{ data: Object.values(dist), backgroundColor: ['#2ecc71', '#f1c40f', 'orange', '#e74c3c', 'darkred'] }]
        }
    });

    // Line Chart - Progress
    new Chart(document.getElementById('lineChart'), {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{ label: 'Score Over Time', data: scores, borderColor: '#e74c3c', fill: false }]
        }
    });
});
''')

print("All frontend files generated.")
