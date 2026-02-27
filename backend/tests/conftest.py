import sys
from pathlib import Path
import pytest
from flask import g


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from main import app as flask_app
from main import db

@pytest.fixture
def app():
  
    flask_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    })

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.drop_all()  

@pytest.fixture
def client(app):
    """Fixture สำหรับจำลองการส่ง request (GET, POST, etc.)"""
    return app.test_client()

@pytest.fixture
def app_context(app):
    """Fixture สำหรับใช้งาน db.session ภายใน test function"""
    with app.app_context():
        yield

@pytest.fixture(autouse=True)
def no_jwt(monkeypatch):
    """Fixture นี้จะทำงานอัตโนมัติเพื่อ Bypass การตรวจสอบ JWT Token"""
    def no_verify(*args, **kwargs):
        from flask_jwt_extended.config import config

        g._jwt_extended_jwt = {
            'sub': 'test_user' 
        }

    from flask_jwt_extended import view_decorators

    monkeypatch.setattr(view_decorators, 'verify_jwt_in_request', no_verify)