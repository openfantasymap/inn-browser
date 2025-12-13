#!/usr/bin/env python
"""
Script to create premium upgrade templates for temporary speedups
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inn_project.settings')
django.setup()

from game_api.models import UpgradeTemplate

# Premium upgrade templates
premium_upgrades = [
    {
        'upgrade_id': 'premium_2x_speed_1h',
        'name': '2x Speed (1 Hour)',
        'description': 'Double your game speed for 1 hour! Guests check in/out faster, rooms clean faster, everything happens twice as fast.',
        'cost': 0.0,  # No gold cost
        'effect_type': 'game_speed',
        'effect_value': 2.0,
        'is_premium': True,
        'premium_price_cents': 99,  # $0.99
        'duration_seconds': 3600,  # 1 hour
        'is_consumable': True,
    },
    {
        'upgrade_id': 'premium_2x_speed_4h',
        'name': '2x Speed (4 Hours)',
        'description': 'Double your game speed for 4 hours! Great value for extended play sessions.',
        'cost': 0.0,
        'effect_type': 'game_speed',
        'effect_value': 2.0,
        'is_premium': True,
        'premium_price_cents': 299,  # $2.99
        'duration_seconds': 14400,  # 4 hours
        'is_consumable': True,
    },
    {
        'upgrade_id': 'premium_5x_speed_1h',
        'name': '5x Speed (1 Hour)',
        'description': 'Quintuple your game speed for 1 hour! Perfect for rapid progression and testing builds.',
        'cost': 0.0,
        'effect_type': 'game_speed',
        'effect_value': 5.0,
        'is_premium': True,
        'premium_price_cents': 499,  # $4.99
        'duration_seconds': 3600,  # 1 hour
        'is_consumable': True,
    },
    {
        'upgrade_id': 'premium_10x_speed_30m',
        'name': '10x Speed (30 Minutes)',
        'description': 'Extreme speed boost! 10x game speed for 30 minutes. Use wisely for maximum efficiency.',
        'cost': 0.0,
        'effect_type': 'game_speed',
        'effect_value': 10.0,
        'is_premium': True,
        'premium_price_cents': 499,  # $4.99
        'duration_seconds': 1800,  # 30 minutes
        'is_consumable': True,
    },
    {
        'upgrade_id': 'premium_instant_clean',
        'name': 'Instant Clean All Rooms',
        'description': 'Instantly clean all rooms to 100% cleanliness. Great for when you need to accept guests quickly!',
        'cost': 0.0,
        'effect_type': 'instant_clean',
        'effect_value': 1.0,
        'is_premium': True,
        'premium_price_cents': 199,  # $1.99
        'duration_seconds': 0,  # Instant effect (no duration)
        'is_consumable': True,
    },
    {
        'upgrade_id': 'premium_2x_gold_2h',
        'name': '2x Gold Earnings (2 Hours)',
        'description': 'Double all gold earnings for 2 hours! Guests pay twice as much, perfect for building your treasury.',
        'cost': 0.0,
        'effect_type': 'income_multiplier',
        'effect_value': 2.0,
        'is_premium': True,
        'premium_price_cents': 299,  # $2.99
        'duration_seconds': 7200,  # 2 hours
        'is_consumable': True,
    },
    {
        'upgrade_id': 'premium_2x_gold_8h',
        'name': '2x Gold Earnings (8 Hours)',
        'description': 'Double all gold earnings for 8 hours! Best value for dedicated players.',
        'cost': 0.0,
        'effect_type': 'income_multiplier',
        'effect_value': 2.0,
        'is_premium': True,
        'premium_price_cents': 999,  # $9.99
        'duration_seconds': 28800,  # 8 hours
        'is_consumable': True,
    },
    {
        'upgrade_id': 'premium_3x_gold_1h',
        'name': '3x Gold Earnings (1 Hour)',
        'description': 'Triple all gold earnings for 1 hour! Stack with other bonuses for maximum profit.',
        'cost': 0.0,
        'effect_type': 'income_multiplier',
        'effect_value': 3.0,
        'is_premium': True,
        'premium_price_cents': 499,  # $4.99
        'duration_seconds': 3600,  # 1 hour
        'is_consumable': True,
    },
]

def create_upgrades():
    """Create or update premium upgrade templates"""
    created_count = 0
    updated_count = 0

    for upgrade_data in premium_upgrades:
        upgrade, created = UpgradeTemplate.objects.update_or_create(
            upgrade_id=upgrade_data['upgrade_id'],
            defaults=upgrade_data
        )

        if created:
            created_count += 1
            print(f"✓ Created: {upgrade.name} (${upgrade.premium_price_cents/100:.2f})")
        else:
            updated_count += 1
            print(f"↻ Updated: {upgrade.name} (${upgrade.premium_price_cents/100:.2f})")

    print(f"\n{'='*60}")
    print(f"Premium Upgrades Summary:")
    print(f"  Created: {created_count}")
    print(f"  Updated: {updated_count}")
    print(f"  Total: {len(premium_upgrades)}")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    create_upgrades()
