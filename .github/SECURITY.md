# 🔐 Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability please
**do not** open a public GitHub issue.

Instead email us directly:

📧 **gemachistesfaye36@gmail.com**
Subject: `[SECURITY] Vulnerability Report`

Please include:
- Clear description of the vulnerability
- Steps to reproduce it
- Potential impact
- Any suggested fixes

---

## ⏱️ Response Timeline

| Step | Timeframe |
|---|---|
| Acknowledgement | Within 24 hours |
| Initial assessment | Within 48 hours |
| Fix or mitigation | As soon as possible |

---

## 📢 Disclosure

We follow responsible disclosure. After a fix
is released we will publish a security advisory
and credit the reporter if they wish.

---

## 🛡️ Security Best Practices

- All secrets stored in `.env` — never in source code
- `.env` and `.db` files are gitignored
- Passwords hashed with `werkzeug` bcrypt
- All SQL queries use parameterized statements
- Session-based authentication on all protected routes
- Dependencies audited regularly with `pip-audit`

---

*Thank you for helping keep GradeEvaluator AI
safe for students! 🌟*
