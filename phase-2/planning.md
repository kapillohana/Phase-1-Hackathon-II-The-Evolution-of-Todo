# Planning Document: Advanced Todo Application - Phase 2

## High-Level System Design

### Architecture Overview
The application follows a microservices architecture with clear separation between frontend and backend services. The frontend provides the user interface using Next.js with App Router, while the backend exposes RESTful API endpoints using FastAPI. Both services communicate over HTTP with JWT-based authentication for security.

### Component Responsibilities
- **Frontend**: User interface, authentication flow, task management UI, API communication
- **Backend**: Authentication logic, database operations, business logic, API endpoints
- **Database**: Data persistence, user management, task storage, relationship maintenance
- **Authentication Service**: JWT token generation, validation, session management

## Backend Responsibilities

### API Layer (src/api/)
- Define RESTful endpoints for authentication and task management
- Validate incoming requests and sanitize input data
- Extract and validate user identity from JWT tokens
- Handle error responses and status codes appropriately

### Authentication Layer (src/auth/)
- Implement JWT token creation and validation
- Verify user credentials against stored password hashes
- Manage token expiration and refresh mechanisms
- Secure password handling with bcrypt hashing

### Data Access Layer (src/crud/)
- Perform database operations for users and tasks
- Apply user_id filtering to all queries
- Handle database transactions and error management
- Optimize queries for performance and security

### Database Layer (src/database/)
- Establish database connections using SQLModel
- Configure connection pooling and security settings
- Handle database migrations and schema management
- Ensure connection security and resource cleanup

### Models Layer (src/models/)
- Define SQLModel data structures for users and tasks
- Establish relationships between entities
- Implement data validation and constraints
- Ensure data integrity and consistency

## Frontend Responsibilities

### Routing Layer (src/app/)
- Implement Next.js App Router pages for authentication
- Create protected routes for authenticated users
- Handle navigation and URL parameter management
- Manage route-based data loading and error handling

### Component Layer (src/components/)
- Build reusable UI components for task management
- Implement authentication forms and user interfaces
- Create responsive layouts with mobile-first design
- Develop drag-and-drop interfaces for task organization

### Library Layer (src/lib/)
- Implement API client with JWT token management
- Create authentication context and state management
- Develop utility functions for data transformation
- Handle error boundaries and global state

## Authentication Flow

### Registration Process
1. User submits registration form with email and password
2. Frontend validates input and sends request to backend
3. Backend creates user record with hashed password
4. Backend generates JWT token and returns to frontend
5. Frontend stores token and redirects to dashboard

### Login Process
1. User submits login form with credentials
2. Frontend validates input and sends request to backend
3. Backend verifies credentials against stored hash
4. Backend generates new JWT token and returns to frontend
5. Frontend stores token and redirects to dashboard

### Token Management
1. JWT tokens are stored securely in browser cookies
2. Interceptors automatically attach tokens to API requests
3. Token expiration is monitored and handled gracefully
4. Refresh mechanisms activate before token expiration

## Data Flow

### Task Creation Flow
1. User fills out task creation form in frontend
2. Frontend validates input and constructs API request
3. JWT token is attached to request headers
4. Backend extracts user_id from JWT token
5. Backend creates task record linked to authenticated user
6. Backend returns created task object to frontend
7. Frontend updates UI with new task

### Task Retrieval Flow
1. Frontend detects need to load user's tasks
2. Frontend extracts user_id from authentication context
3. Frontend makes API request with JWT token
4. Backend validates token and extracts user_id
5. Backend queries database filtering by user_id
6. Backend returns filtered task array to frontend
7. Frontend renders tasks in user interface

### Security Validation Flow
1. Each API request includes JWT token in headers
2. Backend middleware extracts and validates token
3. User_id is extracted from token claims
4. Path parameters are compared with JWT user_id
5. Database queries are filtered by validated user_id
6. Results are returned only for authenticated user