Hackathon Phase-2 — The Evolution of Todo (Full-Stack)
📌 Overview

This repository contains the Phase-2 implementation of the Evolution of Todo project, built as part of the Hackathon using a Spec-Driven Development methodology (Spec-Kit Plus).

Phase-2 extends Phase-1 by introducing:

Full-stack architecture

Authentication & authorization

Persistent database

Multi-user task isolation

Secure frontend–backend integration

All development follows the required workflow:

Constitution → Specification → Planning → Tasks → Implementation

pec-Driven Development (Spec-Kit Plus)

This project strictly follows Spec-Kit Plus conventions:

1️⃣ Constitution

Defines:

Development rules

No-manual-coding constraint

Security and quality standards

2️⃣ Specification

Defines:

Functional requirements

User stories

API behavior

Auth & isolation requirements

3️⃣ Planning

Defines:

Architecture decisions

Tech stack

Data models

Security strategy

4️⃣ Tasks

Defines:

Granular task breakdown

Ordered execution

Feature-to-code mapping

📁 All artifacts are available in specs/

🔐 Authentication & Security
Authentication

JWT-based authentication

Token issued on login

Token required for all protected routes

Authorization & Isolation

JWT user identity is authoritative

Path parameters validated against JWT user

Database queries filtered by user_id

Cross-user data access is prevented

🚨 Security is enforced at API + DB level

🧩 Backend (FastAPI)

Features

RESTful API

JWT auth

SQLModel ORM

PostgreSQL database

Alembic migrations

Core Endpoints

Auth (signup / signin)

Create task

Read user tasks

Update task

Delete task

📁 Located in backend/

🎨 Frontend (Next.js / React)

Features

Authentication flows (signin/signup)

Protected routes

Token-based API requests

User-specific task UI

Security

JWT attached to all protected API calls

Unauthorized access blocked at routing level

📁 Located in frontend/

🔁 Frontend ↔ Backend Integration

JWT stored securely on client

API client attaches token automatically

Backend verifies token on every request

Errors handled gracefully

🧾 History & Evidence

📁 history/ contains:

Prompt trails

Decision logs

Evidence of:

Spec → Plan → Tasks → Implementation

This provides full auditability for judges.

🧪 Testing

Backend unit tests included

API behavior validated

Auth and isolation logic verified

📁 backend/tests/

⚙️ How to Run (Local)
Backend
cd backend
pip install -r requirements.txt
uvicorn src.api.main:app --reload

Frontend
cd frontend
npm install
npm run dev
