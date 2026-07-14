# System Architecture Document
## Amaanitvam Foundation — Volunteer Management Portal

---

## 1. Architecture Overview

### 1.1 Architectural Style
**Monolithic Modular Architecture** with clear separation of concerns.

While microservices offer scalability, a monolithic approach is optimal for this 24-hour MVP because:
- Simpler deployment and debugging
- Lower operational overhead
- Easier to achieve code coverage targets
- Faster iteration during development

The architecture is **modular** — each domain (auth, events, tasks, AI) is isolated in its own package/module, making future extraction to microservices straightforward.

### 1.2 High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT LAYER                                    │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐               │
│  │   Web Browser   │  │  Mobile Browser │  │   Admin Panel   │               │
│  │   (Volunteers)  │  │  (Coordinators) │  │   (Admins)      │               │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘               │
└───────────┼───────────────────┼───────────────────┼─────────────────────────┘
            │                   │                   │
            └───────────────────┼───────────────────┘
                                │ HTTPS
┌───────────────────────────────┼─────────────────────────────────────────────┐
│                          API GATEWAY LAYER                                   │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │  Nginx (Reverse Proxy) + Uvicorn (ASGI Server)                        ││
│  │  ├── SSL Termination                                                  ││
│  │  ├── Rate Limiting (100 req/min)                                      ││
│  │  ├── Static File Serving                                              ││
│  │  └── Load Balancing (future)                                          ││
│  └─────────────────────────────────────────────────────────────────────────┘│
└───────────────────────────────┬─────────────────────────────────────────────┘
                                │
┌───────────────────────────────┼─────────────────────────────────────────────┐
│                        APPLICATION LAYER (FastAPI)                           │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │  MIDDLEWARE STACK                                                      ││
│  │  ├── CORS Middleware                                                   ││
│  │  ├── Authentication Middleware (JWT validation)                          ││
│  │  ├── Authorization Middleware (RBAC checks)                              ││
│  │  ├── Rate Limiting Middleware                                          ││
│  │  ├── Request Logging Middleware                                        ││
│  │  └── Exception Handling Middleware                                       ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │   AUTH      │ │  VOLUNTEER  │ │   EVENT     │ │    TASK     │          │
│  │   MODULE    │ │   MODULE    │ │   MODULE    │ │   MODULE    │          │
│  │             │ │             │ │             │ │             │          │
│  │ • Register  │ │ • Profile   │ │ • Create    │ │ • Create    │          │
│  │ • Login     │ │ • Skills    │ │ • Update    │ │ • Assign    │          │
│  │ • JWT       │ │ • Avail.    │ │ • List      │ │ • Complete  │          │
│  │ • RBAC      │ │ • Search    │ │ • Register  │ │ • Status    │          │
│  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘ └──────┬──────┘          │
│         │               │               │               │                   │
│  ┌──────┴──────┐ ┌──────┴──────┐ ┌──────┴──────┐ ┌──────┴──────┐          │
│  │  AI MATCH   │ │  NOTIFICATION│ │  DASHBOARD  │ │   REPORT    │          │
│  │   MODULE    │ │   MODULE     │ │   MODULE    │ │   MODULE    │          │
│  │             │ │              │ │             │ │             │          │
│  │ • Recommend │ │ • Email      │ │ • KPI Cards │ │ • Export    │          │
│  │ • Score     │ │ • In-App     │ │ • Charts    │ │ • Filter    │          │
│  │ • Fallback  │ │ • Templates  │ │ • Real-time │ │ • Schedule  │          │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘          │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │  SERVICE LAYER (Business Logic)                                         ││
│  │  ├── AuthService, VolunteerService, EventService, TaskService          ││
│  │  ├── AIService (Matching Engine)                                        ││
│  │  ├── NotificationService                                               ││
│  │  └── ReportService                                                      ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │  DATA ACCESS LAYER (SQLAlchemy ORM)                                     ││
│  │  ├── Repository Pattern (UserRepo, EventRepo, TaskRepo, etc.)          ││
│  │  ├── Unit of Work Pattern                                               ││
│  │  └── Database Migrations (Alembic)                                      ││
│  └─────────────────────────────────────────────────────────────────────────┘│
└───────────────────────────────┬─────────────────────────────────────────────┘
                                │
