# Specification: Advanced Todo Application - Phase 2

## Functional Requirements

### Authentication System
- User registration with email and password
- User login with credentials verification
- JWT token generation upon successful authentication
- Token validation for protected API endpoints
- User profile retrieval with authentication verification

### Task Management System
- Create new tasks associated with authenticated user
- Retrieve all tasks for authenticated user with filtering options
- Update specific task details with user ownership validation
- Delete specific tasks with user ownership validation
- Toggle task completion status with user ownership validation

### Advanced Features
- Task prioritization with high/medium/low levels
- Task tagging system for categorization
- Search functionality across user's tasks
- Filtering by status (completed/incomplete), priority, and date
- Sorting capabilities for task lists
- Due date assignment with calendar picker integration
- Recurring task configuration (daily/weekly/monthly)

### Multi-User Isolation
- Each user can only access their own tasks
- Database queries filter results by authenticated user_id
- API endpoints validate user identity before data access
- User ID validation occurs at both path parameter and JWT token levels

## API Behavior

### Authentication Endpoints
```
POST /auth/register
- Request: {email: string, password: string, name?: string}
- Response: {access_token: string, token_type: "bearer", user: UserObject}
- Validation: Email uniqueness, password strength requirements

POST /auth/login
- Request: {email: string, password: string}
- Response: {access_token: string, token_type: "bearer", user: UserObject}
- Validation: Credentials verification, account status

GET /auth/me
- Headers: Authorization: Bearer {token}
- Response: {id: string, email: string, name: string, created_at: timestamp}
- Validation: JWT token validity
```

### Task Management Endpoints
```
GET /{user_id}/tasks
- Path: user_id from URL
- Query: status?, priority?, tag?, search?, sort_by?, page?, limit?
- Headers: Authorization: Bearer {token}
- Response: {tasks: TaskArray, total: number, page: number, limit: number}
- Validation: user_id matches JWT token, query parameter sanitization

POST /{user_id}/tasks
- Path: user_id from URL
- Headers: Authorization: Bearer {token}
- Body: {title: string, description?: string, priority?: string, tags?: string[], due_date?: string, recurrence?: string}
- Response: {id: string, ...TaskFields}
- Validation: user_id matches JWT token, required fields, data types

GET /{user_id}/tasks/{task_id}
- Path: user_id, task_id from URL
- Headers: Authorization: Bearer {token}
- Response: {id: string, ...TaskFields}
- Validation: user_id matches JWT token, task belongs to user

PUT /{user_id}/tasks/{task_id}
- Path: user_id, task_id from URL
- Headers: Authorization: Bearer {token}
- Body: Partial<TaskFields>
- Response: {id: string, ...TaskFields}
- Validation: user_id matches JWT token, task belongs to user, data types

DELETE /{user_id}/tasks/{task_id}
- Path: user_id, task_id from URL
- Headers: Authorization: Bearer {token}
- Response: {success: boolean}
- Validation: user_id matches JWT token, task belongs to user

PATCH /{user_id}/tasks/{task_id}/complete
- Path: user_id, task_id from URL
- Headers: Authorization: Bearer {token}
- Body: {completed: boolean}
- Response: {id: string, completed: boolean}
- Validation: user_id matches JWT token, task belongs to user
```

## Authentication Rules

### Token Generation
- JWT tokens are generated with configurable expiration (default: 7 days)
- Tokens contain user_id, email, and expiration information
- Secret key is configured through environment variables
- Algorithm used: HS256 for symmetric signing

### Token Validation
- All protected endpoints require valid JWT token in Authorization header
- Token validity is checked against expiration time
- User existence is verified against database records
- Token signature is validated using configured secret

### Session Management
- Tokens are stored in browser cookies with HttpOnly and Secure flags
- Token refresh mechanisms handle expiration gracefully
- Logout functionality invalidates current session
- Concurrent session management handles multiple device access

## User Isolation Rules

### Database Level Isolation
- All task queries include WHERE clause filtering by user_id
- User ID is extracted from authenticated JWT token
- Foreign key relationships enforce user-task associations
- No direct access to tasks belonging to other users

### API Level Isolation
- Path parameters validate user_id against JWT token user_id
- Additional security layer prevents user impersonation
- Error responses do not reveal existence of resources owned by other users
- Access attempts to foreign resources return 404 instead of 403

### Application Logic Isolation
- Business logic enforces user ownership validation
- UI components only display data for authenticated user
- Form submissions validate user ownership before processing
- Administrative functions are restricted to authorized roles