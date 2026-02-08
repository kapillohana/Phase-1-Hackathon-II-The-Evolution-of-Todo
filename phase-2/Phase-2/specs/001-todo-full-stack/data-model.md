# Data Model: Advanced Full-Stack Todo Web Application

**Feature**: 001-todo-full-stack
**Date**: 2026-01-11
**Status**: Complete

## Overview

This document defines the data model for the Advanced Full-Stack Todo Web Application, including entities, relationships, and validation rules derived from the feature specification.

## Entity Definitions

### User
**Description**: Represents a registered user of the application

**Fields**:
- `id`: Integer (Auto-increment, Primary Key)
- `email`: String (Unique, Required, Max length: 255)
- `hashed_password`: String (Required, Max length: 255)
- `created_at`: DateTime (Auto-generated on creation)
- `updated_at`: DateTime (Auto-generated on update)

**Validation Rules**:
- Email must be valid email format
- Email must be unique across all users
- Hashed password must be present and not empty
- Email length must not exceed 255 characters

**Relationships**:
- One-to-Many with Task entity (one user can have many tasks)

### Task
**Description**: Represents a user's task with all advanced features

**Fields**:
- `id`: Integer (Auto-increment, Primary Key)
- `user_id`: Integer (Foreign Key to User.id, Required)
- `title`: String (Required, Max length: 255)
- `description`: String (Optional, Max length: 1000)
- `completed`: Boolean (Default: False)
- `priority`: String (Default: "medium", Values: "high", "medium", "low")
- `tags`: JSON/Array (Optional, Array of strings, Max: 10 tags)
- `due_date`: DateTime (Optional)
- `recurring`: String (Default: "none", Values: "none", "daily", "weekly", "monthly")
- `created_at`: DateTime (Auto-generated on creation)
- `updated_at`: DateTime (Auto-generated on update)
- `completed_at`: DateTime (Optional, populated when task is marked complete)

**Validation Rules**:
- Title must be present and not empty
- Title length must not exceed 255 characters
- Description length must not exceed 1000 characters
- Priority must be one of: "high", "medium", "low"
- Tags array must not contain more than 10 tags
- Each tag string must not exceed 50 characters
- Due date must be a valid future date if provided
- Recurring must be one of: "none", "daily", "weekly", "monthly"
- User_id must reference an existing user
- Completed status can only be updated by the task owner

**Relationships**:
- Many-to-One with User entity (many tasks belong to one user)

## Entity Relationships

```
User (1) <---> (Many) Task
User.id ←→ Task.user_id
```

**Relationship Constraints**:
- When a user is deleted, all their tasks should be deleted (CASCADE delete)
- All queries must filter tasks by user_id to maintain data isolation
- Only the task owner can modify or delete a task

## State Transitions

### Task States
- **Pending**: `completed = false`, `completed_at = null`
- **Completed**: `completed = true`, `completed_at = [timestamp]`

### Valid State Transitions
- **Pending → Completed**: When user marks task as complete
- **Completed → Pending**: When user unmarks task as complete
- **Auto-Recurring**: When completed task has `recurring != "none"`, a new instance is created with adjusted due_date

### State Transition Rules
- A task can only be completed by its owner
- When a recurring task is completed, a new instance is automatically created based on the recurrence pattern
- The new recurring task inherits title, description, priority, and tags from the original
- The new recurring task has a due_date calculated based on the recurrence pattern and original due_date

## Indexes

### Required Indexes
1. **User.email**: Unique index for efficient user lookup
2. **Task.user_id**: Index for filtering tasks by user (critical for user isolation)
3. **Task.completed**: Index for filtering completed vs pending tasks
4. **Task.priority**: Index for priority-based filtering
5. **Task.due_date**: Index for date-based filtering and sorting
6. **Task.created_at**: Index for chronological ordering

### Composite Indexes
1. **Task.user_id + completed**: For user-specific completed/pending queries
2. **Task.user_id + priority**: For user-specific priority filtering
3. **Task.user_id + due_date**: For user-specific date-based queries

## Business Rules

### Data Integrity
- Foreign key constraints ensure referential integrity between User and Task
- Not-null constraints on required fields
- Check constraints on enum-like fields (priority, recurring)

### Access Control
- All task operations must verify user ownership via user_id
- Users can only access their own tasks
- No cross-user data access is permitted

### Advanced Features
- Recurring tasks automatically generate new instances upon completion
- Due date validation ensures dates are reasonable (not more than 1 year in the future)
- Tag validation ensures proper format and quantity limits

## API Considerations

### Query Parameters Support
- **Search**: Title and description text search
- **Filter**: By completion status, priority, due date range, tags
- **Sort**: By due date, priority, creation date, alphabetical
- **Pagination**: Standard offset/limit parameters

### Validation at API Level
- All API endpoints must validate user_id matches authenticated user
- Input validation must match data model constraints
- Bulk operations must maintain transactional integrity

## Performance Considerations

### Query Optimization
- Use indexes appropriately for common query patterns
- Implement pagination for large result sets
- Consider caching for frequently accessed user data

### Storage Efficiency
- Use appropriate data types to minimize storage
- Compress tags array efficiently
- Archive completed tasks if needed for performance

This data model supports all feature requirements including basic CRUD operations, intermediate features (priorities, tags, search, filter, sort), and advanced features (recurring tasks, due dates) while maintaining security and performance requirements.