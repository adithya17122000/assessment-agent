# Team 4 - Assessment & Quiz Agent Backend 🎯

A powerful FastAPI backend service for managing quizzes, tracking employee attempts, and delivering assessments for the GenAI Learning Program.

## 📋 Table of Contents
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Quick Start for New Users](#-quick-start-for-new-users)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Testing](#-testing)
- [Troubleshooting](#-troubleshooting)

## ✨ Features

- 📝 **Quiz Management**: Create, read, update, and delete quizzes
- 👥 **Employee Management**: Track employees and their assessment progress
- 📊 **Attempt Tracking**: Monitor quiz attempts, scores, and completion status
- 🔄 **Retry Logic**: Support for multiple quiz attempts with configurable limits
- 📄 **Pagination**: Efficient data handling with built-in pagination
- 🔍 **Search & Filter**: Advanced filtering options for quizzes and attempts
- 📚 **Interactive API Docs**: Auto-generated Swagger UI and ReDoc documentation
- ✅ **Validation**: Comprehensive request/response validation with Pydantic

## 🛠️ Tech Stack

- **Framework**: FastAPI (modern, fast Python web framework)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Validation**: Pydantic v2
- **Testing**: Pytest with async support
- **Code Quality**: Black, Ruff, MyPy

## 🚀 Quick Start for New Users

If you're cloning this repository for the first time, follow these steps to get the backend running on your machine.

### Prerequisites

Make sure you have these installed:
- **Python 3.11+** ([Download here](https://www.python.org/downloads/))
- **PostgreSQL 14+** ([Download here](https://www.postgresql.org/download/))
- **Git** (for cloning the repository)

### Step 1️⃣: Clone the Repository

```bash
# Clone the repository
git clone <your-repository-url>

# Navigate to the backend folder
cd backend
```

### Step 2️⃣: Set Up Python Virtual Environment

A virtual environment keeps your project dependencies isolated from other Python projects.

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

💡 **Tip**: When activated, you'll see `(venv)` appear in your terminal prompt.

### Step 3️⃣: Install Dependencies

```bash
# Upgrade pip (package manager)
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

This will install FastAPI, SQLAlchemy, PostgreSQL drivers, and other dependencies.

### Step 4️⃣: Set Up PostgreSQL Database

#### Option A: Local PostgreSQL (Recommended for Development)

```bash
# Create a new database
createdb team4_assessment_db

# Or using psql command line:
psql postgres
CREATE DATABASE team4_assessment_db;
\q
```

#### Option B: Use Supabase (Cloud Database)

1. Go to [supabase.com](https://supabase.com) and sign up
2. Create a new project
3. Go to **Project Settings** → **Database**
4. Copy your connection string

### Step 5️⃣: Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Open .env in your text editor and update the values
```

**Edit `.env` with your database credentials:**

```env
# Database Configuration (Local PostgreSQL)
DATABASE_URL=postgresql://your_username:your_password@localhost:5432/team4_assessment_db

# Or for Supabase:
# DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres

# Application Settings
API_V1_PREFIX=/api/v1
PROJECT_NAME=Team 4 Assessment & Quiz Agent
VERSION=1.0.0
DEBUG=true
HOST=0.0.0.0
PORT=8000

# CORS (Add your frontend URLs)
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]
```

💡 **Important**: Replace `your_username` and `your_password` with your actual PostgreSQL credentials.

### Step 6️⃣: Initialize the Database

This creates all the necessary tables in your database:

```bash
# Run the database initialization script
python init_db.py
```

✅ You should see: `Database tables created successfully!`

### Step 7️⃣: Start the Development Server

```bash
# Start the server with auto-reload
uvicorn app.main:app --reload --port 8000

# Or use the provided script:
chmod +x start_server.sh
./start_server.sh
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345]
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 8️⃣: Test Your Installation

Open your browser and visit:

1. **Health Check**: http://localhost:8000/health
   - Should return: `{"status": "healthy"}`

2. **API Documentation**: http://localhost:8000/docs
   - Interactive Swagger UI where you can test all endpoints

3. **Root Endpoint**: http://localhost:8000/
   - API information and version

**🎉 Success!** Your backend is now running!

## 📚 API Documentation

Once the server is running, you can access:

- **Swagger UI (Interactive)**: http://localhost:8000/docs
  - Try out API endpoints directly from your browser
  - See request/response schemas
  
- **ReDoc (Alternative)**: http://localhost:8000/redoc
  - Clean, organized API documentation

- **Health Check**: http://localhost:8000/health
  - Quick way to verify the server is running

## 🗂️ Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── employees.py      # Employee CRUD endpoints
│   │       └── quizzes.py        # Quiz & Attempt endpoints
│   ├── core/
│   │   ├── config.py             # App configuration & settings
│   │   └── dependencies.py       # Database session dependency
│   ├── db/
│   │   ├── base.py               # SQLAlchemy base class
│   │   └── database.py           # Database engine & session
│   ├── models/
│   │   ├── employee.py           # Employee SQLAlchemy model
│   │   ├── quiz.py               # Quiz SQLAlchemy model
│   │   └── attempt.py            # Attempt SQLAlchemy model
│   ├── schemas/
│   │   ├── employee.py           # Employee Pydantic schemas
│   │   ├── quiz.py               # Quiz Pydantic schemas
│   │   ├── attempt.py            # Attempt Pydantic schemas
│   │   └── pagination.py         # Pagination helpers
│   ├── tests/
│   │   ├── conftest.py           # Test fixtures
│   │   └── test_api.py           # API endpoint tests
│   └── main.py                   # FastAPI app initialization
├── .env                          # Environment variables (create this)
├── .env.example                  # Environment template
├── .gitignore                    # Git ignore rules
├── init_db.py                    # Database initialization script
├── requirements.txt              # Python dependencies
├── start_server.sh               # Quick start script
└── README.md                     # This file
```

## 🔌 API Endpoints

### Employee Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/employees/{employee_id}/quizzes` | Get all quizzes for an employee |
| GET | `/api/v1/employees/{employee_id}/quiz-attempts` | Get cross-quiz attempt history |

### Quiz Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/quizzes/{quiz_id}/attempts` | Get all attempts for a specific quiz |

## 🧪 Testing

Run tests with pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest app/tests/test_api.py -v
```

## 🔧 Configuration

Key environment variables in `.env`:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/team4_assessment_db

# API
API_V1_PREFIX=/api/v1
PROJECT_NAME=Team 4 Assessment & Quiz Agent
DEBUG=True

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]

# Pagination
DEFAULT_PAGE_SIZE=20
MAX_PAGE_SIZE=100
```

## 📝 API Contract Compliance

This implementation follows the Team 4 API Contract V1:
- ✅ All field names use `snake_case`
- ✅ All IDs are strings
- ✅ Status values are lowercase
- ✅ Routes use `/quizzes/` (not `/quizes/`)
- ✅ Timestamps are ISO 8601 UTC
- ✅ Pagination with `limit`, `offset`, `search` parameters
- ✅ Standard error responses
- ✅ Integration with Team 1's skill ontology

## 🔗 Integration with Other Teams

- **Team 1**: Consumes `skill_id` from shared skill ontology
- **Team 2**: References course IDs and module information
- **Team 3**: Leverages tutor interaction data for adaptive quizzes
- **Team 5**: Provides endpoints for dashboard analytics

## 🐛 Troubleshooting

### Database connection errors
```bash
# Check PostgreSQL is running
pg_isready

# Check database exists
psql -l | grep team4_assessment_db
```

### Port already in use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### Import errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## 📦 Deployment

### Production Checklist
- [ ] Set `DEBUG=False` in production
- [ ] Configure production database
- [ ] Set up proper authentication middleware
- [ ] Configure CORS origins
- [ ] Enable HTTPS
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy

## 🤝 Contributing

1. Follow the API contract specifications
2. Write tests for new features
3. Update documentation
4. Follow Python PEP 8 style guide
5. Run tests before committing

## 📄 License

Internal project for GenAI Learning Program

---

**Team 4 — Assessment & Quiz Agent**  
**Version**: 1.0  
**Last Updated**: 2026-07-06
