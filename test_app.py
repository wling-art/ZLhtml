import pytest
from app import app
import time


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert "钟乐 - 创意无限 创新无极限".encode('utf-8') in response.data


def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert "登录至 ZLServer".encode('utf-8') in response.data


def test_invalid_route(client):
    response = client.get('/invalid-route')
    assert response.status_code == 404