┌───────────────────────────────┼─────────────────────────────────────────────┐
│                         DATA LAYER                                           │
│  ┌─────────────────────────────┐  ┌─────────────────────────────────────────┐│
│  │     PostgreSQL 15           │  │         Redis (Optional)                ││
│  │  ┌───────────────────────┐  │  │  ┌─────────────────────────────────┐   ││
│  │  │  volunteer_portal    │  │  │  │  • JWT Blacklist                │   ││
│  │  │  ├── users           │  │  │  │  • Rate Limit Counters          │   ││
│  │  │  ├── events          │  │  │  │  • Session Cache                │   ││
│  │  │  ├── tasks           │  │  │  │  • Notification Queue           │   ││
│  │  │  ├── skills          │  │  │  └─────────────────────────────────┘   ││
│  │  │  ├── notifications   │  │  └─────────────────────────────────────────┘│
│  │  │  └── ...           │  │                                             │
│  │  └───────────────────────┘  │  ┌─────────────────────────────────────────┐│
│  │                             │  │      File Storage (Local/Cloud)        ││
│  │  • ACID Transactions       │  │  ┌─────────────────────────────────┐   ││
│  │  • Row-Level Security      │  │  │  • Profile Images               │   ││
│  │  • Full-Text Search        │  │  │  • Event Images                 │   ││
│  │  • JSONB for flexible data │  │  │  • Exported Reports             │   ││
│  │  • Automated Backups       │  │  └─────────────────────────────────┘   ││
│  └─────────────────────────────┘  └─────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Component Architecture

### 2.1 Backend Structure (FastAPI)

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # Application entry point
│   ├── config.py                  # Environment configuration (Pydantic Settings)
│   ├── dependencies.py           # FastAPI dependencies (DB session, auth)
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py            # /api/v1/auth/* endpoints
│   │   │   ├── users.py           # /api/v1/users/* endpoints
│   │   │   ├── volunteers.py      # /api/v1/volunteers/* endpoints
│   │   │   ├── events.py          # /api/v1/events/* endpoints
│   │   │   ├── tasks.py           # /api/v1/tasks/* endpoints
│   │   │   ├── ai.py              # /api/v1/ai/* endpoints
│   │   │   ├── dashboard.py       # /api/v1/dashboard/* endpoints
│   │   │   ├── notifications.py   # /api/v1/notifications/* endpoints
│   │   │   └── reports.py         # /api/v1/reports/* endpoints
│   │   └── deps.py                # Common dependencies (get_db, get_current_user)
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py            # JWT, password hashing, encryption
│   │   ├── permissions.py         # RBAC decorators and checks
│   │   ├── exceptions.py           # Custom exception classes
│   │   └── logging.py             # Structured logging configuration
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                # SQLAlchemy User model
│   │   ├── volunteer.py           # Volunteer profile model
│   │   ├── event.py               # Event model
│   │   ├── task.py                # Task model
│   │   ├── skill.py               # Skill model
│   │   ├── notification.py        # Notification model
│   │   └── attendance.py         # Attendance model
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py                # Pydantic User schemas (request/response)
│   │   ├── volunteer.py           # Volunteer schemas
│   │   ├── event.py               # Event schemas
│   │   ├── task.py                # Task schemas
│   │   ├── ai.py                  # AI recommendation schemas
│   │   └── dashboard.py           # Dashboard data schemas
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py        # Authentication business logic
│   │   ├── volunteer_service.py    # Volunteer management logic
│   │   ├── event_service.py        # Event lifecycle logic
│   │   ├── task_service.py         # Task assignment & tracking
│   │   ├── ai_service.py           # Matching engine logic
│   │   ├── notification_service.py # Email & in-app notifications
│   │   └── report_service.py      # Report generation
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base.py                # Generic repository base class
│   │   ├── user_repo.py           # User data access
│   │   ├── volunteer_repo.py      # Volunteer data access
│   │   ├── event_repo.py          # Event data access
│   │   └── task_repo.py           # Task data access
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── session.py             # Database session management
│   │   └── base.py                # SQLAlchemy base & engine setup
│   │
│   └── utils/
│       ├── __init__.py
│       ├── email.py               # Email template & sending utilities
│       ├── validators.py          # Custom validators
│       └── helpers.py             # Common helper functions
│
├── alembic/                       # Database migration scripts
│   ├── versions/
│   └── env.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Pytest fixtures
│   ├── test_auth.py
│   ├── test_events.py
│   ├── test_tasks.py
│   └── test_ai.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

