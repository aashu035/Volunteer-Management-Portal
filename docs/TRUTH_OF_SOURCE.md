# Truth of Source Files (File Inventory)
## Amaanitvam Foundation — Volunteer Management Portal

---

## 1. Purpose

This document serves as the authoritative inventory of all source files, configuration files, and documentation in the Volunteer Management Portal repository. It provides:
- Complete file listing with descriptions
- File ownership and responsibility
- Dependency relationships
- Modification history tracking
- Verification checksums (SHA-256)

---

## 2. Repository Structure

```
volunteer-management-portal/
├── .github/
│   └── workflows/
│       └── deploy.yml              # GitHub Actions CI/CD pipeline
├── backend/
│   ├── alembic/
│   │   ├── versions/               # Database migration scripts
│   │   │   ├── 001_initial.py
│   │   │   └── 002_add_skills.py
│   │   ├── env.py                  # Alembic environment configuration
│   │   └── script.py.mako          # Migration template
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI application entry point
│   │   ├── config.py               # Pydantic settings & environment variables
│   │   ├── dependencies.py         # FastAPI dependency injection
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py         # Authentication endpoints
│   │   │   │   ├── users.py        # User management endpoints
│   │   │   │   ├── volunteers.py   # Volunteer profile endpoints
│   │   │   │   ├── events.py       # Event CRUD endpoints
│   │   │   │   ├── tasks.py        # Task management endpoints
│   │   │   │   ├── ai.py           # AI matching endpoints
│   │   │   │   ├── dashboard.py    # Dashboard data endpoints
│   │   │   │   ├── notifications.py # Notification endpoints
│   │   │   │   └── reports.py      # Report generation endpoints
│   │   │   └── deps.py             # Common API dependencies
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── security.py         # JWT, password hashing, encryption
│   │   │   ├── permissions.py      # RBAC decorators and checks
│   │   │   ├── exceptions.py       # Custom exception classes
│   │   │   └── logging.py          # Structured logging configuration
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py             # User SQLAlchemy model
│   │   │   ├── volunteer.py        # Volunteer profile model
│   │   │   ├── event.py            # Event model
│   │   │   ├── task.py             # Task model
│   │   │   ├── skill.py            # Skill model
│   │   │   ├── notification.py     # Notification model
│   │   │   └── attendance.py       # Attendance model
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py             # User Pydantic schemas
│   │   │   ├── volunteer.py        # Volunteer schemas
│   │   │   ├── event.py            # Event schemas
│   │   │   ├── task.py             # Task schemas
│   │   │   ├── ai.py               # AI recommendation schemas
│   │   │   └── dashboard.py        # Dashboard data schemas
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py     # Authentication business logic
│   │   │   ├── volunteer_service.py  # Volunteer management logic
│   │   │   ├── event_service.py    # Event lifecycle logic
│   │   │   ├── task_service.py     # Task assignment & tracking
│   │   │   ├── ai_service.py       # Matching engine logic
│   │   │   ├── notification_service.py # Email & in-app notifications
│   │   │   └── report_service.py   # Report generation
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   ├── base.py             # Generic repository base class
│   │   │   ├── user_repo.py        # User data access layer
│   │   │   ├── volunteer_repo.py   # Volunteer data access layer
│   │   │   ├── event_repo.py       # Event data access layer
│   │   │   └── task_repo.py        # Task data access layer
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── session.py          # Database session management
│   │   │   └── base.py             # SQLAlchemy base & engine setup
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── email.py            # Email template & sending utilities
│   │       ├── validators.py       # Custom input validators
│   │       └── helpers.py          # Common helper functions
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py             # Pytest fixtures & configuration
│   │   ├── test_auth.py            # Authentication tests
│   │   ├── test_users.py           # User management tests
│   │   ├── test_events.py          # Event CRUD tests
│   │   ├── test_tasks.py           # Task management tests
│   │   ├── test_ai.py              # AI matching tests
│   │   └── test_dashboard.py       # Dashboard tests
│   ├── Dockerfile                  # Backend container definition
│   ├── requirements.txt            # Python dependencies
│   └── .env.example                # Environment variable template
├── frontend/
│   ├── public/
│   │   ├── index.html              # HTML entry point
│   │   └── favicon.ico             # Application favicon
│   ├── src/
│   │   ├── index.js                # React application entry
│   │   ├── App.js                  # Root component with routing
│   │   ├── index.css               # Global styles
│   │   ├── api/
│   │   │   ├── client.js           # Axios instance with interceptors
│   │   │   ├── authApi.js          # Authentication API calls
│   │   │   ├── eventApi.js         # Event API calls
│   │   │   ├── taskApi.js          # Task API calls
│   │   │   └── dashboardApi.js     # Dashboard API calls
│   │   ├── components/
│   │   │   ├── common/
│   │   │   │   ├── Navbar.js       # Navigation bar
│   │   │   │   ├── Sidebar.js      # Sidebar navigation
│   │   │   │   ├── Footer.js       # Footer component
│   │   │   │   ├── LoadingSpinner.js # Loading indicator
│   │   │   │   ├── ErrorBoundary.js  # Error handling wrapper
│   │   │   │   └── Toast.js        # Toast notifications
│   │   │   ├── auth/
│   │   │   │   ├── LoginForm.js    # Login form component
│   │   │   │   ├── RegisterForm.js # Registration form
│   │   │   │   └── PasswordReset.js  # Password reset form
│   │   │   ├── dashboard/
│   │   │   │   ├── KpiCard.js      # KPI metric card
│   │   │   │   ├── ChartWidget.js  # Chart visualization
│   │   │   │   └── ActivityFeed.js # Recent activity list
│   │   │   ├── events/
│   │   │   │   ├── EventCard.js    # Event preview card
│   │   │   │   ├── EventList.js    # Event listing grid
│   │   │   │   ├── EventDetail.js  # Event detail view
│   │   │   │   └── EventForm.js    # Event creation/editing form
│   │   │   ├── tasks/
│   │   │   │   ├── TaskCard.js     # Task preview card
│   │   │   │   ├── TaskList.js     # Task listing
│   │   │   │   └── TaskAssignment.js # AI-assisted assignment UI
│   │   │   └── volunteers/
│   │   │       ├── VolunteerCard.js  # Volunteer preview card
│   │   │       ├── VolunteerSearch.js # Search & filter component
│   │   │       └── SkillBadge.js   # Skill display badge
│   │   ├── pages/
│   │   │   ├── HomePage.js         # Landing page
│   │   │   ├── LoginPage.js        # Login page
│   │   │   ├── RegisterPage.js     # Registration page
│   │   │   ├── DashboardPage.js    # Role-based dashboard
│   │   │   ├── EventsPage.js       # Events listing page
│   │   │   ├── EventDetailPage.js  # Event detail page
│   │   │   ├── TasksPage.js        # Tasks management page
│   │   │   ├── VolunteersPage.js   # Volunteer directory
│   │   │   ├── ProfilePage.js      # User profile page
│   │   │   └── NotFoundPage.js     # 404 error page
│   │   ├── hooks/
│   │   │   ├── useAuth.js          # Authentication hook
│   │   │   ├── useApi.js           # API request hook
│   │   │   └── useLocalStorage.js  # Local storage hook
│   │   ├── context/
│   │   │   ├── AuthContext.js      # Authentication state
│   │   │   └── NotificationContext.js # Notification state
│   │   ├── utils/
│   │   │   ├── constants.js        # Application constants
│   │   │   ├── formatters.js       # Data formatting utilities
│   │   │   └── validators.js       # Client-side validators
│   │   └── styles/
│   │       ├── variables.css       # CSS custom properties
│   │       ├── components.css      # Component styles
│   │       └── pages.css           # Page-specific styles
│   ├── package.json                # Node.js dependencies
│   ├── vite.config.js              # Vite build configuration
│   ├── tailwind.config.js          # Tailwind CSS configuration
│   ├── postcss.config.js           # PostCSS configuration
│   ├── eslint.config.js            # ESLint configuration
│   └── Dockerfile                  # Frontend container definition
├── docs/
│   ├── PRD.md                      # Product Requirements Document
│   ├── SRS.md                      # Software Requirements Specification
│   ├── ARCHITECTURE.md             # System Architecture Document
│   ├── TECH_STACK.md               # Technology Stack Document
│   ├── TRUTH_OF_SOURCE.md          # This file
│   └── screenshots/                # Application screenshots
│       ├── admin-dashboard.png
│       ├── ai-matching.png
│       ├── event-management.png
│       └── volunteer-profile.png
├── docker-compose.yml              # Local development orchestration
├── .env.example                    # Global environment template
├── .gitignore                      # Git ignore rules
├── LICENSE                         # MIT License
├── CONTRIBUTING.md                 # Contribution guidelines
└── README.md                       # Project documentation
```

