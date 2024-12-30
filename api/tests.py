import pytest
from django.urls import reverse
from rest_framework import status


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

    def test_retrieve_single_question(self, client):
        url = reverse("question-detail", kwargs={"pk": 2})
        response = client.get(url)
        data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert data["Question"] == "What is the capital of France?"
