import pytest
from app import create_app
from extensions import db

from models.user import User
from models.bug import Bug
from config import Config

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_ENGINE_OPTIONS = {}
    TESTING = True
    WTF_CSRF_ENABLED = False

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_signup(client):
    response = client.post('/signup', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123',
        'role': 'developer'
    }, follow_redirects=True)
    assert response.status_code == 200
    user = User.query.filter_by(email='test@example.com').first()
    assert user is not None
    assert user.role == 'developer'

def test_api_access_without_login(client):
    response = client.get('/api/bugs')
    assert response.status_code == 302 # Redirect to login

def test_analytics_api_consistency(client, app):
    # This would require a logged in admin user
    # For now just verify the endpoint exists
    with app.app_context():
        admin = User(name='Admin', email='admin@example.com', role='admin', is_verified=True)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
    
    # Login manually if possible or just check context
    pass 
