# Deployment Guide - Render

## 🚀 Deploy to Render

### Prerequisites
- GitHub account
- Render account (free tier available)
- Your code pushed to GitHub

---

## Step 1: Prepare Your Repository

### 1.1 Update .gitignore
Already configured to exclude:
- `.env` (sensitive data)
- `db.sqlite3` (local database)
- `*.log` (log files)
- `__pycache__/` (Python cache)
- `staticfiles/` (collected static files)
- `media/*` (user uploads)

### 1.2 Required Files (Already Created)
- ✅ `requirements.txt` - Python dependencies
- ✅ `build.sh` - Build script for Render
- ✅ `render.yaml` - Render configuration
- ✅ `.env.example` - Environment variables template

### 1.3 Push to GitHub
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

---

## Step 2: Create Render Account

1. Go to https://render.com
2. Sign up with GitHub
3. Authorize Render to access your repositories

---

## Step 3: Create PostgreSQL Database

1. Click **"New +"** → **"PostgreSQL"**
2. Configure:
   - **Name**: `dental-management-db`
   - **Database**: `dental_management`
   - **User**: `dental_user`
   - **Region**: Choose closest to you
   - **Plan**: Free
3. Click **"Create Database"**
4. Wait for database to be created
5. Copy the **Internal Database URL** (starts with `postgresql://`)

---

## Step 4: Create Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:

### Basic Settings:
- **Name**: `dental-management`
- **Region**: Same as database
- **Branch**: `main`
- **Root Directory**: Leave empty (or `dentalmanagement` if nested)
- **Runtime**: `Python 3`
- **Build Command**: 
  ```bash
  pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
  ```
- **Start Command**: 
  ```bash
  gunicorn dentalmanagement.wsgi:application
  ```

### Environment Variables:
Click **"Advanced"** → **"Add Environment Variable"**

Add these variables:

```
SECRET_KEY=your-secret-key-here-generate-a-new-one
DEBUG=False
ALLOWED_HOSTS=.onrender.com
DATABASE_URL=<paste-internal-database-url-from-step-3>

# Stripe (Test Mode)
STRIPE_PUBLISHABLE_KEY=pk_test_your_key
STRIPE_SECRET_KEY=sk_test_your_key
STRIPE_CURRENCY=inr

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Instance Type:
- **Plan**: Free

4. Click **"Create Web Service"**

---

## Step 5: Wait for Deployment

1. Render will:
   - Clone your repository
   - Install dependencies
   - Run migrations
   - Collect static files
   - Start the server

2. Monitor the logs for any errors

3. Once deployed, you'll get a URL like:
   ```
   https://dental-management.onrender.com
   ```

---

## Step 6: Create Superuser (Admin)

1. Go to your Render dashboard
2. Click on your web service
3. Click **"Shell"** tab
4. Run:
   ```bash
   python manage.py createsuperuser
   ```
5. Follow prompts to create admin account

---

## Step 7: Test Your Deployment

1. Visit your Render URL
2. Test login with created accounts
3. Test all features:
   - Patient registration
   - Doctor login
   - Appointment booking
   - Payment processing
   - Treatment plans
   - Medical records

---

## 🔧 Troubleshooting

### Issue: Static files not loading
**Solution**: 
1. Check `STATIC_ROOT` in settings.py
2. Run: `python manage.py collectstatic`
3. Verify `whitenoise` is in `MIDDLEWARE`

### Issue: Database connection error
**Solution**:
1. Verify `DATABASE_URL` environment variable
2. Check database is running in Render dashboard
3. Ensure `dj-database-url` is in requirements.txt

### Issue: 500 Internal Server Error
**Solution**:
1. Check Render logs
2. Verify all environment variables are set
3. Check `ALLOWED_HOSTS` includes `.onrender.com`
4. Ensure `DEBUG=False` in production

### Issue: Media files not persisting
**Solution**
Render's free tier has ephemeral storage. For persistent media:
1. Use Cloudinary (free tier)
2. Use AWS S3
3. Use Render's persistent disk (paid)

---

## 📊 Monitoring

### View Logs:
1. Render Dashboard → Your Service → Logs
2. Real-time log streaming
3. Filter by severity

### Metrics:
1. CPU usage
2. Memory usage
3. Request count
4. Response times

---

## 🔄 Updating Your Deployment

### Automatic Deployment:
Render automatically deploys when you push to GitHub:
```bash
git add .
git commit -m "Update feature"
git push origin main
```

### Manual Deployment:
1. Render Dashboard → Your Service
2. Click **"Manual Deploy"** → **"Deploy latest commit"**

---

## 🔐 Security Checklist

- ✅ `DEBUG=False` in production
- ✅ Strong `SECRET_KEY` (generate new one)
- ✅ `.env` file excluded from git
- ✅ `ALLOWED_HOSTS` properly configured
- ✅ Database credentials secure
- ✅ HTTPS enabled (automatic on Render)
- ✅ CSRF protection enabled
- ✅ SQL injection protection (Django ORM)

---

## 💰 Cost Estimate

### Free Tier:
- Web Service: Free (with limitations)
- PostgreSQL: Free (limited storage)
- SSL Certificate: Free
- Custom domain: Free

### Limitations:
- Service spins down after 15 min of inactivity
- 750 hours/month free
- Limited CPU/RAM
- Ephemeral storage

### Paid Plans:
- Starter: $7/month (always on)
- Standard: $25/month (more resources)
- Pro: $85/month (dedicated resources)

---

## 🌐 Custom Domain (Optional)

1. Buy domain from provider (Namecheap, GoDaddy, etc.)
2. Render Dashboard → Your Service → Settings
3. Add custom domain
4. Update DNS records:
   ```
   Type: CNAME
   Name: www
   Value: your-app.onrender.com
   ```
5. Wait for DNS propagation (up to 48 hours)

---

## 📝 Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| SECRET_KEY | Django secret key | `django-insecure-...` |
| DEBUG | Debug mode | `False` |
| ALLOWED_HOSTS | Allowed domains | `.onrender.com` |
| DATABASE_URL | PostgreSQL URL | `postgresql://...` |
| STRIPE_PUBLISHABLE_KEY | Stripe public key | `pk_test_...` |
| STRIPE_SECRET_KEY | Stripe secret key | `sk_test_...` |
| EMAIL_HOST_USER | Email address | `your@gmail.com` |
| EMAIL_HOST_PASSWORD | Email app password | `abcd efgh ijkl mnop` |

---

## 🎯 Post-Deployment Tasks

1. ✅ Create superuser account
2. ✅ Test all features
3. ✅ Set up monitoring
4. ✅ Configure custom domain (optional)
5. ✅ Set up email notifications
6. ✅ Test payment processing
7. ✅ Create sample data (optional)
8. ✅ Set up backups

---

## 📞 Support

- Render Docs: https://render.com/docs
- Render Community: https://community.render.com
- Django Docs: https://docs.djangoproject.com

---

**Deployment Status**: Ready for Render ✅  
**Estimated Setup Time**: 15-30 minutes  
**Difficulty**: Easy 🟢
