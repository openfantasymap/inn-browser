import uuid
import random
from datetime import datetime, timedelta
from typing import Dict, List
from app.models.game_models import (
    InnState, Room, Guest, Upgrade, Resources,
    RoomType, GuestType, TavernItem, Recipe, Inventory,
    ItemType, ItemQuality, Ingredient, IngredientRarity,
    IngredientRequirement, IngredientInventory
)


class GameService:
    def __init__(self):
        self.game_states: Dict[str, InnState] = {}
        self.guest_names = [
            "Aldric", "Brunhilde", "Cedric", "Elara", "Finnian",
            "Gwendolyn", "Thorne", "Isolde", "Magnus", "Rosalind",
            "Gareth", "Freya", "Ragnar", "Sylvia", "Oswald",
            "Bjorn", "Aria", "Dorian", "Lyra", "Cassius",
            "Seraphina", "Orion", "Luna", "Dante", "Aurora",
            "Zephyr", "Celeste", "Raven", "Phoenix", "Sage",
            "Grimwald", "Mystique", "Shadow", "Titus", "Ophelia"
        ]

    def create_new_game(self, player_id: str) -> InnState:
        """Initialize a new game state"""
        initial_rooms = [
            Room(
                id=str(uuid.uuid4()),
                room_type=RoomType.BASIC,
                level=1,
                income_rate=1.0
            ) for _ in range(3)
        ]

        initial_upgrades = self._generate_initial_upgrades()

        game_state = InnState(
            resources=Resources(gold=100.0, reputation=0.0, max_guests=5),
            rooms=initial_rooms,
            guests=[],
            upgrades=initial_upgrades,
            total_income_multiplier=1.0,
            auto_clean_enabled=False,
            last_update=datetime.utcnow(),
            game_speed=1.0
        )

        self.game_states[player_id] = game_state
        return game_state

    def get_game_state(self, player_id: str) -> InnState:
        """Get current game state or create new one"""
        if player_id not in self.game_states:
            return self.create_new_game(player_id)
        return self.game_states[player_id]

    def _generate_initial_upgrades(self) -> List[Upgrade]:
        """Generate available upgrades"""
        return [
            Upgrade(
                id="upgrade_income_1",
                name="Better Beds",
                description="Increase income from all rooms by 50%",
                cost=200.0,
                effect_type="income_multiplier",
                effect_value=1.5
            ),
            Upgrade(
                id="upgrade_auto_clean",
                name="Hire Cleaning Staff",
                description="Automatically clean rooms over time",
                cost=300.0,
                effect_type="auto_clean",
                effect_value=1.0
            ),
            Upgrade(
                id="upgrade_capacity_1",
                name="Expand Inn",
                description="Increase max guest capacity by 5",
                cost=400.0,
                effect_type="guest_capacity",
                effect_value=5.0
            ),
            Upgrade(
                id="upgrade_room_standard",
                name="Standard Room",
                description="Unlock Standard room type (2x income)",
                cost=500.0,
                effect_type="unlock_room",
                effect_value=2.0
            ),
            Upgrade(
                id="upgrade_income_2",
                name="Luxury Furnishings",
                description="Increase income from all rooms by 100%",
                cost=1000.0,
                effect_type="income_multiplier",
                effect_value=2.0
            ),
            Upgrade(
                id="upgrade_room_deluxe",
                name="Deluxe Room",
                description="Unlock Deluxe room type (4x income)",
                cost=2000.0,
                effect_type="unlock_room",
                effect_value=4.0
            ),
            Upgrade(
                id="upgrade_tavern",
                name="Build Tavern",
                description="Unlock the tavern to serve food and drinks to guests",
                cost=150.0,
                effect_type="unlock_tavern",
                effect_value=1.0
            ),
        ]

    def _generate_tavern_items(self) -> List[TavernItem]:
        """Generate all available tavern items"""
        return [
            # FOOD - Basic
            TavernItem(
                id="food_bread",
                name="Bread",
                item_type=ItemType.FOOD,
                quality=ItemQuality.BASIC,
                cost=2.0,
                gold_bonus=0.1,
                patience_bonus=5.0,
                satisfaction_bonus=10.0,
                description="Simple bread, satisfying and cheap"
            ),
            TavernItem(
                id="food_stew",
                name="Vegetable Stew",
                item_type=ItemType.FOOD,
                quality=ItemQuality.BASIC,
                cost=5.0,
                gold_bonus=0.2,
                patience_bonus=10.0,
                satisfaction_bonus=15.0,
                description="Warm and hearty stew"
            ),
            # FOOD - Good
            TavernItem(
                id="food_roast",
                name="Roasted Chicken",
                item_type=ItemType.FOOD,
                quality=ItemQuality.GOOD,
                cost=12.0,
                gold_bonus=0.5,
                patience_bonus=15.0,
                reputation_bonus=0.1,
                satisfaction_bonus=25.0,
                description="Delicious roasted chicken"
            ),
            TavernItem(
                id="food_pie",
                name="Meat Pie",
                item_type=ItemType.FOOD,
                quality=ItemQuality.GOOD,
                cost=15.0,
                gold_bonus=0.6,
                patience_bonus=18.0,
                reputation_bonus=0.15,
                satisfaction_bonus=30.0,
                description="Rich and savory meat pie"
            ),
            # FOOD - Fine
            TavernItem(
                id="food_feast",
                name="Royal Feast",
                item_type=ItemType.FOOD,
                quality=ItemQuality.FINE,
                cost=30.0,
                gold_bonus=1.2,
                patience_bonus=25.0,
                reputation_bonus=0.3,
                satisfaction_bonus=45.0,
                description="A magnificent feast fit for royalty"
            ),
            # FOOD - Exquisite
            TavernItem(
                id="food_dragon_steak",
                name="Dragon Steak",
                item_type=ItemType.FOOD,
                quality=ItemQuality.EXQUISITE,
                cost=80.0,
                gold_bonus=3.0,
                patience_bonus=35.0,
                reputation_bonus=0.8,
                satisfaction_bonus=60.0,
                description="Legendary dragon meat, incredibly rare"
            ),

            # BEVERAGES - Basic
            TavernItem(
                id="drink_water",
                name="Water",
                item_type=ItemType.BEVERAGE,
                quality=ItemQuality.BASIC,
                cost=1.0,
                patience_bonus=3.0,
                satisfaction_bonus=5.0,
                description="Fresh water from the well"
            ),
            TavernItem(
                id="drink_ale",
                name="Ale",
                item_type=ItemType.BEVERAGE,
                quality=ItemQuality.BASIC,
                cost=3.0,
                gold_bonus=0.15,
                patience_bonus=8.0,
                satisfaction_bonus=12.0,
                description="Common ale, popular with adventurers"
            ),
            # BEVERAGES - Good
            TavernItem(
                id="drink_mead",
                name="Honey Mead",
                item_type=ItemType.BEVERAGE,
                quality=ItemQuality.GOOD,
                cost=10.0,
                gold_bonus=0.4,
                patience_bonus=12.0,
                reputation_bonus=0.1,
                satisfaction_bonus=20.0,
                description="Sweet mead made from honey"
            ),
            TavernItem(
                id="drink_wine",
                name="Fine Wine",
                item_type=ItemType.BEVERAGE,
                quality=ItemQuality.GOOD,
                cost=18.0,
                gold_bonus=0.7,
                patience_bonus=15.0,
                reputation_bonus=0.2,
                satisfaction_bonus=28.0,
                description="Quality wine from distant vineyards"
            ),
            # BEVERAGES - Fine
            TavernItem(
                id="drink_elven_wine",
                name="Elven Wine",
                item_type=ItemType.BEVERAGE,
                quality=ItemQuality.FINE,
                cost=40.0,
                gold_bonus=1.5,
                patience_bonus=20.0,
                reputation_bonus=0.4,
                satisfaction_bonus=40.0,
                description="Mystical wine from the elven forests"
            ),
            # BEVERAGES - Legendary
            TavernItem(
                id="drink_ambrosia",
                name="Divine Ambrosia",
                item_type=ItemType.BEVERAGE,
                quality=ItemQuality.LEGENDARY,
                cost=100.0,
                gold_bonus=4.0,
                patience_bonus=40.0,
                reputation_bonus=1.0,
                satisfaction_bonus=70.0,
                description="The drink of gods, impossibly rare"
            ),
        ]

    def _generate_recipes(self, items: List[TavernItem]) -> List[Recipe]:
        """Generate recipes for tavern items"""
        recipes = []

        # Basic items are unlocked by default
        basic_items = [item for item in items if item.quality == ItemQuality.BASIC]
        for item in basic_items:
            recipes.append(Recipe(
                id=f"recipe_{item.id}",
                name=f"Recipe: {item.name}",
                item_id=item.id,
                unlocked=True,
                cost_to_unlock=0.0,
                ingredients_cost=item.cost
            ))

        # Good quality requires unlocking
        good_items = [item for item in items if item.quality == ItemQuality.GOOD]
        for item in good_items:
            recipes.append(Recipe(
                id=f"recipe_{item.id}",
                name=f"Recipe: {item.name}",
                item_id=item.id,
                unlocked=False,
                cost_to_unlock=50.0,
                ingredients_cost=item.cost
            ))

        # Fine quality requires more investment
        fine_items = [item for item in items if item.quality == ItemQuality.FINE]
        for item in fine_items:
            recipes.append(Recipe(
                id=f"recipe_{item.id}",
                name=f"Recipe: {item.name}",
                item_id=item.id,
                unlocked=False,
                cost_to_unlock=150.0,
                ingredients_cost=item.cost
            ))

        # Exquisite and Legendary are very expensive
        special_items = [item for item in items if item.quality in [ItemQuality.EXQUISITE, ItemQuality.LEGENDARY]]
        for item in special_items:
            cost = 500.0 if item.quality == ItemQuality.EXQUISITE else 1000.0
            recipes.append(Recipe(
                id=f"recipe_{item.id}",
                name=f"Recipe: {item.name}",
                item_id=item.id,
                unlocked=False,
                cost_to_unlock=cost,
                ingredients_cost=item.cost
            ))

        return recipes

    def _generate_ingredients(self) -> List[Ingredient]:
        """Generate all available ingredients"""
        return [
            # COMMON ingredients
            Ingredient(
                id="ing_flour",
                name="Flour",
                rarity=IngredientRarity.COMMON,
                description="Basic flour for baking",
                base_drop_chance=0.30
            ),
            Ingredient(
                id="ing_water",
                name="Fresh Water",
                rarity=IngredientRarity.COMMON,
                description="Clean water from the well",
                base_drop_chance=0.35
            ),
            Ingredient(
                id="ing_salt",
                name="Salt",
                rarity=IngredientRarity.COMMON,
                description="Common salt for preserving",
                base_drop_chance=0.25
            ),
            Ingredient(
                id="ing_herbs",
                name="Herbs",
                rarity=IngredientRarity.COMMON,
                description="Wild herbs from the forest",
                base_drop_chance=0.30
            ),
            # UNCOMMON ingredients
            Ingredient(
                id="ing_meat",
                name="Fresh Meat",
                rarity=IngredientRarity.UNCOMMON,
                description="Meat from local hunters",
                base_drop_chance=0.15
            ),
            Ingredient(
                id="ing_honey",
                name="Wild Honey",
                rarity=IngredientRarity.UNCOMMON,
                description="Sweet honey from forest bees",
                base_drop_chance=0.12
            ),
            Ingredient(
                id="ing_grapes",
                name="Grapes",
                rarity=IngredientRarity.UNCOMMON,
                description="Fresh grapes for wine",
                base_drop_chance=0.10
            ),
            Ingredient(
                id="ing_spices",
                name="Exotic Spices",
                rarity=IngredientRarity.UNCOMMON,
                description="Rare spices from distant lands",
                base_drop_chance=0.08
            ),
            # RARE ingredients
            Ingredient(
                id="ing_truffle",
                name="Truffle",
                rarity=IngredientRarity.RARE,
                description="Rare truffle mushroom",
                base_drop_chance=0.05
            ),
            Ingredient(
                id="ing_elven_herbs",
                name="Elven Herbs",
                rarity=IngredientRarity.RARE,
                description="Mystical herbs from elven forests",
                base_drop_chance=0.04
            ),
            Ingredient(
                id="ing_aged_wine",
                name="Aged Wine Base",
                rarity=IngredientRarity.RARE,
                description="Wine aged in ancient barrels",
                base_drop_chance=0.03
            ),
            # EPIC ingredients
            Ingredient(
                id="ing_phoenix_feather",
                name="Phoenix Feather",
                rarity=IngredientRarity.EPIC,
                description="A feather from a phoenix, incredibly rare",
                base_drop_chance=0.02
            ),
            Ingredient(
                id="ing_dragon_blood",
                name="Dragon Blood",
                rarity=IngredientRarity.EPIC,
                description="Blood from a dragon, very powerful",
                base_drop_chance=0.015
            ),
            Ingredient(
                id="ing_moonflower",
                name="Moonflower",
                rarity=IngredientRarity.EPIC,
                description="Flower that blooms only under full moon",
                base_drop_chance=0.01
            ),
            # LEGENDARY ingredients
            Ingredient(
                id="ing_ambrosia_essence",
                name="Ambrosia Essence",
                rarity=IngredientRarity.LEGENDARY,
                description="Divine essence from the gods",
                base_drop_chance=0.005
            ),
            Ingredient(
                id="ing_time_crystal",
                name="Time Crystal",
                rarity=IngredientRarity.LEGENDARY,
                description="Crystal that holds the essence of time itself",
                base_drop_chance=0.003
            ),
        ]

    def process_tick(self, player_id: str) -> InnState:
        """Process one game tick"""
        game_state = self.get_game_state(player_id)
        now = datetime.utcnow()

        # Calculate time delta for incremental progress
        time_delta = (now - game_state.last_update).total_seconds()
        ticks = max(1, int(time_delta * game_state.game_speed))

        # Process each tick
        for _ in range(ticks):
            self._process_single_tick(game_state)

        game_state.last_update = now
        return game_state

    def _process_single_tick(self, game_state: InnState):
        """Process a single game tick"""
        # Generate income from occupied rooms
        for room in game_state.rooms:
            if room.occupied and room.current_guest:
                guest = next((g for g in game_state.guests if g.id == room.current_guest), None)
                if guest:
                    income = room.income_rate * guest.gold_per_tick * game_state.total_income_multiplier
                    game_state.resources.gold += income

                    # Decrease room cleanliness
                    room.cleanliness = max(0, room.cleanliness - 0.5)

                    # Decrease guest patience if room is dirty
                    if room.cleanliness < 50:
                        guest.patience = max(0, guest.patience - 1.0)

        # Auto-clean if enabled
        if game_state.auto_clean_enabled:
            for room in game_state.rooms:
                room.cleanliness = min(100, room.cleanliness + 2.0)

        # Check for guests leaving
        guests_to_remove = []
        for guest in game_state.guests:
            if guest.patience <= 0 or guest.check_in_time and \
               (datetime.utcnow() - guest.check_in_time).total_seconds() > guest.stay_duration:
                # Guest leaves
                if guest.room_id:
                    room = next((r for r in game_state.rooms if r.id == guest.room_id), None)
                    if room:
                        room.occupied = False
                        room.current_guest = None

                # Add reputation bonus if guest was happy
                if guest.patience > 70:
                    game_state.resources.reputation += guest.reputation_bonus

                # Drop ingredients if tavern is unlocked and guest is satisfied
                if game_state.tavern_unlocked and guest.satisfaction >= 80:
                    self._drop_ingredients_from_guest(game_state, guest)

                guests_to_remove.append(guest.id)

        game_state.guests = [g for g in game_state.guests if g.id not in guests_to_remove]

        # Potentially spawn new guest
        if len(game_state.guests) < game_state.resources.max_guests and random.random() < 0.1:
            self._spawn_guest(game_state)

    def _spawn_guest(self, game_state: InnState):
        """Spawn a new guest with randomized attributes"""
        guest_type = random.choice(list(GuestType))

        # Base attributes for each guest type with ranges for randomization
        # Format: (base_gold_min, base_gold_max, base_rep_min, base_rep_max, rarity_weight)
        type_configs = {
            GuestType.PEASANT: (0.3, 0.7, 0.05, 0.15, 10),  # Comune
            GuestType.MERCHANT: (1.0, 2.0, 0.2, 0.4, 8),  # Comune
            GuestType.NOBLE: (2.5, 4.0, 0.4, 0.7, 5),  # Non comune
            GuestType.ADVENTURER: (1.5, 2.5, 0.3, 0.5, 7),  # Comune
            GuestType.WIZARD: (3.0, 5.0, 0.6, 1.0, 4),  # Raro
            GuestType.BANDIT: (2.0, 4.0, -0.3, 0.1, 6),  # Alto oro, bassa/negativa rep
            GuestType.MONK: (0.2, 0.5, 0.8, 1.5, 5),  # Basso oro, alta rep
            GuestType.BARD: (1.0, 1.5, 0.7, 1.2, 6),  # Medio oro, alta rep
            GuestType.DRAGON_DISGUISED: (8.0, 15.0, -0.5, 2.0, 1),  # Rarissimo, stats estremi
            GuestType.BEGGAR: (0.1, 0.3, 0.2, 0.4, 8),  # Bassissimo oro
            GuestType.PRINCE: (4.0, 7.0, 1.5, 3.0, 2),  # Molto raro, ottimi stats
            GuestType.THIEF: (2.5, 4.5, -0.5, -0.1, 5),  # Alto oro, rep negativa
            GuestType.SCHOLAR: (0.5, 1.0, 0.9, 1.6, 6),  # Basso oro, alta rep
            GuestType.DRUNK: (1.2, 2.0, -0.2, 0.2, 7),  # Medio oro, bassa rep
            GuestType.GHOST: (0.0, 0.1, 1.0, 2.5, 3),  # Quasi nessun oro, altissima rep
        }

        # Weighted random selection based on rarity
        types_list = list(type_configs.keys())
        weights = [type_configs[t][4] for t in types_list]
        guest_type = random.choices(types_list, weights=weights)[0]

        config = type_configs[guest_type]

        # Generate random attributes within the type's range
        gold_per_tick = round(random.uniform(config[0], config[1]), 2)
        reputation_bonus = round(random.uniform(config[2], config[3]), 2)

        # Add some extra randomization (±20%) to make each guest unique
        variation = random.uniform(0.8, 1.2)
        gold_per_tick = max(0, round(gold_per_tick * variation, 2))
        reputation_bonus = round(reputation_bonus * variation, 2)

        # Random stay duration based on guest type
        if guest_type in [GuestType.BEGGAR, GuestType.DRUNK]:
            stay_duration = random.randint(3, 8)  # Short stay
        elif guest_type in [GuestType.NOBLE, GuestType.PRINCE, GuestType.WIZARD]:
            stay_duration = random.randint(15, 30)  # Long stay
        else:
            stay_duration = random.randint(8, 20)  # Normal stay

        guest = Guest(
            id=str(uuid.uuid4()),
            name=random.choice(self.guest_names),
            guest_type=guest_type,
            patience=100.0,
            gold_per_tick=gold_per_tick,
            reputation_bonus=reputation_bonus,
            stay_duration=stay_duration
        )

        game_state.guests.append(guest)

    def _drop_ingredients_from_guest(self, game_state: InnState, guest: Guest):
        """Drop ingredients from satisfied guests"""
        # Merchants have 2x chance, others use satisfaction as multiplier
        chance_multiplier = 2.0 if guest.guest_type == GuestType.MERCHANT else (guest.satisfaction / 100.0)

        # Each ingredient has its own drop chance
        for ingredient in game_state.available_ingredients:
            # Base chance modified by guest type and satisfaction
            drop_chance = ingredient.base_drop_chance * chance_multiplier

            # Nobles, Princes, and Wizards have bonus for rare ingredients
            if guest.guest_type in [GuestType.NOBLE, GuestType.PRINCE, GuestType.WIZARD]:
                if ingredient.rarity in [IngredientRarity.RARE, IngredientRarity.EPIC, IngredientRarity.LEGENDARY]:
                    drop_chance *= 1.5

            # Dragons drop epic/legendary ingredients more frequently
            if guest.guest_type == GuestType.DRAGON_DISGUISED:
                if ingredient.rarity in [IngredientRarity.EPIC, IngredientRarity.LEGENDARY]:
                    drop_chance *= 3.0

            # Roll for drop
            if random.random() < drop_chance:
                quantity = 1
                # Rare chance for multiple drops (merchants especially)
                if guest.guest_type == GuestType.MERCHANT and random.random() < 0.3:
                    quantity = random.randint(2, 3)

                if ingredient.id not in game_state.ingredient_inventory.ingredients:
                    game_state.ingredient_inventory.ingredients[ingredient.id] = 0
                game_state.ingredient_inventory.ingredients[ingredient.id] += quantity

    def assign_guest_to_room(self, player_id: str, guest_id: str, room_id: str) -> InnState:
        """Assign a guest to a room"""
        game_state = self.get_game_state(player_id)

        guest = next((g for g in game_state.guests if g.id == guest_id), None)
        room = next((r for r in game_state.rooms if r.id == room_id), None)

        if guest and room and not room.occupied:
            guest.room_id = room_id
            guest.check_in_time = datetime.utcnow()
            room.occupied = True
            room.current_guest = guest_id

        return game_state

    def clean_room(self, player_id: str, room_id: str) -> InnState:
        """Manually clean a room"""
        game_state = self.get_game_state(player_id)

        room = next((r for r in game_state.rooms if r.id == room_id), None)
        if room:
            room.cleanliness = 100.0

        return game_state

    def purchase_upgrade(self, player_id: str, upgrade_id: str) -> InnState:
        """Purchase an upgrade"""
        game_state = self.get_game_state(player_id)

        upgrade = next((u for u in game_state.upgrades if u.id == upgrade_id), None)

        if upgrade and not upgrade.purchased and game_state.resources.gold >= upgrade.cost:
            game_state.resources.gold -= upgrade.cost
            upgrade.purchased = True

            # Apply upgrade effect
            if upgrade.effect_type == "income_multiplier":
                game_state.total_income_multiplier *= upgrade.effect_value
            elif upgrade.effect_type == "auto_clean":
                game_state.auto_clean_enabled = True
            elif upgrade.effect_type == "guest_capacity":
                game_state.resources.max_guests += int(upgrade.effect_value)
            elif upgrade.effect_type == "unlock_room":
                # Add new room of unlocked type
                new_room_type = RoomType.STANDARD if "standard" in upgrade_id else RoomType.DELUXE
                new_room = Room(
                    id=str(uuid.uuid4()),
                    room_type=new_room_type,
                    level=1,
                    income_rate=upgrade.effect_value
                )
                game_state.rooms.append(new_room)
            elif upgrade.effect_type == "unlock_tavern":
                # Unlock tavern and initialize items, recipes, and ingredients
                game_state.tavern_unlocked = True
                game_state.tavern_items = self._generate_tavern_items()
                game_state.recipes = self._generate_recipes(game_state.tavern_items)
                game_state.available_ingredients = self._generate_ingredients()

        return game_state

    def build_room(self, player_id: str, room_type: RoomType) -> InnState:
        """Build a new room"""
        game_state = self.get_game_state(player_id)

        # Room costs
        costs = {
            RoomType.BASIC: 50,
            RoomType.STANDARD: 200,
            RoomType.DELUXE: 800,
            RoomType.ROYAL: 3000
        }

        income_rates = {
            RoomType.BASIC: 1.0,
            RoomType.STANDARD: 2.0,
            RoomType.DELUXE: 4.0,
            RoomType.ROYAL: 8.0
        }

        cost = costs.get(room_type, 100)

        if game_state.resources.gold >= cost:
            game_state.resources.gold -= cost
            new_room = Room(
                id=str(uuid.uuid4()),
                room_type=room_type,
                level=1,
                income_rate=income_rates.get(room_type, 1.0)
            )
            game_state.rooms.append(new_room)

        return game_state

    def unlock_recipe(self, player_id: str, recipe_id: str) -> InnState:
        """Unlock a recipe"""
        game_state = self.get_game_state(player_id)

        if not game_state.tavern_unlocked:
            return game_state

        recipe = next((r for r in game_state.recipes if r.id == recipe_id), None)

        if recipe and not recipe.unlocked and game_state.resources.gold >= recipe.cost_to_unlock:
            game_state.resources.gold -= recipe.cost_to_unlock
            recipe.unlocked = True

        return game_state

    def craft_item(self, player_id: str, item_id: str, quantity: int = 1) -> InnState:
        """Craft tavern items"""
        game_state = self.get_game_state(player_id)

        if not game_state.tavern_unlocked:
            return game_state

        # Check if recipe is unlocked
        recipe = next((r for r in game_state.recipes if r.item_id == item_id), None)
        if not recipe or not recipe.unlocked:
            return game_state

        # Calculate total cost
        total_cost = recipe.ingredients_cost * quantity

        if game_state.resources.gold >= total_cost:
            game_state.resources.gold -= total_cost

            # Add items to inventory
            if item_id not in game_state.inventory.items:
                game_state.inventory.items[item_id] = 0
            game_state.inventory.items[item_id] += quantity

        return game_state

    def serve_guest(self, player_id: str, guest_id: str, item_id: str) -> InnState:
        """Serve food or beverage to a guest"""
        game_state = self.get_game_state(player_id)

        if not game_state.tavern_unlocked:
            return game_state

        # Check inventory
        if item_id not in game_state.inventory.items or game_state.inventory.items[item_id] <= 0:
            return game_state

        # Find guest and item
        guest = next((g for g in game_state.guests if g.id == guest_id), None)
        item = next((i for i in game_state.tavern_items if i.id == item_id), None)

        if not guest or not item:
            return game_state

        # Consume item from inventory
        game_state.inventory.items[item_id] -= 1

        # Apply bonuses
        if item.item_type == ItemType.FOOD:
            if not guest.fed:
                guest.fed = True
                guest.food_served = item_id
                guest.gold_per_tick += item.gold_bonus
                guest.reputation_bonus += item.reputation_bonus
                guest.patience = min(100, guest.patience + item.patience_bonus)
                guest.satisfaction = min(100, guest.satisfaction + item.satisfaction_bonus)
        elif item.item_type == ItemType.BEVERAGE:
            if not guest.served_drink:
                guest.served_drink = True
                guest.beverage_served = item_id
                guest.gold_per_tick += item.gold_bonus
                guest.reputation_bonus += item.reputation_bonus
                guest.patience = min(100, guest.patience + item.patience_bonus)
                guest.satisfaction = min(100, guest.satisfaction + item.satisfaction_bonus)

        return game_state


# Global instance
game_service = GameService()
