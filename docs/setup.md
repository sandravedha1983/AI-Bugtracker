# Developer Setup Guide

## Local Development

1. **Install Python 3.9+**
2. **Create Virtual Environment**:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Setup Environment**: Create `.env` from `.env.example`.
5. **Database Setup**:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```
6. **Run App**:
   ```bash
   python run.py
   ```

## Testing
Run tests using pytest:
```bash
pytest
```
The CI/CD pipeline will automatically run these tests on every Pull Request.
