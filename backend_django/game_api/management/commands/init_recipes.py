"""
Management command to initialize recipe templates
"""
from django.core.management.base import BaseCommand
from game_api.models import RecipeTemplate, TavernItem


class Command(BaseCommand):
    help = 'Initialize recipe templates for all tavern items'

    def handle(self, *args, **options):
        self.stdout.write('Initializing recipe templates...')

        # Clear existing recipes
        RecipeTemplate.objects.all().delete()

        # Create recipes
        self._create_recipes()

        self.stdout.write(self.style.SUCCESS('Recipe templates initialized successfully!'))

    def _create_recipes(self):
        """Create all recipe templates"""
        recipes = [
            # FOOD - Basic
            {
                'recipe_id': 'recipe_bread',
                'name': 'Simple Bread Recipe',
                'item_id': 'food_bread',
                'required_ingredients': [
                    {'ingredient_id': 'ing_flour', 'quantity': 2},
                    {'ingredient_id': 'ing_water', 'quantity': 1},
                ],
                'cost_to_unlock': 0.0,
                'ingredients_cost': 3.0,
                'discoverable': True,
                'auto_unlocked': True  # Basic recipe, available from start
            },
            {
                'recipe_id': 'recipe_stew',
                'name': 'Vegetable Stew Recipe',
                'item_id': 'food_stew',
                'required_ingredients': [
                    {'ingredient_id': 'ing_water', 'quantity': 2},
                    {'ingredient_id': 'ing_herbs', 'quantity': 2},
                    {'ingredient_id': 'ing_salt', 'quantity': 1},
                ],
                'cost_to_unlock': 0.0,
                'ingredients_cost': 5.0,
                'discoverable': True,
                'auto_unlocked': True
            },
            # FOOD - Good
            {
                'recipe_id': 'recipe_roast',
                'name': 'Roasted Chicken Recipe',
                'item_id': 'food_roast',
                'required_ingredients': [
                    {'ingredient_id': 'ing_meat', 'quantity': 3},
                    {'ingredient_id': 'ing_herbs', 'quantity': 1},
                    {'ingredient_id': 'ing_salt', 'quantity': 1},
                ],
                'cost_to_unlock': 10.0,
                'ingredients_cost': 12.0,
                'discoverable': True,
                'auto_unlocked': False
            },
            {
                'recipe_id': 'recipe_pie',
                'name': 'Meat Pie Recipe',
                'item_id': 'food_pie',
                'required_ingredients': [
                    {'ingredient_id': 'ing_flour', 'quantity': 2},
                    {'ingredient_id': 'ing_meat', 'quantity': 2},
                    {'ingredient_id': 'ing_spices', 'quantity': 1},
                ],
                'cost_to_unlock': 15.0,
                'ingredients_cost': 15.0,
                'discoverable': True,
                'auto_unlocked': False
            },
            # FOOD - Fine
            {
                'recipe_id': 'recipe_feast',
                'name': 'Royal Feast Recipe',
                'item_id': 'food_feast',
                'required_ingredients': [
                    {'ingredient_id': 'ing_meat', 'quantity': 4},
                    {'ingredient_id': 'ing_spices', 'quantity': 2},
                    {'ingredient_id': 'ing_truffle', 'quantity': 1},
                ],
                'cost_to_unlock': 50.0,
                'ingredients_cost': 30.0,
                'discoverable': True,
                'auto_unlocked': False
            },
            # FOOD - Exquisite
            {
                'recipe_id': 'recipe_dragon_steak',
                'name': 'Dragon Steak Recipe',
                'item_id': 'food_dragon_steak',
                'required_ingredients': [
                    {'ingredient_id': 'ing_dragon_blood', 'quantity': 3},
                    {'ingredient_id': 'ing_spices', 'quantity': 2},
                    {'ingredient_id': 'ing_phoenix_feather', 'quantity': 1},
                ],
                'cost_to_unlock': 200.0,
                'ingredients_cost': 80.0,
                'discoverable': True,
                'auto_unlocked': False
            },
            # BEVERAGES - Basic
            {
                'recipe_id': 'recipe_water',
                'name': 'Fresh Water',
                'item_id': 'drink_water',
                'required_ingredients': [
                    {'ingredient_id': 'ing_water', 'quantity': 1},
                ],
                'cost_to_unlock': 0.0,
                'ingredients_cost': 1.0,
                'discoverable': True,
                'auto_unlocked': True
            },
            {
                'recipe_id': 'recipe_ale',
                'name': 'Common Ale Recipe',
                'item_id': 'drink_ale',
                'required_ingredients': [
                    {'ingredient_id': 'ing_flour', 'quantity': 1},
                    {'ingredient_id': 'ing_water', 'quantity': 2},
                    {'ingredient_id': 'ing_honey', 'quantity': 1},
                ],
                'cost_to_unlock': 0.0,
                'ingredients_cost': 3.0,
                'discoverable': True,
                'auto_unlocked': True
            },
            # BEVERAGES - Good
            {
                'recipe_id': 'recipe_mead',
                'name': 'Honey Mead Recipe',
                'item_id': 'drink_mead',
                'required_ingredients': [
                    {'ingredient_id': 'ing_honey', 'quantity': 3},
                    {'ingredient_id': 'ing_water', 'quantity': 2},
                ],
                'cost_to_unlock': 10.0,
                'ingredients_cost': 10.0,
                'discoverable': True,
                'auto_unlocked': False
            },
            {
                'recipe_id': 'recipe_wine',
                'name': 'Fine Wine Recipe',
                'item_id': 'drink_wine',
                'required_ingredients': [
                    {'ingredient_id': 'ing_grapes', 'quantity': 4},
                    {'ingredient_id': 'ing_water', 'quantity': 1},
                ],
                'cost_to_unlock': 20.0,
                'ingredients_cost': 18.0,
                'discoverable': True,
                'auto_unlocked': False
            },
            # BEVERAGES - Fine
            {
                'recipe_id': 'recipe_elven_wine',
                'name': 'Elven Wine Recipe',
                'item_id': 'drink_elven_wine',
                'required_ingredients': [
                    {'ingredient_id': 'ing_aged_wine', 'quantity': 2},
                    {'ingredient_id': 'ing_elven_herbs', 'quantity': 2},
                    {'ingredient_id': 'ing_moonflower', 'quantity': 1},
                ],
                'cost_to_unlock': 80.0,
                'ingredients_cost': 40.0,
                'discoverable': True,
                'auto_unlocked': False
            },
            # BEVERAGES - Exquisite
            {
                'recipe_id': 'recipe_dwarven_ale',
                'name': 'Dwarven Ale Recipe',
                'item_id': 'drink_dwarven_ale',
                'required_ingredients': [
                    {'ingredient_id': 'ing_honey', 'quantity': 3},
                    {'ingredient_id': 'ing_truffle', 'quantity': 2},
                    {'ingredient_id': 'ing_herbs', 'quantity': 3},
                ],
                'cost_to_unlock': 100.0,
                'ingredients_cost': 60.0,
                'discoverable': True,
                'auto_unlocked': False
            },
            # BEVERAGES - Legendary
            {
                'recipe_id': 'recipe_ambrosia',
                'name': 'Divine Ambrosia Recipe',
                'item_id': 'drink_ambrosia',
                'required_ingredients': [
                    {'ingredient_id': 'ing_ambrosia_essence', 'quantity': 5},
                    {'ingredient_id': 'ing_phoenix_feather', 'quantity': 2},
                    {'ingredient_id': 'ing_moonflower', 'quantity': 2},
                    {'ingredient_id': 'ing_time_crystal', 'quantity': 1},
                ],
                'cost_to_unlock': 500.0,
                'ingredients_cost': 100.0,
                'discoverable': True,
                'auto_unlocked': False
            },
        ]

        for recipe_data in recipes:
            item_id = recipe_data.pop('item_id')
            try:
                item = TavernItem.objects.get(item_id=item_id)
                RecipeTemplate.objects.create(
                    item=item,
                    **recipe_data
                )
                self.stdout.write(f'  Created: {recipe_data["name"]} → {item.name}')
            except TavernItem.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'  Skipped {recipe_data["name"]}: Item {item_id} not found')
                )
