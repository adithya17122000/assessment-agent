# 🚀 Pushing Your Backend to GitHub

This guide will help you push your Team 4 backend to GitHub.

## Prerequisites

- Git installed on your machine
- GitHub account created
- Repository created on GitHub (can be public or private)

## Step-by-Step Instructions

### Step 1️⃣: Initialize Git Repository (if not already done)

```bash
cd /Users/adithya.anjanappa/Desktop/APEX/APEX-29-06-26/backend

# Initialize git repository
git init

# Check if .gitignore exists
cat .gitignore
```

Your `.gitignore` should already include:
- `venv/` - virtual environment
- `.env` - environment variables with secrets
- `__pycache__/` - Python cache files
- `*.pyc` - compiled Python files

### Step 2️⃣: Create Repository on GitHub

1. Go to [github.com](https://github.com)
2. Click the **"+"** icon in the top right → **"New repository"**
3. Fill in:
   - **Repository name**: `team4-assessment-backend` (or your preferred name)
   - **Description**: "Assessment & Quiz Agent Backend - FastAPI + PostgreSQL"
   - **Visibility**: Choose Public or Private
   - **⚠️ Important**: Do NOT initialize with README, .gitignore, or license (we have them already)
4. Click **"Create repository"**

### Step 3️⃣: Add All Files to Git

```bash
# Check current status
git status

# Add all files (respects .gitignore)
git add .

# Commit with a message
git commit -m "Initial commit: Team 4 Assessment & Quiz Agent Backend"
```

### Step 4️⃣: Connect to GitHub Remote

Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual GitHub details:

```bash
# Add GitHub as remote origin
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Verify remote was added
git remote -v
```

### Step 5️⃣: Push to GitHub

```bash
# Push to main branch
git branch -M main
git push -u origin main
```

**If prompted for credentials:**
- **Username**: Your GitHub username
- **Password**: Use a [Personal Access Token](https://github.com/settings/tokens) (not your password)
  - Go to: Settings → Developer settings → Personal access tokens → Generate new token
  - Select scopes: `repo` (full control of private repositories)
  - Copy the token and use it as your password

### Step 6️⃣: Verify on GitHub

1. Go to your repository URL: `https://github.com/YOUR_USERNAME/YOUR_REPO_NAME`
2. You should see all your files!
3. The README.md will be displayed automatically

## 📝 Creating a Good README for GitHub

Your README.md already includes:
- ✅ Project description
- ✅ Features
- ✅ Tech stack
- ✅ Complete setup instructions for new users
- ✅ API documentation links
- ✅ Project structure
- ✅ Testing instructions
- ✅ Troubleshooting guide

### Optional Enhancements

You might want to add:

1. **Badges** at the top:
```markdown
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-blue.svg)
```

2. **Screenshots** of the API docs
3. **Live demo** link (if deployed)
4. **Team members** or contributors

## 🔄 Making Future Changes

After your initial push, when you make changes:

```bash
# Check what changed
git status

# Add changed files
git add .

# Or add specific files
git add app/api/v1/quizzes.py

# Commit with descriptive message
git commit -m "Add new endpoint for quiz statistics"

# Push to GitHub
git push
```

## 🌿 Working with Branches (Recommended)

For feature development:

```bash
# Create and switch to new branch
git checkout -b feature/add-analytics

# Make your changes...

# Commit changes
git add .
git commit -m "Add analytics endpoints"

# Push branch to GitHub
git push -u origin feature/add-analytics

# Create Pull Request on GitHub
# After review, merge to main branch
```

## 🔐 Security Reminder

**Never commit:**
- ❌ `.env` file (contains database passwords)
- ❌ `venv/` directory (can be recreated)
- ❌ API keys or secrets
- ❌ Database credentials

These are already in `.gitignore` ✅

## 📋 Example Repository Structure on GitHub

After pushing, your GitHub repository will look like:

```
team4-assessment-backend/
├── .gitignore
├── README.md                    ← Displays on GitHub homepage
├── SETUP_GUIDE.md
├── GITHUB_SETUP.md             ← This file
├── PROJECT_SUMMARY.md
├── requirements.txt
├── pyproject.toml
├── init_db.py
├── setup.sh
├── start_server.sh
├── .env.example                ← Safe to share
└── app/                        ← All your code
    ├── main.py
    ├── api/
    ├── core/
    ├── db/
    ├── models/
    ├── schemas/
    └── tests/
```

## 🎯 Example Following Team Structure

Looking at the reference repository structure from [levelup-skill-profiler](https://github.com/GreeshmakRaj/levelup-skill-profiler), they organized it as:

```
levelup-skill-profiler/
├── README.md                   ← Root project README
├── frontend/                   ← React/Next.js
│   ├── README.md
│   └── ...
└── backend/                    ← FastAPI (this is your folder)
    ├── README.md
    ├── app/
    └── ...
```

If you want to follow this structure, you might want to:
1. Push the entire parent folder (`APEX-29-06-26/`) instead
2. Have separate README files for backend and frontend
3. Have a root README that explains the overall project

## 🤝 Collaboration Tips

1. **Clone the repo** (for team members):
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

2. **Follow the README setup instructions**

3. **Create branches** for new features

4. **Use Pull Requests** for code review

## ✨ Next Steps

After pushing to GitHub:

1. ✅ Add a detailed README (already done!)
2. ✅ Add `.gitignore` (already done!)
3. 📝 Add LICENSE file (optional)
4. 📝 Set up GitHub Actions for CI/CD (optional)
5. 📝 Add CONTRIBUTING.md for team guidelines (optional)
6. 🌐 Deploy to cloud (Render, Railway, Heroku, etc.)

---

**Need help?** Create an issue on GitHub or refer to [Git Documentation](https://git-scm.com/doc)
