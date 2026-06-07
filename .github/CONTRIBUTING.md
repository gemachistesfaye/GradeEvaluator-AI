# 🤝 Contributing to GradeEvaluator AI

Thank you for contributing! Every bug report
and pull request helps students track their
grades better. 🎓

---

## 🐛 Bug or Feature Request?

Check the [Issues page](https://github.com/gemachistesfaye/GradeEvaluator/issues)
first. If it's not there, open a
[new one](https://github.com/gemachistesfaye/GradeEvaluator/issues/new/choose).

---

## 🛠️ Setup

```bash
git clone https://github.com/YOUR_USERNAME/GradeEvaluator.git
cd GradeEvaluator
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
python run.py
```

Create a `.env` file in the root:

```
FLASK_SECRET_KEY=your_key
GEMINI_API_KEY=your_gemini_key
```

---

## 🌿 Workflow

```bash
# Create a branch
git checkout -b fix/your-fix-name

# Commit clearly
git commit -m "fix: what you changed"

# Push
git push origin fix/your-fix-name
```

Then open a **Pull Request** and include
screenshots for any UI changes.

---

## 📋 Guidelines

- Vanilla CSS and JS only — no frameworks
- Use CSS variables — never hardcode colors
- Test both light and dark mode
- Follow PEP 8 for all Python code
- Always check `"user_id" in session`
- Use parameterized SQL — never string formatting
- Never commit `.env` or `.db` files

---

## 📬 Contact

📧 gemachistesfaye36@gmail.com
🔗 [@gemachistesfaye](https://github.com/gemachistesfaye)

*Built with ❤️ for Ethiopian Students · June 2026*
