<div align="center">

# 🌍 Amaanitvam Foundation — Volunteer Management Portal

**An intelligent, AI-powered volunteer management ecosystem for streamlined recruitment, task assignment, event coordination, and impact tracking.**

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React_18-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://react.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL_15-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

[Live Demo](#-live-demo) · [Features](#-features) · [Quick Start](#-quick-start) · [API Docs](#-api-documentation) · [Architecture](#-architecture) · [Contributing](#-contributing)

</div>

---

## 📖 Overview

The **Volunteer Management Portal** is a production-grade full-stack application designed to empower the Amaanitvam Foundation with data-driven volunteer engagement. It features an **AI-powered matching engine** that intelligently pairs volunteers with tasks based on skills, availability, and historical performance — maximizing social impact while minimizing coordination overhead.

### ✨ Built for Impact

- **AI-Powered Matching** — Rule-based scoring with optional LLM enhancement (Ollama / OpenAI)
- **Zero-Cloud-Cost Baseline** — Local LLM fallback ensures operation without cloud API costs
- **Zero-PII Architecture** — Privacy-first design inspired by award-winning Vitalis platform
- **Production Hardened** — Gunicorn process manager, health checks, async-safe operations

---

## 🎯 Features

### Core Functionality

| Feature | Description | Status |
|---------|-------------|--------|
| **JWT Authentication** | Secure login with role-based access control (Admin, Coordinator, Volunteer) | ✅ |
| **Volunteer Profiles** | Comprehensive profiles with skills, availability, and badges | ✅ |
| **Event Management** | Create, manage, and track events with capacity limits | ✅ |
| **Task Assignment** | Manual and AI-assisted volunteer-to-task matching | ✅ |
| **AI Matching Engine** | Intelligent recommendations with confidence scores and explainability | ✅ |
| **Dashboard & Analytics** | Real-time KPIs with Chart.js visualizations | ✅ |
| **In-App Notifications** | Alerts for assignments, reminders, and event updates | ✅ |
| **Attendance Tracking** | Check-in/check-out with automatic hour logging | ✅ |

### AI-Powered Matching

The portal features a sophisticated matching engine that considers:
- **Skill Matching** — Exact (100%) and fuzzy (70%) skill alignment via RapidFuzz
- **Availability** — Real-time schedule conflict detection
- **Historical Performance** — Completion rate bonuses/penalties
- **Explainable AI** — Clear reasoning for every recommendation

> 🔮 **Coming Soon:** PDF/CSV report export, email notifications (SMTP configured), recurring events

---

## 🚀 Live Demo

| Environment | URL | Status |
|-------------|-----|--------|
| **Production** | [volunteer-portal-demo.onrender.com](https://volunteer-portal-demo.onrender.com) | 🟢 Live |
| **API Docs** | [volunteer-portal-demo.onrender.com/docs](https://volunteer-portal-demo.onrender.com/docs) | 🟢 Live |

### Demo Accounts

| Role | Email | Password |
|------|-------|----------|
| Admin | `admin@amaanitvam.org` | `Admin@123` |
| Coordinator | `coordinator@amaanitvam.org` | `Coord@123` |
| Volunteer | `volunteer@amaanitvam.org` | `Vol@123` |

---

## 🛠️ Tech Stack

<table>
<tr>
<td>

### Backend
- **FastAPI** — High-performance async Python framework
- **PostgreSQL 15** — ACID-compliant with JSONB support
- **SQLAlchemy 2.0** — Modern async ORM
- **Gunicorn + Uvicorn** — Production ASGI server
- **bcrypt** — Async-safe password hashing
- **Alembic** — Database migrations

</td>
<td>

### Frontend
- **React 18** — Component-based UI with concurrent features
- **Vite 5** — Lightning-fast build tooling
- **Tailwind CSS 3.4** — Utility-first styling
- **TanStack Query** — Server state management
- **Chart.js** — Data visualization
- **React Hook Form + Zod** — Form handling & validation

</td>
</tr>
<tr>
<td>

### Infrastructure
- **Docker** — Multi-stage containerization
- **GitHub Actions** — CI/CD pipeline
- **Render / Railway** — Cloud deployment

</td>
<td>

### AI & Data
- **RapidFuzz** — Fast fuzzy string matching
- **Ollama** — Local LLM (zero cost)
- **OpenAI** — Cloud LLM fallback

</td>
</tr>
</table>

---

## 🏗️ Architecture

```
┌─────────────────┐      ┌───────────────────────┐      ┌─────────────────┐
│   React SPA     │◄────►│  FastAPI + Gunicorn    │◄────►│  PostgreSQL 15  │
│   (Vite 5)      │ HTTPS│  (4 Uvicorn Workers)  │      │  (JSONB + FTS)  │
└─────────────────┘      └───────────────────────┘      └─────────────────┘
                                    │
                                    ▼
                           ┌─────────────────┐
                           │  AI Matching     │
                           │  Engine          │
                           │  (Rule-based +   │
                           │   LLM Fallback)  │
                           └─────────────────┘
```

For detailed architecture, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

---

## ⚡ Quick Start

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) 24.0+
- [Docker Compose](https://docs.docker.com/compose/install/) 2.0+
- [Git](https://git-scm.com/downloads)

### One-Command Setup

```bash
# Clone the repository
git clone https://github.com/aashu035/volunteer-management-portal.git
cd volunteer-management-portal

# Start all services
docker-compose up --build

# 🎉 Access the application
# Frontend:  http://localhost:5173
# Backend:   http://localhost:8000
# API Docs:  http://localhost:8000/docs
# Health:    http://localhost:8000/health
```

### Manual Setup (Development)

<details>
<summary><strong>Backend</strong></summary>

```bash
cd backend
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env         # Edit with your database credentials
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

</details>

<details>
<summary><strong>Frontend</strong></summary>

```bash
cd frontend
npm install
cp .env.example .env         # Edit with your API URL
npm run dev
```

</details>

---

## 📡 API Documentation

Interactive API documentation is auto-generated by FastAPI:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`

### Key Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/auth/register` | Register new user | No |
| POST | `/api/v1/auth/login` | User login | No |
| GET | `/api/v1/users/me` | Current user profile | Yes |
| GET | `/api/v1/events` | List all events | Yes |
| POST | `/api/v1/events` | Create event | Coordinator+ |
| POST | `/api/v1/events/{id}/register` | Register for event | Volunteer |
| POST | `/api/v1/tasks/{id}/assign` | Assign volunteer | Coordinator+ |
| POST | `/api/v1/ai/recommend` | AI recommendations | Coordinator+ |
| GET | `/api/v1/dashboard/admin` | Admin dashboard | Admin |

For the complete API reference, see [docs/SRS.md](docs/SRS.md).

---

## 📁 Project Structure

```
volunteer-management-portal/
├── backend/                      # FastAPI application
│   ├── app/
│   │   ├── api/v1/              # API route handlers
│   │   ├── core/                # Security, RBAC, logging
│   │   ├── models/              # SQLAlchemy ORM models
│   │   ├── schemas/             # Pydantic request/response schemas
│   │   ├── services/            # Business logic layer
│   │   ├── repositories/        # Data access layer
│   │   ├── db/                  # Database engine & sessions
│   │   └── utils/               # Helpers & validators
│   ├── alembic/                 # Database migrations
│   ├── tests/                   # Pytest test suite
│   ├── Dockerfile               # Multi-stage Docker build
│   └── requirements.txt         # Python dependencies
│
├── frontend/                     # React SPA
│   ├── src/
│   │   ├── api/                 # Axios API client modules
│   │   ├── components/          # Reusable UI components
│   │   ├── pages/               # Route page components
│   │   ├── hooks/               # Custom React hooks
│   │   ├── context/             # React Context providers
│   │   └── utils/               # Constants, formatters, cn()
│   ├── Dockerfile               # Multi-stage Docker build
│   └── package.json             # Node.js dependencies
│
├── docs/                         # Project documentation
│   ├── PRD.md                   # Product Requirements
│   ├── SRS.md                   # Software Requirements
│   ├── ARCHITECTURE.md          # System Architecture
│   └── TECH_STACK.md            # Technology Stack
│
├── .github/workflows/           # CI/CD pipelines
├── docker-compose.yml           # Local dev orchestration
├── Makefile                     # Common dev commands
├── CONTRIBUTING.md              # Contribution guidelines
├── LICENSE                      # MIT License
└── README.md                    # This file
```

---

## 🧪 Testing

```bash
# Run backend tests with coverage
make test-backend

# Or manually:
cd backend && pytest --cov=app --cov-report=term-missing -v

# Lint frontend
cd frontend && npm run lint
```

---

## 🚢 Deployment

### Production (Render)

1. Push code to GitHub
2. Connect repository to [Render](https://render.com)
3. Set environment variables in Render dashboard
4. Deploy automatically on push to `main`

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `JWT_SECRET` | 256-bit secret for JWT signing | Yes |
| `ENV` | `development` or `production` | Yes |
| `FRONTEND_URL` | Frontend origin for CORS | Yes |
| `OLLAMA_URL` | Local LLM endpoint | No |
| `OPENAI_API_KEY` | OpenAI API key | No |
| `SMTP_HOST` | SMTP server hostname | No |
| `SMTP_USER` | SMTP username | No |
| `SMTP_PASS` | SMTP password | No |

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

```bash
# Fork → Clone → Branch → Commit → PR
git checkout -b feature/amazing-feature
git commit -m 'feat: add amazing feature'
git push origin feature/amazing-feature
```

---

## 📜 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

## 📫 Contact

**Harsh Sharma**

[![Email](https://img.shields.io/badge/Email-aashusharma2332@gmail.com-red?style=flat&logo=gmail)](mailto:aashusharma2332@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Harsh_Sharma-blue?style=flat&logo=linkedin)](https://linkedin.com/in/harsh-sharma-597b02216)
[![GitHub](https://img.shields.io/badge/GitHub-aashu035-black?style=flat&logo=github)](https://github.com/aashu035)

**Project Link:** [github.com/aashu035/volunteer-management-portal](https://github.com/aashu035/volunteer-management-portal)

---

<div align="center">

*Built with passion for the Amaanitvam Foundation. Every line of code is a step toward a better world.* 🌍

</div>