### 2.2 Frontend Structure (React)

```
frontend/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── index.js
│   ├── App.js
│   ├── index.css
│   │
│   ├── api/
│   │   ├── client.js              # Axios instance with interceptors
│   │   ├── authApi.js
│   │   ├── eventApi.js
│   │   ├── taskApi.js
│   │   └── dashboardApi.js
│   │
│   ├── components/
│   │   ├── common/
│   │   │   ├── Navbar.js
│   │   │   ├── Sidebar.js
│   │   │   ├── Footer.js
│   │   │   ├── LoadingSpinner.js
│   │   │   ├── ErrorBoundary.js
│   │   │   └── Toast.js
│   │   ├── auth/
│   │   │   ├── LoginForm.js
│   │   │   ├── RegisterForm.js
│   │   │   └── PasswordReset.js
│   │   ├── dashboard/
│   │   │   ├── KpiCard.js
│   │   │   ├── ChartWidget.js
│   │   │   └── ActivityFeed.js
│   │   ├── events/
│   │   │   ├── EventCard.js
│   │   │   ├── EventList.js
│   │   │   ├── EventDetail.js
│   │   │   └── EventForm.js
│   │   ├── tasks/
│   │   │   ├── TaskCard.js
│   │   │   ├── TaskList.js
│   │   │   └── TaskAssignment.js
│   │   └── volunteers/
│   │       ├── VolunteerCard.js
│   │       ├── VolunteerSearch.js
│   │       └── SkillBadge.js
│   │
│   ├── pages/
│   │   ├── HomePage.js
│   │   ├── LoginPage.js
│   │   ├── RegisterPage.js
│   │   ├── DashboardPage.js
│   │   ├── EventsPage.js
│   │   ├── EventDetailPage.js
│   │   ├── TasksPage.js
│   │   ├── VolunteersPage.js
│   │   ├── ProfilePage.js
│   │   └── NotFoundPage.js
│   │
│   ├── hooks/
│   │   ├── useAuth.js
│   │   ├── useApi.js
│   │   └── useLocalStorage.js
│   │
│   ├── context/
│   │   ├── AuthContext.js
│   │   └── NotificationContext.js
│   │
│   ├── utils/
│   │   ├── constants.js
│   │   ├── formatters.js
│   │   └── validators.js
│   │
│   └── styles/
│       ├── variables.css
│       ├── components.css
│       └── pages.css
│
├── package.json
├── tailwind.config.js
└── Dockerfile
```

---

## 3. Data Flow Architecture

### 3.1 Authentication Flow

```
┌──────────┐     POST /api/v1/auth/register     ┌──────────────┐
│  Client  │ ─────────────────────────────────> │   FastAPI    │
│          │                                      │   Backend    │
│          │ <───────────────────────────────── │              │
│          │     201 Created + JWT Token         │              │
│          │                                      │              │
│          │     POST /api/v1/auth/login         │              │
│          │ ─────────────────────────────────> │              │
│          │                                      │              │
│          │ <───────────────────────────────── │              │
│          │     200 OK + Access & Refresh       │              │
│          │                                      └──────────────┘
│          │                                           │
│          │     Subsequent Requests                    │
│          │     Authorization: Bearer <token>         │
│          │ ─────────────────────────────────>        │
│          │                                      ┌──────────────┐
│          │                                      │   JWT Verify  │
│          │                                      │   Middleware  │
│          │                                      └──────────────┘
```

### 3.2 AI Matching Flow

