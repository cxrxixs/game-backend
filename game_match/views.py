from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import GameMatch, GameMatchPlayer, GameRound
from .serializers import GameMatchPlayerSerializer, GameMatchSerializer, GameRoundSerializer


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse("<h1>Game Match</h1>")


class GameMatchViewSet(viewsets.ModelViewSet):
    queryset = GameMatch.objects.all()
    serializer_class = GameMatchSerializer

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
