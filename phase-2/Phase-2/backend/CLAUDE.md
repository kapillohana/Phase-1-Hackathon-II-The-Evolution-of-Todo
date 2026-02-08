# Advanced Todo Application - Backend

## Overview

This is the backend component of the Advanced Todo Application, built with FastAPI and SQLModel. It provides a secure REST API with authentication, user management, and task management capabilities.

## Technology Stack

- **Framework**: FastAPI
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Database**: PostgreSQL (compatible with Neon)
- **Authentication**: JWT with PyJWT
- **Password Hashing**: bcrypt with Passlib
- **Validation**: Pydantic

## Key Features

### Authentication & Security
- JWT-based authentication with 7-day expiry
- Secure password hashing with bcrypt
- User registration and login endpoints
- Token verification and user session management
- User ID validation and isolation

### API Endpoints
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user profile
- `GET /{user_id}/tasks` - Get all tasks for user with filters
- `POST /{user_id}/tasks` - Create new task
- `GET /{user_id}/tasks/{task_id}` - Get specific task
- `PUT /{user_id}/tasks/{task_id}` - Update task
- `DELETE /{user_id}/tasks/{task_id}` - Delete task
- `PATCH /{user_id}/tasks/{task_id}/complete` - Toggle task completion

### Task Management
- Full CRUD operations for tasks
- Advanced filtering (by status, priority, date)
- Search functionality
- Sorting capabilities
- Pagination support
- Priority levels (high/medium/low)
- Tagging system
- Due dates and recurring tasks

### Data Isolation
- User ID verification in all endpoints
- Path parameter vs JWT token validation
- Database queries filtered by user_id
- Prevents unauthorized access to other users' data

## Project Structure

```
backend/
├── src/
│   ├── api/              # API route definitions
│   │   ├── main.py       # Main API routes
│   │   └── auth.py       # Authentication routes
│   ├── auth/             # Authentication logic
│   │   └── auth.py       # JWT handling and verification
│   ├── crud/             # Data access layer
│   │   └── crud.py       # Create, read, update, delete operations
│   ├── database/         # Database connection and session
│   │   └── database.py   # Engine and session management
│   ├── models/           # Data models
│   │   └── models.py     # User and Task models
│   └── schemas/          # Pydantic schemas
│       └── user_schemas.py  # User-related schemas
├── requirements.txt      # Python dependencies
├── alembic/              # Database migration files
├── pyproject.toml        # Project metadata
└── .env                  # Environment variables
```

## Environment Variables

The backend requires the following environment variables:

```env
DATABASE_URL=postgresql://username:password@localhost/dbname
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
PORT=8000
```

## Running the Application

### Installation
```bash
pip install -r requirements.txt
```

### Development
```bash
uvicorn src.main:app --reload --port 8000
```

### With Environment Configuration
```bash
DATABASE_URL=postgresql://... BETTER_AUTH_SECRET=... uvicorn src.main:app --reload --port 8000
```

## Key Files

- `src/auth/auth.py` - JWT token creation, verification, and user authentication
- `src/database/database.py` - Database connection and session management
- `src/models/models.py` - SQLModel definitions for User and Task
- `src/crud/crud.py` - Data access operations
- `src/api/main.py` - Main API endpoints with user isolation
- `src/api/auth.py` - Authentication endpoints