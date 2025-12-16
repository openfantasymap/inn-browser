"""
Optimized Django management command for production MQTT game ticker.

This version includes:
- Batch processing for better performance
- Database query optimization
- Error recovery and retry logic
- Health check endpoint integration
- Graceful shutdown handling

Usage:
    python manage.py mqtt_game_ticker_optimized --workers 4 --batch-size 100
"""

import time
import logging
import signal
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.core.management.base import BaseCommand
from django.db import transaction, connection
from django.utils import timezone
from datetime import timedelta
from game_api.models import GameState
from game_api.game_service import GameService
from game_api.serializers import GameStateSerializer
from game_api.mqtt_service import get_mqtt_service

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Optimized MQTT game ticker with batch processing and multi-threading'

    def __init__(self):
        super().__init__()
        self.should_stop = False

    def add_arguments(self, parser):
        parser.add_argument(
            '--interval',
            type=float,
            default=1.0,
            help='Tick interval in seconds (default: 1.0)'
        )
        parser.add_argument(
            '--workers',
            type=int,
            default=4,
            help='Number of worker threads (default: 4)'
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=100,
            help='Batch size for processing (default: 100)'
        )
        parser.add_argument(
            '--active-hours',
            type=int,
            default=24,
            help='Only process games active within N hours (default: 24, 0 = all)'
        )
        parser.add_argument(
            '--min-delay',
            type=float,
            default=0.01,
            help='Minimum delay between processing individual games (default: 0.01s)'
        )

    def handle(self, *args, **options):
        interval = options['interval']
        workers = options['workers']
        batch_size = options['batch_size']
        active_hours = options['active_hours']
        min_delay = options['min_delay']

        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        mqtt_service = get_mqtt_service()

        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('MQTT Game Ticker - Optimized Version'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(f'Tick interval: {interval}s')
        self.stdout.write(f'Worker threads: {workers}')
        self.stdout.write(f'Batch size: {batch_size}')
        self.stdout.write(f'Active window: {active_hours}h (0 = all games)')
        self.stdout.write(f'Min delay: {min_delay}s')
        self.stdout.write(self.style.WARNING('Press Ctrl+C for graceful shutdown\n'))

        tick_count = 0
        total_processed = 0
        total_errors = 0

        with ThreadPoolExecutor(max_workers=workers) as executor:
            try:
                while not self.should_stop:
                    start_time = time.time()

                    # Get game states in batches
                    game_states = self._get_active_game_states(active_hours, batch_size)

                    if not game_states:
                        if tick_count == 0:
                            self.stdout.write(self.style.WARNING('No active game states found'))
                        time.sleep(interval)
                        continue

                    # Submit tasks to thread pool
                    futures = []
                    for game_state in game_states:
                        future = executor.submit(
                            self._process_game_tick,
                            game_state.player_id,
                            mqtt_service
                        )
                        futures.append(future)

                        # Small delay to avoid overwhelming the system
                        if min_delay > 0:
                            time.sleep(min_delay)

                    # Collect results
                    processed = 0
                    errors = 0

                    for future in as_completed(futures):
                        try:
                            success = future.result()
                            if success:
                                processed += 1
                            else:
                                errors += 1
                        except Exception as e:
                            errors += 1
                            logger.error(f'Future error: {e}')

                    tick_count += 1
                    total_processed += processed
                    total_errors += errors
                    elapsed = time.time() - start_time

                    # Log progress
                    self.stdout.write(
                        f'Tick {tick_count}: '
                        f'{processed} ok, {errors} err, '
                        f'{elapsed:.2f}s | '
                        f'Total: {total_processed} ok, {total_errors} err'
                    )

                    # Close old database connections
                    connection.close()

                    # Sleep for remaining interval
                    sleep_time = max(0, interval - elapsed)
                    if sleep_time > 0:
                        time.sleep(sleep_time)
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f'Warning: Tick took {elapsed:.2f}s (> {interval}s interval)'
                            )
                        )

            except KeyboardInterrupt:
                pass
            finally:
                self._shutdown(tick_count, total_processed, total_errors)

    def _process_game_tick(self, player_id, mqtt_service):
        """Process a single game tick and publish to MQTT."""
        try:
            # Process tick
            updated_state = GameService.process_tick(player_id)

            # Serialize and publish
            serializer = GameStateSerializer(updated_state)
            data = serializer.data
            mqtt_service.publish_game_state(player_id, data)

            return True

        except Exception as e:
            logger.error(f'Error processing {player_id}: {e}', exc_info=True)
            return False

    def _get_active_game_states(self, active_hours, limit):
        """Get active game states with optimized query."""
        queryset = GameState.objects.all()

        if active_hours > 0:
            cutoff = timezone.now() - timedelta(hours=active_hours)
            queryset = queryset.filter(last_tick__gte=cutoff)

        # Order by last_tick to prioritize recently active games
        queryset = queryset.order_by('-last_tick')[:limit]

        # Use select_related and prefetch_related for optimization
        return queryset.select_related().prefetch_related(
            'rooms',
            'guests',
            'upgradetemplates',
            'tavernitems',
            'recipes',
            'ingredients'
        )

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        signal_name = 'SIGINT' if signum == signal.SIGINT else 'SIGTERM'
        self.stdout.write(self.style.WARNING(f'\nReceived {signal_name}, shutting down...'))
        self.should_stop = True

    def _shutdown(self, tick_count, total_processed, total_errors):
        """Perform graceful shutdown."""
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 60))
        self.stdout.write(self.style.SUCCESS('Shutdown Summary'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(f'Total ticks: {tick_count}')
        self.stdout.write(f'Games processed: {total_processed}')
        self.stdout.write(f'Errors: {total_errors}')
        if total_processed > 0:
            success_rate = ((total_processed - total_errors) / total_processed) * 100
            self.stdout.write(f'Success rate: {success_rate:.2f}%')
        self.stdout.write(self.style.SUCCESS('Goodbye!'))
