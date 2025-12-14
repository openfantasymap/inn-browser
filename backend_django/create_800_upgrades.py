#!/usr/bin/env python
"""
Generate 800 diverse upgrade templates covering all game aspects
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inn_project.settings')
django.setup()

from game_api.models import UpgradeTemplate

def generate_all_upgrades():
    """Generate 800+ upgrade templates across all game systems"""

    upgrades = []

    # ========================================================================
    # INCOME UPGRADES (150 total)
    # ========================================================================

    # Basic income multipliers (50 tiers)
    for i in range(1, 51):
        multiplier = 1.0 + (i * 0.1)
        cost = 100 * (1.5 ** i)
        upgrades.append({
            'upgrade_id': f'income_mult_tier_{i}',
            'name': f'Income Boost {i}',
            'description': f'Increase all income by {int((multiplier - 1) * 100)}%',
            'cost': cost,
            'effect_type': 'income_multiplier',
            'effect_value': multiplier,
        })

    # Flat gold bonuses (25 tiers)
    for i in range(1, 26):
        bonus = i * 5
        cost = 50 * (1.3 ** i)
        upgrades.append({
            'upgrade_id': f'gold_flat_tier_{i}',
            'name': f'Gold Fortune {i}',
            'description': f'Gain +{bonus} gold per guest checkout',
            'cost': cost,
            'effect_type': 'gold_flat_bonus',
            'effect_value': float(bonus),
        })

    # Percentage income boosts (25 tiers)
    for i in range(1, 26):
        percent = i * 5
        cost = 150 * (1.4 ** i)
        upgrades.append({
            'upgrade_id': f'income_percent_tier_{i}',
            'name': f'Prosperity {i}',
            'description': f'+{percent}% income from all sources',
            'cost': cost,
            'effect_type': 'income_percentage',
            'effect_value': float(percent),
        })

    # Compound interest upgrades (25 tiers)
    for i in range(1, 26):
        rate = i * 0.5
        cost = 200 * (1.5 ** i)
        upgrades.append({
            'upgrade_id': f'compound_tier_{i}',
            'name': f'Compound Growth {i}',
            'description': f'Gain {rate}% of current gold every minute',
            'cost': cost,
            'effect_type': 'compound_interest',
            'effect_value': rate,
        })

    # Per-room income (25 tiers)
    for i in range(1, 26):
        bonus = i * 2
        cost = 80 * (1.4 ** i)
        upgrades.append({
            'upgrade_id': f'room_income_tier_{i}',
            'name': f'Room Revenue {i}',
            'description': f'+{bonus} gold per room per tick',
            'cost': cost,
            'effect_type': 'room_income_bonus',
            'effect_value': float(bonus),
        })

    # ========================================================================
    # GAME SPEED UPGRADES (100 total)
    # ========================================================================

    # Basic speed boosts (50 tiers)
    for i in range(1, 51):
        speed = 1.0 + (i * 0.05)
        cost = 120 * (1.45 ** i)
        upgrades.append({
            'upgrade_id': f'speed_tier_{i}',
            'name': f'Time Acceleration {i}',
            'description': f'Game runs {int((speed - 1) * 100)}% faster',
            'cost': cost,
            'effect_type': 'game_speed',
            'effect_value': speed,
        })

    # Tick rate increases (25 tiers)
    for i in range(1, 26):
        rate = 1.0 + (i * 0.1)
        cost = 150 * (1.4 ** i)
        upgrades.append({
            'upgrade_id': f'tick_rate_tier_{i}',
            'name': f'Faster Ticks {i}',
            'description': f'Increase tick rate by {int((rate - 1) * 100)}%',
            'cost': cost,
            'effect_type': 'tick_rate_multiplier',
            'effect_value': rate,
        })

    # Guest service speed (25 tiers)
    for i in range(1, 26):
        speed = 1.0 + (i * 0.08)
        cost = 100 * (1.35 ** i)
        upgrades.append({
            'upgrade_id': f'service_speed_tier_{i}',
            'name': f'Swift Service {i}',
            'description': f'Guests are served {int((speed - 1) * 100)}% faster',
            'cost': cost,
            'effect_type': 'service_speed',
            'effect_value': speed,
        })

    # ========================================================================
    # ROOM UPGRADES (120 total)
    # ========================================================================

    # Room capacity (30 tiers)
    for i in range(1, 31):
        rooms = i
        cost = 200 * (1.6 ** i)
        upgrades.append({
            'upgrade_id': f'room_capacity_tier_{i}',
            'name': f'Expansion {i}',
            'description': f'Build {rooms} more room slot{"s" if rooms > 1 else ""}',
            'cost': cost,
            'effect_type': 'room_capacity',
            'effect_value': float(rooms),
        })

    # Auto-clean efficiency (30 tiers)
    for i in range(1, 31):
        efficiency = i * 3
        cost = 150 * (1.4 ** i)
        upgrades.append({
            'upgrade_id': f'clean_efficiency_tier_{i}',
            'name': f'Cleaning Power {i}',
            'description': f'Rooms clean {efficiency}% faster',
            'cost': cost,
            'effect_type': 'clean_efficiency',
            'effect_value': float(efficiency),
        })

    # Room level bonuses (30 tiers)
    for i in range(1, 31):
        bonus = i * 0.1
        cost = 180 * (1.5 ** i)
        upgrades.append({
            'upgrade_id': f'room_level_bonus_tier_{i}',
            'name': f'Mastery {i}',
            'description': f'+{int(bonus * 100)}% effectiveness for all room levels',
            'cost': cost,
            'effect_type': 'room_level_multiplier',
            'effect_value': 1.0 + bonus,
        })

    # Cleanliness decay reduction (30 tiers)
    for i in range(1, 31):
        reduction = i * 2
        cost = 100 * (1.3 ** i)
        upgrades.append({
            'upgrade_id': f'decay_reduction_tier_{i}',
            'name': f'Preservation {i}',
            'description': f'Rooms get dirty {reduction}% slower',
            'cost': cost,
            'effect_type': 'decay_reduction',
            'effect_value': float(reduction),
        })

    # ========================================================================
    # GUEST UPGRADES (150 total)
    # ========================================================================

    # Guest capacity (30 tiers)
    for i in range(1, 31):
        guests = i
        cost = 250 * (1.5 ** i)
        upgrades.append({
            'upgrade_id': f'guest_capacity_tier_{i}',
            'name': f'Hospitality {i}',
            'description': f'Host {guests} more guest{"s" if guests > 1 else ""}',
            'cost': cost,
            'effect_type': 'guest_capacity',
            'effect_value': float(guests),
        })

    # Patience bonuses (30 tiers)
    for i in range(1, 31):
        patience = i * 5
        cost = 120 * (1.4 ** i)
        upgrades.append({
            'upgrade_id': f'patience_tier_{i}',
            'name': f'Patience Charm {i}',
            'description': f'Guests start with +{patience} patience',
            'cost': cost,
            'effect_type': 'patience_bonus',
            'effect_value': float(patience),
        })

    # Satisfaction bonuses (30 tiers)
    for i in range(1, 31):
        satisfaction = i * 3
        cost = 140 * (1.35 ** i)
        upgrades.append({
            'upgrade_id': f'satisfaction_tier_{i}',
            'name': f'Comfort {i}',
            'description': f'Guests gain +{satisfaction}% satisfaction',
            'cost': cost,
            'effect_type': 'satisfaction_bonus',
            'effect_value': float(satisfaction),
        })

    # Guest spawn rate (30 tiers)
    for i in range(1, 31):
        rate = i * 5
        cost = 180 * (1.45 ** i)
        upgrades.append({
            'upgrade_id': f'spawn_rate_tier_{i}',
            'name': f'Fame {i}',
            'description': f'Guests arrive {rate}% more often',
            'cost': cost,
            'effect_type': 'spawn_rate',
            'effect_value': float(rate),
        })

    # Guest gold multiplier (30 tiers)
    for i in range(1, 31):
        mult = 1.0 + (i * 0.05)
        cost = 200 * (1.5 ** i)
        upgrades.append({
            'upgrade_id': f'guest_gold_mult_tier_{i}',
            'name': f'Generosity {i}',
            'description': f'Guests pay {int((mult - 1) * 100)}% more',
            'cost': cost,
            'effect_type': 'guest_gold_multiplier',
            'effect_value': mult,
        })

    # ========================================================================
    # REPUTATION UPGRADES (60 total)
    # ========================================================================

    # Reputation multipliers (30 tiers)
    for i in range(1, 31):
        mult = 1.0 + (i * 0.1)
        cost = 150 * (1.4 ** i)
        upgrades.append({
            'upgrade_id': f'reputation_mult_tier_{i}',
            'name': f'Renown {i}',
            'description': f'+{int((mult - 1) * 100)}% reputation from all sources',
            'cost': cost,
            'effect_type': 'reputation_multiplier',
            'effect_value': mult,
        })

    # Flat reputation bonuses (30 tiers)
    for i in range(1, 31):
        bonus = i * 0.5
        cost = 100 * (1.3 ** i)
        upgrades.append({
            'upgrade_id': f'reputation_flat_tier_{i}',
            'name': f'Prestige {i}',
            'description': f'+{bonus} reputation per guest',
            'cost': cost,
            'effect_type': 'reputation_flat_bonus',
            'effect_value': bonus,
        })

    # ========================================================================
    # TAVERN/CRAFTING UPGRADES (80 total)
    # ========================================================================

    # Ingredient drop rate (30 tiers)
    for i in range(1, 31):
        rate = i * 5
        cost = 120 * (1.4 ** i)
        upgrades.append({
            'upgrade_id': f'ingredient_drop_tier_{i}',
            'name': f'Fortune\'s Favor {i}',
            'description': f'+{rate}% ingredient drop chance',
            'cost': cost,
            'effect_type': 'ingredient_drop_rate',
            'effect_value': float(rate),
        })

    # Crafting cost reduction (25 tiers)
    for i in range(1, 26):
        reduction = i * 2
        cost = 100 * (1.35 ** i)
        upgrades.append({
            'upgrade_id': f'craft_cost_tier_{i}',
            'name': f'Efficiency {i}',
            'description': f'Crafting costs {reduction}% less',
            'cost': cost,
            'effect_type': 'craft_cost_reduction',
            'effect_value': float(reduction),
        })

    # Recipe quality bonus (25 tiers)
    for i in range(1, 26):
        quality = i * 3
        cost = 150 * (1.4 ** i)
        upgrades.append({
            'upgrade_id': f'recipe_quality_tier_{i}',
            'name': f'Mastery {i}',
            'description': f'Crafted items are {quality}% better',
            'cost': cost,
            'effect_type': 'recipe_quality',
            'effect_value': float(quality),
        })

    # ========================================================================
    # OFFLINE UPGRADES (40 total)
    # ========================================================================

    # Offline time extensions (20 tiers)
    for i in range(1, 21):
        hours = 12 + (i * 2)
        cost = 300 * (1.5 ** i)
        upgrades.append({
            'upgrade_id': f'offline_time_tier_{i}',
            'name': f'Extended Absence {i}',
            'description': f'Earn offline for up to {hours} hours',
            'cost': cost,
            'effect_type': 'offline_hours',
            'effect_value': float(hours),
        })

    # Offline multipliers (20 tiers)
    for i in range(1, 21):
        mult = 1.0 + (i * 0.1)
        cost = 250 * (1.4 ** i)
        upgrades.append({
            'upgrade_id': f'offline_mult_tier_{i}',
            'name': f'Idle Prosperity {i}',
            'description': f'Offline earnings are {int((mult - 1) * 100)}% higher',
            'cost': cost,
            'effect_type': 'offline_multiplier',
            'effect_value': mult,
        })

    # ========================================================================
    # AUTOMATION UPGRADES (40 total)
    # ========================================================================

    # Auto-assign speed (20 tiers)
    for i in range(1, 21):
        speed = 1.0 + (i * 0.1)
        cost = 200 * (1.5 ** i)
        upgrades.append({
            'upgrade_id': f'auto_assign_tier_{i}',
            'name': f'Smart Assignment {i}',
            'description': f'Auto-assign guests {int((speed - 1) * 100)}% faster',
            'cost': cost,
            'effect_type': 'auto_assign_speed',
            'effect_value': speed,
        })

    # Auto-serve efficiency (20 tiers)
    for i in range(1, 21):
        efficiency = i * 5
        cost = 180 * (1.4 ** i)
        upgrades.append({
            'upgrade_id': f'auto_serve_tier_{i}',
            'name': f'Butler Service {i}',
            'description': f'Auto-serve is {efficiency}% more efficient',
            'cost': cost,
            'effect_type': 'auto_serve_efficiency',
            'effect_value': float(efficiency),
        })

    # ========================================================================
    # COMBO/SYNERGY UPGRADES (60 total)
    # ========================================================================

    # Speed + Income combos (15 tiers)
    for i in range(1, 16):
        speed = 1.0 + (i * 0.03)
        income = 1.0 + (i * 0.05)
        cost = 300 * (1.6 ** i)
        upgrades.append({
            'upgrade_id': f'speed_income_combo_{i}',
            'name': f'Momentum {i}',
            'description': f'+{int((speed-1)*100)}% speed, +{int((income-1)*100)}% income',
            'cost': cost,
            'effect_type': 'speed_income_combo',
            'effect_value': speed,  # Store speed, income calculated separately
        })

    # Guest + Room combos (15 tiers)
    for i in range(1, 16):
        guest_bonus = i * 3
        room_bonus = i * 2
        cost = 280 * (1.55 ** i)
        upgrades.append({
            'upgrade_id': f'guest_room_combo_{i}',
            'name': f'Harmony {i}',
            'description': f'+{guest_bonus}% guest satisfaction, +{room_bonus}% room quality',
            'cost': cost,
            'effect_type': 'guest_room_combo',
            'effect_value': float(guest_bonus),
        })

    # All-arounder upgrades (15 tiers)
    for i in range(1, 16):
        bonus = i * 2
        cost = 400 * (1.7 ** i)
        upgrades.append({
            'upgrade_id': f'all_around_tier_{i}',
            'name': f'Master of All {i}',
            'description': f'+{bonus}% to all stats',
            'cost': cost,
            'effect_type': 'all_stats_bonus',
            'effect_value': float(bonus),
        })

    # Critical chance upgrades (15 tiers)
    for i in range(1, 16):
        crit_chance = i * 2
        cost = 250 * (1.5 ** i)
        upgrades.append({
            'upgrade_id': f'critical_tier_{i}',
            'name': f'Lucky Strike {i}',
            'description': f'{crit_chance}% chance to double guest payments',
            'cost': cost,
            'effect_type': 'critical_chance',
            'effect_value': float(crit_chance),
        })

    print(f"Generated {len(upgrades)} upgrade templates!")
    return upgrades


def create_upgrades(upgrades):
    """Create or update upgrades in database"""
    created_count = 0
    updated_count = 0

    for upgrade_data in upgrades:
        upgrade, created = UpgradeTemplate.objects.update_or_create(
            upgrade_id=upgrade_data['upgrade_id'],
            defaults=upgrade_data
        )

        if created:
            created_count += 1
        else:
            updated_count += 1

    print(f"\n{'='*70}")
    print(f"Upgrade Templates Summary:")
    print(f"  Created: {created_count}")
    print(f"  Updated: {updated_count}")
    print(f"  Total: {len(upgrades)}")
    print(f"{'='*70}\n")

    # Show breakdown by category
    print("Category Breakdown:")
    print(f"  Income Upgrades: 150")
    print(f"  Game Speed: 100")
    print(f"  Room Upgrades: 120")
    print(f"  Guest Upgrades: 150")
    print(f"  Reputation: 60")
    print(f"  Tavern/Crafting: 80")
    print(f"  Offline: 40")
    print(f"  Automation: 40")
    print(f"  Combo/Synergy: 60")
    print(f"  {'─'*70}")
    print(f"  TOTAL: 800 upgrades")


if __name__ == '__main__':
    print("Generating 800 comprehensive upgrade templates...")
    print()

    upgrades = generate_all_upgrades()
    create_upgrades(upgrades)

    print("\n✓ All upgrades created successfully!")
    print("\nYou can now:")
    print("  - View them in Django admin: http://localhost:8000/admin/game_api/upgradetemplate/")
    print("  - Purchase them in-game")
    print("  - Create dependencies between upgrades")