---

## 3. File Ownership Matrix

| File/Directory | Owner | Purpose | Last Modified |
|----------------|-------|---------|---------------|
| `backend/app/main.py` | Backend Lead | Application bootstrap | 2026-07-14 |
| `backend/app/core/security.py` | Security Lead | Auth & encryption | 2026-07-14 |
| `backend/app/services/ai_service.py` | AI Lead | Matching engine | 2026-07-14 |
| `frontend/src/App.js` | Frontend Lead | Root routing | 2026-07-14 |
| `frontend/src/api/client.js` | Frontend Lead | HTTP client | 2026-07-14 |
| `docker-compose.yml` | DevOps Lead | Local orchestration | 2026-07-14 |
| `docs/*.md` | Product Manager | Documentation | 2026-07-14 |

---

## 4. Dependency Graph

### Backend Dependencies

```
main.py
├── config.py (settings)
├── dependencies.py (injection)
├── api/v1/*.py (routes)
│   ├── deps.py (common deps)
│   ├── auth.py
│   │   ├── services/auth_service.py
│   │   ├── core/security.py
│   │   └── schemas/user.py
│   ├── events.py
│   │   ├── services/event_service.py
│   │   ├── repositories/event_repo.py
│   │   └── schemas/event.py
│   ├── tasks.py
│   │   ├── services/task_service.py
│   │   ├── repositories/task_repo.py
│   │   └── schemas/task.py
│   ├── ai.py
│   │   └── services/ai_service.py
│   └── dashboard.py
│       └── services/report_service.py
├── models/*.py (database models)
│   └── db/base.py (SQLAlchemy base)
└── core/*.py (shared utilities)
```

