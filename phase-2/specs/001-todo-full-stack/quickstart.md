# Quickstart Guide: Advanced Full-Stack Todo Web Application

**Feature**: 001-todo-full-stack
**Date**: 2026-01-11
**Status**: Complete

## Overview

This quickstart guide provides the essential information to set up and run the Advanced Full-Stack Todo Web Application. The application follows a monorepo structure with separate frontend and backend applications.

## Prerequisites

### System Requirements
- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend development)
- PostgreSQL-compatible database (Neon Serverless recommended)
- Git for version control

### Environment Setup
- Access to Neon Serverless PostgreSQL database
- Ability to set environment variables

## Initial Setup

### 1. Clone the Repository
```bash
git clone [repository-url]
cd [repository-name]
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend/

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database URL and auth secret
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend/

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with your API endpoints
```

## Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://username:password@host:port/database_name
BETTER_AUTH_SECRET=your-secure-jwt-secret-here
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
```

## Running the Applications

### 1. Start the Backend
```bash
cd backend/
source venv/bin/activate  # Activate virtual environment
uvicorn src.api.main:app --reload --port 8000
```

### 2. Start the Frontend
```bash
cd frontend/
npm run dev
```

### 3. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Key Endpoints

### Backend API
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks` - List tasks with search/filter/sort
- `GET /api/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion

### Frontend Pages
- `/` - Landing page (redirects to auth or tasks)
- `/auth/signin` - Login page
- `/auth/signup` - Registration page
- `/tasks` - Main task dashboard

## Running Tests

### Backend Tests
```bash
cd backend/
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend/
npm run test
```

## Database Migrations

### Setting up the database
```bash
cd backend/
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Key Features Available

1. **Authentication**: User registration and login with JWT
2. **Task Management**: Create, read, update, delete tasks
3. **Advanced Features**:
   - Task priorities (high/medium/low)
   - Task tags (work/home/custom)
   - Search and filtering
   - Sorting by due date, priority, or alphabetically
   - Recurring tasks (daily/weekly)
   - Due date assignments
   - Browser notifications for due tasks
4. **UI Features**:
   - Responsive design
   - Dark mode toggle
   - Animations for user interactions
   - Form validation
   - Toast notifications

## Development Commands

### Backend
```bash
# Run with auto-reload
uvicorn src.api.main:app --reload

# Run tests
pytest

# Format code
black src/

# Check types
mypy src/
```

### Frontend
```bash
# Development server
npm run dev

# Build for production
npm run build

# Run tests
npm run test

# Lint code
npm run lint
```

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Verify DATABASE_URL is correct in backend/.env
   - Ensure database service is running

2. **Frontend Cannot Connect to Backend**
   - Check NEXT_PUBLIC_API_BASE_URL in frontend/.env.local
   - Ensure backend is running on specified port

3. **Authentication Issues**
   - Verify BETTER_AUTH_SECRET is the same in both frontend and backend
   - Check that JWT configuration is consistent

4. **Missing Environment Variables**
   - Ensure all required environment variables are set
   - Restart applications after changing environment variables

## Next Steps

1. Customize the UI components in `frontend/src/components/`
2. Extend the API endpoints in `backend/src/api/main.py`
3. Add additional features as needed
4. Configure production deployment settings
5. Set up monitoring and logging as needed

## Additional Resources

- API documentation available at `/docs` endpoint
- Database schema defined in `backend/src/models/models.py`
- Component library in `frontend/src/components/`
- API client in `frontend/src/lib/api.ts`
- Authentication utilities in `frontend/src/lib/auth.ts`