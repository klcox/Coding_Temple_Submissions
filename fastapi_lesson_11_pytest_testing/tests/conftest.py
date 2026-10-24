import pytest
from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app


TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool  # Ensures that the same connection is reused (required for :memory: databases)
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture
def client():
    """Pytest fixture that provides a TestClient with an isolated in-memory DB."""

    Base.metadata.create_all(bind=test_engine)  # Create tables in the test DB

    def override_get_db():  # Yield a test session to the endpoints
        
        db = TestingSessionLocal()

        try:
            yield db

        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db  # Override use of get_db in favor of override_get_db (utilizes test session and test DB)

    yield TestClient(app)  # TestClient makes HTTP requests in-process, without running the server

    Base.metadata.drop_all(bind=test_engine)  # Drop tables from the test DB
    
    app.dependency_overrides.clear()  # Remove the override


@pytest.fixture
def sample_task(client):
    """Create and return a sample task for tests that need existing data."""

    response = client.post("/tasks", json={
        "title": "Test Title",
        "completed": False
    })

    return response.json()