from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    grade_level = models.IntegerField(
        validators=[MaxValueValidator(12)],
        null=True,
        blank=True,
    )
    latest_score = models.IntegerField(
        validators=[MaxValueValidator(1600)],
        null=True,
        blank=True,
    )
    high_score = models.IntegerField(
        validators=[MaxValueValidator(1600)],
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.user.username}'s profile"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
