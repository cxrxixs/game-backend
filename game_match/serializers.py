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
                {
                    "game_match": "Only 2 players are allowed in the match.",
                },
            )
        if game_match.status != game_match.Status.ONGOING:
            raise serializers.ValidationError(
                {
                    "game_match": "Match is already closed.",
                },
            )

        return attrs


class PlayerAnswerSerializer(serializers.ModelSerializer):
    player_id = serializers.CharField(source="match_player.player_id", read_only=True)
    is_host = serializers.SerializerMethodField(read_only=True)
    round_index = serializers.IntegerField(source="game_round.round_index", read_only=True)

    class Meta:
        model = PlayerAnswer
        fields = "__all__"
        extra_kwargs = {
            "answer_index": {
                "required": True,
            },
            "answer": {
                "required": True,
            },
            "time": {
                "required": True,
            },
        }

    def get_is_host(self, obj):
        return str(obj.match_player.player_id) == str(obj.game_round.game_match.host_id)

    def validate(self, attrs):
        game_round = attrs.get("game_round", getattr(self.instance, "game_round", None))
        match_player = attrs.get("match_player", getattr(self.instance, "match_player", None))

        if game_round and match_player:
            if match_player.game_match != game_round.game_match:
                raise serializers.ValidationError(
                    {
                        "game_match": "The match_player must be part of the same match as the game_round.",
                    },
                )
            if game_round.game_match.status != game_round.game_match.Status.ONGOING:
                raise serializers.ValidationError(
                    {
                        "game_match": "Match is already closed.",
                    },
                )

        return attrs


class AddPlayerSerializer(serializers.Serializer):
    player_id = serializers.CharField(required=True)


class GameRoundSerializer(serializers.ModelSerializer):
    answers = PlayerAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = GameRound
        fields = "__all__"

    def validate(self, attrs):
        game_match = attrs["game_match"]
        if game_match.status != game_match.Status.ONGOING:
            raise serializers.ValidationError(
                {
                    "game_match": "Match is already closed.",
                },
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
