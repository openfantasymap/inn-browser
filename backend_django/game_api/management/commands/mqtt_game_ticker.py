"""
Django management command to continuously process game ticks and publish MQTT updates.

Usage:
    python manage.py mqtt_game_ticker

This command runs indefinitely, processing game ticks for all active game states
every second and publishing updates via MQTT.

Press Ctrl+C to stop.
"""

import time
import logging
from django.core.management.base import BaseCommand
from django.db import transaction
from game_api.models import GameState
from game_api.game_service import GameService
from game_api.serializers import GameStateSerializer
from game_api.mqtt_service import get_mqtt_service

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Continuously process game ticks and publish MQTT updates for all game states'

    def add_arguments(self, parser):
        parser.add_argument(
            '--interval',
            type=float,
            default=1.0,
            help='Tick interval in seconds (default: 1.0)'
        )
        parser.add_argument(
            '--active-only',
            action='store_true',
            help='Only process game states active in the last 24 hours'
        )
        parser.add_argument(
            '--player-id',
            type=str,
            help='Process only a specific player ID'
        )

    def handle(self, *args, **options):
        interval = options['interval']
        active_only = options['active_only']
        player_id = options['player_id']


        self.stdout.write(self.style.SUCCESS(f'Starting MQTT game ticker (interval: {interval}s)'))

        if player_id:
            self.stdout.write(f'Processing only player: {player_id}')
        elif active_only:
            self.stdout.write('Processing only active game states (24h)')
        else:
            self.stdout.write('Processing all game states')

        self.stdout.write(self.style.WARNING('Press Ctrl+C to stop\n'))

        tick_count = 0

        try:
            while True:
                start_time = time.time()

                # Get game states to process
                game_states = self._get_game_states(player_id, active_only)

                if not game_states:
                    if tick_count == 0:
                        self.stdout.write(self.style.WARNING('No game states found'))
                    time.sleep(interval)
                    continue

                # Process each game state
                processed = 0
                errors = 0

                for game_state in game_states:
                    try:
                        # Process tick for this game state
                        updated_state = GameService.process_tick(game_state.player_id)

                        mqtt_service = get_mqtt_service()

                        # Optimize queryset to avoid N+1 queries - refresh with prefetch_related
                        updated_state = GameState.objects.prefetch_related(
                            'rooms',
                            'guests',
                            #'player_recipes__item',
                            'purchased_upgrades__upgrade_template',
                            'active_buffs__upgrade_template'
                        ).get(player_id=game_state.player_id)

                        # Serialize and publish via MQTT
                        serializer = GameStateSerializer(updated_state)
                        data = serializer.data
                        mqtt_service.publish_game_state(game_state.player_id, data)

                        processed += 1

                    except Exception as e:
                        errors += 1
                        logger.error(f'Error processing tick for player {game_state.player_id}: {e}')

                tick_count += 1
                elapsed = time.time() - start_time

                # Log progress every 10 ticks
                if tick_count % 10 == 0:
                    self.stdout.write(
                        f'Tick {tick_count}: Processed {processed} games, '
                        f'{errors} errors, {elapsed:.3f}s elapsed'
                    )

                # Sleep for remaining time to maintain interval
                sleep_time = max(0, interval - elapsed)
                if sleep_time > 0:
                    time.sleep(sleep_time)
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Tick {tick_count}: Processing took {elapsed:.3f}s '
                            f'(longer than interval {interval}s)'
                        )
                    )

        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS(f'\nStopping after {tick_count} ticks'))
            self.stdout.write('Goodbye!')

    def _get_game_states(self, player_id, active_only):
        """Get game states to process based on filters."""
        from django.utils import timezone
        from datetime import timedelta

        queryset = GameState.objects.all()

        if player_id:
            queryset = queryset.filter(player_id=player_id)
        elif active_only:
            # Only process games with activity in last 24 hours
            cutoff = timezone.now() - timedelta(hours=24)
            queryset = queryset.filter(last_tick__gte=cutoff)

        return queryset.prefetch_related(
            'rooms',
            'guests',
            #'player_recipes__item',
            'purchased_upgrades__upgrade_template',
            'active_buffs__upgrade_template'
        )
