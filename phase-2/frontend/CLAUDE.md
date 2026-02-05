# Advanced Todo Application - Frontend

## Overview

This is the frontend component of the Advanced Todo Application, built with Next.js 16+ and React. It provides a modern, responsive user interface with authentication, task management features, and advanced UI capabilities.

## Technology Stack

- **Framework**: Next.js 16+ with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Animations**: Framer Motion
- **Drag-and-drop**: @dnd-kit
- **Date Handling**: date-fns

## Key Features

### Authentication
- User registration and login forms
- JWT token management in cookies
- Protected routes and user session handling
- User profile management

### Task Management UI
- Task listing with search, filter, and sort capabilities
- Add/edit task forms with advanced fields
- Priority badges and tag chips
- Due date calendar picker
- Recurring task configuration

### UI Components
- Responsive layout with mobile-first design
- Dark/light mode toggle
- Loading spinners and skeleton screens
- Toast notifications for user feedback
- Animations for task interactions
- Drag-and-drop task reordering

### API Integration
- JWT token inclusion in API requests
- Comprehensive error handling
- Automatic token refresh
- User ID extraction from tokens

## Project Structure

```
frontend/
├── src/
│   ├── app/                 # Next.js App Router pages
│   │   ├── auth/
│   │   │   ├── signin/     # Sign in page
│   │   │   └── signup/     # Sign up page
│   │   ├── dashboard/      # Dashboard page
│   │   ├── tasks/          # Task management pages
│   │   ├── layout.tsx      # Root layout
│   │   └── page.tsx        # Home page
│   ├── components/         # Reusable UI components
│   │   ├── ui/            # Base UI components
│   │   ├── TaskList.tsx   # Task list container
│   │   ├── TaskItem.tsx   # Individual task display
│   │   └── TaskForm.tsx   # Task creation/editing form
│   ├── lib/               # Utility functions
│   │   ├── auth.tsx       # Authentication utilities
│   │   └── api.ts         # API client with JWT handling
│   └── styles/            # Global styles
├── public/                # Static assets
├── package.json           # Dependencies and scripts
├── next.config.mjs        # Next.js configuration
├── tailwind.config.ts     # Tailwind CSS configuration
└── tsconfig.json          # TypeScript configuration
```

## Environment Variables

The frontend requires the following environment variables:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
```

## Running the Application

### Installation
```bash
npm install
```

### Development
```bash
npm run dev
```

### Production Build
```bash
npm run build
npm start
```

## Key Files

- `src/lib/auth.tsx` - Authentication context and utilities
- `src/lib/api.ts` - API client with JWT token management
- `src/app/layout.tsx` - Root layout with providers
- `src/components/TaskList.tsx` - Main task management component
- `src/components/ui/` - Base UI components (buttons, inputs, etc.)