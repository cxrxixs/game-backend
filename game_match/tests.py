import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from game_match.models import GameMatch, GameMatchPlayer, GameRound


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_match(db):
    # Create and return a GameMatch instance for testing
    return GameMatch.objects.create(host_id="host1")


@pytest.fixture
def create_round(db, create_match):
    """Creates a GameRound instance associated with a GameMatch."""
    match = create_match
    return GameRound.objects.create(game_match=match, question_content="What is the capital of France?")


@pytest.mark.django_db
def test_create_game_match(api_client):
    PLAYER = "host1"
    payload = {"host_id": PLAYER}
    url = reverse("match-list")

    response = api_client.post(url, payload, format="json")
    data = response.data

    assert response.status_code == status.HTTP_201_CREATED
    assert data["players"][0]["player_id"] == PLAYER
    assert data["players"][0]["is_host"]


@pytest.mark.django_db
def test_get_game_match_list(api_client, create_match):
    url = reverse("match-list")
    response = api_client.get(url)
    data = response.data
    assert response.status_code == status.HTTP_200_OK
    assert any(match["match_id"] == str(create_match.match_id) for match in data)
    assert data[0]["players"][0]["is_host"]


@pytest.mark.django_db
def test_game_match_add_user(api_client, create_match):
    match_id = str(create_match.match_id)
    PLAYER_2 = "player_2"
    payload = {"player_id": PLAYER_2}
    url = reverse("match-add-player-action", kwargs={"pk": match_id})

    response = api_client.post(url, payload)
    data = response.data

    assert response.status_code == status.HTTP_201_CREATED
    assert data.get("player_id") == PLAYER_2
    assert data.get("is_host") == GameMatchPlayer.objects.get(player_id=PLAYER_2).is_host


@pytest.mark.django_db
def test_game_match_create_round(api_client, create_match):
    match_id = create_match.match_id
    url = reverse("round-list")
    payload = {"match_id": match_id, "question_content": "Test question"}

    response = api_client.post(url, payload)
    data = response.data

    assert response.status_code == status.HTTP_201_CREATED
    assert data.get("match_id") == match_id
    assert data.get("round_index") == 0
    assert data.get("answers") == []
    assert data.get("question_content") == "Test question"


@pytest.mark.django_db
def test_game_match_create_answer(api_client, create_match, create_round):
    player_id = create_match.host_id
    game_round_id = create_round.id
    url = reverse("answer-list")
    ANSWER_INDEX = 3
    ANSWER = "Paris"
    TIME_DURATION = 24.51

    payload = {
        "player_id": player_id,
        "game_round_id": game_round_id,
        "answer_index": ANSWER_INDEX,
        "answer": ANSWER,
        "time": TIME_DURATION,
    }

    response = api_client.post(url, payload)
    data = response.data

    assert response.status_code == status.HTTP_201_CREATED
    assert data.get("player_id") == player_id
    assert data.get("is_host") == GameMatchPlayer.objects.get(game_match=create_round.game_match).is_host
    assert data.get("game_round_id") == game_round_id
    assert data.get("round_index") == create_round.round_index
    assert data.get("question_content") == create_round.question_content
    assert data.get("answer_index") == ANSWER_INDEX
    assert data.get("answer") == ANSWER
    assert data.get("time") == TIME_DURATION
