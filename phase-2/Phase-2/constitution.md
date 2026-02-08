# Project Constitution: Advanced Todo Application - Phase 2

## Core Principles

### 1. Full-Stack Architecture
- Maintain clear separation between frontend and backend services
- Ensure frontend (Next.js) communicates with backend (FastAPI) via RESTful API
- Preserve user data isolation across multi-user environment

### 2. Security-First Design
- Implement robust authentication and authorization mechanisms
- Protect all user data with proper encryption and access controls
- Enforce user isolation to prevent cross-user data access

### 3. Persistent Data Management
- Utilize SQLModel ORM for database operations
- Support PostgreSQL for production deployments
- Maintain data integrity and consistency across all operations

### 4. Spec-Driven Development
- All code generation follows specification-driven principles
- No manual coding interventions allowed during development
- All features must be traceable to documented specifications

## Constraints

### Technical Constraints
- Backend: FastAPI framework with Python 3.11+
- Frontend: Next.js 16+ with App Router architecture
- Database: SQLModel ORM with PostgreSQL compatibility
- Authentication: JWT-based with configurable expiration
- Environment: Node.js 18+ for frontend, Python 3.11+ for backend

### Security Constraints
- All API endpoints must validate user identity
- Database queries must filter by authenticated user_id
- JWT tokens must be properly validated and refreshed
- Passwords must be hashed using bcrypt
- Cross-origin requests must be properly configured

### Architecture Constraints
- Frontend and backend must remain separate services
- All user-specific data must be isolated by user_id
- Authentication state must persist across sessions
- Error handling must be consistent across both services

## Security Guarantees

### User Data Isolation
- Each user can only access their own tasks and data
- Database queries are filtered by user_id from JWT token
- Path parameters are validated against JWT user_id for additional security

### Authentication Security
- JWT tokens are signed with secret key and have configurable expiration
- Login credentials are verified against hashed passwords
- Session management is handled through JWT lifecycle
- Token refresh mechanisms are implemented where appropriate

### Data Protection
- All sensitive data is encrypted in transit via HTTPS
- Database connections use secure protocols
- Environment variables protect sensitive configuration
- Input validation prevents injection attacks

## No-Manual-Coding Declaration

### Development Process
- All code was generated through Spec-Kit Plus automation
- No manual coding interventions occurred during implementation
- All features were implemented following specification-driven methodology
- Changes were made only through specification updates and regeneration

### Verification Protocol
- Commit history confirms spec-driven development process
- Code artifacts correlate directly to specification documents
- Implementation follows planned task sequences from documentation
- No direct code modifications occurred outside spec-driven workflow