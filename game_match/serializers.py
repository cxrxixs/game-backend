from rest_framework import serializers

from .models import (
    GameMatch,
    GameMatchPlayer,
    GameRound,
    PlayerAnswer,
)


class GameMatchPlayerSerializer(serializers.ModelSerializer):
    match_id = serializers.PrimaryKeyRelatedField(
        queryset=GameMatch.objects.all(), source="game_match", label="Match ID"
    )

    is_host = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = GameMatchPlayer
        fields = [
            "id",
            "created_at",
            "player_id",
            "match_id",
            "is_host",
        ]

    def get_is_host(self, obj):
        return str(obj.player_id) == str(obj.game_match.host_id)

    def validate(self, attrs):
        game_match = attrs["game_match"]
        if game_match.players.count() >= 2:
            raise serializers.ValidationError(
                {"game_match": "Only 2 players are allowed in the match."},
            )
        if game_match.status != game_match.Status.ONGOING:
            raise serializers.ValidationError(
                {"game_match": "Match is already closed."},
            )

        return attrs


class PlayerAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerAnswer
        fields = "__all__"


class GameRoundSerializer(serializers.ModelSerializer):
    answers = PlayerAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = GameRound
        fields = "__all__"

    def validate(self, attrs):
        game_match = attrs["game_match"]
        if game_match.status != game_match.Status.ONGOING:
            raise serializers.ValidationError(
                {"game_match": "Match is already closed."},
            )

        return attrs


class GameMatchSerializer(serializers.ModelSerializer):
    players = GameMatchPlayerSerializer(many=True, read_only=True)
    rounds = GameRoundSerializer(many=True, read_only=True)

    class Meta:
        model = GameMatch
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields["host_id"].read_only = True
            self.fields["player_id"] = serializers.CharField(write_only=True, required=False)
