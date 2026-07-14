# Technology Stack Document
## Amaanitvam Foundation — Volunteer Management Portal

---

## 1. Executive Summary

This document defines the complete technology stack for the Volunteer Management Portal, including backend, frontend, database, infrastructure, and development tools. Each technology is selected based on team expertise, project requirements, and production readiness.

---

## 2. Backend Stack

### 2.1 Core Framework: FastAPI

| Attribute | Detail |
|-----------|--------|
| **Version** | 0.111+ |
| **Language** | Python 3.11+ |
| **License** | MIT |

**Why FastAPI?**
- **Proven in production** — Used in CareerForge (22-agent system) and Vitalis (Technova 2026 winner)
- **Async/await support** — Handles concurrent requests efficiently
- **Auto-generated OpenAPI docs** — Interactive Swagger UI at `/docs`
- **Pydantic integration** — Automatic request validation and serialization
- **Type hints** — Better IDE support and fewer runtime errors
- **Performance** — One of the fastest Python frameworks (on par with Node.js/Go)

**Key Dependencies:**
```
fastapi==0.111.0
uvicorn[standard]==0.30.0       # ASGI server with HTTP/2 & WebSocket support
pydantic==2.7.0                  # Data validation & settings management
pydantic-settings==2.2.0          # Environment-based configuration
python-multipart==0.0.9          # Form data parsing (file uploads)
python-jose[cryptography]==3.3.0  # JWT token handling
passlib[bcrypt]==1.7.4           # Password hashing
```

### 2.2 Database: PostgreSQL 15

| Attribute | Detail |
|-----------|--------|
| **Version** | 15.x |
| **Driver** | asyncpg (async) + psycopg2 (sync migrations) |
| **ORM** | SQLAlchemy 2.0 |

**Why PostgreSQL?**
- **ACID compliance** — Data integrity for critical operations
- **JSONB support** — Flexible schema for skills, badges, settings
- **Full-text search** — Built-in search for volunteers and events
- **Row-level security** — Fine-grained access control
- **Proven in Vitalis** — Award-winning platform used PostgreSQL

**Key Dependencies:**
```
sqlalchemy==2.0.30
asyncpg==0.29.0                  # Async PostgreSQL driver
alembic==1.13.0                  # Database migrations
```

### 2.3 Authentication & Security

| Component | Technology | Purpose |
|-----------|------------|---------|
| Password Hashing | bcrypt (12 rounds) | Secure password storage |
| JWT Tokens | python-jose + HS256 | Stateless authentication |
| Input Validation | Pydantic schemas | Request sanitization |
| CORS | FastAPI middleware | Cross-origin request handling |
| Rate Limiting | slowapi | API abuse prevention |

```
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
slowapi==0.1.9
```

### 2.4 AI Matching Engine

| Component | Technology | Purpose |
|-----------|------------|---------|
| Core Algorithm | Python (rule-based) | Skill/availability matching |
| LLM Enhancement | Ollama (local) / OpenAI API (cloud) | Intelligent recommendations |
| Fuzzy Matching | rapidfuzz | Skill similarity scoring |
| Data Processing | pandas | Analytics and scoring |

```
ollama==0.2.0                    # Local LLM inference (zero cost)
openai==1.30.0                   # Cloud LLM fallback
rapidfuzz==3.9.0                 # Fast string matching
pandas==2.2.0                    # Data manipulation
```

### 2.5 Email & Notifications

| Component | Technology | Purpose |
|-----------|------------|---------|
| SMTP Client | aiosmtplib | Async email sending |
| Templates | Jinja2 | HTML email templates |
| Background Tasks | FastAPI BackgroundTasks | Non-blocking notifications |

```
aiosmtplib==3.0.0
jinja2==3.1.0
```

### 2.6 Testing

| Component | Technology | Purpose |
|-----------|------------|---------|
| Test Framework | pytest | Unit & integration tests |
| HTTP Client | httpx | Async test requests |
| Coverage | pytest-cov | Code coverage reporting |
| Fixtures | pytest-asyncio | Async test support |

```
pytest==8.2.0
pytest-asyncio==0.23.0
httpx==0.27.0
pytest-cov==5.0.0
```

---

## 3. Frontend Stack

### 3.1 Core Framework: React 18

