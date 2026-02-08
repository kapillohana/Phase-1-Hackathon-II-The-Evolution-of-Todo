# API Contract: Advanced Full-Stack Todo Web Application

**Feature**: 001-todo-full-stack
**Date**: 2026-01-11
**Status**: Complete

## Overview

This document defines the API contract for the Advanced Full-Stack Todo Web Application. The API follows REST principles with JWT authentication and user isolation through path parameters.

## Base URL

`https://api.todo-app.com` (Production)
`http://localhost:8000` (Development)

## Authentication

All endpoints require JWT authentication in the Authorization header:
```
Authorization: Bearer {jwt-token}
```

## Common Response Format

### Success Response
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation successful"
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error message",
  "code": "ERROR_CODE"
}
```

## Endpoints

### 1. Create Task
**POST** `/api/{user_id}/tasks`

**Description**: Create a new task for the specified user

**Parameters**:
- `user_id` (path): User ID (must match authenticated user)

**Request Body**:
```json
{
  "title": "Task title (required, max 255 chars)",
  "description": "Task description (optional, max 1000 chars)",
  "priority": "Task priority (optional, default: 'medium', values: 'high'|'medium'|'low')",
  "tags": ["tag1", "tag2"] (optional, max 10 tags, max 50 chars each),
  "due_date": "2026-12-31T23:59:59Z" (optional, ISO 8601 format),
  "recurring": "Task recurrence (optional, default: 'none', values: 'none'|'daily'|'weekly'|'monthly')"
}
```

**Response**:
- 201 Created: Task created successfully
```json
{
  "success": true,
  "data": {
    "id": 123,
    "user_id": 456,
    "title": "Task title",
    "description": "Task description",
    "completed": false,
    "priority": "medium",
    "tags": ["tag1", "tag2"],
    "due_date": "2026-12-31T23:59:59Z",
    "recurring": "none",
    "created_at": "2026-01-11T10:00:00Z",
    "updated_at": "2026-01-11T10:00:00Z"
  },
  "message": "Task created successfully"
}
```
- 400 Bad Request: Invalid input
- 401 Unauthorized: Invalid or missing token
- 403 Forbidden: User ID mismatch
- 404 Not Found: User not found

### 2. List Tasks
**GET** `/api/{user_id}/tasks`

**Description**: Get all tasks for the specified user with optional filtering, searching, and sorting

**Parameters**:
- `user_id` (path): User ID (must match authenticated user)
- `search` (query): Search keyword in title/description
- `filter_status` (query): Filter by completion status ('completed', 'pending', 'all')
- `filter_priority` (query): Filter by priority ('high', 'medium', 'low')
- `filter_tag` (query): Filter by tag
- `sort_by` (query): Sort field ('due_date', 'priority', 'created_at', 'title')
- `sort_order` (query): Sort order ('asc', 'desc')
- `page` (query): Page number (default: 1)
- `page_size` (query): Items per page (default: 20, max: 100)

**Response**:
- 200 OK: Tasks retrieved successfully
```json
{
  "success": true,
  "data": {
    "tasks": [
      {
        "id": 123,
        "user_id": 456,
        "title": "Task title",
        "description": "Task description",
        "completed": false,
        "priority": "medium",
        "tags": ["tag1", "tag2"],
        "due_date": "2026-12-31T23:59:59Z",
        "recurring": "none",
        "created_at": "2026-01-11T10:00:00Z",
        "updated_at": "2026-01-11T10:00:00Z",
        "completed_at": null
      }
    ],
    "pagination": {
      "page": 1,
      "page_size": 20,
      "total": 150,
      "total_pages": 8,
      "has_next": true,
      "has_prev": false
    }
  },
  "message": "Tasks retrieved successfully"
}
```
- 401 Unauthorized: Invalid or missing token
- 403 Forbidden: User ID mismatch

### 3. Get Task
**GET** `/api/{user_id}/tasks/{id}`

**Description**: Get a specific task by ID

**Parameters**:
- `user_id` (path): User ID (must match authenticated user)
- `id` (path): Task ID

**Response**:
- 200 OK: Task retrieved successfully
```json
{
  "success": true,
  "data": {
    "id": 123,
    "user_id": 456,
    "title": "Task title",
    "description": "Task description",
    "completed": false,
    "priority": "medium",
    "tags": ["tag1", "tag2"],
    "due_date": "2026-12-31T23:59:59Z",
    "recurring": "none",
    "created_at": "2026-01-11T10:00:00Z",
    "updated_at": "2026-01-11T10:00:00Z",
    "completed_at": null
  },
  "message": "Task retrieved successfully"
}
```
- 401 Unauthorized: Invalid or missing token
- 403 Forbidden: User ID mismatch or task doesn't belong to user
- 404 Not Found: Task not found

### 4. Update Task
**PUT** `/api/{user_id}/tasks/{id}`

**Description**: Update a specific task with partial or full updates

**Parameters**:
- `user_id` (path): User ID (must match authenticated user)
- `id` (path): Task ID

**Request Body** (all fields optional):
```json
{
  "title": "Updated task title",
  "description": "Updated task description",
  "priority": "high",
  "tags": ["new_tag1", "new_tag2"],
  "due_date": "2026-12-31T23:59:59Z",
  "recurring": "weekly"
}
```

**Response**:
- 200 OK: Task updated successfully
```json
{
  "success": true,
  "data": {
    "id": 123,
    "user_id": 456,
    "title": "Updated task title",
    "description": "Updated task description",
    "completed": false,
    "priority": "high",
    "tags": ["new_tag1", "new_tag2"],
    "due_date": "2026-12-31T23:59:59Z",
    "recurring": "weekly",
    "created_at": "2026-01-11T10:00:00Z",
    "updated_at": "2026-01-11T11:00:00Z",
    "completed_at": null
  },
  "message": "Task updated successfully"
}
```
- 400 Bad Request: Invalid input
- 401 Unauthorized: Invalid or missing token
- 403 Forbidden: User ID mismatch or task doesn't belong to user
- 404 Not Found: Task not found

### 5. Delete Task
**DELETE** `/api/{user_id}/tasks/{id}`

**Description**: Delete a specific task

**Parameters**:
- `user_id` (path): User ID (must match authenticated user)
- `id` (path): Task ID

**Response**:
- 200 OK: Task deleted successfully
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```
- 401 Unauthorized: Invalid or missing token
- 403 Forbidden: User ID mismatch or task doesn't belong to user
- 404 Not Found: Task not found

