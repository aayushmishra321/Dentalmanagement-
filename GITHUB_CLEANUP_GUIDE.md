# GitHub Repository Cleanup Guide

## 🎯 Goal
Clean up your GitHub repository to include only essential files for deployment and development.

---

## 📋 Files to Keep in GitHub

### Essential Files ✅
```
dentalmanagement/
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
├── manage.py                    # Django management
├── .gitignore                   # Git ignore rules
├── .env.example                 # Environment template (NO SECRETS)
├── build.sh                     # Render build script
├── render.yaml                  # Render configuration
├── DEPLOYMENT.md                # Deployment guide
├── start_and_open.py            # Local development script
│
├── dentalmanagement/            # Django settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   ├── celery.py
│   └── logging_filters.py
│
├── home/                        # Main application
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── utils.py
│   ├── reports.py
│   ├── security.py
│   ├── tasks.py
│   ├── api_views.py
│   └── serializers.py
│
├── templates/                   # HTML templates (42 files)
├── static/                      # CSS, JS, images
├── media/.gitkeep              # Keep directory structure
└── logs/.gitkeep               # Keep directory structure
```

### Files to EXCLUDE from GitHub ❌
These are already in `.gitignore`:
```
.env                    # Contains secrets (NEVER commit)
db.sqlite3              # Local database
*.log                   # Log files
__pycache__/            # Python cache
*.pyc                   # Compiled Python
staticfiles/            # Collected static files
media/*                 # User uploads (except .gitkeep)
.DS_Store               # Mac system files
```

---

## 🧹 Cleanup Steps

### Step 1: Remove Unnecessary Files from Git History

If you've already committed files that should be ignored:

```bash
# Remove .env from git (if committed)
git rm --cached .env

# Remove database from git (if committed)
git rm --cached db.sqlite3

# Remove log files from git (if committed)
git rm --cached logs/*.log

# Remove staticfiles from git (if committed)
git rm -r --cached staticfiles/

# Remove media files from git (if committed, keep .gitkeep)
git rm -r --cached media/
git add media/.gitkeep

# Remove __pycache__ directories
find . -type d -name __pycache__ -exec git rm -r --cached {} +

# Commit the changes
git commit -m "Remove unnecessary files from repository"
```

### Step 2: Verify .gitignore is Working

```bash
# Check what will be committed
git status

# Should NOT see:
# - .env
# - db.sqlite3
# - *.log files
# - __pycache__ directories
# - staticfiles/
# - media/* (except .gitkeep)
```

### Step 3: Clean Local Files (Optional)

```bash
# Remove Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Remove collected static files
rm -rf staticfiles/

# Remove log files (keep directory)
rm -f logs/*.log
```

### Step 4: Push Clean Repository

```bash
git add .
git commit -m "Clean repository for deployment"
git push origin main
```

---

## 📁 Current Repository Structure

After cleanup, your GitHub repo should look like:

```
dentalmanagement/
├── .gitignore                   ✅ Ignore rules
├── README.md                    ✅ Documentation
├── requirements.txt             ✅ Dependencies
├── manage.py                    ✅ Django CLI
├── .env.example                 ✅ Config template
├── build.sh                     ✅ Build script
├── render.yaml                  ✅ Render config
├── DEPLOYMENT.md                ✅ Deploy guide
├── start_and_open.py            ✅ Dev script
├── dentalmanagement/            ✅ Settings
├── home/                        ✅ Main app
├── templates/                   ✅ HTML files
├── static/                      ✅ CSS/JS
├── media/.gitkeep              ✅ Directory marker
└── logs/.gitkeep               ✅ Directory marker
```

---

## 🔒 Security Checklist

Before pushing to GitHub:

- [ ] `.env` file is in `.gitignore`
- [ ] No API keys in code
- [ ] No passwords in code
- [ ] No SECRET_KEY in settings.py (use environment variable)
- [ ] `.env.example` has placeholder values only
- [ ] Database credentials not committed
- [ ] Stripe keys not committed

---

## 📝 .env.example Template

Your `.env.example` should look like this (NO REAL VALUES):

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (for local development)
DATABASE_URL=sqlite:///db.sqlite3

# Stripe (Test Mode)
STRIPE_PUBLISHABLE_KEY=pk_test_your_key_here
STRIPE_SECRET_KEY=sk_test_your_key_here
STRIPE_CURRENCY=inr

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

---

## 🚀 After Cleanup

### For Local Development:
1. Clone repository
2. Copy `.env.example` to `.env`
3. Fill in real values in `.env`
4. Run: `pip install -r requirements.txt`
5. Run: `python manage.py migrate`
6. Run: `python start_and_open.py`

### For Render Deployment:
1. Push clean repository to GitHub
2. Follow `DEPLOYMENT.md` guide
3. Set environment variables in Render dashboard
4. Deploy!

---

## 🔍 Verify Repository is Clean

### Check on GitHub:
1. Go to your repository on GitHub
2. Verify you DON'T see:
   - `.env` file
   - `db.sqlite3` file
   - `*.log` files
   - `__pycache__/` directories
   - `staticfiles/` directory
   - Media files (except `.gitkeep`)

3. Verify you DO see:
   - `README.md`
   - `requirements.txt`
   - `.gitignore`
   - `.env.example`
   - `build.sh`
   - `render.yaml`
   - All Python code files
   - All templates
   - All static files

---

## 🎯 Quick Cleanup Commands

Run these commands to clean everything at once:

```bash
# Remove from git tracking
git rm --cached .env 2>/dev/null || true
git rm --cached db.sqlite3 2>/dev/null || true
git rm --cached logs/*.log 2>/dev/null || true
git rm -r --cached staticfiles/ 2>/dev/null || true
git rm -r --cached media/ 2>/dev/null || true
git add media/.gitkeep logs/.gitkeep

# Clean local files
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
rm -rf staticfiles/ 2>/dev/null || true
rm -f logs/*.log 2>/dev/null || true

# Commit and push
git add .
git commit -m "Clean repository for deployment"
git push origin main
```

---

## ✅ Checklist

Before deploying:

- [ ] `.gitignore` is properly configured
- [ ] `.env` is NOT in repository
- [ ] `.env.example` has placeholder values
- [ ] No secrets in code
- [ ] `build.sh` is executable (`chmod +x build.sh`)
- [ ] `render.yaml` is configured
- [ ] `requirements.txt` is up to date
- [ ] `README.md` is updated
- [ ] Repository is pushed to GitHub
- [ ] All tests pass locally

---

## 📞 Need Help?

If you see sensitive data in your GitHub history:
1. Use `git filter-branch` or `BFG Repo-Cleaner`
2. Or create a new repository and push clean code
3. Never commit `.env` files!

---

**Status**: Repository Ready for GitHub ✅  
**Next Step**: Follow DEPLOYMENT.md to deploy on Render
