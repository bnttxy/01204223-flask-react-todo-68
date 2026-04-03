import sys
from pathlib import Path
import pytest

# เพิ่ม Path ของ backend เพื่อให้ import models/main ได้
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from main import app as flask_app
from models import db

@pytest.fixture
def app():
    flask_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    })

    with flask_app.app_context():
        db.drop_all()
        db.create_all()
        yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def app_context(app):
    with app.app_context():
        yield

@pytest.fixture(autouse=True)
def no_jwt(monkeypatch):
    """Mock JWT เพื่อข้ามการตรวจสอบรหัสผ่านในการเทส"""
    def no_verify(*args, **kwargs):
        from flask import g
        from flask_jwt_extended.config import config
        g._jwt_extended_jwt = {
            config.identity_claim_key: 'test_user'
        }

    from flask_jwt_extended import view_decorators
    monkeypatch.setattr(view_decorators, 'verify_jwt_in_request', no_verify)