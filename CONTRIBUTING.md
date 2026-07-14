# Contributing to Volunteer Management Portal

Thank you for your interest in contributing to the Amaanitvam Foundation Volunteer Management Portal! This guide will help you get started.

---

## 🚀 Quick Start

```bash
# 1. Fork & clone
git clone https://github.com/<your-username>/volunteer-management-portal.git
cd volunteer-management-portal

# 2. Start services
docker-compose up --build

# 3. Verify
# Frontend: http://localhost:3000
# Backend:  http://localhost:8000/docs
```

---

## 📋 Development Workflow

### Branch Naming

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feature/<description>` | `feature/volunteer-search` |
| Bug Fix | `fix/<description>` | `fix/auth-token-refresh` |
| Docs | `docs/<description>` | `docs/api-reference` |
| Refactor | `refactor/<description>` | `refactor/event-service` |

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add volunteer skill matching algorithm
fix: resolve JWT expiry race condition
docs: update API endpoint documentation
test: add event registration tests
refactor: extract matching logic to service layer
```

---

## 🔧 Local Development

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env         # Edit with your local config
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env         # Edit with your API URL
npm run dev
```

---

## 🧪 Testing

### Backend

```bash
cd backend
pytest --cov=app -v
```

### Frontend

```bash
cd frontend
npm run lint
```

---

## 📐 Code Standards

### Python (Backend)
- **Formatter:** Black (line length 100)
- **Import Sort:** isort
- **Linter:** flake8
- **Type Hints:** Required for all function signatures

### JavaScript (Frontend)
- **Formatter:** Prettier
- **Linter:** ESLint
- **Components:** Functional components with hooks only
- **File Extensions:** `.jsx` for all React components

---

## 🔒 Security

- **Never** commit `.env` files, API keys, or secrets
- Use environment variables for all sensitive configuration
- Report security vulnerabilities privately via email

---

## 📝 Pull Request Process

1. Ensure your code passes all tests and linting
2. Update documentation if you change any API endpoints
3. Fill out the PR template completely
4. Request review from at least one maintainer
5. Squash commits before merging

---

## 📜 Code of Conduct

Be respectful, inclusive, and constructive. We're building for a foundation that helps people — let's embody those values in our collaboration.

---

## 📫 Questions?

Open an issue or reach out to [aashusharma2332@gmail.com](mailto:aashusharma2332@gmail.com).
