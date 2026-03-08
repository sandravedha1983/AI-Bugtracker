# 🐞 AI Bug Tracker — Enterprise-Grade Issue Management

A high-performance, Flask-based bug tracking platform featuring **AI-driven priority classification**, **6-digit OTP Email Verification**, **Google OAuth 2.0 Authentication**, and a **Separate Administration Portal**.

---

## ✨ Core Features

- **🧠 AI-Powered Triage**: Automatically predicts bug priority and generates summaries using HuggingFace models.
- **🔐 Secure Authentication**: 
    - **6-digit OTP Verification**: Mandatory email verification for all new signups.
    - **Google Sign-In**: Seamless authentication via Google OAuth 2.0.
- **🛡️ Multi-Tier RBAC**: Distinct roles for Admins, Developers, and Testers with granular access control.
- **📊 Real-Time Analytics**: Interactive dashboards with Chart.js visualization for bug trends and priorities.
- **💼 Platform Administration**: A dedicated, separate portal for system management at `/platform-admin`.
- **🔌 Database Stability**: Optimized for cloud deployment (Neon PostgreSQL) with connection pooling and pre-pinging.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.x, Flask, SQLAlchemy (PostgreSQL in production, SQLite locally)
- **Frontend**: Tailwind CSS, Vanilla JS, Chart.js
- **Auth**: Flask-Login + Flask-Dance (Google OAuth) + Flask-Mail (OTP)
- **AI/ML**: HuggingFace Transformers

---

## 🚀 Setup Instructions

### 1. Installation
```bash
git clone https://github.com/sandravedha1983/AI-Bugtracker.git
cd AI-Bugtracker
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configuration (.env)
Create a `.env` file in the root directory:
```env
SECRET_KEY=your_generated_secret_key
DATABASE_URL=postgresql://user:pass@ep-round-shape.aws.neon.tech/neondb?sslmode=require
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-digit-app-password
MAIL_DEFAULT_SENDER=AI Bug Tracker <your-email@gmail.com>
GOOGLE_CLIENT_ID=your_google_id
GOOGLE_CLIENT_SECRET=your_google_secret
OAUTHLIB_INSECURE_TRANSPORT=1 # Set to 1 ONLY for local dev
```

### 3. Initialize Database
The application automatically creates tables on startup. To manually update the schema with the latest OTP columns:
```bash
python scripts/update_db.py
```

### 4. Run Application
```bash
python app.py
```
- **Login/Signup**: `http://127.0.0.1:5000/login`
- **Admin Dashboard**: `http://127.0.0.1:5000/platform-admin/login`

---

## 🔒 Security & Optimization
- **OTP Verification**: Accounts are locked until the 6-digit code sent via email is verified.
- **OAuth 2.0**: Secure third-party authentication with Google.
- **Connection Stability**: Configured with `pool_pre_ping=True` and `pool_recycle=300` for 24/7 reliability on Neon PostgreSQL.
- **Role Isolation**: Admin actions are separated from standard user routes.

---
*Developed for modern engineering teams.*
