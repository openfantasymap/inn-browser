"""
Management command to initialize game data (TavernItems and Ingredients)
"""
from django.core.management.base import BaseCommand
from game_api.models import TavernItem, Ingredient


class Command(BaseCommand):
    help = 'Initialize game data: TavernItems and Ingredients'

    def handle(self, *args, **options):
        self.stdout.write('Initializing game data...')

        # Clear existing data
        TavernItem.objects.all().delete()
        Ingredient.objects.all().delete()

        # Create Tavern Items
        self._create_tavern_items()

        # Create Ingredients
        self._create_ingredients()

        self.stdout.write(self.style.SUCCESS('Game data initialized successfully!'))

    def _create_tavern_items(self):
        """Create all tavern items"""
        tavern_items = [
            # FOOD - Basic
            {
                'item_id': 'food_bread',
                'name': 'Bread',
                'item_type': 'food',
                'quality': 'basic',
                'cost': 2.0,
                'gold_bonus': 0.1,
                'patience_bonus': 5.0,
                'satisfaction_bonus': 10.0,
                'description': 'Simple bread, satisfying and cheap'
            },
            {
                'item_id': 'food_stew',
                'name': 'Vegetable Stew',
                'item_type': 'food',
                'quality': 'basic',
                'cost': 5.0,
                'gold_bonus': 0.2,
                'patience_bonus': 10.0,
                'satisfaction_bonus': 15.0,
                'description': 'Warm and hearty stew'
            },
            # FOOD - Good
            {
                'item_id': 'food_roast',
                'name': 'Roasted Chicken',
                'item_type': 'food',
                'quality': 'good',
                'cost': 12.0,
                'gold_bonus': 0.5,
                'patience_bonus': 15.0,
                'reputation_bonus': 0.1,
                'satisfaction_bonus': 25.0,
                'description': 'Delicious roasted chicken'
            },
            {
                'item_id': 'food_pie',
                'name': 'Meat Pie',
                'item_type': 'food',
                'quality': 'good',
                'cost': 15.0,
                'gold_bonus': 0.6,
                'patience_bonus': 18.0,
                'reputation_bonus': 0.15,
                'satisfaction_bonus': 30.0,
                'description': 'Rich and savory meat pie'
            },
            # FOOD - Fine
            {
                'item_id': 'food_feast',
                'name': 'Royal Feast',
                'item_type': 'food',
                'quality': 'fine',
                'cost': 30.0,
                'gold_bonus': 1.2,
                'patience_bonus': 25.0,
                'reputation_bonus': 0.3,
                'satisfaction_bonus': 45.0,
                'description': 'A magnificent feast fit for royalty'
            },
            # FOOD - Exquisite
            {
                'item_id': 'food_dragon_steak',
                'name': 'Dragon Steak',
                'item_type': 'food',
                'quality': 'exquisite',
                'cost': 80.0,
                'gold_bonus': 3.0,
                'patience_bonus': 35.0,
                'reputation_bonus': 0.8,
                'satisfaction_bonus': 60.0,
                'description': 'Legendary dragon meat, incredibly rare'
            },
            # BEVERAGES - Basic
            {
                'item_id': 'drink_water',
                'name': 'Water',
                'item_type': 'beverage',
                'quality': 'basic',
                'cost': 1.0,
                'patience_bonus': 3.0,
                'satisfaction_bonus': 5.0,
                'description': 'Fresh water from the well'
            },
            {
                'item_id': 'drink_ale',
                'name': 'Ale',
                'item_type': 'beverage',
                'quality': 'basic',
                'cost': 3.0,
                'gold_bonus': 0.15,
                'patience_bonus': 8.0,
                'satisfaction_bonus': 12.0,
                'description': 'Common ale, popular with adventurers'
            },
            # BEVERAGES - Good
            {
                'item_id': 'drink_mead',
                'name': 'Honey Mead',
                'item_type': 'beverage',
                'quality': 'good',
                'cost': 10.0,
                'gold_bonus': 0.4,
                'patience_bonus': 12.0,
                'reputation_bonus': 0.1,
                'satisfaction_bonus': 20.0,
                'description': 'Sweet mead made from honey'
            },
            {
                'item_id': 'drink_wine',
                'name': 'Fine Wine',
                'item_type': 'beverage',
                'quality': 'good',
                'cost': 18.0,
                'gold_bonus': 0.7,
                'patience_bonus': 15.0,
                'reputation_bonus': 0.2,
                'satisfaction_bonus': 28.0,
                'description': 'Quality wine from distant vineyards'
            },
            # BEVERAGES - Fine
            {
                'item_id': 'drink_elven_wine',
                'name': 'Elven Wine',
                'item_type': 'beverage',
                'quality': 'fine',
                'cost': 40.0,
                'gold_bonus': 1.5,
                'patience_bonus': 20.0,
                'reputation_bonus': 0.4,
                'satisfaction_bonus': 40.0,
                'description': 'Mystical wine from the elven forests'
            },
            # BEVERAGES - Exquisite
            {
                'item_id': 'drink_dwarven_ale',
                'name': 'Dwarven Ale',
                'item_type': 'beverage',
                'quality': 'exquisite',
                'cost': 60.0,
                'gold_bonus': 2.5,
                'patience_bonus': 30.0,
                'reputation_bonus': 0.6,
                'satisfaction_bonus': 55.0,
                'description': 'Legendary ale brewed by dwarves'
            },
            # BEVERAGES - Legendary
            {
                'item_id': 'drink_ambrosia',
                'name': 'Divine Ambrosia',
                'item_type': 'beverage',
                'quality': 'legendary',
                'cost': 100.0,
                'gold_bonus': 4.0,
                'patience_bonus': 40.0,
                'reputation_bonus': 1.0,
                'satisfaction_bonus': 70.0,
                'description': 'The drink of gods, impossibly rare'
            },
        ]

        for item_data in tavern_items:
            TavernItem.objects.create(**item_data)
            self.stdout.write(f'  Created: {item_data["name"]}')

    def _create_ingredients(self):
        """Create all ingredients"""
        ingredients = [
            # COMMON ingredients
            {
                'ingredient_id': 'ing_flour',
                'name': 'Flour',
                'rarity': 'common',
                'description': 'Basic flour for baking',
                'base_drop_chance': 0.30
            },
            {
                'ingredient_id': 'ing_water',
                'name': 'Fresh Water',
                'rarity': 'common',
                'description': 'Clean water from the well',
                'base_drop_chance': 0.35
            },
            {
                'ingredient_id': 'ing_salt',
                'name': 'Salt',
                'rarity': 'common',
                'description': 'Common salt for preserving',
                'base_drop_chance': 0.25
            },
            {
                'ingredient_id': 'ing_herbs',
                'name': 'Herbs',
                'rarity': 'common',
                'description': 'Wild herbs from the forest',
                'base_drop_chance': 0.30
            },
            # UNCOMMON ingredients
            {
                'ingredient_id': 'ing_meat',
                'name': 'Fresh Meat',
                'rarity': 'uncommon',
                'description': 'Meat from local hunters',
                'base_drop_chance': 0.15
            },
            {
                'ingredient_id': 'ing_honey',
                'name': 'Wild Honey',
                'rarity': 'uncommon',
                'description': 'Sweet honey from forest bees',
                'base_drop_chance': 0.12
            },
            {
                'ingredient_id': 'ing_grapes',
                'name': 'Grapes',
                'rarity': 'uncommon',
                'description': 'Fresh grapes for wine',
                'base_drop_chance': 0.10
            },
            {
                'ingredient_id': 'ing_spices',
                'name': 'Exotic Spices',
                'rarity': 'uncommon',
                'description': 'Rare spices from distant lands',
                'base_drop_chance': 0.08
            },
            # RARE ingredients
            {
                'ingredient_id': 'ing_truffle',
                'name': 'Truffle',
                'rarity': 'rare',
                'description': 'Rare truffle mushroom',
                'base_drop_chance': 0.05
            },
            {
                'ingredient_id': 'ing_elven_herbs',
                'name': 'Elven Herbs',
                'rarity': 'rare',
                'description': 'Mystical herbs from elven forests',
                'base_drop_chance': 0.04
            },
            {
                'ingredient_id': 'ing_aged_wine',
                'name': 'Aged Wine Base',
                'rarity': 'rare',
                'description': 'Wine aged in ancient barrels',
                'base_drop_chance': 0.03
            },
            # EPIC ingredients
            {
                'ingredient_id': 'ing_phoenix_feather',
                'name': 'Phoenix Feather',
                'rarity': 'epic',
                'description': 'A feather from a phoenix, incredibly rare',
                'base_drop_chance': 0.02
            },
            {
                'ingredient_id': 'ing_dragon_blood',
                'name': 'Dragon Blood',
                'rarity': 'epic',
                'description': 'Blood from a dragon, very powerful',
                'base_drop_chance': 0.015
            },
            {
                'ingredient_id': 'ing_moonflower',
                'name': 'Moonflower',
                'rarity': 'epic',
                'description': 'Flower that blooms only under full moon',
                'base_drop_chance': 0.01
            },
            # LEGENDARY ingredients
            {
                'ingredient_id': 'ing_ambrosia_essence',
                'name': 'Ambrosia Essence',
                'rarity': 'legendary',
                'description': 'Divine essence from the gods',
                'base_drop_chance': 0.005
            },
            {
                'ingredient_id': 'ing_time_crystal',
                'name': 'Time Crystal',
                'rarity': 'legendary',
                'description': 'Crystal that holds the essence of time itself',
                'base_drop_chance': 0.003
            },
        ]

        for ing_data in ingredients:
            Ingredient.objects.create(**ing_data)
            self.stdout.write(f'  Created: {ing_data["name"]} ({ing_data["rarity"]})')
