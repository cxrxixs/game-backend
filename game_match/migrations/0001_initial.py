# Generated by Django 4.2.17 on 2025-01-20 02:13

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GameMatch',
            fields=[
                ('match_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('host_id', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('ongoing', 'Ongoing'), ('expired', 'Expired'), ('finished', 'Finished')], default='ongoing', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='GameMatchPlayer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('player_id', models.CharField(max_length=50)),
                ('game_match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='players', to='game_match.gamematch')),
            ],
        ),
        migrations.CreateModel(
            name='GameRound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('round_index', models.PositiveIntegerField(null=True)),
                ('question_content', models.TextField()),
                ('game_match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rounds', to='game_match.gamematch')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('answer_index', models.PositiveIntegerField()),
                ('answer', models.TextField()),
                ('time', models.FloatField()),
                ('game_round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='game_match.gameround')),
                ('match_player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='game_match.gamematchplayer')),
            ],
            options={
                'unique_together': {('game_round', 'match_player')},
            },
        ),
        migrations.AddConstraint(
            model_name='gameround',
            constraint=models.UniqueConstraint(fields=('game_match', 'round_index'), name='uq_game_round_player'),
        ),
        migrations.AddConstraint(
            model_name='gamematchplayer',
            constraint=models.UniqueConstraint(fields=('game_match', 'player_id'), name='uq_game_match_player'),
        ),
    ]
