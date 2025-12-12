from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


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


# ============================================================================
# TEMPLATE MODELS - Shared across all players
# ============================================================================

class RoomTypeTemplate(models.Model):
    """Template defining room type attributes"""
    room_type_id = models.CharField(max_length=50, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(default="")

    # Costs and attributes
    base_cost = models.FloatField(default=50.0)
    income_multiplier = models.FloatField(default=1.0)

    # Display
    emoji = models.CharField(max_length=10, default="🏠")

    # Requirements (optional) - which upgrade is needed to unlock this room type
    required_upgrade = models.ForeignKey(
        'UpgradeTemplate',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='unlocks_room_types'
    )

    class Meta:
        verbose_name = "Room Type Template"
        verbose_name_plural = "Room Type Templates"
        ordering = ['base_cost']

    def __str__(self):
        return f"{self.emoji} {self.name} (×{self.income_multiplier})"


class UpgradeTemplate(models.Model):
    """Template defining upgrade attributes"""
    upgrade_id = models.CharField(max_length=100, unique=True, primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()

    # Cost and effects
    cost = models.FloatField(default=0.0)
    effect_type = models.CharField(max_length=50)
    effect_value = models.FloatField(default=0.0)

    # Requirements (optional)
    required_upgrade = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='unlocks'
    )

    class Meta:
        verbose_name = "Upgrade Template"
        verbose_name_plural = "Upgrade Templates"
        ordering = ['cost']

    def __str__(self):
        return f"{self.name} (${self.cost:.0f})"


class RecipeTemplate(models.Model):
    """Template defining recipe attributes - shared across all players"""
    recipe_id = models.CharField(max_length=100, unique=True, primary_key=True)
    name = models.CharField(max_length=200)
    item = models.ForeignKey('TavernItem', on_delete=models.CASCADE, related_name='recipe_templates')

    # Required ingredients (stored as JSON)
    # Format: [{"ingredient_id": "flour", "quantity": 2}, ...]
    required_ingredients = models.JSONField(default=list)

    # Costs
    cost_to_unlock = models.FloatField(default=0.0)
    ingredients_cost = models.FloatField(default=0.0)

    # Discovery settings
    discoverable = models.BooleanField(default=True)  # Can be discovered through experimentation
    auto_unlocked = models.BooleanField(default=False)  # Automatically unlocked for new players

    class Meta:
        verbose_name = "Recipe Template"
        verbose_name_plural = "Recipe Templates"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} → {self.item.name}"


# ============================================================================
# GAME STATE AND PLAYER-SPECIFIC MODELS
# ============================================================================

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
    """Inn rooms - player-specific instances"""
    game_state = models.ForeignKey(GameState, on_delete=models.CASCADE, related_name='rooms')
    room_template = models.ForeignKey(RoomTypeTemplate, on_delete=models.PROTECT, related_name='instances')

    # Player-specific attributes
    level = models.IntegerField(default=1)
    occupied = models.BooleanField(default=False)
    cleanliness = models.FloatField(default=100.0)

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"

    @property
    def income_rate(self):
        """Calculate income rate based on template and level"""
        return self.room_template.income_multiplier * self.level

    @property
    def room_type(self):
        """Get room type from template for backward compatibility"""
        return self.room_template.room_type_id

    def __str__(self):
        status = "Occupied" if self.occupied else "Empty"
        return f"{self.room_template.name} Lv.{self.level} ({status})"


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


class PlayerRecipe(models.Model):
    """Player-specific recipe discovery tracking"""
    game_state = models.ForeignKey(GameState, on_delete=models.CASCADE, related_name='player_recipes')
    recipe_template = models.ForeignKey(RecipeTemplate, on_delete=models.PROTECT, related_name='player_instances')

    # Discovery status
    discovered = models.BooleanField(default=False)
    discovered_at = models.DateTimeField(null=True, blank=True)

    # Unlock status (some recipes might need to be unlocked with gold after discovery)
    unlocked = models.BooleanField(default=False)
    unlocked_at = models.DateTimeField(null=True, blank=True)

    # Stats
    times_crafted = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Player Recipe"
        verbose_name_plural = "Player Recipes"
        unique_together = [['game_state', 'recipe_template']]
        ordering = ['-discovered_at']

    # Properties for backward compatibility
    @property
    def recipe_id(self):
        return self.recipe_template.recipe_id

    @property
    def name(self):
        return self.recipe_template.name

    @property
    def item(self):
        return self.recipe_template.item

    @property
    def required_ingredients(self):
        return self.recipe_template.required_ingredients

    @property
    def cost_to_unlock(self):
        return self.recipe_template.cost_to_unlock

    @property
    def ingredients_cost(self):
        return self.recipe_template.ingredients_cost

    def __str__(self):
        if self.unlocked:
            status = "✓ Unlocked"
        elif self.discovered:
            status = "? Discovered"
        else:
            status = "✗ Hidden"
        return f"{status} {self.name}"


class Upgrade(models.Model):
    """Player's purchased upgrades - created only when purchased"""
    game_state = models.ForeignKey(GameState, on_delete=models.CASCADE, related_name='purchased_upgrades')
    upgrade_template = models.ForeignKey(UpgradeTemplate, on_delete=models.PROTECT, related_name='player_purchases')

    # Purchase tracking
    purchased_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Purchased Upgrade"
        verbose_name_plural = "Purchased Upgrades"
        unique_together = [['game_state', 'upgrade_template']]

    # Properties for backward compatibility
    @property
    def upgrade_id(self):
        return self.upgrade_template.upgrade_id

    @property
    def id(self):
        return self.upgrade_template.upgrade_id

    @property
    def name(self):
        return self.upgrade_template.name

    @property
    def description(self):
        return self.upgrade_template.description

    @property
    def cost(self):
        return self.upgrade_template.cost

    @property
    def effect_type(self):
        return self.upgrade_template.effect_type

    @property
    def effect_value(self):
        return self.upgrade_template.effect_value

    @property
    def purchased(self):
        """For backward compatibility - always True since existence = purchased"""
        return True

    def __str__(self):
        return f"✓ {self.name}"
