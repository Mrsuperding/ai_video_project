"""
Pytest Configuration and Fixtures
"""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Base, get_db
from app.core.security import create_access_token


@pytest.fixture(scope="session")
def db_engine():
    """Create in-memory database for session"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False
    )

    Base.metadata.create_all(bind=engine)

    yield engine

    engine.dispose()


@pytest.fixture(scope="function")
def db(db_engine):
    """Provide session and clean all tables before each test"""
    session = sessionmaker(bind=db_engine)()

    with db_engine.connect() as conn:
        conn.execute(text("PRAGMA foreign_keys = OFF"))
        conn.commit()

        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tables = [row[0] for row in result]

        for table in tables:
            conn.execute(text(f"DELETE FROM {table}"))

        conn.execute(text("PRAGMA foreign_keys = ON"))
        conn.commit()

    yield session
    session.close()


@pytest.fixture(scope="function")
def client(db):
    """Provide test client with database override"""
    from app.api import api_router

    test_app = FastAPI()
    test_app.include_router(api_router)

    def override_get_db():
        yield db

    test_app.dependency_overrides[get_db] = override_get_db
    with TestClient(test_app, raise_server_exceptions=False) as c:
        yield c


@pytest.fixture(scope="function")
def auth_headers(db) -> dict:
    """Create a test user and return auth headers"""
    from app.models.user import User
    from app.core.security import hash_password

    user = User(
        phone="13800138000",
        nickname="test_user",
        password_hash=hash_password("password123"),
        status="active"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": str(user.id), "type": "access"})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def admin_headers(db) -> dict:
    """Create a test admin and return auth headers"""
    from app.models.admin import Admin
    from app.core.security import hash_password

    admin = Admin(
        username="admin",
        password_hash=hash_password("admin123"),
        real_name="Admin User",
        role="admin",
        status="active"
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)

    token = create_access_token({"sub": str(admin.id), "type": "admin"})
    return {"Authorization": f"Bearer {token}"}