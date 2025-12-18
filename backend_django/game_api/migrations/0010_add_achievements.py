# Generated manually

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game_api', '0009_add_operational_cost_to_upgrades'),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('achievement_id', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('requirement_type', models.CharField(max_length=50)),
                ('requirement_value', models.IntegerField(default=0)),
                ('requirement_metadata', models.JSONField(blank=True, default=dict)),
                ('icon', models.CharField(default='🏆', max_length=10)),
                ('reward_upgrade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='unlocked_by_achievement', to='game_api.upgradetemplate')),
            ],
            options={
                'verbose_name': 'Achievement',
                'verbose_name_plural': 'Achievements',
                'ordering': ['requirement_value'],
            },
        ),
        migrations.CreateModel(
            name='PlayerAchievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('earned_at', models.DateTimeField(auto_now_add=True)),
                ('progress', models.IntegerField(default=0)),
                ('achievement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game_api.achievement')),
                ('game_state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='achievements', to='game_api.gamestate')),
            ],
            options={
                'verbose_name': 'Player Achievement',
                'verbose_name_plural': 'Player Achievements',
                'unique_together': {('game_state', 'achievement')},
            },
        ),
    ]
