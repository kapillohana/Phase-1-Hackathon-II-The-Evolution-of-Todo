# Advanced Todo Application - Phase 2

## Project Overview

This is a full-stack todo application built with Next.js 16+ frontend and FastAPI backend. The application implements advanced features including user authentication, task management with priorities/tags, search/filter/sort capabilities, and recurring tasks with due dates.

## Architecture

- **Frontend**: Next.js 16+ with App Router, Tailwind CSS, TypeScript
- **Backend**: FastAPI with SQLModel ORM
- **Database**: PostgreSQL (Neon)
- **Authentication**: JWT-based with Better Auth
- **Structure**: Monorepo with separate frontend and backend directories

## Running the Application

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL database

### Installation

#### Backend Setup
```bash
cd Phase-2/backend
pip install -r requirements.txt
```

#### Frontend Setup
```bash
cd Phase-2/frontend
npm install
```

### Environment Variables

Create `.env` files in both backend and frontend directories:

**Backend** (`backend/.env`):
```env
DATABASE_URL=postgresql://username:password@localhost/dbname
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here
```

**Frontend** (`frontend/.env.local`):
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
```

### Running the Application

#### Backend
```bash
cd Phase-2/backend
uvicorn src.main:app --reload --port 8000
```

#### Frontend
```bash
cd Phase-2/frontend
npm run dev
```

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user profile
- `POST /auth/logout` - User logout

### Task Management
- `GET /{user_id}/tasks` - Get all tasks for user with filters
- `POST /{user_id}/tasks` - Create new task
- `GET /{user_id}/tasks/{task_id}` - Get specific task
- `PUT /{user_id}/tasks/{task_id}` - Update task
- `DELETE /{user_id}/tasks/{task_id}` - Delete task
- `PATCH /{user_id}/tasks/{task_id}/complete` - Toggle task completion

## Features

### Basic Task Management
- Add, view, update, and delete tasks
- Mark tasks as complete/incomplete
- Per-user task isolation

### Advanced Features
- Priority levels (high/medium/low)
- Task tagging capability
- Search functionality
- Filtering by status, priority, and date
- Sorting options
- Due dates with calendar picker
- Recurring tasks (daily/weekly/monthly)
- Responsive UI with dark mode

### Security
- JWT-based authentication
- User isolation (users can only access their own tasks)
- Password hashing with bcrypt
- Input validation

## Project Structure

```
Phase-2/
├── backend/
│   ├── src/
│   │   ├── api/
│   │   ├── auth/
│   │   ├── crud/
│   │   ├── database/
│   │   └── models/
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   └── lib/
│   ├── package.json
│   └── .env.example
├── specs/
└── history/
```