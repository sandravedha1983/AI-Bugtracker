# 🐞 AI Bug Tracker — Enterprise-Grade Issue Management

A high-performance, Flask-based bug tracking platform featuring **AI-driven priority classification**, **Google OAuth 2.0 Authentication**, and a **Separate Administration Port**.

---

## ✨ Core Features

- **🧠 AI-Powered Triage**: Automatically predicts bug priority and generates summaries.
- **🔐 Google Sign-In**: Seamless authentication via Google OAuth 2.0.
- **�️ Multi-Tier RBAC**: Distinct roles for Admins, Developers, and Testers.
- **📊 Real-Time Analytics**: Interactive dashboards with Chart.js.
- **💼 Platform Administration**: A dedicated, separate portal for system management at `/platform-admin`.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.x, Flask, SQLAlchemy (PostgreSQL in production, SQLite locally)
- **Frontend**: Tailwind CSS, Vanilla JS, Chart.js
- **Auth**: Flask-Login + Flask-Dance (Google OAuth)
- **AI/ML**: HuggingFace Transformers

---

## 🚀 Setup Instructions

### 1. Installation
```bash
git clone https://github.com/yourusername/AI-Bug-Tracker.git
cd AI-Bug-Tracker
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configuration (.env)
Create a `.env` file with these keys:
```env
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://user:pass@localhost:5432/db # Optional: falls back to SQLite
GOOGLE_CLIENT_ID=your_google_id
GOOGLE_CLIENT_SECRET=your_google_secret
OAUTHLIB_INSECURE_TRANSPORT=1 # Set to 1 ONLY for local dev
```

### 3. Initialize Admin Account
Run the following script to create a system administrator:
```bash
python scripts/create_admin.py
```
Default credentials:
- **Email**: `admin@bugtracker.ai`
- **Password**: `admin_password_123`

### 4. Run Application
```bash
flask run
```
- **Login**: `http://127.0.0.1:5000/login`
- **Admin Dashboard**: `http://127.0.0.1:5000/platform-admin`

---

## 🔒 Security
- **OAuth 2.0**: Secure Google authentication.
- **Platform Admin**: Independent authentication flow for enterprise security.
- **Environment Isolation**: Production uses PostgreSQL; Local uses SQLite.

---
*Developed for modern engineering teams.*
