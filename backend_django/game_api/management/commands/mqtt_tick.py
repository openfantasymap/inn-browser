"""
Management command to initialize room and upgrade templates
"""
from django.core.management.base import BaseCommand
from game_api.models import RoomTypeTemplate, UpgradeTemplate
from game_api.views import * 

import time

class Command(BaseCommand):
    help = 'Initialize room type and upgrade templates'

    def handle(self, *args, **options):
        self.stdout.write('Initializing room and upgrade templates...')
        while True:
            for gs in GameState.objects.all():
                serialize_and_publish(gs, gs.player_id)

            time.sleep(3)



            