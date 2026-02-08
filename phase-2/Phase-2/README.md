# Phase 1 Hackathon - Todo CLI App with Speckit Integration

## Project Overview
This project is a Todo CLI application developed as part of the Hackathon Phase 1. It features integration with Speckit for enhanced functionality.

## Features
- Command-line interface for managing todo items
- Speckit integration for advanced features
- Console-based application for efficient task management

## Repository Structure
- `.claude/` - Claude Code configuration files
- `specs/` - Project specifications
- `todo-console-app/` - Main Todo CLI application source code
- `speckit.constitution` - Speckit configuration file
- `speckit.specify` - Speckit specification file

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL database (or use SQLite for development)

### Installation

#### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd Phase-2/backend
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   # Or using Poetry if preferred
   poetry install
   ```
3. Copy the example environment file and update with your settings:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and secrets
   ```
4. Run database migrations:
   ```bash
   python -m alembic upgrade head
   ```

#### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd Phase-2/frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Copy the example environment file:
   ```bash
   cp .env.local.example .env.local
   # Edit .env.local with your API settings
   ```

### Running the Application

#### Backend (in one terminal):
```bash
cd Phase-2/backend
uvicorn src.main:app --reload --port 8000
```

#### Frontend (in another terminal):
```bash
cd Phase-2/frontend
npm run dev
```

The application will be available at http://localhost:3000

## Technologies Used
- Python (for the CLI application)
- Speckit integration
- Various utility scripts and configurations

## Project Status
Complete Hackathon Phase 1 - Todo CLI App with Speckit integration

## Last Updated
Updated on January 4, 2026 - Testing commit functionality