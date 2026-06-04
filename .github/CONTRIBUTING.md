# Contributing to GradeEvaluator 🚀

First off, thank you for considering contributing to GradeEvaluator! It's people like you that make GradeEvaluator such a great tool for students.

## Where do I go from here?

If you've noticed a bug or have a feature request, make sure to check our [Issues](https://github.com/gemachistesfaye/GradeEvaluator/issues) page to see if someone else has already created a ticket. If not, go ahead and [make one](https://github.com/gemachistesfaye/GradeEvaluator/issues/new/choose)!

## Fork & create a branch

If this is something you think you can fix, then fork GradeEvaluator and create a branch with a descriptive name.

A good branch name would be (where issue #325 is the ticket you're working on):

```sh
git checkout -b 325-add-localization-support
```

## Implementation Guidelines

### Frontend (Vanilla JS + CSS)
- We use Vanilla CSS (no Tailwind) to keep the project lightweight.
- Ensure that any new styles respect our `dark-theme` CSS variables located in `base.html`.
- Maintain the glassmorphism and modern UI aesthetics of the project.
- Write clean, modular Vanilla JavaScript. Keep scope contained.

### Backend (Python/Flask)
- Follow PEP 8 style guide for Python code.
- Ensure all new routes in `app.py` handle both GET and POST requests appropriately if form data is involved.
- Add logging where necessary, but keep it clean.

- **Frontend:** Use Vanilla JS and CSS. Respect existing `dark-theme` variables and maintain glassmorphism aesthetics.
- **Backend (Flask):** Follow PEP 8, handle GET/POST requests appropriately, and keep logs clean.

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run `python run.py` to test locally on `http://localhost:5000`.

## Pull Requests

1. Follow style guidelines.
2. Use a descriptive PR title.
3. Complete the PR template.
4. Include screenshots for UI changes.

We aim to review PRs within one business day. Thank you for contributing! 🎉
