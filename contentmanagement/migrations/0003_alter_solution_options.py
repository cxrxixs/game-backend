# Generated by Django 4.2.17 on 2024-12-26 06:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contentmanagement', '0002_seed_data'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='solution',
            options={'ordering': ['created_at']},
        ),
    ]
