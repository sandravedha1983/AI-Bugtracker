# AI Bug Tracker 🛡️

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![Flask](https://img.shields.io/badge/flask-v3.1-black)
![License](https://img.shields.io/badge/license-MIT-blue)

An enterprise-grade, AI-powered bug tracking system designed for professional development teams.

## 🚀 Key Features

- **AI-Powered Insights**: Automated bug priority classification and issue summarization.
- **Role-Based Workflows**: Tailored dashboards for Admin, Lead, Developer, and Tester.
- **GitHub Sync**: Automatic mirroring of bugs to GitHub Issues.
- **Enterprise Security**: CSRF protection, rate limiting, and Bcrypt password hashing.
- **Dynamic Analytics**: Real-time data visualization using Chart.js.
- **Modular Architecture**: Clean, scalable codebase with blueprint-based routing.
- **API Documentation**: Interactive Swagger/OpenAPI documentation.

## 🛠️ Technology Stack

- **Backend**: Python (Flask), SQLAlchemy
- **Database**: PostgreSQL (Production), SQLite (Test)
- **Frontend**: Tailwind CSS, Chart.js, Vanilla JS
- **DevOps**: Docker, Docker Compose, GitHub Actions
- **AI**: NLP-based priority classifier

## 📂 Project Structure

```text
├── app/                # Application initialization
├── models/             # Database models (User, Bug)
├── routes/             # Blueprint-based route handlers
├── services/           # Service layer (AI, GitHub)
├── static/             # Assets (CSS, JS)
├── templates/          # Jinja2 HTML templates
├── utils/              # Helper functions and decorators
├── tests/              # Automated tests (Pytest)
├── Dockerfile          # Container configuration
└── wsgi.py            # Application entry point
```

## ⚙️ Installation & Setup

### Local Setup
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment variables in `.env`.
4. Run the application: `python wsgi.py`

### Docker Setup
```bash
docker-compose up --build
```

## 🔒 Security & Roles

- **Admin**: System management and global analytics.
- **Lead**: Team oversight and bug assignment.
- **Developer**: Task execution and status tracking.
- **Tester**: Bug reporting and verification.

## 📄 Documentation

Visit `/api/docs` in your browser to access the interactive Swagger API documentation.

Built with ❤️ by AI Bug Tracker
