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
                'name': 'Hire Expert Barkeep',
                'description': 'An experienced barkeep increases your reputation and service quality (+50% income, 5 gold/tick salary)',
                'cost': 200.0,
                'effect_type': 'income_multiplier',
                'effect_value': 1.5,
                'operational_cost_per_tick': 5.0  # Paying better staff
            },
            {
                'upgrade_id': 'upgrade_auto_clean',
                'name': 'Summon House Sprites',
                'description': 'Magical sprites keep your inn spotless while you focus on guests (3 gold/tick for enchanted brooms)',
                'cost': 300.0,
                'effect_type': 'auto_clean',
                'effect_value': 1.0,
                'operational_cost_per_tick': 3.0  # Paying cleaning crew
            },
            {
                'upgrade_id': 'upgrade_capacity_1',
                'name': 'Build Guest Registry',
                'description': 'Hire a doorkeeper to manage more guests efficiently (+5 capacity, 2 gold/tick salary)',
                'cost': 400.0,
                'effect_type': 'guest_capacity',
                'effect_value': 5.0,
                'operational_cost_per_tick': 2.0  # More guest overhead
            },
            {
                'upgrade_id': 'upgrade_room_standard',
                'name': 'Learn Stone Masonry',
                'description': 'Master the art of stone construction to build superior rooms with 2x income potential',
                'cost': 500.0,
                'effect_type': 'unlock_room',
                'effect_value': 2.0,
                'operational_cost_per_tick': 0.0  # One-time unlock, no ongoing cost
            },
            {
                'upgrade_id': 'upgrade_income_2',
                'name': 'Legendary Hospitality',
                'description': 'Hire a master chef and renowned entertainers to double your income (+100%, 12 gold/tick salaries)',
                'cost': 1000.0,
                'effect_type': 'income_multiplier',
                'effect_value': 2.0,
                'operational_cost_per_tick': 12.0  # Higher tier staff
            },
            {
                'upgrade_id': 'upgrade_room_deluxe',
                'name': 'Master Architecture',
                'description': 'Study advanced architectural techniques to build luxurious suites with 4x income potential',
                'cost': 2000.0,
                'effect_type': 'unlock_room',
                'effect_value': 4.0,
                'operational_cost_per_tick': 0.0  # One-time unlock, no ongoing cost
            },
            {
                'upgrade_id': 'upgrade_feature_market',
                'name': 'Establish Tavern Kitchen',
                'description': 'Set up a proper kitchen to craft delicious meals and beverages for your guests',
                'cost': 150.0,
                'effect_type': 'unlock_tavern',  # Generic feature unlock
                'effect_value': 1.0,
                'operational_cost_per_tick': 0.0  # One-time unlock, no ongoing cost
            },
            {
                'upgrade_id': 'upgrade_room_royal',
                'name': 'Royal Engineering Secrets',
                'description': 'Learn palace construction techniques to build opulent royal suites with 8x income potential',
                'cost': 5000.0,
                'effect_type': 'unlock_room',
                'effect_value': 8.0,
                'operational_cost_per_tick': 0.0  # One-time unlock, no ongoing cost
            },
        ]

        for upgrade_data in upgrade_templates:
            UpgradeTemplate.objects.create(**upgrade_data)
            self.stdout.write(f'  Created: {upgrade_data["name"]} (${upgrade_data["cost"]:.0f})')
