import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestApi:
    def test_get_request_response_200(self, client):
        url = reverse("api-questions")
        response = client.get(url)

        assert response.status_code == 200

    def test_response_content(self, client):
        url = reverse("api-questions")
        response = client.get(url)

        data = response.json()
        assert len(data) == 2
