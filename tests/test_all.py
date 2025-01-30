import pytest
from fastapi import status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from unittest.mock import patch
from faker import Faker

from app.database import Base, get_db
from app.main import app
from app.models import User, Post
import app.utils as utils
from app.oauth2 import create_access_token
from app.rabbitmq_producer import send_post_notification
from app.config import settings

faker = Faker()

# Test Database Connection


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    """Creates and cleans up the test database."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    """Creates a FastAPI test client using the test database."""
    app.dependency_overrides[get_db] = lambda: db
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def test_user(db):
    """Creates a test user in the database."""
    user = User(email=faker.email(), password=utils.hash("testpassword"))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def auth_header(test_user):
    """Generates authentication token for the test user."""
    token = create_access_token(data={"user_id": test_user.id})
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def test_post(db, test_user):
    """Creates a test post in the database."""
    db.refresh(test_user)
    post = Post(title=faker.sentence(), content=faker.text(), owner_id=test_user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@pytest.fixture
def mock_rabbitmq():
    """Mocks RabbitMQ to prevent actual connection issues."""
    with patch("app.rabbitmq_producer.pika.BlockingConnection") as mock_connection:
        yield mock_connection

# ------------------ TESTS ------------------

def test_login_success(client, test_user):
    """Test successful login."""
    response = client.post(
        "/login",
        data={"username": test_user.email, "password": "testpassword"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()

# def test_login_invalid_password(client, test_user):
#     """Test login failure with incorrect password."""
#     response = client.post(
#         "/login",
#         data={"username": test_user.email, "password": "wrong"}
#     )
#     assert response.status_code == status.HTTP_403_FORBIDDEN

def test_create_post(client, auth_header, mock_rabbitmq):
    """Test creating a new post."""
    post_data = {"title": "New Post", "content": "Content"}
    response = client.post("/posts/", json=post_data, headers=auth_header)
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["title"] == "New Post"

    # Ensure RabbitMQ notification was sent
    mock_rabbitmq.assert_called_once()

def test_get_post(client, test_post, auth_header):
    """Test retrieving a post by ID."""
    response = client.get(f"/posts/{test_post.id}", headers=auth_header)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == test_post.title

def test_delete_post(client, test_post, auth_header):
    """Test deleting a post."""
    response = client.delete(f"/posts/{test_post.id}", headers=auth_header)
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_create_user(client):
    """Test creating a new user."""
    user_data = {"email": "test@example.com", "password": "testpassword"}
    response = client.post("/users/", json=user_data)
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["email"] == "test@example.com"

def test_get_user(client, test_user):
    """Test retrieving user by ID."""
    response = client.get(f"/users/{test_user.id}")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == test_user.email

def test_send_post_notification(mock_rabbitmq):
    """Test RabbitMQ producer function."""
    send_post_notification("Test Message")
    mock_rabbitmq.assert_called_once()
