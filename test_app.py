import pytest

from app import app


@pytest.fixture
def client():  # 定义用于测试的客户端
    """定义用于测试的客户端"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    """测试主页"""
    response = client.get('/')
    assert response.status_code == 200
    assert "钟乐 - 创意无限 创新无极限".encode('utf-8') in response.data


def test_login_page(client):
    """测试登录页面"""
    response = client.get('/login')
    assert response.status_code == 200
    assert "登录至 ZLServer".encode('utf-8') in response.data


def test_invalid_route(client):
    """测试无效路由"""
    response = client.get('/invalid-route')
    assert response.status_code == 404
