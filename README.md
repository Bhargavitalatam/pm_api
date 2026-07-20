# Project Management API

A containerized RESTful API for project and task management built with FastAPI, PostgreSQL, Docker, and JWT authentication.

## Features

- User registration and JWT-based authentication
- CRUD operations for Projects and Tasks
- Repository pattern for data access abstraction
- Input validation with Pydantic schemas
- Cascade deletion of tasks when projects are deleted
- Ownership verification on all resources
- Docker Compose orchestration with PostgreSQL healthchecks

## Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL 15
- **ORM:** SQLAlchemy 2.0
- **Auth:** JWT (HS256) + bcrypt password hashing
- **Containerization:** Docker + Docker Compose

## Getting Started

### Prerequisites
- Docker and Docker Compose installed

### Run with Docker
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

### Run Tests
```bash
pip install -r requirements.txt pytest
pytest tests/ -v
```

## Seed Credentials

A test user is automatically created on startup:
- **Email:** test@example.com
- **Password:** testpassword123

## API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/register` | Register a new user | No |
| POST | `/api/auth/login` | Login and get JWT token | No |
| GET | `/api/users/me` | Get current user profile | Yes |
| POST | `/api/projects` | Create a new project | Yes |
| GET | `/api/projects` | List user's projects | Yes |
| GET | `/api/projects/{id}` | Get a specific project | Yes |
| PUT | `/api/projects/{id}` | Update a project | Yes |
| DELETE | `/api/projects/{id}` | Delete a project | Yes |
| POST | `/api/projects/{id}/tasks` | Create a task in project | Yes |
| GET | `/api/projects/{id}/tasks` | List tasks in project | Yes |
| GET | `/api/tasks/{id}` | Get a specific task | Yes |
| PUT | `/api/tasks/{id}` | Update a task | Yes |
| DELETE | `/api/tasks/{id}` | Delete a task | Yes |

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://pm_user:pm_password@db:5432/pm_database` |
| `SECRET_KEY` | JWT signing secret | `super-secret-key-for-jwt-signing-2026` |
| `JWT_ALGORITHM` | JWT algorithm | `HS256` |
| `JWT_EXPIRATION_MINUTES` | Token expiration in minutes | `60` |

## Deployment

For deployment options on other hosting providers, see [DEPLOY.md](file:///d:/pm_api/DEPLOY.md).

### Deploy to Koyeb
[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?type=git&repository=github.com/Bhargavitalatam/pm_api&branch=main&name=pm-api&ports=8000;http;/)

