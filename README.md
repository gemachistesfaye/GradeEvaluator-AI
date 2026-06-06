<div align="center">

<img src="static/logo.svg" width="80" alt="GradeEvaluator AI Logo" />

# 🎓 GradeEvaluator AI

**A Premium Academic Tracking & AI Coaching Platform**

<img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" />
<img src="https://img.shields.io/badge/Version-v2.0-blue?style=for-the-badge" />
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" />
<img src="https://img.shields.io/badge/Gemini_AI-4285F4?style=for-the-badge&logo=google&logoColor=white" />
<img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white" />
<img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" />

<br/>

🌐 **[Live Demo](https://grade-evaluator.onrender.com)** · 
🐛 **[Report Bug](https://github.com/gemachistesfaye/GradeEvaluator AI/issues)** · 
✨ **[Request Feature](https://github.com/gemachistesfaye/GradeEvaluator AI/issues)**

</div>

---

## 🌟 Overview

**GradeEvaluator AI** is a modern, full-stack academic performance tracker
built for university students who want deep, AI-powered insights into
their academic trajectory.

Enter your subject scores, get instant letter grades, track your
weighted cumulative GPA across semesters, and chat with **GradeBot** —
your personal AI academic coach powered by Google Gemini.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🤖 **GradeBot AI Chatbot** | Floating AI coach — ask study tips, get weekly plans, understand your GPA impact |
| 📊 **Semester Dashboard** | Bar, pie, and line charts showing performance across all subjects |
| ⭐ **Real Weighted GPA** | Calculates true cumulative GPA using credit hours per course |
| 🌓 **Dark / Light / System Theme** | Three theme modes — saved automatically per device |
| 📄 **PDF & CSV Export** | Download full grade transcripts as PDF or spreadsheet |
| 🔐 **Secure Auth** | Register, login, change password with bcrypt hashing |
| 📋 **Grade History** | Full searchable history with per-grade delete |
| 🏫 **Semester Grouping** | Organize grades by semester, see SGPA per semester |

---

## 📊 Grading Scale

| Score Range | Letter Grade | GPA Points |
|------------|--------------|------------|
| 90 – 100 | A+ | 4.0 |
| 85 – 89.9 | A | 4.0 |
| 80 – 84.9 | A- | 3.75 |
| 75 – 79.9 | B+ | 3.5 |
| 70 – 74.9 | B | 3.0 |
| 65 – 69.9 | B- | 2.75 |
| 60 – 64.9 | C+ | 2.5 |
| 55 – 59.9 | C | 2.0 |
| 50 – 54.9 | C- | 1.75 |
| 40 – 49.9 | D | 1.5 |
| Below 40 | F (NG) | 0.0 |

> ⚠️ **F (NG) = No Grade.** Any F in a course results in
> NG status for that semester's GPA.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.11, Flask |
| **Database** | SQLite (via built-in `sqlite3`) |
| **AI** | Google Gemini API (`google-genai`) |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Charts** | Chart.js |
| **Fonts** | Inter (Google Fonts) |
| **PDF Export** | ReportLab |
| **Auth** | Werkzeug password hashing |
| **Deploy** | Render (via Procfile + gunicorn) |

---

## 📁 Project Structure

```
GradeEvaluator AI/
├── app.py                 # Flask routes & core logic
├── database.py            # SQLite database setup & queries
├── ai_feedback.py         # Google Gemini AI integration
├── export.py              # CSV & PDF export logic
├── run.py                 # App entry point
├── requirements.txt       # Python dependencies
├── Procfile               # Render deployment config
├── .env                   # API keys (git-ignored)
├── .gitignore
├── LICENSE
├── .github/
│   ├── CONTRIBUTING.md
│   ├── CODE_OF_CONDUCT.md
│   ├── SECURITY.md
│   └── PULL_REQUEST_TEMPLATE.md
├── static/
│   ├── style.css          # Global design system
│   ├── chatbot.css        # Floating chatbot styles
│   ├── charts.js          # Chart.js rendering
│   ├── dashboard.js       # Dashboard UI logic
│   └── logo.svg           # App logo
└── templates/
    ├── base.html          # Shared navbar & layout
    ├── index.html         # Landing page
    ├── login.html         # Login page
    ├── register.html      # Register page
    ├── dashboard.html     # Main app dashboard
    ├── history.html       # Grade history table
    ├── profile.html       # User profile & settings
    ├── settings.html      # App settings
    └── notifications.html # Notifications center
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- `pip` package manager
- Google Gemini API key
  (free at [aistudio.google.com](https://aistudio.google.com/app/apikey))

### Installation

**1. Clone the repository:**
```bash
git clone https://github.com/gemachistesfaye/GradeEvaluator AI.git
cd GradeEvaluator AI
```

**2. Create and activate virtual environment:**
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Create your `.env` file:**
```env
FLASK_SECRET_KEY=your_secure_secret_key
GEMINI_API_KEY=your_gemini_api_key_here
FLASK_ENV=development
```

**5. Run the app:**
```bash
python run.py
```

Open **http://localhost:5000** in your browser. 🎉

---

## 📸 Screenshots

| Dashboard | GradeBot AI Chat |
| :---: | :---: |
| <img src="PASTE_SCREENSHOT_1" width="400"/> | <img src="PASTE_SCREENSHOT_2" width="400"/> |

| Dark Mode | Grade History |
| :---: | :---: |
| <img src="PASTE_SCREENSHOT_3" width="400"/> | <img src="PASTE_SCREENSHOT_4" width="400"/> |

| Register Page | PDF Export |
| :---: | :---: |
| <img src="PASTE_SCREENSHOT_5" width="400"/> | <img src="PASTE_SCREENSHOT_6" width="400"/> |

> 📸 To add screenshots: open any GitHub issue,
> drag your screenshots into the comment box,
> copy the generated URLs and paste above.

---

## 🌐 Deployment

This app is deployed on **Render** using `gunicorn`:

```
web: gunicorn app:app
```

Live at: **https://grade-evaluator.onrender.com**

---

## 📅 Changelog

### v2.0.0 — June 2026
- 🤖 GradeBot AI floating chatbot (Google Gemini)
- ⭐ Real weighted cumulative GPA calculator
- 🏫 Semester grouping with SGPA per semester
- 🌓 Dark / Light / System theme modes
- 📈 Interactive Chart.js analytics (bar, pie, line)
- 💾 SQLite persistent database
- 🔐 Full login / register / password change system
- 📄 PDF & CSV export
- 🔔 Notifications center
- ⚙️ Settings page

### v1.0.0 — August 2025
- 🎉 Initial release
- Basic score → letter grade conversion
- Simple Flask web UI
- Deployed on Render

---

## 👨‍💻 About the Developer

**Gemachis Tesfaye**
Full Stack Developer & AI Enthusiast

📧 [gemachistesfaye36@gmail.com](mailto:gemachistesfaye36@gmail.com)
🔗 [github.com/gemachistesfaye](https://github.com/gemachistesfaye)

---

<div align="center">
  Made with ❤️ by Gemachis Tesfaye
  <br/>
  ⭐ Star this repo if you found it helpful!
</div>