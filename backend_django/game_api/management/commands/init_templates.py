"""
Management command to initialize room and upgrade templates
"""
from django.core.management.base import BaseCommand
from game_api.models import RoomTypeTemplate, UpgradeTemplate


class Command(BaseCommand):
    help = 'Initialize room type and upgrade templates'

    def handle(self, *args, **options):
        self.stdout.write('Initializing room and upgrade templates...')

        # Clear existing templates
        RoomTypeTemplate.objects.all().delete()
        UpgradeTemplate.objects.all().delete()

        # Create room type templates
        self._create_room_templates()

        # Create upgrade templates
        self._create_upgrade_templates()

        self.stdout.write(self.style.SUCCESS('Templates initialized successfully!'))

    def _create_room_templates(self):
        """Create all room type templates"""
        room_templates = [
            {
                'room_type_id': 'basic',
                'name': 'Basic Room',
                'description': 'Simple room with basic amenities',
                'base_cost': 50.0,
                'income_multiplier': 1.0,
                'emoji': '🛏️'
            },
            {
                'room_type_id': 'standard',
                'name': 'Standard Room',
                'description': 'Comfortable room with better furnishings',
                'base_cost': 200.0,
                'income_multiplier': 2.0,
                'emoji': '🏠'
            },
            {
                'room_type_id': 'deluxe',
                'name': 'Deluxe Room',
                'description': 'Luxurious room with premium amenities',
                'base_cost': 500.0,
                'income_multiplier': 4.0,
                'emoji': '🏰'
            },
            {
                'room_type_id': 'royal',
                'name': 'Royal Suite',
                'description': 'Opulent suite fit for royalty',
                'base_cost': 1000.0,
                'income_multiplier': 8.0,
                'emoji': '👑'
            },
        ]

        for room_data in room_templates:
            RoomTypeTemplate.objects.create(**room_data)
            self.stdout.write(f'  Created: {room_data["emoji"]} {room_data["name"]}')

    def _create_upgrade_templates(self):
        """Create all upgrade templates"""
        upgrade_templates = [
            {
                'upgrade_id': 'upgrade_income_1',
                'name': 'Better Beds',
                'description': 'Increase income from all rooms by 50%',
                'cost': 200.0,
                'effect_type': 'income_multiplier',
                'effect_value': 1.5
            },
            {
                'upgrade_id': 'upgrade_auto_clean',
                'name': 'Hire Cleaning Staff',
                'description': 'Automatically clean rooms over time',
                'cost': 300.0,
                'effect_type': 'auto_clean',
                'effect_value': 1.0
            },
            {
                'upgrade_id': 'upgrade_capacity_1',
                'name': 'Expand Inn',
                'description': 'Increase max guest capacity by 5',
                'cost': 400.0,
                'effect_type': 'guest_capacity',
                'effect_value': 5.0
            },
            {
                'upgrade_id': 'upgrade_room_standard',
                'name': 'Unlock Standard Rooms',
                'description': 'Unlock the ability to build Standard rooms (2x income)',
                'cost': 500.0,
                'effect_type': 'unlock_room',
                'effect_value': 2.0
            },
            {
                'upgrade_id': 'upgrade_income_2',
                'name': 'Luxury Furnishings',
                'description': 'Increase income from all rooms by 100%',
                'cost': 1000.0,
                'effect_type': 'income_multiplier',
                'effect_value': 2.0
            },
            {
                'upgrade_id': 'upgrade_room_deluxe',
                'name': 'Unlock Deluxe Rooms',
                'description': 'Unlock the ability to build Deluxe rooms (4x income)',
                'cost': 2000.0,
                'effect_type': 'unlock_room',
                'effect_value': 4.0
            },
            {
                'upgrade_id': 'upgrade_tavern',
                'name': 'Build Tavern',
                'description': 'Unlock the tavern to serve food and drinks to guests',
                'cost': 150.0,
                'effect_type': 'unlock_tavern',
                'effect_value': 1.0
            },
            {
                'upgrade_id': 'upgrade_room_royal',
                'name': 'Unlock Royal Suites',
                'description': 'Unlock the ability to build Royal suites (8x income)',
                'cost': 5000.0,
                'effect_type': 'unlock_room',
                'effect_value': 8.0
            },
        ]

        for upgrade_data in upgrade_templates:
            UpgradeTemplate.objects.create(**upgrade_data)
            self.stdout.write(f'  Created: {upgrade_data["name"]} (${upgrade_data["cost"]:.0f})')
