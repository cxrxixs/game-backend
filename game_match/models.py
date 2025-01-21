from uuid import uuid4

from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import Case, F, Max, Value, When


class GameMatch(models.Model):
    class Status(models.TextChoices):
        ONGOING = "ongoing", "Ongoing"
        EXPIRED = "expired", "Expired"
        FINISHED = "finished", "Finished"

    match_id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    host_id = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ONGOING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Match {self.match_id} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Automatically add host as player
        GameMatchPlayer.objects.get_or_create(game_match=self, player_id=self.host_id)
        return self

    @transaction.atomic
    def add_player(self, player_id):
        """Add a player to the game room, ensure only 2 players."""
        if self.players.count() >= 2:
            raise ValueError("A match can only have 2 players.")

        new_player = GameMatchPlayer.objects.create(game_match=self, player_id=player_id)
        return new_player

    @transaction.atomic
    def add_round(self, question_content):
        """
        Create a new GameRound for this match, ensuring concurrency safety
        by locking existing rounds. This prevents two simultaneous calls
        from assigning the same round_index.
        """
        # Lock the rows so no other transaction can insert or update these until we finish.
        self.rounds.select_for_update().all()
        max_round_index = self.rounds.aggregate(max_index=models.Max("round_index"))["max_index"]
        next_index = 0 if max_round_index is None else max_round_index + 1

        return self.rounds.create(round_index=next_index, question_content=question_content)


class GameMatchPlayer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    game_match = models.ForeignKey(GameMatch, on_delete=models.CASCADE, related_name="players")
    player_id = models.CharField(max_length=50)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["game_match", "player_id"], name="uq_game_match_player"),
        ]

    @property
    def is_host(self):
        return str(self.player_id) == str(self.game_match.host_id)

    def clean(self):
        super().clean()

        # Limit number of allowed players to 2
        if not self.pk:
            if self.game_match.players.count() >= 2:
                raise ValidationError("Only 2 players are allowed in the match.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Player {self.player_id} in GameMatch {self.game_match.match_id}"


class GameRound(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    game_match = models.ForeignKey(GameMatch, on_delete=models.CASCADE, related_name="rounds")
    round_index = models.PositiveIntegerField(null=True, blank=True)
    question_content = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["game_match", "round_index"], name="uq_game_round_player"),
        ]

    @transaction.atomic
    def save(self, *args, **kwargs):
        if not self.pk and self.round_index is None:
            GameRound.objects.select_for_update().filter(game_match=self.game_match)
            max_val = GameRound.objects.filter(game_match=self.game_match).aggregate(m=Max("round_index"))["m"]
            self.round_index = 0 if max_val is None else max_val + 1

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Round {self.round_index} in GameMatch {self.game_match.match_id}"


class PlayerAnswerManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                is_host_flag=Case(
                    When(match_player__player_id=F("game_round__game_match__host_id"), then=Value(True)),
                    default=Value(False),
                    output_field=models.BooleanField(),
                )
            )
            .order_by("-is_host_flag", "created_at")
        )


class PlayerAnswer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    game_round = models.ForeignKey(GameRound, on_delete=models.CASCADE, related_name="answers")
    match_player = models.ForeignKey(GameMatchPlayer, on_delete=models.CASCADE, related_name="answers")
    answer_index = models.PositiveIntegerField()
    answer = models.TextField()
    time = models.FloatField()
    # question_content = models.TextField(blank=True, null=True)  # Optional

    class Meta:
        unique_together = ("game_round", "match_player")

    def clean(self):
        super().clean()
        if self.match_player.game_match != self.game_round.game_match:
            raise ValidationError("match_player must be part of game_round.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"Answer from Player {self.match_player.player_id} "
            f"in Round {self.game_round.round_index} "
            f"of GameMatch {self.game_round.game_match.match_id}"
        )

    objects = PlayerAnswerManager()
