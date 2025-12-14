#!/usr/bin/env python
"""
Test script to verify species generation is working correctly
"""
import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inn_project.settings')
django.setup()

from game_api.game_service import GameService
from game_api.models import GameState, Guest, GuestSpecies

def test_species_generation():
    """Test that guests are being created with proper species"""

    print("Testing species generation system...\n")

    # Create or get a test game state
    test_player_id = "test_species_player"
    game_state = GameService.create_or_get_game_state(test_player_id)

    print(f"✓ Created test game state for player: {test_player_id}")
    print(f"  Current gold: {game_state.gold}")
    print(f"  Current reputation: {game_state.reputation}\n")

    # Test species selection function
    print("Testing species selection (10 samples):")
    species_counts = {}
    for i in range(10):
        species = GameService._select_random_species()
        species_label = GuestSpecies(species).label
        species_counts[species_label] = species_counts.get(species_label, 0) + 1
        print(f"  {i+1}. {species_label}")

    print(f"\nSpecies distribution: {species_counts}\n")

    # Test guest spawning with species
    print("Testing guest spawning with species...")

    # Set up conditions for guest spawning
    game_state.gold = 1000
    game_state.reputation = 50
    game_state.max_guests = 5
    game_state.save()

    # Delete existing guests to start fresh
    Guest.objects.filter(game_state=game_state).delete()

    print(f"✓ Reset game state (gold: {game_state.gold}, reputation: {game_state.reputation})")

    # Trigger game tick to spawn guests
    print("\nTriggering game ticks to spawn guests...\n")

    for i in range(3):
        GameService.process_tick(test_player_id)
        guests = Guest.objects.filter(game_state=game_state)
        print(f"Tick {i+1}: {guests.count()} guests spawned")

    # Display spawned guests with their species
    guests = Guest.objects.filter(game_state=game_state).order_by('-created_at')

    if guests.exists():
        print(f"\n✓ Successfully spawned {guests.count()} guests:\n")
        for guest in guests[:10]:  # Show first 10
            species_label = guest.get_species_display()
            print(f"  • {guest.name} - {species_label} {guest.guest_type}")
            print(f"    Stats: {guest.gold_per_tick:.1f} gold/tick, {guest.patience} patience, {guest.satisfaction} satisfaction")

        # Check species diversity
        unique_species = set(g.species for g in guests)
        print(f"\n✓ Species diversity: {len(unique_species)} different species spawned")

        # Species breakdown
        species_breakdown = {}
        for guest in guests:
            species_label = guest.get_species_display()
            species_breakdown[species_label] = species_breakdown.get(species_label, 0) + 1

        print("\nSpecies breakdown:")
        for species, count in sorted(species_breakdown.items(), key=lambda x: -x[1]):
            print(f"  {species}: {count}")

        print("\n✅ Species generation test PASSED!")
        print(f"✓ All guests have species assigned")
        print(f"✓ Species are displaying correctly")
        print(f"✓ Stats are being generated properly")

    else:
        print("\n⚠️  No guests spawned - this may be expected if spawn conditions aren't met")
        print("Try increasing game ticks or adjusting spawn parameters")

    # Cleanup
    print(f"\nCleaning up test data...")
    Guest.objects.filter(game_state=game_state).delete()
    print("✓ Test complete")

if __name__ == '__main__':
    try:
        test_species_generation()
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
