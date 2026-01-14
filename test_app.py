"""
Unit tests for the Hello World Flask application
"""

import pytest
from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_hello_endpoint(client):
    """Test the main hello endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert 'Hello World' in data['message']
    assert 'version' in data
    assert 'hostname' in data
    assert 'timestamp' in data

def test_health_endpoint(client):
    """Test the health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'version' in data

def test_ready_endpoint(client):
    """Test the readiness check endpoint"""
    response = client.get('/ready')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ready'
    assert 'version' in data

def test_info_endpoint(client):
    """Test the info endpoint"""
    response = client.get('/info')
    assert response.status_code == 200
    data = response.get_json()
    assert data['application'] == 'NAB POC Python Hello World'
    assert 'version' in data
    assert 'hostname' in data
    assert 'port' in data
    assert 'environment' in data
    assert 'timestamp' in data

