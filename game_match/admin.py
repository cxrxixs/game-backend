from django.contrib import admin

from .models import GameMatch, GameMatchPlayer, GameRound, PlayerAnswer

admin.site.register(GameMatch)
admin.site.register(GameMatchPlayer)
admin.site.register(GameRound)
admin.site.register(PlayerAnswer)
