import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestHelloWorld:
    """Test cases for Hello World views"""

    @pytest.mark.skip(reason="TDD tests are currently disabled")
    def test_hello_world_view(self, client):
        """Test the hello_world view returns correct response"""
        url = reverse('hello_world')
        response = client.get(url)
        assert response.status_code == 200
        assert b"Hello, World!" in response.content

    @pytest.mark.skip(reason="TDD tests are currently disabled")
    def test_hello_world_api(self):
        """Test the HelloWorldAPIView returns correct response"""
        client = APIClient()
        url = reverse('hello_api')
        response = client.get(url)
        assert response.status_code == 200
        assert response.data['message'] == "Hello, World!"
        assert response.data['project'] == "Steam Downgrade Python"
        assert response.data['status'] == "Running successfully"
