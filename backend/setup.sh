#!/bin/bash
# Quick setup script for Team 4 Backend

set -e  # Exit on error

echo "=================================="
echo "Team 4 Backend - Quick Setup"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python version
echo "🔍 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found!${NC}"
    echo "Install it with: brew install python3"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✅ Python ${PYTHON_VERSION} found${NC}"

# Check PostgreSQL
echo ""
echo "🔍 Checking PostgreSQL..."
if ! command -v psql &> /dev/null; then
    echo -e "${RED}❌ PostgreSQL not found!${NC}"
    echo "Install it with: brew install postgresql@14"
    exit 1
fi
echo -e "${GREEN}✅ PostgreSQL found${NC}"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${YELLOW}⚠️  Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo ""
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "⬆️  Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt --quiet
echo -e "${GREEN}✅ Dependencies installed${NC}"

# Create .env file
echo ""
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo -e "${GREEN}✅ .env file created${NC}"
    echo -e "${YELLOW}⚠️  Please update DATABASE_URL in .env with your PostgreSQL credentials${NC}"
else
    echo -e "${YELLOW}⚠️  .env file already exists${NC}"
fi

# Check if database exists
echo ""
echo "🗄️  Checking database..."
DB_NAME="team4_assessment_db"
if psql -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
    echo -e "${YELLOW}⚠️  Database '$DB_NAME' already exists${NC}"
else
    echo "Creating database '$DB_NAME'..."
    createdb $DB_NAME 2>/dev/null || {
        echo -e "${RED}❌ Failed to create database. Please create it manually:${NC}"
        echo "   createdb $DB_NAME"
        exit 1
    }
    echo -e "${GREEN}✅ Database created${NC}"
fi

# Initialize database
echo ""
echo "🔄 Initializing database tables..."
python3 init_db.py
echo -e "${GREEN}✅ Database initialized${NC}"

# Success message
echo ""
echo "=================================="
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Start the development server:"
echo "   uvicorn app.main:app --reload"
echo ""
echo "3. Visit the API documentation:"
echo "   http://localhost:8000/docs"
echo ""
echo "4. Run tests:"
echo "   pytest"
echo ""
echo -e "${YELLOW}Note: Update .env file with your PostgreSQL credentials if needed${NC}"
echo ""
