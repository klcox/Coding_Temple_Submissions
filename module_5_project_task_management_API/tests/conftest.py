from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
import pytest
from app.database import Base, get_db
from app.main import app
from app.routers import tasks as tasks_router
from fastapi.testclient import TestClient
from app.utils.limiter import limiter
from app.models.user import User
from app.utils.security import hash_password
from app.config import settings
from app.utils.security import create_access_token


TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool  # Ensures that the same connection is reused (required for :memory: databases)
)

TestingSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=test_engine
)


@pytest.fixture
def client(monkeypatch):
    """
    Pytest fixture that provides a TestClient with an isolated in-memory database.

    monkeypatch temporarily replaces SessionLocal with TestingSessionLocal in the tasks_router module.

    Upon completion of a test, the test database tables are dropped, and monkeypatch restores SessionLocal.    
    """

    Base.metadata.create_all(bind=test_engine)  # Create tables in the test database

    def override_get_db():  # Yield a test session to the endpoints
        
        db = TestingSessionLocal()

        try:
            yield db

        finally:
            db.close()  # Close the test database session after the request

    app.dependency_overrides[get_db] = override_get_db  # Override use of get_db in favor of override_get_db (utilizes test session and test database)

    monkeypatch.setattr(
        tasks_router,
        "SessionLocal",
        TestingSessionLocal
    )

    try: 
        with TestClient(app) as test_client:  # TestClient makes HTTP requests in-process, without running the server

            yield test_client

    finally:
        app.dependency_overrides.pop(get_db, None)  # Remove the dependency override
        Base.metadata.drop_all(bind=test_engine)  # Drop tables from the test database once the test is complete
        
        test_engine.dispose()  # Close the engine's database connections


# ================
# TESTING FIXTURES
# ================


@pytest.fixture(autouse=True)
def disable_rate_limiting():
    """Disables rate limiting for the purpose and duration of testing."""

    limiter.enabled = False
    yield
    limiter.enabled = True


@pytest.fixture
def db_session(client):
    """Provides a session that enables querying the test database."""

    db = TestingSessionLocal()

    try:
        yield db

    finally:
        db.close()


@pytest.fixture
def sample_user(client):
    """Creates and returns a sample user for tests that require existing data."""

    response = client.post("/auth/register", json={
        "username": "test_username",
        "email": "sample_email@test.com",
        "password": "test_password"
    })

    return response.json()


@pytest.fixture
def sample_admin_user(client, db_session):
    """Creates and returns a sample admin user for testing admin-only endpoints."""

    sample_admin = User(
        username = "admin_one",
        email = "test_email@test.com",
        hashed_password = hash_password(settings.ADMIN_PASSWORD),
        is_admin = True
    )

    db_session.add(sample_admin)
    db_session.commit()
    db_session.refresh(sample_admin)

    return sample_admin


@pytest.fixture
def sample_auth_headers(sample_user):
    """Creates and returns a sample token for tests that require authentication; to be used with a sample standard user."""

    token = create_access_token(data={
        "sub": sample_user["username"]
    })

    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_admin_auth_headers(sample_admin_user):
    """Creates and returns a sample token for tests that require authentication; to be used with a sample admin user."""

    token = create_access_token(data={
        "sub": sample_admin_user.username
    })

    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def deactivated_user(client, sample_auth_headers, sample_user):
    """Creates and returns a deactivated user for use with tests that require authentication."""

    client.delete("/users/me", headers=sample_auth_headers)

    return sample_user


@pytest.fixture
def sample_task(client, sample_auth_headers):
    """Creates and returns a sample task for tests that require existing data; to be used with a sample standard user."""

    response = client.post(
        "/tasks", 
        headers = sample_auth_headers,
        json={
            "title": "Test Title"        
    })

    return response.json()

@pytest.fixture
def sample_admin_task(client, sample_admin_auth_headers):
    """Creates and returns a sample task for tests that require existing data; to be used with an sample admin user."""

    response = client.post(
        "/tasks", 
        headers = sample_admin_auth_headers,
        json={
            "title": "Admin Test Title"        
    })

    return response.json()