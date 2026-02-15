# 🦷 Dental Management System

A comprehensive, full-featured Django-based dental clinic management system with advanced features for both patients and doctors. Built with modern web technologies and best practices.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2.11-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)]()
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

## 📋 Table of Contents
- [Features](#-features)
- [Demo Accounts](#-demo-accounts)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Deployment](#-deployment)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 👤 For Patients

#### Appointment Management
- 📅 **Book Appointments** - Schedule regular and emergency appointments
- 🔄 **Reschedule Appointments** - Easy rescheduling with conflict detection
- ⏰ **Appointment Reminders** - Email and in-app notifications
- 📋 **Appointment History** - View past and upcoming appointments
- 🚨 **Emergency Booking** - Priority booking for urgent cases
- 📝 **Waitlist** - Join waitlist for fully booked slots

#### Payment & Billing
- 💳 **Multiple Payment Methods** - Cash, Card (Stripe), UPI, Online Banking
- 🔒 **Secure Payments** - Stripe integration with test mode
- 📧 **Automated Invoices** - Email invoices after payment
- 💰 **Payment History** - Track all payments and download invoices
- 📊 **Payment Analytics** - View spending patterns

#### Medical Records & Treatment
- 🏥 **Medical Records** - Access complete medical history
- 📋 **Treatment Plans** - View detailed treatment plans from doctors
- 💊 **Prescriptions** - Digital prescription access
- 📈 **Progress Tracking** - Monitor treatment progress
- 📄 **Document Management** - Upload and manage medical documents

#### User Experience
- ⭐ **Rate & Review Doctors** - Share feedback and experiences
- 🔔 **Real-time Notifications** - Instant updates on appointments and payments
- 🔍 **Advanced Search** - Find doctors by specialization, location, rating
- 📱 **Responsive Design** - Works seamlessly on all devices
- 🔐 **Two-Factor Authentication** - Enhanced account security
- 👤 **Profile Management** - Update personal information easily

### 👨‍⚕️ For Doctors

#### Schedule & Appointments
- 📅 **Daily Schedule** - View and manage today's appointments
- 👥 **Patient Management** - Access patient information quickly
- ⏰ **Time Slot Management** - Configure available time slots
- 🔄 **Recurring Appointments** - Set up recurring patient visits
- ❌ **No-Show Tracking** - Mark and track patient no-shows
- 📊 **Appointment Analytics** - View booking patterns

#### Patient Care
- 💊 **Digital Prescriptions** - Generate and send prescriptions
- 🏥 **Medical Records** - Add and update patient medical records
- 📋 **Treatment Plans** - Create comprehensive treatment plans
- 📈 **Progress Monitoring** - Track patient treatment progress
- 📝 **Session Notes** - Document consultation notes

#### Business Management
- 📊 **Analytics Dashboard** - Revenue, appointments, performance metrics
- 📈 **Reports Generation** - Daily, weekly, monthly reports (PDF/CSV)
- 💰 **Revenue Tracking** - Monitor income and payment trends
- ⭐ **Ratings & Reviews** - View patient feedback
- 📧 **Email Notifications** - Automated patient communication
- 📱 **Mobile Access** - Manage practice on the go

#### Professional Profile
- 👤 **Doctor Profile** - Showcase qualifications and specializations
- ⭐ **Rating System** - Display patient ratings and reviews
- 🏥 **Clinic Information** - Manage clinic details and location
- 📸 **Profile Customization** - Add photos and descriptions

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/aayushmishra321/Dentalmanagement-.git
   cd Dentalmanagement-
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy example file
   cp .env.example .env
   
   # Edit .env with your configuration
   # Add your SECRET_KEY, Stripe keys, email settings, etc.
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser** (admin account)
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

8. **Start the development server**
   ```bash
   python start_and_open.py
   ```
   Or manually:
   ```bash
   python manage.py runserver 8080
   ```

9. **Access the application**
   ```
   http://localhost:8080/
   ```

10. **Access admin panel**
    ```
    http://localhost:8080/admin/
    ```

---

## 👥 Demo Accounts

### Test Patients
```
Email: aayushmishra018@gmail.com
Password: password123

Email: patient@example.com
Password: password123
```

### Test Doctors
```
Email: Piyush@hospital.com
Password: password123

Email: Aman@hospital.com
Password: password123
```

**Note**: All passwords are hashed using PBKDF2-SHA256 for security.

---

## 🛠️ Tech Stack

### Backend
- **Framework**: Django 4.2.11
- **Language**: Python 3.8+
- **Database**: SQLite3 (Development) / PostgreSQL (Production)
- **ORM**: Django ORM
- **Authentication**: Django Auth + Custom 2FA
- **API**: Django REST Framework
- **Task Queue**: Celery + Redis
- **WSGI Server**: Gunicorn

### Frontend
- **Template Engine**: Django Templates
- **Styling**: Custom CSS3
- **JavaScript**: Vanilla JS
- **Icons**: Font Awesome 6.5.1
- **Responsive**: Mobile-first design

### Payment Integration
- **Payment Gateway**: Stripe API
- **Supported Methods**: Card, UPI, Cash, Online Banking
- **Security**: PCI DSS compliant (via Stripe)

### Email & Notifications
- **Email Backend**: SMTP (Gmail, SendGrid, etc.)
- **Notifications**: Django Notifications HQ
- **Real-time**: WebSocket support ready

### Security
- **Password Hashing**: PBKDF2-SHA256
- **2FA**: Django OTP with QR codes
- **CSRF Protection**: Django built-in
- **XSS Protection**: Template auto-escaping
- **SQL Injection**: ORM protection
- **Rate Limiting**: Django Ratelimit
- **Session Security**: Secure cookies

### DevOps & Deployment
- **Version Control**: Git
- **Hosting**: Render (recommended)
- **Static Files**: WhiteNoise
- **Media Storage**: Local / Cloudinary / S3
- **Monitoring**: Django logging
- **CI/CD**: GitHub Actions ready

---

## 📦 Project Structure

```
dentalmanagement/
├── dentalmanagement/           # Project settings
│   ├── settings.py            # Main configuration
│   ├── urls.py                # Root URL configuration
│   ├── wsgi.py                # WSGI application
│   ├── asgi.py                # ASGI application
│   ├── celery.py              # Celery configuration
│   └── logging_filters.py     # Custom logging
│
├── home/                       # Main application
│   ├── models.py              # Database models (15+ models)
│   ├── views.py               # View functions (50+ views)
│   ├── urls.py                # URL patterns (52 URLs)
│   ├── admin.py               # Admin configuration
│   ├── utils.py               # Utility functions
│   ├── reports.py             # Report generation
│   ├── security.py            # Security features
│   ├── tasks.py               # Background tasks
│   ├── api_views.py           # API endpoints
│   └── serializers.py         # API serializers
│
├── templates/                  # HTML templates (42 files)
│   ├── index.html             # Homepage
│   ├── login.html             # Login page
│   ├── registrationpage.html  # Registration
│   ├── userhomepage.html      # Patient dashboard
│   ├── doctorschedule.html    # Doctor schedule
│   ├── payment.html           # Payment page
│   ├── treatment_plan*.html   # Treatment plans
│   └── ...                    # More templates
│
├── static/                     # Static files
│   ├── cssfiles/              # CSS stylesheets (20+ files)
│   ├── service-worker.js      # PWA service worker
│   └── manifest.json          # PWA manifest
│
├── media/                      # User uploads
│   └── reports/               # Generated reports
│
├── logs/                       # Application logs
│   └── dental_management.log  # Main log file
│
├── staticfiles/                # Collected static files (production)
│
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in git)
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
├── build.sh                   # Render build script
├── render.yaml                # Render configuration
├── README.md                  # This file
└── DEPLOYMENT.md              # Deployment guide
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Django Settings
SECRET_KEY=your-secret-key-here-generate-a-new-one
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Development)
DATABASE_URL=sqlite:///db.sqlite3

# Database (Production - PostgreSQL)
# DATABASE_URL=postgresql://user:password@host:port/database

# Stripe Payment Gateway (Test Mode)
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key
STRIPE_SECRET_KEY=sk_test_your_secret_key
STRIPE_CURRENCY=inr

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Redis (for Celery - optional)
REDIS_URL=redis://localhost:6379/0

# Security (Production)
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Stripe Test Cards

For testing payments:
- **Success**: 4242 4242 4242 4242
- **Decline**: 4000 0000 0000 0002
- **Requires Authentication**: 4000 0025 0000 3155

---

## 🚀 Deployment

### Deploy to Render (Recommended)

1. **Clean your repository**
   ```bash
   # Windows
   cleanup_git.bat
   
   # Mac/Linux
   chmod +x cleanup_git.sh
   ./cleanup_git.sh
   ```

2. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

3. **Follow deployment guide**
   - See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions
   - Or [DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md) for quick reference

4. **Estimated deployment time**: 15-30 minutes

### Deploy to Other Platforms

- **Heroku**: Supported (add Procfile)
- **Railway**: Supported
- **PythonAnywhere**: Supported
- **AWS/GCP/Azure**: Supported (requires configuration)

---

## 📖 Usage

### For Patients

1. **Register Account**
   - Go to homepage
   - Click "Register"
   - Fill in details
   - Verify email (if configured)

2. **Book Appointment**
   - Login to your account
   - Click "Book Appointment"
   - Select doctor and time slot
   - Confirm booking

3. **Make Payment**
   - Go to "Appointments"
   - Click "Pay Now" on appointment
   - Select payment method
   - Complete payment

4. **View Treatment Plans**
   - Click user menu (top right)
   - Select "Treatment Plans"
   - View plan details and progress

### For Doctors

1. **Login**
   - Use doctor credentials
   - Access doctor dashboard

2. **View Schedule**
   - See today's appointments
   - Patient information displayed

3. **Create Treatment Plan**
   - Click "Treatment Plan" on appointment
   - Fill in plan details
   - Submit to patient

4. **Generate Reports**
   - Go to Analytics Dashboard
   - Select report type
   - Download PDF or CSV

---

## 📊 Database Models

### Core Models
- **UserDetail** - Patient information
- **DoctorDetail** - Doctor information
- **bookappointment** - Appointment records

### Payment Models
- **Payment** - Payment transactions
- **Invoice** - Invoice records

### Medical Models
- **MedicalRecord** - Patient medical history
- **TreatmentPlan** - Treatment plans
- **TreatmentSession** - Treatment sessions
- **Prescription** - Prescription records

### Rating & Review
- **DoctorRating** - Doctor ratings and reviews

### Notification
- **Notification** - User notifications

### Advanced Features
- **Waitlist** - Appointment waitlist
- **TwoFactorAuth** - 2FA settings
- **RecurringAppointment** - Recurring appointments

---

## 🔒 Security Features

- ✅ Password hashing (PBKDF2-SHA256)
- ✅ Two-factor authentication (2FA)
- ✅ CSRF protection
- ✅ XSS protection
- ✅ SQL injection prevention
- ✅ Secure session management
- ✅ Rate limiting
- ✅ Input validation
- ✅ Secure payment processing (Stripe)
- ✅ HTTPS enforcement (production)
- ✅ Security headers
- ✅ Content Security Policy

---

## 📱 Responsive Design

The application is fully responsive and tested on:
- ✅ Desktop (1920x1080, 1366x768)
- ✅ Laptop (1440x900, 1280x800)
- ✅ Tablet (iPad, Android tablets)
- ✅ Mobile (iPhone, Android phones)
- ✅ All modern browsers (Chrome, Firefox, Safari, Edge)

---

## 🌟 Key Features Summary

### Patient Features (15+)
✅ Appointment booking & management  
✅ Multiple payment methods  
✅ Treatment plan viewing  
✅ Medical records access  
✅ Doctor ratings & reviews  
✅ Real-time notifications  
✅ Advanced search  
✅ 2FA security  
✅ Payment history  
✅ Profile management  

### Doctor Features (15+)
✅ Schedule management  
✅ Patient management  
✅ Treatment plan creation  
✅ Medical record management  
✅ Prescription generation  
✅ Analytics dashboard  
✅ Report generation  
✅ Revenue tracking  
✅ Rating management  
✅ Profile customization  

### Admin Features (10+)
✅ User management  
✅ Doctor approval  
✅ System monitoring  
✅ Report generation  
✅ Payment tracking  
✅ Content management  
✅ Email configuration  
✅ Security settings  
✅ Backup management  
✅ Analytics overview  

---

## 🤝 Contributing

This is a private project. For any issues or suggestions:

1. Create an issue on GitHub
2. Fork the repository
3. Create a feature branch
4. Make your changes
5. Submit a pull request

### Development Guidelines
- Follow PEP 8 style guide
- Write unit tests for new features
- Update documentation
- Use meaningful commit messages

---

## 📄 License

All rights reserved. This is a proprietary dental management system.

Copyright © 2024-2026 Dental Management System

---

## 👨‍💻 Author

**Aayush Mishra**
- GitHub: [@aayushmishra321](https://github.com/aayushmishra321)
- Email: aayushmishra018@gmail.com

---

## 🙏 Acknowledgments

- Django Framework
- Stripe Payment Gateway
- Font Awesome Icons
- Bootstrap (inspiration)
- Open Source Community

---

## 📞 Support

For support and questions:
- 📧 Email: aayushmishra018@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/aayushmishra321/Dentalmanagement-/issues)
- 📖 Documentation: See DEPLOYMENT.md

---

## 🗺️ Roadmap

### Upcoming Features
- [ ] Video consultation integration
- [ ] Mobile app (React Native)
- [ ] AI-powered diagnosis assistance
- [ ] Multi-language support
- [ ] Advanced analytics with ML
- [ ] Inventory management
- [ ] Lab integration
- [ ] Insurance claim processing
- [ ] Telemedicine features
- [ ] Patient portal enhancements

---

## 📈 Version History

### v1.0.0 (Current)
- ✅ Complete appointment management
- ✅ Payment integration (Stripe)
- ✅ Treatment plans
- ✅ Medical records
- ✅ Analytics dashboard
- ✅ 2FA security
- ✅ Email notifications
- ✅ Responsive design

---

## 🎯 Project Stats

- **Lines of Code**: 15,000+
- **Templates**: 42
- **Views**: 50+
- **Models**: 15+
- **URLs**: 52
- **Features**: 40+
- **Development Time**: 6 months
- **Status**: Production Ready ✅

---

## 💡 Tips & Tricks

### For Development
```bash
# Run with debug toolbar
pip install django-debug-toolbar

# Generate secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Create migrations
python manage.py makemigrations

# Check for issues
python manage.py check
```

### For Production
```bash
# Collect static files
python manage.py collectstatic --noinput

# Run with gunicorn
gunicorn dentalmanagement.wsgi:application

# Check deployment readiness
python manage.py check --deploy
```

---

## ⚡ Performance

- **Page Load Time**: < 2 seconds
- **API Response Time**: < 500ms
- **Database Queries**: Optimized with select_related/prefetch_related
- **Caching**: Redis caching ready
- **Static Files**: Compressed and minified
- **Images**: Optimized and lazy-loaded

---

## 🔧 Troubleshooting

### Common Issues

**Issue**: Static files not loading
```bash
python manage.py collectstatic --noinput
```

**Issue**: Database errors
```bash
python manage.py migrate
```

**Issue**: Port already in use
```bash
# Use different port
python manage.py runserver 8000
```

**Issue**: Stripe payment fails
- Check API keys in .env
- Verify test mode is active
- Check Stripe dashboard logs

---

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Stripe API Docs](https://stripe.com/docs/api)
- [Deployment Guide](DEPLOYMENT.md)
- [GitHub Cleanup Guide](GITHUB_CLEANUP_GUIDE.md)

---

**Built with ❤️ using Django**

**Status**: Production Ready ✅  
**Version**: 1.0.0  
**Last Updated**: February 15, 2026

---

⭐ **Star this repository if you find it helpful!** ⭐
