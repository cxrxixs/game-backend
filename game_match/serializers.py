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
    player_id = serializers.CharField(source="match_player.player_id", required=False)
    game_round_id = serializers.PrimaryKeyRelatedField(queryset=GameRound.objects.all(), source="game_round")
    is_host = serializers.SerializerMethodField(read_only=True)
    round_index = serializers.IntegerField(source="game_round.round_index", read_only=True)
    question_content = serializers.CharField(source="game_round.question_content", read_only=True)

    class Meta:
        model = PlayerAnswer
        fields = [
            "id",
            "created_at",
            "player_id",
            "game_round_id",
            "answer_index",
            "answer",
            "time",
            "round_index",
            "question_content",
            "is_host",
        ]
        extra_kwargs = {
            "answer_index": {"required": True},
            "answer": {"required": True},
            "time": {"required": True},
        }

    def get_is_host(self, obj):
        return str(obj.match_player.player_id) == str(obj.game_round.game_match.host_id)

    def create(self, validated_data):
        match_player_data = validated_data.pop("match_player", {})
        player_id_value = match_player_data.get("player_id")

        if not player_id_value:
            raise serializers.ValidationError({"player_id": "This field is required."})

        game_round = validated_data.get("game_round")
        if not game_round:
            raise serializers.ValidationError({"game_round": "This field is required."})

        try:
            match_player_obj = GameMatchPlayer.objects.get(player_id=player_id_value, game_match=game_round.game_match)

        except GameMatchPlayer.DoesNotExist:
            raise serializers.ValidationError({"player_id": "No matching player found for this match."})

        except GameMatchPlayer.MultipleObjectsReturned:
            raise serializers.ValidationError({"player_id": "Multiple players found for this ID in the match."})

        validated_data["match_player"] = match_player_obj

        game_round = validated_data.get("game_round")
        if game_round:
            if match_player_obj.game_match != game_round.game_match:
                raise serializers.ValidationError({
                    "player_id": "The specified player must be part of the same match as the game round."
                })
            if game_round.game_match.status != game_round.game_match.Status.ONGOING:
                raise serializers.ValidationError({"match_id": "Match is already closed."})

        return super().create(validated_data)


class AddPlayerSerializer(serializers.Serializer):
    player_id = serializers.CharField(required=True)


class GameRoundSerializer(serializers.ModelSerializer):
    answers = PlayerAnswerSerializer(many=True, read_only=True)
    match_id = serializers.PrimaryKeyRelatedField(queryset=GameMatch.objects.all(), source="game_match")

    class Meta:
        model = GameRound
        fields = (
            "id",
            "created_at",
            "match_id",
            "round_index",
            "question_content",
            "answers",
        )
        read_only_fields = ("round_index",)

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
        extra_kwargs = {
            "status": {
                # "required": False,
                "allow_null": True,
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields["host_id"].read_only = True
            self.fields["player_id"] = serializers.CharField(write_only=True, required=False)

    def create(self, validated_data):
        if validated_data.get("status") is None:
            validated_data["status"] = GameMatch.Status.ONGOING
        return super().create(validated_data)
