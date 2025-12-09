from django.db import models
from django.contrib.auth.models import User


class RoomType(models.TextChoices):
    BASIC = 'basic', 'Basic'
    STANDARD = 'standard', 'Standard'
    DELUXE = 'deluxe', 'Deluxe'
    ROYAL = 'royal', 'Royal'


class GuestType(models.TextChoices):
    PEASANT = 'peasant', 'Peasant'
    MERCHANT = 'merchant', 'Merchant'
    NOBLE = 'noble', 'Noble'
    ADVENTURER = 'adventurer', 'Adventurer'
    WIZARD = 'wizard', 'Wizard'
    BANDIT = 'bandit', 'Bandit'
    MONK = 'monk', 'Monk'
    BARD = 'bard', 'Bard'
    DRAGON_DISGUISED = 'dragon_disguised', 'Dragon (Disguised)'
    BEGGAR = 'beggar', 'Beggar'
    PRINCE = 'prince', 'Prince'
    THIEF = 'thief', 'Thief'
    SCHOLAR = 'scholar', 'Scholar'
    DRUNK = 'drunk', 'Drunk'
    GHOST = 'ghost', 'Ghost'


class ItemType(models.TextChoices):
    FOOD = 'food', 'Food'
    BEVERAGE = 'beverage', 'Beverage'


class ItemQuality(models.TextChoices):
    BASIC = 'basic', 'Basic'
    GOOD = 'good', 'Good'
    FINE = 'fine', 'Fine'
    EXQUISITE = 'exquisite', 'Exquisite'
    LEGENDARY = 'legendary', 'Legendary'


class IngredientRarity(models.TextChoices):
    COMMON = 'common', 'Common'
    UNCOMMON = 'uncommon', 'Uncommon'
    RARE = 'rare', 'Rare'
    EPIC = 'epic', 'Epic'
    LEGENDARY = 'legendary', 'Legendary'


class GameState(models.Model):
    """Main game state for a player"""
    player_id = models.CharField(max_length=100, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    # Resources
    gold = models.FloatField(default=100.0)
    reputation = models.FloatField(default=0.0)
    max_guests = models.IntegerField(default=5)

    # Game settings
    total_income_multiplier = models.FloatField(default=1.0)
    auto_clean_enabled = models.BooleanField(default=False)
    game_speed = models.FloatField(default=1.0)
    tavern_unlocked = models.BooleanField(default=False)

    # Inventories (stored as JSON)
    item_inventory = models.JSONField(default=dict)  # {item_id: quantity}
    ingredient_inventory = models.JSONField(default=dict)  # {ingredient_id: quantity}

    class Meta:
        verbose_name = "Game State"
        verbose_name_plural = "Game States"
        ordering = ['-last_update']

    def __str__(self):
        return f"Game State: {self.player_id} (Gold: {self.gold:.0f})"


class Room(models.Model):
    """Inn rooms"""
    game_state = models.ForeignKey(GameState, on_delete=models.CASCADE, related_name='rooms')
    room_type = models.CharField(max_length=20, choices=RoomType.choices, default=RoomType.BASIC)
    level = models.IntegerField(default=1)
    occupied = models.BooleanField(default=False)
    income_rate = models.FloatField(default=1.0)
    cleanliness = models.FloatField(default=100.0)

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"

    def __str__(self):
        status = "Occupied" if self.occupied else "Empty"
        return f"{self.get_room_type_display()} Room Lv.{self.level} ({status})"


class Guest(models.Model):
    """Guests staying at the inn"""
    game_state = models.ForeignKey(GameState, on_delete=models.CASCADE, related_name='guests')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_guest')

    name = models.CharField(max_length=100)
    guest_type = models.CharField(max_length=20, choices=GuestType.choices)

    # Stats
    patience = models.FloatField(default=100.0)
    satisfaction = models.FloatField(default=50.0)
    gold_per_tick = models.FloatField(default=1.0)
    reputation_bonus = models.FloatField(default=0.1)
    stay_duration = models.IntegerField(default=10)

    # Service tracking
    fed = models.BooleanField(default=False)
    served_drink = models.BooleanField(default=False)
    food_served = models.CharField(max_length=100, null=True, blank=True)
    beverage_served = models.CharField(max_length=100, null=True, blank=True)

    # Timestamps
    check_in_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Guest"
        verbose_name_plural = "Guests"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_guest_type_display()})"


class TavernItem(models.Model):
    """Food and beverage items"""
    item_id = models.CharField(max_length=100, unique=True, db_index=True)
    name = models.CharField(max_length=100)
    item_type = models.CharField(max_length=20, choices=ItemType.choices)
    quality = models.CharField(max_length=20, choices=ItemQuality.choices)

    # Costs and bonuses
    cost = models.FloatField(default=0.0)
    gold_bonus = models.FloatField(default=0.0)
    patience_bonus = models.FloatField(default=0.0)
    reputation_bonus = models.FloatField(default=0.0)
    satisfaction_bonus = models.FloatField(default=0.0)

    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Tavern Item"
        verbose_name_plural = "Tavern Items"
        ordering = ['item_type', 'quality']

    def __str__(self):
        return f"{self.name} ({self.get_quality_display()} {self.get_item_type_display()})"


class Ingredient(models.Model):
    """Crafting ingredients"""
    ingredient_id = models.CharField(max_length=100, unique=True, db_index=True)
    name = models.CharField(max_length=100)
    rarity = models.CharField(max_length=20, choices=IngredientRarity.choices)
    base_drop_chance = models.FloatField(default=0.1)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Ingredient"
        verbose_name_plural = "Ingredients"
        ordering = ['rarity', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_rarity_display()})"


class Recipe(models.Model):
    """Crafting recipes"""
    game_state = models.ForeignKey(GameState, on_delete=models.CASCADE, related_name='recipes')
    recipe_id = models.CharField(max_length=100, db_index=True)
    name = models.CharField(max_length=200)
    item = models.ForeignKey(TavernItem, on_delete=models.CASCADE, related_name='recipes')

    # Status
    unlocked = models.BooleanField(default=False)
    discovered = models.BooleanField(default=False)

    # Costs
    cost_to_unlock = models.FloatField(default=0.0)
    ingredients_cost = models.FloatField(default=0.0)

    # Required ingredients (stored as JSON)
    required_ingredients = models.JSONField(default=list)  # [{ingredient_id: str, quantity: int}]

    class Meta:
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"
        unique_together = [['game_state', 'recipe_id']]

    def __str__(self):
        status = "Unlocked" if self.unlocked else "Locked"
        return f"{self.name} ({status})"


class Upgrade(models.Model):
    """Purchasable upgrades"""
    game_state = models.ForeignKey(GameState, on_delete=models.CASCADE, related_name='upgrades')
    upgrade_id = models.CharField(max_length=100, db_index=True)
    name = models.CharField(max_length=200)
    description = models.TextField()

    cost = models.FloatField(default=0.0)
    purchased = models.BooleanField(default=False)

    effect_type = models.CharField(max_length=50)
    effect_value = models.FloatField(default=0.0)

    class Meta:
        verbose_name = "Upgrade"
        verbose_name_plural = "Upgrades"
        unique_together = [['game_state', 'upgrade_id']]

    def __str__(self):
        status = "✓" if self.purchased else "✗"
        return f"{status} {self.name}"