```
┌──────────────┐     POST /api/v1/ai/recommend     ┌──────────────┐
│ Coordinator  │ ─────────────────────────────────> │  FastAPI     │
│  Dashboard   │      { task_id, top_n: 5 }       │  Backend     │
│              │                                    │              │
│              │ <──────────────────────────────── │              │
│              │     200 OK + Recommendations      │              │
│              │                                    │              │
└──────────────┘                                    └──────┬───────┘
                                                           │
                              ┌────────────────────────────┼────────────────────────────┐
                              │                            │                            │
                              ▼                            ▼                            ▼
                    ┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
                    │  Skill Matcher  │         │ Availability    │         │  Historical     │
                    │  (Rule-Based)   │         │ Checker         │         │  Performance    │
                    │                 │         │                 │         │  Scorer         │
                    │ Exact: 100%      │         │ Full overlap:   │         │ >90%: +15%     │
                    │ Fuzzy: 70%      │         │ No penalty      │         │ <50%: -20%     │
                    │ Expert: +10%     │         │ Partial: -50%   │         │                 │
                    └────────┬────────┘         └────────┬────────┘         └────────┬────────┘
                             │                           │                           │
                             └───────────────────────────┼───────────────────────────┘
                                                         │
                                                         ▼
                                              ┌─────────────────┐
                                              │  Score Aggregator│
                                              │  Weighted Total  │
                                              │  Confidence %     │
                                              └────────┬────────┘
                                                       │
                                                       ▼
                                              ┌─────────────────┐
                                              │  LLM Enhancement │
                                              │  (Optional)      │
                                              │  Fallback: Skip   │
                                              └─────────────────┘
```

### 3.3 Event Registration Flow

```
┌──────────┐     POST /api/v1/events/{id}/register    ┌──────────────┐
│ Volunteer│ ───────────────────────────────────────> │   FastAPI    │
│          │      Authorization: Bearer <token>       │   Backend    │
│          │                                          │              │
│          │ <──────────────────────────────────────  │              │
│          │      200 OK + Registration Confirmed    │              │
│          │                                          │              │
│          │                                          │  ┌──────────┐│
│          │                                          │  │  Check   ││
│          │                                          │  │ Capacity ││
│          │                                          │  └────┬─────┘│
│          │                                          │       │      │
│          │                                          │  ┌────┴─────┐│
│          │                                          │  │  Add to  ││
│          │                                          │  │ Waitlist ││
│          │                                          │  │ if full  ││
│          │                                          │  └──────────┘│
│          │                                          │              │
│          │                                          │  ┌──────────┐│
│          │                                          │  │  Queue   ││
│          │                                          │  │ Notification│
│          │                                          │  │ (Email +  ││
│          │                                          │  │  In-App)  ││
│          │                                          │  └──────────┘│
└──────────┘                                          └──────────────┘
```

---

## 4. Security Architecture

### 4.1 Defense in Depth

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        SECURITY LAYERS                                   │
├─────────────────────────────────────────────────────────────────────────┤
│  LAYER 1: NETWORK                                                        │
│  ├── HTTPS only (TLS 1.3)                                               │
│  ├── Firewall rules (ports 80, 443 only)                                  │
│  └── DDoS protection (Cloudflare/Railway native)                         │
│                                                                          │
│  LAYER 2: APPLICATION                                                    │
│  ├── Rate limiting (100 req/min per IP)                                  │
│  ├── CORS whitelist (frontend origin only)                                │
│  ├── Input validation (Pydantic schemas)                                  │
│  ├── SQL injection prevention (SQLAlchemy ORM, parameterized queries)     │
│  └── XSS prevention (output encoding, CSP headers)                        │
│                                                                          │
│  LAYER 3: AUTHENTICATION                                                 │
│  ├── Password hashing (bcrypt, 12 rounds)                                 │
│  ├── JWT with short expiry (15 min access, 7 day refresh)                │
│  ├── Token blacklisting (Redis)                                           │
│  └── Account lockout (5 failed attempts)                                │
│                                                                          │
│  LAYER 4: AUTHORIZATION                                                  │
│  ├── Role-based access control (RBAC)                                    │
│  ├── Resource ownership checks                                           │
│  └── API endpoint guards                                                  │
│                                                                          │
│  LAYER 5: DATA                                                           │
│  ├── Encryption at rest (PostgreSQL TDE)                                  │
│  ├── Sensitive data masking in logs                                       │
│  └── Zero-PII exposure in API responses                                  │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.2 JWT Token Structure