| Attribute | Detail |
|-----------|--------|
| **Version** | 18.3+ |
| **Build Tool** | Vite 5.x |
| **Package Manager** | npm |

**Why React?**
- **Component reusability** — Modular UI development
- **Large ecosystem** — Extensive library support
- **Job market relevance** — Critical skill for full-stack roles
- **Performance** — Virtual DOM, concurrent features
- **Developer experience** — React DevTools, Hot Module Replacement

### 3.2 Styling: Tailwind CSS

| Attribute | Detail |
|-----------|--------|
| **Version** | 3.4+ |
| **Approach** | Utility-first CSS |

**Why Tailwind CSS?**
- **Rapid development** — No custom CSS files needed
- **Consistency** — Design system via configuration
- **Responsive** — Built-in breakpoints
- **Small bundle** — Purges unused styles in production
- **Dark mode ready** — `dark:` prefix support

### 3.3 State Management

| Component | Technology | Purpose |
|-----------|------------|---------|
| Global State | React Context API | Auth, notifications |
| Server State | TanStack Query (React Query) | API data caching |
| Form State | React Hook Form | Form handling & validation |
| Validation | Zod | Schema-based form validation |

```bash
npm install @tanstack/react-query
npm install react-hook-form zod @hookform/resolvers
```

### 3.4 Data Visualization

| Component | Technology | Purpose |
|-----------|------------|---------|
| Charts | Chart.js + react-chartjs-2 | Dashboard visualizations |
| Tables | TanStack Table | Sortable, filterable data tables |

```bash
npm install chart.js react-chartjs-2
npm install @tanstack/react-table
```

### 3.5 HTTP Client

| Component | Technology | Purpose |
|-----------|------------|---------|
| API Client | Axios | HTTP requests with interceptors |
| Type Safety | Shared types (TypeScript interfaces) | API contract enforcement |

```bash
npm install axios
```

### 3.6 Routing

| Component | Technology | Purpose |
|-----------|------------|---------|
| Router | React Router v6 | Client-side navigation |
| Lazy Loading | React.lazy + Suspense | Code splitting |

```bash
npm install react-router-dom
```

### 3.7 UI Components (Optional)

| Component | Technology | Purpose |
|-----------|------------|---------|
| Component Library | shadcn/ui or Headless UI | Accessible, customizable components |
| Icons | Lucide React | Consistent iconography |
| Toast Notifications | react-hot-toast | User feedback |

```bash
npm install lucide-react react-hot-toast
```

---

## 4. Infrastructure & DevOps

### 4.1 Containerization: Docker

| Component | Technology | Purpose |
|-----------|------------|---------|
| Container Engine | Docker 24.0+ | Application packaging |
| Compose | Docker Compose | Multi-service orchestration |
| Base Image | python:3.11-slim (backend), node:20-alpine (frontend) | Minimal attack surface |

**Why Docker?**
- **Consistency** — Same environment everywhere
- **Isolation** — Dependencies don't conflict
- **Portability** — Deploy anywhere Docker runs
- **Proven in Vitalis** — Docker was key to the Technova-winning architecture

### 4.2 Deployment Platform: Render / Railway