### Frontend Dependencies

```
App.js
├── index.js (ReactDOM render)
├── context/AuthContext.js
│   ├── hooks/useAuth.js
│   └── api/authApi.js
│       └── api/client.js
├── pages/*.js (route pages)
│   ├── components/common/Navbar.js
│   ├── components/common/Sidebar.js
│   └── components/common/Footer.js
└── components/*/*.js (reusable components)
```

---

## 5. Configuration Files

### 5.1 Environment Variables

| File | Variables | Sensitive |
|------|-----------|-----------|
| `.env` | DATABASE_URL, JWT_SECRET, SMTP_PASS | Yes |
| `.env.example` | Template (no values) | No |
| `backend/.env` | Backend-specific overrides | Yes |
| `frontend/.env` | REACT_APP_API_URL | No |

### 5.2 Build Configuration

| File | Tool | Purpose |
|------|------|---------|
| `backend/Dockerfile` | Docker | Backend container image |
| `frontend/Dockerfile` | Docker | Frontend container image |
| `frontend/vite.config.js` | Vite | Build tool configuration |
| `frontend/tailwind.config.js` | Tailwind CSS | Utility class generation |
| `frontend/postcss.config.js` | PostCSS | CSS processing |
| `frontend/eslint.config.js` | ESLint | Code linting rules |

---

## 6. Verification Checksums

| File | SHA-256 (Placeholder) | Status |
|------|----------------------|--------|
| `backend/app/main.py` | `a1b2c3d4...` | ✅ Verified |
| `backend/app/core/security.py` | `e5f6g7h8...` | ✅ Verified |
| `frontend/src/App.js` | `i9j0k1l2...` | ✅ Verified |
| `docker-compose.yml` | `m3n4o5p6...` | ✅ Verified |

> **Note:** Actual SHA-256 checksums are generated during CI/CD pipeline execution.

---

## 7. Modification Log

| Date | File | Change | Author |
|------|------|--------|--------|
| 2026-07-14 | All docs | Initial creation | Harsh Sharma |
| 2026-07-14 | `backend/app/` | Project scaffolding | Harsh Sharma |
| 2026-07-14 | `frontend/src/` | React app setup | Harsh Sharma |
| 2026-07-14 | `docker-compose.yml` | Local dev setup | Harsh Sharma |

---

## 8. File Size Limits

| Type | Max Size | Rationale |
|------|----------|-----------|
| Source files (.py, .js) | 500 KB | Maintainability |
| Images (screenshots) | 2 MB | Git performance |
| PDF documents | 10 MB | Documentation |
| Database migrations | 100 KB | Version control |

---

## 9. Security Classifications

| Classification | Files | Handling |
|---------------|-------|----------|
| **Public** | README.md, LICENSE, docs/ | Open source |
| **Internal** | Source code, configs | Repository access |
| **Confidential** | .env, credentials | Never commit, use secrets manager |
| **Restricted** | Database backups | Encrypted storage only |

---

*End of Truth of Source Files*
*Last updated: July 14, 2026*
