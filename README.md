# 🛡️ AI Bug Tracker - Production-Grade Issue Management

[![CI/CD Pipeline](https://github.com/sandravedha1983/AI-Bugtracker/actions/workflows/ci.yml/badge.svg)](https://github.com/sandravedha1983/AI-Bugtracker/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-%23000.svg?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)

An intelligent, industry-level bug tracking platform powered by AI. Streamline your software development lifecycle with automated issue classification, predictive severity analysis, and seamless GitHub integration.

---

## 🚀 Key Features

- **🧠 AI Bug Classification**: Automatically triage incoming bugs using Zero-shot classification (Hugging Face).
- **📊 Advanced Analytics**: Real-time insights into system health, resolution trends, and developer workload.
- **🔐 Enterprise RBAC**: Role-Based Access Control for Admin, Team Lead, Developer, and Tester roles.
- **🐙 GitHub Sync**: Automatic GitHub Issue creation and status synchronization.
- **📈 Predictive Severity**: AI-driven priority suggestion based on bug descriptions.
- **🌐 Google OAuth 2.0**: Secure, one-click authentication.
- **📚 API Documentation**: Interactive Swagger/OpenAPI documentation.
- **🐳 Docker Ready**: Full containerization for consistent development and deployment.
- **🛡️ Security First**: Rate limiting, CSRF protection, and secure audit logging.

---

## 🛠️ Tech Stack

**Backend:**
- Flask (Python Framework)
- SQLAlchemy (ORM)
- PostgreSQL / MySQL (Database)
- Flask-Login & Google OAuth (Auth)
- Flasgger (Swagger/OpenAPI)

**AI & Integration:**
- Hugging Face Inference API
- PyGithub (GitHub Integration)

**Frontend:**
- Modern HTML5 / Vanilla CSS3
- ApexCharts (Analytics)
- SweetAlert2 (Notifications)

**DevOps:**
- Docker & Docker Compose
- GitHub Actions (CI/CD)
- Gunicorn (Production Server)
- Render (Deployment)

---

## 🏗️ Architecture

The project follows a **Service-Oriented Repository Pattern** for maximum maintainability:

- **`app/api`**: RESTful API endpoints.
- **`app/models`**: Database schemas and business entities.
- **`app/services`**: Business logic layer (AI, GitHub, Bug management).
- **`app/middleware`**: Security and request processing.
- **`app/utils`**: Reusable helpers (Email, Decorators, Seeds).
- **`app/templates`**: Jinja2 UI components.

---

## 📸 Screenshots

| Login Page | Analytics Dashboard |
|------------|---------------------|
| ![Login](https://via.placeholder.com/400x250?text=Login+Page) | ![Analytics](https://via.placeholder.com/400x250?text=Analytics+Dashboard) |

| Bug Management | Admin Panel |
|----------------|-------------|
| ![Bugs](https://via.placeholder.com/400x250?text=Bug+List) | ![Admin](https://via.placeholder.com/400x250?text=Admin+Panel) |

---

## ⚙️ Installation

### Prerequisites
- Python 3.9+
- Docker (optional)

### Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/sandravedha1983/AI-Bugtracker.git
   cd AI-Bugtracker
   ```

2. **Create Virtual Environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment:**
   Copy `.env.example` to `.env` and fill in your credentials.

5. **Run Migrations:**
   ```bash
   flask db upgrade
   ```

6. **Start Development Server:**
   ```bash
   python run.py
   ```

---

## 🔌 API Documentation

Detailed API documentation is available at `/apidocs` when the server is running.

### Sample Endpoints:

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/bugs` | List all bugs | 🔑 |
| POST | `/api/bugs` | Report new bug | 🔑 |
| GET | `/api/analytics/summary` | Get system metrics | 🔑 |
| POST | `/api/bugs/<id>` | Update bug status | 🔑 |

---

## 🐳 Docker Usage

**Run with Docker Compose:**
```bash
docker-compose up --build
```

---

## 🛡️ Security & Reliability

- **Password Hashing**: Bcrypt with salt.
- **Rate Limiting**: Throttling to prevent brute-force attacks.
- **Audit Logging**: Every action is recorded in the `audit_logs` table.
- **CI/CD**: Automatic linting and testing on every push.

---

## 🤝 Contributing

Contributions are welcome! Please read the [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

**Developed with ❤️ by [Your Name/GitHub]**
