# Quick Setup Guide

For the full step-by-step setup instructions, see [README.md](README.md#-quick-start-for-new-users).

## TL;DR - Quick Commands

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy environment file
cp .env.example .env
# Then edit .env with your database credentials

# 4. Create database
createdb team4_assessment_db

# 5. Initialize database tables
python init_db.py

# 6. Start the server
uvicorn app.main:app --reload --port 8000
# Or use: ./start_server.sh
```

## Automated Setup

For macOS/Linux users with PostgreSQL installed:

```bash
chmod +x setup.sh
./setup.sh
```

This will:
- Create virtual environment
- Install dependencies
- Create database
- Initialize tables
- Provide next steps

## Need Help?

See the [Troubleshooting](README.md#-troubleshooting) section in README.md.