### 6. Toggle Task Completion
**PATCH** `/api/{user_id}/tasks/{id}/complete`

**Description**: Toggle the completion status of a task

**Parameters**:
- `user_id` (path): User ID (must match authenticated user)
- `id` (path): Task ID

**Request Body**:
```json
{
  "completed": true  // Optional, if omitted, toggles current status
}
```

**Response**:
- 200 OK: Task completion status updated
```json
{
  "success": true,
  "data": {
    "id": 123,
    "completed": true,
    "completed_at": "2026-01-11T12:00:00Z"
  },
  "message": "Task completion status updated"
}
```
- 401 Unauthorized: Invalid or missing token
- 403 Forbidden: User ID mismatch or task doesn't belong to user
- 404 Not Found: Task not found

## Error Codes

| Code | Description |
|------|-------------|
| TASK_NOT_FOUND | The specified task does not exist |
| USER_MISMATCH | The user ID in the path does not match the authenticated user |
| INVALID_INPUT | The request body contains invalid data |
| UNAUTHORIZED | Missing or invalid authentication token |
| RATE_LIMITED | Too many requests from the same user |

## Security Considerations

1. All endpoints require JWT authentication
2. User ID in path must match authenticated user
3. Users can only access their own tasks
4. Input validation on all fields
5. Rate limiting on API endpoints
6. Proper error handling without information disclosure