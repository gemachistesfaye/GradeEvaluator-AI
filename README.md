<div align="center">
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" alt="Status" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript" />

  <h1>🎓 GradeEvaluator AI</h1>
  <p><strong>A Premium Academic Tracking & AI Analytics Platform</strong></p>
</div>

---

## 🌟 Overview

**GradeEvaluator** is a modern, full-stack academic performance tracker designed for students who want deep insights into their academic trajectory. Moving beyond simple calculators, GradeEvaluator features a beautiful glassmorphic UI, robust data visualizations, and an integrated **AI Academic Advisor (GradeBot)** that provides personalized feedback, study plans, and grade improvement strategies.
💡 **Tip:** Use [shields.io](https://shields.io) to generate custom status badges and banners for your project.
## ✨ Key Features

- **📊 Comprehensive Dashboard:** Instantly view your Cumulative GPA, Average Scores, and Total Earned Credits.
- **🤖 GradeBot AI:** An integrated, floating AI chatbot and report generator that analyzes your semester performance and offers actionable academic advice.
- **🌓 Dynamic Dark Mode:** A stunning, system-aware dark/light theme engine that transforms the entire UI instantly.
- **📈 Interactive Analytics:** Beautiful Chart.js integration showing score progression and grade distribution.
- **🖨️ Professional Exporting:** One-click CSV exports and fully formatted, print-ready PDF official transcripts.
- **📱 Responsive Design:** Flawless experience across desktop, tablet, and mobile devices.

## 🛠️ Tech Stack

- **Backend:** Python, Flask, SQLite (SQLAlchemy)
- **Frontend:** Vanilla JavaScript, HTML5, Vanilla CSS (Custom Design System)
- **Data Visualization:** Chart.js
- **AI Integration:** Google Gemini Pro API

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- `pip` package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/gemachistesfaye/GradeEvaluator.git
   cd GradeEvaluator
   ```

2. **Create a virtual environment & install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up Environment Variables:**
   Create a `.env` file in the root directory and add your API keys:
   ```env
   SECRET_KEY=your_secure_secret_key
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. **Initialize the Database:**
   ```bash
   python init_db.py
   ```

5. **Run the Application:**
   ```bash
   python run.py
   ```
   Navigate to `http://localhost:5000` in your browser.

## 📸 Screenshots

*(Replace these links with the image links you get from uploading screenshots to a GitHub issue)*

| Dashboard Analytics | AI Academic Report |
| :---: | :---: |
| <img src="PASTE_YOUR_GITHUB_ISSUE_IMAGE_LINK_HERE_1" width="400"/> | <img src="PASTE_YOUR_GITHUB_ISSUE_IMAGE_LINK_HERE_2" width="400"/> |

| Dark Mode UI | Print-Ready Transcript |
| :---: | :---: |
| <img src="PASTE_YOUR_GITHUB_ISSUE_IMAGE_LINK_HERE_3" width="400"/> | <img src="PASTE_YOUR_GITHUB_ISSUE_IMAGE_LINK_HERE_4" width="400"/> |

| User Profile | Chatbot Interaction |
| :---: | :---: |
| <img src="PASTE_YOUR_GITHUB_ISSUE_IMAGE_LINK_HERE_5" width="400"/> | <img src="PASTE_YOUR_GITHUB_ISSUE_IMAGE_LINK_HERE_6" width="400"/> |

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/gemachistesfaye/GradeEvaluator/issues). Please read our [Contributing Guidelines](.github/CONTRIBUTING.md) before submitting a PR.

## 📄 License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.
## 🔒 Security

- **Secure Authentication:** Uses Flask session secret keys and HTTPS recommendations.
- **Input Validation:** All form inputs are sanitized and validated on both client and server sides.
- **CSRF Protection:** Implemented via Flask‑WTF CSRF token.
- **Dependency Audits:** Regularly run `pip-audit` to detect vulnerable packages.


## 👨‍💻 About the Developer

**Gemachis Tesfaye**  
Full Stack Developer & AI Enthusiast  
📧 Contact: gemachistesfaye36@gmail.com  
🔗 GitHub: [@gemachistesfaye](https://github.com/gemachistesfaye)
