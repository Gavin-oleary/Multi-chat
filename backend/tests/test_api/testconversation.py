import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_conversation():
    """Test creating a new conversation"""
    response = client.post(
        "/api/v1/conversations/",
        json={"title": "Test Conversation"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Conversation"
    assert "id" in data
    assert "created_at" in data


def test_list_conversations():
    """Test listing conversations"""
    response = client.get("/api/v1/conversations/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_conversation():
    """Test getting a specific conversation"""
    # First create a conversation
    create_response = client.post(
        "/api/v1/conversations/",
        json={"title": "Test Get Conversation"}
    )
    conversation_id = create_response.json()["id"]
    
    # Then retrieve it
    response = client.get(f"/api/v1/conversations/{conversation_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == conversation_id
    assert data["title"] == "Test Get Conversation"
    assert "messages" in data


def test_update_conversation():
    """Test updating a conversation"""
    # Create a conversation
    create_response = client.post(
        "/api/v1/conversations/",
        json={"title": "Original Title"}
    )
    conversation_id = create_response.json()["id"]
    
    # Update it
    response = client.patch(
        f"/api/v1/conversations/{conversation_id}",
        json={"title": "Updated Title"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"


def test_delete_conversation():
    """Test deleting a conversation"""
    # Create a conversation
    create_response = client.post(
        "/api/v1/conversations/",
        json={"title": "To Be Deleted"}
    )
    conversation_id = create_response.json()["id"]
    
    # Delete it
    response = client.delete(f"/api/v1/conversations/{conversation_id}")
    assert response.status_code == 200
    
    # Verify it's gone
    get_response = client.get(f"/api/v1/conversations/{conversation_id}")
    assert get_response.status_code == 404