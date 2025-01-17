from uuid import uuid4

from django.db import models

import game_match


class GameMatch(models.Model):
    class Status(models.TextChoices):
        ONGOING = "ongoing", "Ongoing"
        EXPIRED = "expired", "Expired"
        FINISHED = "finished", "Finished"

    match_id = models.UUIDField(default=uuid4, editable=False, unique=True)
    host_id = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ONGOING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Match {self.match_id} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        """Automatically add host as a player in the match."""
        super().save(*args, **kwargs)
        GameMatchPlayer.objects.create(game_match=self, player_id=self.host_id)
        return self

    def add_player(self, player_id):
        """Add a player to the game room, ensure only 2 players."""
        if self.players.count() < 2:
            GameMatchPlayer.objects.create(game_match=self, player_id=player_id)
        else:
            raise ValueError("A match can only have 2 players.")


class GameMatchPlayer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    game_match = models.ForeignKey(GameMatch, on_delete=models.CASCADE, related_name="players")
    player_id = models.CharField(max_length=50)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["game_match", "player_id"], name="uq_game_match_player"),
        ]

    def __str__(self):
        return f"Player {self.player_id} in GameMatch {self.game_match.match_id}"


class GameRound(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    game_match = models.ForeignKey(GameMatch, on_delete=models.CASCADE, related_name="rounds")
    round_index = models.PositiveIntegerField()
    question_content = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["game_match", "round_index"], name="uq_game_round_player"),
        ]

    def save(self, *args, **kwargs):
        # If this is a new instance and round_index is not explicitly set
        if not self.pk and self.round_index is None:
            # Get the current highest round_index for this game_match
            max_round_index = (
                GameRound.objects.filter(game_match=self.game_match)
                .aggregate(max_index=models.Max("round_index"))
                .get("max_index")
            )
            # Increment the round index or start at 0 if no rounds exist
            self.round_index = 0 if max_round_index is None else max_round_index + 1

        # Call the original save method
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Round {self.round_index} in GameMatch {self.game_match.match_id}"


class PlayerAnswer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    game_round = models.ForeignKey(GameRound, on_delete=models.CASCADE, related_name="answers")
    player_id = models.UUIDField()
    answer_index = models.PositiveIntegerField()
    answer = models.TextField()
    time = models.FloatField()  # Time taken by the player to answer
    question_content = models.TextField(blank=True, null=True)  # Optional

    class Meta:
        unique_together = ("game_round", "player_id")

    def __str__(self):
        return f"Answer from Player {self.player_id} in Round {self.round.round_index} of GameMatch {self.round.game_match.match_id}"
