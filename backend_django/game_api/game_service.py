"""
Game service layer - contains all game business logic
"""
import uuid
import random
from datetime import datetime, timedelta
from django.utils import timezone
from django.db import transaction
from .models import (
    GameState, Room, Guest, TavernItem, Ingredient,
    Recipe, Upgrade, GuestType, RoomTypeTemplate, UpgradeTemplate
)


class GameService:
    """Service class for game logic"""

    # Guest names pool
    GUEST_NAMES = [
        "Aldric", "Brunhilde", "Cedric", "Elara", "Finnian",
        "Gwendolyn", "Thorne", "Isolde", "Magnus", "Rosalind",
        "Gareth", "Freya", "Ragnar", "Sylvia", "Oswald",
        "Bjorn", "Aria", "Dorian", "Lyra", "Cassius",
        "Seraphina", "Orion", "Luna", "Dante", "Aurora",
        "Zephyr", "Celeste", "Raven", "Phoenix", "Sage",
        "Grimwald", "Mystique", "Shadow", "Titus", "Ophelia"
    ]

    @staticmethod
    @transaction.atomic
    def create_or_get_game_state(player_id: str) -> GameState:
        """Create a new game state or get existing one"""
        game_state, created = GameState.objects.get_or_create(
            player_id=player_id,
            defaults={
                'gold': 100.0,
                'reputation': 0.0,
                'max_guests': 5,
                'total_income_multiplier': 1.0,
                'auto_clean_enabled': False,
                'game_speed': 1.0,
                'tavern_unlocked': False,
            }
        )

        if created:
            # Create initial rooms using basic template
            basic_template = RoomTypeTemplate.objects.get(room_type_id='basic')
            for _ in range(3):
                Room.objects.create(
                    game_state=game_state,
                    room_template=basic_template,
                    level=1,
                    cleanliness=100.0
                )

            # Create initial upgrade instances for all templates
            GameService._create_initial_upgrades(game_state)

            # Create recipes for all items
            GameService._create_recipes_for_items(game_state)

        return game_state

    @staticmethod
    def _create_initial_upgrades(game_state: GameState):
        """Create upgrade instances for all available templates"""
        for template in UpgradeTemplate.objects.all():
            Upgrade.objects.create(
                game_state=game_state,
                upgrade_template=template,
                purchased=False
            )

    @staticmethod
    def _create_recipes_for_items(game_state: GameState):
        """Create recipes for all tavern items"""
        items = TavernItem.objects.all()

        for item in items:
            unlocked = item.quality == 'basic'  # Basic items start unlocked
            cost_to_unlock = 0.0

            if item.quality == 'good':
                cost_to_unlock = 50.0
            elif item.quality == 'fine':
                cost_to_unlock = 150.0
            elif item.quality == 'exquisite':
                cost_to_unlock = 500.0
            elif item.quality == 'legendary':
                cost_to_unlock = 1000.0

            Recipe.objects.create(
                game_state=game_state,
                recipe_id=f"recipe_{item.item_id}",
                name=f"Recipe: {item.name}",
                item=item,
                unlocked=unlocked,
                discovered=unlocked,
                cost_to_unlock=cost_to_unlock,
                required_ingredients=[]  # Can be extended later
            )

    @staticmethod
    @transaction.atomic
    def process_tick(player_id: str) -> GameState:
        """Process one game tick"""
        game_state = GameService.create_or_get_game_state(player_id)
        now = timezone.now()

        # Calculate time delta for incremental progress
        time_delta = (now - game_state.last_update).total_seconds()
        ticks = max(1, int(time_delta * game_state.game_speed))

        # Process each tick
        for _ in range(min(ticks, 10)):  # Limit to prevent too many ticks
            GameService._process_single_tick(game_state)

        game_state.last_update = now
        game_state.save()

        return game_state

    @staticmethod
    def _process_single_tick(game_state: GameState):
        """Process a single game tick"""
        # Generate income from occupied rooms
        for room in game_state.rooms.all():
            if room.occupied:
                # Get the guest in this room (using reverse relation)
                guest = room.current_guest.first()
                if guest:
                    income = room.income_rate * guest.gold_per_tick * game_state.total_income_multiplier
                    game_state.gold += income

                    # Decrease room cleanliness
                    room.cleanliness = max(0, room.cleanliness - 0.5)
                    room.save()

                    # Decrease guest patience if room is dirty
                    if room.cleanliness < 50:
                        guest.patience = max(0, guest.patience - 1.0)
                        guest.save()

        # Auto-clean if enabled
        if game_state.auto_clean_enabled:
            for room in game_state.rooms.all():
                room.cleanliness = min(100, room.cleanliness + 2.0)
                room.save()

        # Check for guests leaving
        guests_to_remove = []
        for guest in game_state.guests.all():
            should_leave = False

            if guest.patience <= 0:
                should_leave = True
            elif guest.check_in_time:
                time_stayed = (timezone.now() - guest.check_in_time).total_seconds()
                if time_stayed > guest.stay_duration:
                    should_leave = True
                    # Check if satisfied enough for ingredient drops
                    if guest.satisfaction >= 80:
                        GameService._drop_ingredients_from_guest(game_state, guest)

            if should_leave:
                if guest.room:
                    guest.room.occupied = False
                    guest.room.save()

                # Add reputation
                if guest.satisfaction >= 80:
                    game_state.reputation += guest.reputation_bonus
                elif guest.satisfaction < 30:
                    game_state.reputation -= abs(guest.reputation_bonus) * 0.5

                guests_to_remove.append(guest.id)

        # Remove guests that left
        Guest.objects.filter(id__in=guests_to_remove).delete()

        # Try to spawn new guests
        GameService._try_spawn_guest(game_state)

    @staticmethod
    def _drop_ingredients_from_guest(game_state: GameState, guest: Guest):
        """Drop ingredients from satisfied guests"""
        # Merchants have 2x drop chance
        chance_multiplier = 2.0 if guest.guest_type == GuestType.MERCHANT else (guest.satisfaction / 100.0)

        for ingredient in Ingredient.objects.all():
            drop_chance = ingredient.base_drop_chance * chance_multiplier

            # Nobles, Princes, and Wizards have bonus for rare ingredients
            if guest.guest_type in [GuestType.NOBLE, GuestType.PRINCE, GuestType.WIZARD]:
                if ingredient.rarity in ['rare', 'epic', 'legendary']:
                    drop_chance *= 1.5

            # Dragons drop epic/legendary ingredients more frequently
            if guest.guest_type == GuestType.DRAGON_DISGUISED:
                if ingredient.rarity in ['epic', 'legendary']:
                    drop_chance *= 3.0

            # Roll for drop
            if random.random() < drop_chance:
                current_amount = game_state.ingredient_inventory.get(ingredient.ingredient_id, 0)
                game_state.ingredient_inventory[ingredient.ingredient_id] = current_amount + 1

        game_state.save()

    @staticmethod
    def _try_spawn_guest(game_state: GameState):
        """Try to spawn a new guest"""
        # Check if we have capacity and available rooms
        current_guests = game_state.guests.count()
        if current_guests >= game_state.max_guests:
            return

        available_rooms = game_state.rooms.filter(occupied=False)
        if not available_rooms.exists():
            return

        # Spawn chance: 20% per tick
        if random.random() > 0.2:
            return

        # Select random guest type with weighted probabilities
        guest_type = GameService._select_random_guest_type()

        # Create guest attributes based on type
        guest_data = GameService._get_guest_attributes(guest_type)

        # Select a room
        room = random.choice(list(available_rooms))

        # Create guest
        guest = Guest.objects.create(
            game_state=game_state,
            room=room,
            name=random.choice(GameService.GUEST_NAMES),
            guest_type=guest_type,
            patience=100.0,
            satisfaction=50.0,
            gold_per_tick=guest_data['gold_per_tick'],
            reputation_bonus=guest_data['reputation_bonus'],
            stay_duration=guest_data['stay_duration'],
            check_in_time=timezone.now()
        )

        # Mark room as occupied
        room.occupied = True
        room.save()

    @staticmethod
    def _select_random_guest_type() -> str:
        """Select a random guest type with weighted probabilities"""
        guest_types = [
            (GuestType.PEASANT, 25),
            (GuestType.MERCHANT, 20),
            (GuestType.ADVENTURER, 20),
            (GuestType.NOBLE, 10),
            (GuestType.WIZARD, 8),
            (GuestType.BANDIT, 5),
            (GuestType.MONK, 5),
            (GuestType.BARD, 5),
            (GuestType.BEGGAR, 3),
            (GuestType.SCHOLAR, 3),
            (GuestType.DRUNK, 3),
            (GuestType.THIEF, 2),
            (GuestType.PRINCE, 1),
            (GuestType.DRAGON_DISGUISED, 0.5),
            (GuestType.GHOST, 0.5),
        ]

        types, weights = zip(*guest_types)
        return random.choices(types, weights=weights, k=1)[0]

    @staticmethod
    def _get_guest_attributes(guest_type: str) -> dict:
        """Get attributes for a guest type with randomization"""
        base_attributes = {
            GuestType.PEASANT: {'gold': 1.0, 'reputation': 0.05, 'stay': 120},
            GuestType.MERCHANT: {'gold': 3.0, 'reputation': 0.15, 'stay': 180},
            GuestType.NOBLE: {'gold': 8.0, 'reputation': 0.5, 'stay': 300},
            GuestType.ADVENTURER: {'gold': 4.0, 'reputation': 0.2, 'stay': 150},
            GuestType.WIZARD: {'gold': 6.0, 'reputation': 0.4, 'stay': 240},
            GuestType.BANDIT: {'gold': 5.0, 'reputation': -0.3, 'stay': 90},
            GuestType.MONK: {'gold': 0.5, 'reputation': 0.6, 'stay': 200},
            GuestType.BARD: {'gold': 2.5, 'reputation': 0.4, 'stay': 160},
            GuestType.DRAGON_DISGUISED: {'gold': 20.0, 'reputation': random.uniform(-1.0, 2.0), 'stay': 300},
            GuestType.BEGGAR: {'gold': 0.1, 'reputation': 0.1, 'stay': 80},
            GuestType.PRINCE: {'gold': 15.0, 'reputation': 1.5, 'stay': 400},
            GuestType.THIEF: {'gold': 6.0, 'reputation': -0.5, 'stay': 100},
            GuestType.SCHOLAR: {'gold': 1.5, 'reputation': 0.5, 'stay': 250},
            GuestType.DRUNK: {'gold': 3.0, 'reputation': -0.2, 'stay': 120},
            GuestType.GHOST: {'gold': 0.0, 'reputation': 0.8, 'stay': 180},
        }

        base = base_attributes.get(guest_type, {'gold': 1.0, 'reputation': 0.05, 'stay': 120})

        # Add ±20% randomization
        return {
            'gold_per_tick': base['gold'] * random.uniform(0.8, 1.2),
            'reputation_bonus': base['reputation'] * random.uniform(0.8, 1.2) if guest_type != GuestType.DRAGON_DISGUISED else base['reputation'],
            'stay_duration': int(base['stay'] * random.uniform(0.8, 1.2))
        }

    @staticmethod
    @transaction.atomic
    def add_room(player_id: str, room_type: str = 'basic') -> GameState:
        """Add a new room to the inn"""
        game_state = GameService.create_or_get_game_state(player_id)

        # Get room template
        try:
            room_template = RoomTypeTemplate.objects.get(room_type_id=room_type)
        except RoomTypeTemplate.DoesNotExist:
            raise ValueError(f"Room type {room_type} not found")

        cost = room_template.base_cost

        if game_state.gold < cost:
            raise ValueError(f"Not enough gold. Need {cost}, have {game_state.gold}")

        # Deduct cost
        game_state.gold -= cost

        # Create room
        Room.objects.create(
            game_state=game_state,
            room_template=room_template,
            level=1,
            cleanliness=100.0
        )

        game_state.save()
        return game_state

    @staticmethod
    @transaction.atomic
    def clean_room(player_id: str, room_id: str) -> GameState:
        """Clean a specific room"""
        game_state = GameService.create_or_get_game_state(player_id)

        try:
            room = game_state.rooms.get(id=room_id)
            room.cleanliness = 100.0
            room.save()
        except Room.DoesNotExist:
            raise ValueError(f"Room {room_id} not found")

        return game_state

    @staticmethod
    @transaction.atomic
    def purchase_upgrade(player_id: str, upgrade_id: str) -> GameState:
        """Purchase an upgrade"""
        game_state = GameService.create_or_get_game_state(player_id)

        try:
            upgrade = game_state.upgrades.get(
                upgrade_template__upgrade_id=upgrade_id,
                purchased=False
            )
        except Upgrade.DoesNotExist:
            raise ValueError(f"Upgrade {upgrade_id} not found or already purchased")

        if game_state.gold < upgrade.cost:
            raise ValueError(f"Not enough gold. Need {upgrade.cost}, have {game_state.gold}")

        # Deduct cost
        game_state.gold -= upgrade.cost

        # Mark as purchased
        upgrade.purchased = True
        upgrade.save()

        # Apply effect
        if upgrade.effect_type == 'income_multiplier':
            game_state.total_income_multiplier *= upgrade.effect_value
        elif upgrade.effect_type == 'auto_clean':
            game_state.auto_clean_enabled = True
        elif upgrade.effect_type == 'guest_capacity':
            game_state.max_guests += int(upgrade.effect_value)
        elif upgrade.effect_type == 'unlock_tavern':
            game_state.tavern_unlocked = True

        game_state.save()
        return game_state

    @staticmethod
    @transaction.atomic
    def unlock_recipe(player_id: str, recipe_id: str) -> GameState:
        """Unlock a recipe"""
        game_state = GameService.create_or_get_game_state(player_id)

        try:
            recipe = game_state.recipes.get(recipe_id=recipe_id, unlocked=False)
        except Recipe.DoesNotExist:
            raise ValueError(f"Recipe {recipe_id} not found or already unlocked")

        if game_state.gold < recipe.cost_to_unlock:
            raise ValueError(f"Not enough gold. Need {recipe.cost_to_unlock}, have {game_state.gold}")

        # Deduct cost
        game_state.gold -= recipe.cost_to_unlock

        # Unlock recipe
        recipe.unlocked = True
        recipe.discovered = True
        recipe.save()

        game_state.save()
        return game_state

    @staticmethod
    @transaction.atomic
    def craft_item(player_id: str, item_id: str, quantity: int = 1) -> GameState:
        """Craft tavern items"""
        game_state = GameService.create_or_get_game_state(player_id)

        try:
            item = TavernItem.objects.get(item_id=item_id)
        except TavernItem.DoesNotExist:
            raise ValueError(f"Item {item_id} not found")

        # Check if recipe is unlocked
        try:
            recipe = game_state.recipes.get(item__item_id=item_id, unlocked=True)
        except Recipe.DoesNotExist:
            raise ValueError(f"Recipe for {item.name} is not unlocked")

        total_cost = item.cost * quantity

        if game_state.gold < total_cost:
            raise ValueError(f"Not enough gold. Need {total_cost}, have {game_state.gold}")

        # Deduct cost
        game_state.gold -= total_cost

        # Add to inventory
        current_amount = game_state.item_inventory.get(item_id, 0)
        game_state.item_inventory[item_id] = current_amount + quantity

        game_state.save()
        return game_state

    @staticmethod
    @transaction.atomic
    def serve_guest(player_id: str, guest_id: str, item_id: str) -> GameState:
        """Serve food or drink to a guest"""
        game_state = GameService.create_or_get_game_state(player_id)

        try:
            guest = game_state.guests.get(id=guest_id)
        except Guest.DoesNotExist:
            raise ValueError(f"Guest {guest_id} not found")

        try:
            item = TavernItem.objects.get(item_id=item_id)
        except TavernItem.DoesNotExist:
            raise ValueError(f"Item {item_id} not found")

        # Check inventory
        current_amount = game_state.item_inventory.get(item_id, 0)
        if current_amount <= 0:
            raise ValueError(f"No {item.name} in inventory")

        # Remove from inventory
        game_state.item_inventory[item_id] = current_amount - 1

        # Apply bonuses
        guest.patience = min(100, guest.patience + item.patience_bonus)
        guest.satisfaction = min(100, guest.satisfaction + item.satisfaction_bonus)
        guest.gold_per_tick += item.gold_bonus
        guest.reputation_bonus += item.reputation_bonus

        # Mark as fed or served drink
        if item.item_type == 'food':
            guest.fed = True
            guest.food_served = item_id
        else:
            guest.served_drink = True
            guest.beverage_served = item_id

        guest.save()
        game_state.save()

        return game_state
