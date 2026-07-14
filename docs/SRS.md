# Software Requirements Specification (SRS)
## Amaanitvam Foundation — Volunteer Management Portal

---

## 1. Introduction

### 1.1 Purpose
This document provides a detailed specification for the Volunteer Management Portal, serving as the primary reference for developers, testers, and stakeholders throughout the development lifecycle.

### 1.2 Scope
The system encompasses a web-based platform with REST API backend, responsive frontend, PostgreSQL database, and an AI-powered matching microservice.

### 1.3 Definitions & Acronyms
| Acronym | Full Form |
|---------|-----------|
| API | Application Programming Interface |
| RBAC | Role-Based Access Control |
| ORM | Object-Relational Mapping |
| CORS | Cross-Origin Resource Sharing |
| SMTP | Simple Mail Transfer Protocol |

### 1.4 References
- PRD v1.0 (this project's Product Requirements Document)
- OWASP Top 10:2021
- WCAG 2.1 Guidelines
- FastAPI Official Documentation
- PostgreSQL 15 Documentation

---

## 2. Overall Description

### 2.1 Product Perspective
The Volunteer Management Portal is a standalone web application with no external system dependencies except for:
- Email SMTP server (for notifications)
- AI/LLM API (for matching recommendations)

### 2.2 User Classes and Characteristics

```
┌─────────────────────────────────────────────────────────────┐
│                      USER HIERARCHY                          │
├─────────────────────────────────────────────────────────────┤
│  ADMIN (Full Access)                                        │
│  ├── Manage all users (CRUD)                                │
│  ├── Manage all events and tasks                            │
│  ├── View analytics and generate reports                    │
│  ├── Configure system settings                              │
│  └── Access AI matching engine                              │
│                                                             │
│  COORDINATOR (Limited Admin)                                │
│  ├── Create and manage own events                           │
│  ├── Assign volunteers to tasks                             │
│  ├── Mark attendance                                        │
│  ├── Send announcements                                     │
│  └── View event-specific analytics                          │
│                                                             │
│  VOLUNTEER (Self-Service)                                   │
│  ├── View and edit own profile                              │
│  ├── Browse available events                                  │
│  ├── Register for events                                    │
│  ├── View assigned tasks and hours                          │
│  └── Receive notifications                                  │
└─────────────────────────────────────────────────────────────┘
```

### 2.3 Operating Environment
- **Server OS:** Linux (Ubuntu 22.04 LTS recommended)
- **Runtime:** Python 3.11+
- **Database:** PostgreSQL 15+
- **Web Server:** Uvicorn (ASGI)
- **Container:** Docker 24.0+
- **Client:** Modern browsers (Chrome, Firefox, Safari, Edge)

### 2.4 Design and Implementation Constraints
- Must use FastAPI for backend (team expertise)
- Must use PostgreSQL for data persistence
- Must containerize with Docker
- Must implement JWT authentication
- Must follow RESTful API conventions
- AI matching must work without external API costs (local fallback)

---

## 3. System Features

### 3.1 User Authentication Module

#### 3.1.1 Description
Secure user authentication with role-based access control.

#### 3.1.2 Functional Requirements

**SRS-AUTH-001: User Registration**
- Input: Full name, email, password, phone number, role (Volunteer default)
- Validation: Email uniqueness, password strength (min 8 chars, 1 uppercase, 1 number)
- Output: User account created, JWT token returned
- Error Handling: Duplicate email → 409 Conflict; Weak password → 400 Bad Request

**SRS-AUTH-002: User Login**
- Input: Email, password
- Process: Verify credentials, generate JWT with claims (user_id, role, exp)
- Output: Access token + Refresh token
- Error Handling: Invalid credentials → 401 Unauthorized; Account locked → 403 Forbidden

**SRS-AUTH-003: Token Refresh**
- Input: Valid refresh token
- Output: New access token
- Constraint: Refresh token expiry = 7 days

**SRS-AUTH-004: Password Reset**
- Input: Email address
- Process: Generate reset token (expires in 1 hour), send email
- Output: Success message (even if email doesn't exist — security)

**SRS-AUTH-005: Logout**
- Input: Current access token
- Process: Blacklist token (store in Redis/cache until expiry)
- Output: Success confirmation

---

### 3.2 Volunteer Profile Module

#### 3.2.1 Description
Comprehensive volunteer profile management with skills and availability.

#### 3.2.2 Functional Requirements

**SRS-PROF-001: Create Profile**
- Fields: Bio, location, skills (array), interests, availability schedule, emergency contact
- Skills: Predefined list + custom input with admin approval
- Availability: Day-of-week + time-range (e.g., "Monday 09:00-17:00")

**SRS-PROF-002: Update Profile**
- Volunteers can update own profile only
- Coordinators can update volunteer status
- Admins can update any field

**SRS-PROF-003: View Profile**
- Public: Name, skills, total hours, badges
- Private: Contact info, availability, emergency contact

**SRS-PROF-004: Skill Management**
- Predefined skills: Teaching, Medical, Logistics, IT Support, Counseling, etc.
- Skill proficiency levels: Beginner, Intermediate, Expert
- Skill verification by coordinator

---

### 3.3 Event Management Module

#### 3.3.1 Description
End-to-end event lifecycle management from planning to completion.

#### 3.3.2 Functional Requirements

**SRS-EVT-001: Create Event**
- Required: Title, description, start_date, end_date, location, max_volunteers
- Optional: Required skills, image, recurring pattern, coordinator assignment
- Validation: End date > Start date; Max volunteers > 0

**SRS-EVT-002: Update Event**
- Status transitions: Planning → Open → In Progress → Completed → Cancelled
- Only coordinator who created or admin can update
- Cannot cancel event with confirmed volunteers without notification

**SRS-EVT-003: Delete Event**
- Soft delete (mark as cancelled)
- Notify all registered volunteers

**SRS-EVT-004: List Events**
- Filters: Status, date range, location, required skills
- Sorting: Date (default), popularity, recently added
- Pagination: 20 items per page

**SRS-EVT-005: Event Detail**
- Full event info + registered volunteers + available slots + task breakdown

---

### 3.4 Task Management Module

#### 3.4.1 Description
Granular task tracking within events.

#### 3.4.2 Functional Requirements

**SRS-TSK-001: Create Task**
- Fields: Title, description, event_id, required_skills, estimated_hours, deadline
- Assignment: Optional at creation time

**SRS-TSK-002: Assign Volunteer**
- Manual: Coordinator selects from available volunteers
- AI-Assisted: System recommends top 3 matches with confidence scores
- Notification: Email + in-app to assigned volunteer

**SRS-TSK-003: Update Task Status**
- Status: Pending → In Progress → Completed → Blocked
- Volunteer can update own task status
- Coordinator can update any task in their events

**SRS-TSK-004: Task Completion**
- Volunteer marks complete with optional notes
- Coordinator verifies and logs actual hours
- Hours added to volunteer's total

---

### 3.5 AI Matching Engine Module

#### 3.5.1 Description
Intelligent volunteer-to-task recommendation system.

#### 3.5.2 Functional Requirements

**SRS-AI-001: Skill Matching Algorithm**
- Exact match: 100% score for matching skills
- Fuzzy match: 70% score for related skills (e.g., "Teaching" ≈ "Tutoring")
- Proficiency bonus: +10% for Expert, +5% for Intermediate

**SRS-AI-002: Availability Matching**
- Check volunteer's availability against task schedule
- Penalty: -50% score if partial overlap, -100% if no overlap

**SRS-AI-003: Historical Performance**
- Bonus: +15% for volunteers with >90% completion rate
- Penalty: -20% for volunteers with <50% completion rate

**SRS-AI-004: Recommendation API**
- Endpoint: `POST /api/ai/recommend`
- Input: task_id, top_n (default 5)
- Output: Array of {volunteer_id, name, match_score, match_reasons[]}
- Fallback: If AI service unavailable, use rule-based scoring only

---

### 3.6 Dashboard & Reporting Module

#### 3.6.1 Description
Analytics and visualization for data-driven decision making.

#### 3.6.2 Functional Requirements

**SRS-DASH-001: Admin Dashboard**
- KPI Cards: Total Volunteers, Active Events, Hours This Month, Pending Tasks
- Charts: Volunteer growth (line), Event distribution (pie), Hours by category (bar)
- Real-time updates via WebSocket or polling (5-minute interval)

**SRS-DASH-002: Coordinator Dashboard**
- My Events summary
- Volunteer roster for each event
- Pending task assignments
- Upcoming deadlines

**SRS-DASH-003: Volunteer Dashboard**
- My Upcoming Events
- My Tasks (with status)
- Hours Logged (total + this month)
- Badges/Achievements

**SRS-RPT-001: Generate Report**
- Types: Volunteer Activity, Event Summary, Impact Report
- Formats: PDF, CSV
- Filters: Date range, event, volunteer

---

### 3.7 Notification Module

#### 3.7.1 Description
Multi-channel notification system.

#### 3.7.2 Functional Requirements

**SRS-NOT-001: Notification Types**
| Type | Trigger | Channels |
|------|---------|----------|
| Event Reminder | 24h before event | Email + In-app |
| Task Assigned | Immediate | Email + In-app |
| Task Due Soon | 12h before deadline | In-app |
| Event Cancelled | Immediate | Email + In-app |
| Achievement Unlocked | Immediate | In-app |

**SRS-NOT-002: In-App Notifications**
- Stored in database
- Mark as read/unread
- Delete after 30 days

**SRS-NOT-003: Email Notifications**
- SMTP configuration in admin settings
- HTML templates with foundation branding
- Queue-based sending (Celery/background task)

---

## 4. External Interface Requirements

### 4.1 User Interfaces
- Responsive web application (mobile-first design)
- Dashboard with data visualization (Chart.js or similar)
- Form validation with inline error messages
- Loading states and skeleton screens
- Toast notifications for actions

### 4.2 Hardware Interfaces
- Standard web server hardware
- No specialized hardware required

### 4.3 Software Interfaces
| System | Protocol | Purpose |
|--------|----------|---------|
| PostgreSQL | TCP/IP | Primary data storage |
| SMTP Server | TCP/IP | Email notifications |
| LLM API (optional) | HTTPS | AI matching enhancement |
| Redis (optional) | TCP/IP | Token blacklisting, caching |

### 4.4 Communications Interfaces
- REST API over HTTPS
- JSON data format
- Standard HTTP status codes
- CORS enabled for frontend origin

---

## 5. Non-Functional Requirements (Detailed)

### 5.1 Performance Requirements
- API response time: < 200ms (95th percentile)
- Database query time: < 100ms (95th percentile)
- Concurrent users: 500+
- Throughput: 100 requests/second

### 5.2 Security Requirements
- Password hashing: bcrypt with salt rounds = 12
- JWT secret: 256-bit random key, rotated quarterly
- Rate limiting: 100 requests/minute per IP
- SQL injection: Parameterized queries (SQLAlchemy ORM)
- XSS prevention: Output encoding in frontend
- CSRF protection: Not needed (stateless JWT)

### 5.3 Availability Requirements
- Uptime: 99.5%
- Maintenance windows: Scheduled, < 2 hours/month
- Recovery Time Objective (RTO): 4 hours
- Recovery Point Objective (RPO): 24 hours (daily backups)

### 5.4 Maintainability Requirements
- Code coverage: > 80%
- API documentation: Auto-generated (OpenAPI/Swagger)
- Logging: Structured JSON logs with correlation IDs
- Monitoring: Health check endpoint, error tracking

---

## 6. Data Requirements

### 6.1 Data Models (High-Level)

```
USERS
├── id (PK, UUID)
├── email (UNIQUE)
├── password_hash
├── full_name
├── phone
├── role (ENUM: admin, coordinator, volunteer)
├── status (ENUM: pending, active, inactive, alumni)
├── created_at, updated_at

VOLUNTEER_PROFILES
├── user_id (FK)
├── bio
├── location
├── emergency_contact
├── total_hours
├── badges (JSON)

SKILLS
├── id (PK)
├── name (UNIQUE)
├── category

VOLUNTEER_SKILLS
├── volunteer_id (FK)
├── skill_id (FK)
├── proficiency (ENUM)
├── verified (BOOLEAN)

AVAILABILITY
├── id (PK)
├── volunteer_id (FK)
├── day_of_week (0-6)
├── start_time, end_time

EVENTS
├── id (PK, UUID)
├── title
├── description
├── location
├── start_date, end_date
├── max_volunteers
├── status (ENUM)
├── coordinator_id (FK)
├── created_at

EVENT_SKILLS
├── event_id (FK)
├── skill_id (FK)
├── min_proficiency

TASKS
├── id (PK, UUID)
├── event_id (FK)
├── title, description
├── required_skills (JSON)
├── estimated_hours
├── deadline
├── assigned_to (FK, nullable)
├── status (ENUM)
├── actual_hours (nullable)

NOTIFICATIONS
├── id (PK)
├── user_id (FK)
├── type (ENUM)
├── title, message
├── is_read (BOOLEAN)
├── created_at

ATTENDANCE
├── id (PK)
├── event_id (FK)
├── volunteer_id (FK)
├── check_in_time
├── check_out_time
├── hours_logged
├── status (ENUM: present, absent, partial)
```

### 6.2 Data Retention
- User data: Retain for 2 years after last activity
- Event data: Retain indefinitely (archived after 1 year)
- Notifications: Auto-delete after 30 days
- Logs: Retain for 90 days

---

## 7. Appendix

### A. API Endpoints Summary

```
AUTH
├── POST /api/auth/register
├── POST /api/auth/login
├── POST /api/auth/refresh
├── POST /api/auth/logout
├── POST /api/auth/forgot-password
├── POST /api/auth/reset-password

USERS
├── GET    /api/users/me
├── PUT    /api/users/me
├── GET    /api/users (admin only)
├── GET    /api/users/{id} (admin/coordinator)

VOLUNTEERS
├── GET    /api/volunteers
├── GET    /api/volunteers/{id}
├── PUT    /api/volunteers/{id}/skills
├── GET    /api/volunteers/{id}/availability
├── PUT    /api/volunteers/{id}/availability

EVENTS
├── GET    /api/events
├── POST   /api/events (coordinator+)
├── GET    /api/events/{id}
├── PUT    /api/events/{id} (coordinator+)
├── DELETE /api/events/{id} (coordinator+)
├── POST   /api/events/{id}/register
├── POST   /api/events/{id}/attendance

TASKS
├── GET    /api/events/{event_id}/tasks
├── POST   /api/events/{event_id}/tasks (coordinator+)
├── GET    /api/tasks/{id}
├── PUT    /api/tasks/{id}
├── POST   /api/tasks/{id}/assign
├── POST   /api/tasks/{id}/complete

AI
├── POST   /api/ai/recommend (coordinator+)

DASHBOARD
├── GET    /api/dashboard/admin (admin)
├── GET    /api/dashboard/coordinator (coordinator)
├── GET    /api/dashboard/volunteer (volunteer)

NOTIFICATIONS
├── GET    /api/notifications
├── PUT    /api/notifications/{id}/read
├── DELETE /api/notifications/{id}

REPORTS
├── GET    /api/reports/volunteers (admin)
├── GET    /api/reports/events (admin)
├── GET    /api/reports/export (admin)
```

### B. Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| AUTH001 | 401 | Invalid credentials |
| AUTH002 | 401 | Token expired |
| AUTH003 | 403 | Insufficient permissions |
| AUTH004 | 409 | Email already registered |
| VAL001 | 400 | Missing required field |
| VAL002 | 400 | Invalid date range |
| VAL003 | 400 | Invalid skill proficiency |
| RES001 | 404 | Resource not found |
| RES002 | 409 | Resource already exists |
| SRV001 | 500 | Internal server error |

---

*End of SRS*
