import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test the home page loads successfully"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Flask' in response.data or b'Hello' in response.data

def test_health_endpoint(client):
    """Test health check endpoint if exists"""
    response = client.get('/health')
    # Adjust based on your app's endpoints
    assert response.status_code in [200, 404]
