from django.core.exceptions import ValidationError
from django.db.models import BooleanField, Case, F, Value, When
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import GameMatch, GameMatchPlayer, GameRound, PlayerAnswer
from .serializers import (
    AddPlayerSerializer,
    GameMatchPlayerSerializer,
    GameMatchSerializer,
    GameRoundSerializer,
    PlayerAnswerSerializer,
)


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse("<h1>Game Match</h1>")


class GameMatchViewSet(viewsets.ModelViewSet):
    queryset = GameMatch.objects.all()
    serializer_class = GameMatchSerializer

    @action(
        detail=True,
        methods=["get", "post"],
        url_path="player",
        serializer_class=AddPlayerSerializer,
    )
    def add_player_action(self, request, pk=None):
        match = self.get_object()

        if request.method == "GET":
            players = match.players.all()
            serializer = GameMatchPlayerSerializer(players, many=True, context=self.get_serializer_context())
            return Response(serializer.data)

        # Use the AddPlayerSerializer to validate input
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        player_id = serializer.validated_data["player_id"]

        try:
            new_player = match.add_player(player_id)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize the newly created GameMatchPlayer record with its serializer
        player_serializer = GameMatchPlayerSerializer(new_player, context=self.get_serializer_context())
        return Response(player_serializer.data, status=201)

    @action(detail=False, methods=["get"], url_path="ongoing")
    def ongoing_matches(self, request):
        """
        Custom endpoint: GET /gamematch/ongoing/?player_id=<player_id>
        Returns matches that are Ongoing and include this player_id.
        """
        player_id = request.query_params.get("player_id")
        if not player_id:
            return Response({"error": "player_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.filter_queryset(self.get_queryset()).filter(
            status=GameMatch.Status.ONGOING, players__player_id=player_id
        )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="finished")
    def finished_matches(self, request):
        """
        Custom endpoint: GET /gamematch/finished/?player_id=<player_id>
        Returns matches that are Finished and include this player_id.
        """
        player_id = request.query_params.get("player_id")
        if not player_id:
            return Response({"error": "player_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.filter_queryset(self.get_queryset()).filter(
            status=GameMatch.Status.FINISHED, players__player_id=player_id
        )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="expired")
    def expired_matches(self, request):
        """
        Custom endpoint: GET /gamematch/expired/?player_id=<player_id>
        Returns matches that are Finished and include this player_id.
        """
        player_id = request.query_params.get("player_id")
        if not player_id:
            return Response({"error": "player_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.filter_queryset(self.get_queryset()).filter(
            status=GameMatch.Status.EXPIRED, players__player_id=player_id
        )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)  # Support for PATCH vs. PUT
        instance = self.get_object()

        # Extract and validate player_id from request data
        player_id = request.data.get("player_id")
        if not player_id:
            return Response({"detail": "player_id is required in the payload."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the provided player_id is part of this match
        if not instance.players.filter(player_id=player_id).exists():
            return Response(
                {"detail": "The specified player is not part of this match."}, status=status.HTTP_403_FORBIDDEN
            )

        # Restrict updates to only the 'status' field
        data = request.data.copy()

        # Only allow 'status' field to be updated
        allowed_fields = {"status"}
        # Filter out any disallowed fields
        data = {key: value for key, value in data.items() if key in allowed_fields}

        # Proceed with update using the sanitized data
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_update(serializer)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)


class GameMatchPlayerViewSet(viewsets.ModelViewSet):
    queryset = GameMatchPlayer.objects.all()
    serializer_class = GameMatchPlayerSerializer


class GameRoundViewSet(viewsets.ModelViewSet):
    queryset = GameRound.objects.all()
    serializer_class = GameRoundSerializer


class PlayerAnswerViewSet(viewsets.ModelViewSet):
    queryset = (
        PlayerAnswer.objects.all()
        .annotate(
            is_host_flag=Case(
                When(match_player__player_id=F("game_round__game_match__host_id"), then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            )
        )
        .order_by("-is_host_flag")
    )
    serializer_class = PlayerAnswerSerializer
