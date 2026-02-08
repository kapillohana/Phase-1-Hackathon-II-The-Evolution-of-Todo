---
title: Advanced Todo Application Backend
emoji: ✅
colorFrom: blue
colorTo: green
sdk: docker
sdk_version: "3.10"
python_version: "3.10"
app_file: app.py
pinned: false
---

# Advanced Todo Application Backend

This is the backend for the Advanced Todo Application, built with FastAPI and deployed on Hugging Face Spaces.

## Features

- User authentication and authorization
- Task management with CRUD operations
- Priority levels and tagging system
- Due dates and recurring tasks
- RESTful API endpoints

## Endpoints

- `/` - Health check endpoint
- `/docs` - Interactive API documentation
- `/redoc` - Alternative API documentation
- `/api/{user_id}/tasks` - Task management endpoints
- `/auth` - Authentication endpoints

## Environment Variables

- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - Secret key for JWT tokens