```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user_uuid",
    "role": "volunteer",
    "iat": 1720963200,
    "exp": 1720964100,
    "jti": "unique_token_id"
  }
}
```

---

## 5. Deployment Architecture

### 5.1 Docker Compose (Development)

```yaml
# docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: volunteer_portal
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://postgres:${DB_PASSWORD}@db:5432/volunteer_portal
      JWT_SECRET: ${JWT_SECRET}
      SMTP_HOST: ${SMTP_HOST}
      SMTP_USER: ${SMTP_USER}
      SMTP_PASS: ${SMTP_PASS}
    ports:
      - "8000:8000"
    depends_on:
      - db
    volumes:
      - ./backend:/app

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

volumes:
  postgres_data:
```

### 5.2 Production Deployment (Render/Railway)

```
┌─────────────────────────────────────────────────────────────────┐
│                     PRODUCTION ENVIRONMENT                       │
│                                                                  │
│  ┌─────────────────┐      ┌─────────────────┐                 │
│  │   Render/Railway │      │   Render/Railway │                 │
│  │   (Frontend)     │      │   (Backend)      │                 │
│  │                  │      │                  │                 │
│  │  Static Site     │<────>│  Web Service     │                 │
│  │  (React Build)   │ HTTPS│  (Docker)        │                 │
│  └─────────────────┘      └────────┬────────┘                 │
│                                     │                            │
│                                     │ PostgreSQL                 │
│                                     │ Connection                 │
│                                     ▼                            │
│                            ┌─────────────────┐                  │
│                            │  Render/Railway  │                  │
│                            │  (PostgreSQL)    │                  │
│                            │  Managed DB      │                  │
│                            └─────────────────┘                  │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  ENVIRONMENT VARIABLES                                   │    │
│  │  ├── DATABASE_URL (provided by platform)                 │    │
│  │  ├── JWT_SECRET (256-bit random)                         │    │
│  │  ├── SMTP_HOST, SMTP_USER, SMTP_PASS                     │    │
│  │  ├── FRONTEND_URL (CORS origin)                          │    │
│  │  └── ENV=production                                      │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### 5.3 CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r backend/requirements.txt
      - name: Run tests
        run: pytest backend/tests/ --cov=app --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Render
        run: |
          curl -X POST ${{ secrets.RENDER_DEPLOY_HOOK }}
```

---

## 6. Scalability Considerations

### 6.1 Current (MVP) Scale
- Single container deployment
- Single PostgreSQL instance
- In-memory rate limiting (sufficient for <1000 users)

### 6.2 Future Scale (10,000+ users)
- **Backend:** Horizontal scaling with multiple Uvicorn workers + load balancer
- **Database:** Read replicas for GET requests, connection pooling (PgBouncer)
- **Caching:** Redis for session storage, query result caching, rate limiting
- **AI Service:** Extract to separate microservice with its own scaling
- **Static Assets:** CDN for frontend build and uploaded images
- **Monitoring:** Prometheus + Grafana for metrics, Sentry for error tracking

---

## 7. Technology Rationale

| Technology | Alternative | Reason for Choice |
|------------|-------------|-------------------|
| **FastAPI** | Django, Flask | Async support, auto-generated OpenAPI docs, Pydantic validation, proven in CareerForge & Vitalis |
| **PostgreSQL** | MySQL, MongoDB | ACID compliance, JSONB support, full-text search, proven in Vitalis |
| **SQLAlchemy** | Peewee, Tortoise | Mature ORM, Alembic migrations, team familiarity |
| **React** | Vue, Angular | Component ecosystem, job market demand, flexible state management |
| **Docker** | VMs, Bare Metal | Consistent environments, easy deployment, proven in Vitalis |
| **bcrypt** | Argon2, scrypt | Battle-tested, Python native support, sufficient for this threat model |
| **JWT** | Session Cookies | Stateless, scalable, works with mobile and SPAs |

---

*End of Architecture Document*
