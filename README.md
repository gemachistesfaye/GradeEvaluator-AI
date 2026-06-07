<div align="center">

<img src="static/logo.svg" width="80" 
     alt="GradeEvaluator AI Logo" />

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
🐛 **[Report Bug](https://github.com/gemachistesfaye/GradeEvaluator-AI/issues)** ·
✨ **[Request Feature](https://github.com/gemachistesfaye/GradeEvaluator-AI/issues)**

</div>

---

## 🌟 Overview

**GradeEvaluator AI** is a modern, full-stack
academic performance tracker built for university
students who want deep, AI-powered insights into
their academic trajectory.

Enter your subject scores, get instant letter
grades, track your weighted cumulative GPA across
semesters and chat with **GradeBot** — your
personal AI academic coach powered by Google Gemini.

---

## 📸 Screenshots

### Project Interface Overview

| Landing Page | Grade Report | GradeBot AI Chatbot |
| :---: | :---: | :---: |
| ![Landing](https://github.com/user-attachments/assets/f1126582-2de9-46d4-af1c-259aedeac304) | ![Grade Report](https://github.com/user-attachments/assets/65d2ce44-f27d-452b-8a88-27c00162af78) | ![GradeBot](https://github.com/user-attachments/assets/7dd4cc97-7263-4d5e-9dec-1386f0d3e686) |

| Dashboard & Analytics | Dark Mode Interface | Grade History |
| :---: | :---: | :---: |
| ![Dashboard](https://github.com/user-attachments/assets/f901cc98-8401-4940-b3e1-48cb2f85406a) | ![Dark Mode](https://github.com/user-attachments/assets/84d6fa3a-8a64-4952-a7bd-6c09c3f4d317) | ![History](https://github.com/user-attachments/assets/6f5d2385-a081-4f7b-857e-aae9055f9447) |

| Registration Page | Notifications |
| :---: | :---: |
| ![Register](https://github.com/user-attachments/assets/849d28fc-a6e6-4895-9ef3-6a7118166650) | ![Notifications](https://github.com/user-attachments/assets/7be85e46-1be7-4112-8120-909bad6e8cb2) |

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🤖 **GradeBot AI Chatbot** | Floating AI coach — study tips, weekly plans, GPA impact |
| 📊 **Semester Dashboard** | Bar, pie, and line charts across all subjects |
| ⭐ **Real Weighted GPA** | True CGPA calculated using credit hours per course |
| 🌓 **Dark / Light / System Theme** | Three theme modes saved automatically per device |
| 📄 **PDF & CSV Export** | Download full grade transcripts anytime |
| 🔐 **Secure Auth** | Register, login, change password with bcrypt hashing |
| 📋 **Grade History** | Full searchable history with per-grade delete |
| 🏫 **Semester Grouping** | Organize grades by semester, see GPA per semester |

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

> ⚠️ **F (NG) = No Grade.** Any F results in
> NG status for that semester's GPA.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.11, Flask |
| **Database** | SQLite (`sqlite3`) |
| **AI** | Google Gemini API |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Charts** | Chart.js |
| **Fonts** | Inter (Google Fonts) |
| **PDF Export** | ReportLab |
| **Auth** | Werkzeug password hashing |
| **Deploy** | Render + gunicorn |

---

## 📁 Project Structure

```
GradeEvaluator-AI/
├── app.py                 # Flask routes & core logic
├── database.py            # SQLite setup & queries
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
│   ├── chatbot.css        # Chatbot styles
│   ├── charts.js          # Chart.js rendering
│   ├── dashboard.js       # Dashboard UI logic
│   └── logo.svg           # App logo
└── templates/
    ├── base.html          # Shared navbar & layout
    ├── index.html         # Landing page
    ├── login.html         # Login page
    ├── register.html      # Register page
    ├── dashboard.html     # Main dashboard
    ├── history.html       # Grade history
    ├── profile.html       # User profile
    ├── settings.html      # App settings
    └── notifications.html # Notifications
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Google Gemini API key
  (free at [aistudio.google.com](https://aistudio.google.com/app/apikey))

### Installation

**1. Clone the repository:**
```bash
git clone https://github.com/gemachistesfaye/GradeEvaluator-AI.git
cd GradeEvaluator-AI
```

**2. Create virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Create `.env` file:**
```env
FLASK_SECRET_KEY=your_secure_secret_key
GEMINI_API_KEY=your_gemini_api_key_here
FLASK_ENV=development
```

**5. Run the app:**
```bash
python run.py
```

Open **http://localhost:5000** 🎉

---

## 🌐 Deployment

Deployed on **Render** using gunicorn:

```
web: gunicorn app:app
```

Live at: **https://grade-evaluator.onrender.com**

---

## 📅 Changelog

### v2.0.0 — June 2026
- 🤖 GradeBot AI floating chatbot
- ⭐ Real weighted CGPA calculator
- 🏫 Semester grouping with SGPA
- 🌓 Dark / Light / System theme
- 📈 Interactive Chart.js analytics
- 💾 SQLite persistent database
- 🔐 Full auth system
- 📄 PDF & CSV export
- 🔔 Notifications center
- ⚙️ Settings page

### v1.0.0 — August 2025
- 🎉 Initial release
- Basic score to letter grade conversion
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
