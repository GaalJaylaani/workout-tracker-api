Workout Tracker API

A FastAPI backend that lets users register, log in, and manage their own workouts.  
Built to practice backend fundamentals like JWT authentication, SQLAlchemy models, and RESTful CRUD routes.

Features
JWT authentication (register, login, and access protected routes)
Exercises CRUD (create, read, update, delete)
User accounts (each user manages their own workouts)
SQLite for local development
PostgreSQL for production deployment
Pytest test suite for backend routes
Docker Compose setup for running Postgres locally (optional)

Run Locally (using SQLite)

1. **Create and activate a virtual environment**
```bash
python -m venv .venv
# Windows
.\.venv\Scripts\Activate.ps1
# Mac/Linux
source .venv/bin/activate