| Attribute | Detail |
|-----------|--------|
| **Type** | Platform-as-a-Service (PaaS) |
| **Backend** | Web Service (Docker) |
| **Frontend** | Static Site |
| **Database** | Managed PostgreSQL |
| **SSL** | Automatic (Let's Encrypt) |
| **Cost** | Free tier available |

**Why Render/Railway?**
- **Zero-config deployment** — Push to Git, auto-deploy
- **Free tier** — Suitable for demo/MVP
- **Managed database** — No DBA overhead
- **Custom domains** — Professional appearance
- **Health checks** — Automatic restart on failure

### 4.3 Version Control: Git + GitHub

| Component | Technology | Purpose |
|-----------|------------|---------|
| VCS | Git | Source code management |
| Hosting | GitHub | Repository hosting, CI/CD |
| Branching | GitHub Flow | Simple, effective workflow |
| CI/CD | GitHub Actions | Automated testing & deployment |

### 4.4 Monitoring (Future)

| Component | Technology | Purpose |
|-----------|------------|---------|
| Error Tracking | Sentry | Real-time error monitoring |
| Logs | Structured JSON + Logtail | Centralized logging |
| Metrics | Prometheus + Grafana | Performance dashboards |
| Uptime | UptimeRobot | External health checks |

---

## 5. Development Environment

### 5.1 IDE & Tools

| Tool | Purpose |
|------|---------|
| **VS Code** | Primary IDE with Python & React extensions |
| **Postman / Thunder Client** | API testing and documentation |
| **pgAdmin / DBeaver** | Database management |
| **Docker Desktop** | Local container management |

### 5.2 VS Code Extensions

```
Python (Microsoft)
Pylance (Microsoft)
ESLint (Microsoft)
Prettier (Prettier)
Tailwind CSS IntelliSense (Tailwind Labs)
Thunder Client (Ranga Vadhineni)
Docker (Microsoft)
GitLens (GitKraken)
```

### 5.3 Code Quality

| Tool | Purpose |
|------|---------|
| **Black** | Python code formatting |
| **isort** | Python import sorting |
| **flake8** | Python linting |
| **ESLint** | JavaScript/React linting |
| **Prettier** | Code formatting (JS/CSS) |
| **Husky** | Git hooks for pre-commit checks |

---

## 6. Complete Dependency Lists

### 6.1 Backend Requirements (requirements.txt)

```
# Core Framework
fastapi==0.111.0
uvicorn[standard]==0.30.0

# Database
sqlalchemy==2.0.30
asyncpg==0.29.0
alembic==1.13.0

# Authentication & Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.9
slowapi==0.1.9

# Configuration
pydantic==2.7.0
pydantic-settings==2.2.0
python-dotenv==1.0.0

# AI & Data
ollama==0.2.0
openai==1.30.0
rapidfuzz==3.9.0
pandas==2.2.0

# Email & Notifications
aiosmtplib==3.0.0
jinja2==3.1.0

# Utilities
httpx==0.27.0
python-dateutil==2.9.0

# Testing
pytest==8.2.0
pytest-asyncio==0.23.0
pytest-cov==5.0.0
```

### 6.2 Frontend Dependencies (package.json)

```json
{
  "dependencies": {
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "react-router-dom": "^6.23.0",
    "@tanstack/react-query": "^5.40.0",
    "react-hook-form": "^7.51.0",
    "zod": "^3.23.0",
    "@hookform/resolvers": "^3.4.0",
    "axios": "^1.7.0",
    "chart.js": "^4.4.0",
    "react-chartjs-2": "^5.2.0",
    "@tanstack/react-table": "^8.17.0",
    "lucide-react": "^0.378.0",
    "react-hot-toast": "^2.4.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.3.0"
  },
  "devDependencies": {
    "vite": "^5.2.0",
    "@vitejs/plugin-react": "^4.2.0",
    "tailwindcss": "^3.4.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0",
    "eslint": "^8.57.0",
    "eslint-plugin-react": "^7.34.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "prettier": "^3.2.0",
    "@types/react": "^18.3.0",
    "@types/react-dom": "^18.3.0"
  }
}
```

---

## 7. Technology Compatibility Matrix

| Technology | Version | Compatible With | Notes |
|------------|---------|-----------------|-------|
| Python | 3.11+ | FastAPI 0.111+, SQLAlchemy 2.0+ | Required for async/await |
| Node.js | 20.x | React 18+, Vite 5+ | LTS version |
| PostgreSQL | 15.x | asyncpg 0.29+, SQLAlchemy 2.0+ | JSONB features used |
| Docker | 24.0+ | All services | Multi-stage builds |
| React | 18.3+ | React Router 6+, TanStack Query 5+ | Concurrent features |

---

## 8. Stack Justification Summary

| Decision | Chosen | Rejected | Reason |
|----------|--------|----------|--------|
| Backend Framework | FastAPI | Django, Flask | Async, auto-docs, proven |
| Database | PostgreSQL | MySQL, MongoDB | ACID, JSONB, full-text search |
| Frontend | React | Vue, Angular | Ecosystem, job market |
| Styling | Tailwind | Bootstrap, Material-UI | Utility-first, small bundle |
| State Management | Context + TanStack Query | Redux, Zustand | Simpler, sufficient |
| Deployment | Render/Railway | AWS, GCP | Zero-config, free tier |
| Auth | JWT | Session Cookies | Stateless, SPA-friendly |
| Password Hash | bcrypt | Argon2 | Simpler, sufficient threat model |

---

*End of Technology Stack Document*
