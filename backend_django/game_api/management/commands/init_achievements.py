"""
Management command to initialize achievement templates
"""
from django.core.management.base import BaseCommand
from game_api.models import Achievement, UpgradeTemplate


class Command(BaseCommand):
    help = 'Initialize achievement templates'

    def handle(self, *args, **options):
        self.stdout.write('Initializing achievements...')

        # Clear existing achievements
        Achievement.objects.all().delete()

        # Get reward upgrades (will be created later)
        # For now, create achievements without upgrades, link them after

        achievements = [
            # Customers served achievements
            {
                'achievement_id': 'achievement_serve_10',
                'name': 'Welcome Guests',
                'description': 'Serve 10 satisfied guests (patience > 50%)',
                'requirement_type': 'customers_high_patience',
                'requirement_value': 10,
                'requirement_metadata': {'patience_min': 50},
                'icon': '👋',
                'reward_upgrade': None
            },
            {
                'achievement_id': 'achievement_serve_100',
                'name': 'Renowned Innkeeper',
                'description': 'Serve 100 satisfied guests (patience > 50%)',
                'requirement_type': 'customers_high_patience',
                'requirement_value': 100,
                'requirement_metadata': {'patience_min': 50},
                'icon': '⭐',
                'reward_upgrade': None
            },
            {
                'achievement_id': 'achievement_serve_1000',
                'name': 'Legendary Hospitality Master',
                'description': 'Serve 1000 satisfied guests (patience > 50%)',
                'requirement_type': 'customers_high_patience',
                'requirement_value': 1000,
                'requirement_metadata': {'patience_min': 50},
                'icon': '👑',
                'reward_upgrade': None
            },

            # High patience achievements (exceptional service)
            {
                'achievement_id': 'achievement_patience_90_count_10',
                'name': 'Exceptional Service',
                'description': 'Serve 10 extremely satisfied guests (patience > 90%)',
                'requirement_type': 'customers_high_patience',
                'requirement_value': 10,
                'requirement_metadata': {'patience_min': 90},
                'icon': '💎',
                'reward_upgrade': None
            },
            {
                'achievement_id': 'achievement_patience_90_count_100',
                'name': 'Perfection Seeker',
                'description': 'Serve 100 extremely satisfied guests (patience > 90%)',
                'requirement_type': 'customers_high_patience',
                'requirement_value': 100,
                'requirement_metadata': {'patience_min': 90},
                'icon': '✨',
                'reward_upgrade': None
            },

            # Low patience achievements (handling difficult guests)
            {
                'achievement_id': 'achievement_patience_low_10',
                'name': 'Damage Control',
                'description': 'Serve 10 impatient guests (patience < 30%)',
                'requirement_type': 'customers_low_patience',
                'requirement_value': 10,
                'requirement_metadata': {'patience_max': 30},
                'icon': '🔥',
                'reward_upgrade': None
            },
            {
                'achievement_id': 'achievement_patience_low_100',
                'name': 'Crisis Manager',
                'description': 'Serve 100 impatient guests (patience < 30%)',
                'requirement_type': 'customers_low_patience',
                'requirement_value': 100,
                'requirement_metadata': {'patience_max': 30},
                'icon': '⚡',
                'reward_upgrade': None
            },

            # Race-specific achievements
            {
                'achievement_id': 'achievement_elves_50',
                'name': 'Friend of the Elves',
                'description': 'Serve 50 elven guests',
                'requirement_type': 'customers_race',
                'requirement_value': 50,
                'requirement_metadata': {'race': 'elf'},
                'icon': '🌿',
                'reward_upgrade': None
            },
            {
                'achievement_id': 'achievement_dwarves_50',
                'name': 'Dwarven Hospitality',
                'description': 'Serve 50 dwarven guests',
                'requirement_type': 'customers_race',
                'requirement_value': 50,
                'requirement_metadata': {'race': 'dwarf'},
                'icon': '⛏️',
                'reward_upgrade': None
            },
            {
                'achievement_id': 'achievement_orcs_50',
                'name': 'Orcish Tolerance',
                'description': 'Serve 50 orc guests',
                'requirement_type': 'customers_race',
                'requirement_value': 50,
                'requirement_metadata': {'race': 'orc'},
                'icon': '💪',
                'reward_upgrade': None
            },
            {
                'achievement_id': 'achievement_dragons_10',
                'name': 'Dragon Whisperer',
                'description': 'Serve 10 dragon guests (disguised or not)',
                'requirement_type': 'customers_race',
                'requirement_value': 10,
                'requirement_metadata': {'race': 'dragon'},
                'icon': '🐉',
                'reward_upgrade': None
            },

            # Guest type achievements
            {
                'achievement_id': 'achievement_nobles_25',
                'name': 'Noble Connections',
                'description': 'Serve 25 noble guests',
                'requirement_type': 'customers_type',
                'requirement_value': 25,
                'requirement_metadata': {'guest_type': 'noble'},
                'icon': '🎩',
                'reward_upgrade': None
            },
            {
                'achievement_id': 'achievement_wizards_25',
                'name': 'Arcane Hospitality',
                'description': 'Serve 25 wizard guests',
                'requirement_type': 'customers_type',
                'requirement_value': 25,
                'requirement_metadata': {'guest_type': 'wizard'},
                'icon': '🔮',
                'reward_upgrade': None
            },
            {
                'achievement_id': 'achievement_merchants_50',
                'name': 'Trade Network',
                'description': 'Serve 50 merchant guests',
                'requirement_type': 'customers_type',
                'requirement_value': 50,
                'requirement_metadata': {'guest_type': 'merchant'},
                'icon': '💰',
                'reward_upgrade': None
            },
        ]

        for achievement_data in achievements:
            Achievement.objects.create(**achievement_data)
            self.stdout.write(f'  Created: {achievement_data["icon"]} {achievement_data["name"]}')

        self.stdout.write(self.style.SUCCESS(f'Created {len(achievements)} achievements!'))
