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

        # Create upgrade templates FIRST (needed for room requirements)
        self._create_upgrade_templates()

        # Create room type templates (referencing upgrades)
        self._create_room_templates()

        self.stdout.write(self.style.SUCCESS('Templates initialized successfully!'))

    def _create_room_templates(self):
        """Create all room type templates"""
        # Get upgrade references
        upgrade_standard = UpgradeTemplate.objects.get(upgrade_id='upgrade_room_standard')
        upgrade_deluxe = UpgradeTemplate.objects.get(upgrade_id='upgrade_room_deluxe')
        upgrade_royal = UpgradeTemplate.objects.get(upgrade_id='upgrade_room_royal')

        room_templates = [
            {
                'room_type_id': 'basic',
                'name': 'Basic Room',
                'description': 'Simple room with basic amenities',
                'base_cost': 50.0,
                'income_multiplier': 1.0,
                'emoji': '🛏️',
                'required_upgrade': None  # Always available
            },
            {
                'room_type_id': 'standard',
                'name': 'Standard Room',
                'description': 'Comfortable room with better furnishings',
                'base_cost': 200.0,
                'income_multiplier': 2.0,
                'emoji': '🏠',
                'required_upgrade': upgrade_standard
            },
            {
                'room_type_id': 'deluxe',
                'name': 'Deluxe Room',
                'description': 'Luxurious room with premium amenities',
                'base_cost': 500.0,
                'income_multiplier': 4.0,
                'emoji': '🏰',
                'required_upgrade': upgrade_deluxe
            },
            {
                'room_type_id': 'royal',
                'name': 'Royal Suite',
                'description': 'Opulent suite fit for royalty',
                'base_cost': 1000.0,
                'income_multiplier': 8.0,
                'emoji': '👑',
                'required_upgrade': upgrade_royal
            },
        ]

        for room_data in room_templates:
            room = RoomTypeTemplate.objects.create(**room_data)
            req = f' (requires {room_data["required_upgrade"].name})' if room_data["required_upgrade"] else ' (always available)'
            self.stdout.write(f'  Created: {room_data["emoji"]} {room_data["name"]}{req}')

    def _create_upgrade_templates(self):
        """Create all upgrade templates"""
        upgrade_templates = [
            {
                'upgrade_id': 'upgrade_income_1',
                'name': 'Income Boost I',
                'description': 'Increase income from all sources by 50%',
                'cost': 200.0,
                'effect_type': 'income_multiplier',
                'effect_value': 1.5
            },
            {
                'upgrade_id': 'upgrade_auto_clean',
                'name': 'Auto-Maintenance',
                'description': 'Automatically maintain facilities over time',
                'cost': 300.0,
                'effect_type': 'auto_clean',
                'effect_value': 1.0
            },
            {
                'upgrade_id': 'upgrade_capacity_1',
                'name': 'Capacity Expansion I',
                'description': 'Increase max capacity by 5',
                'cost': 400.0,
                'effect_type': 'guest_capacity',
                'effect_value': 5.0
            },
            {
                'upgrade_id': 'upgrade_room_standard',
                'name': 'Unlock Tier 2',
                'description': 'Unlock the ability to build Tier 2 facilities (2x income)',
                'cost': 500.0,
                'effect_type': 'unlock_room',
                'effect_value': 2.0
            },
            {
                'upgrade_id': 'upgrade_income_2',
                'name': 'Income Boost II',
                'description': 'Increase income from all sources by 100%',
                'cost': 1000.0,
                'effect_type': 'income_multiplier',
                'effect_value': 2.0
            },
            {
                'upgrade_id': 'upgrade_room_deluxe',
                'name': 'Unlock Tier 3',
                'description': 'Unlock the ability to build Tier 3 facilities (4x income)',
                'cost': 2000.0,
                'effect_type': 'unlock_room',
                'effect_value': 4.0
            },
            {
                'upgrade_id': 'upgrade_feature_market',
                'name': 'Unlock Marketplace',
                'description': 'Unlock the marketplace to trade resources and craft items',
                'cost': 150.0,
                'effect_type': 'unlock_tavern',  # Generic feature unlock
                'effect_value': 1.0
            },
            {
                'upgrade_id': 'upgrade_room_royal',
                'name': 'Unlock Tier 4',
                'description': 'Unlock the ability to build Tier 4 facilities (8x income)',
                'cost': 5000.0,
                'effect_type': 'unlock_room',
                'effect_value': 8.0
            },
        ]

        for upgrade_data in upgrade_templates:
            UpgradeTemplate.objects.create(**upgrade_data)
            self.stdout.write(f'  Created: {upgrade_data["name"]} (${upgrade_data["cost"]:.0f})')
