from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from django_lifecycle import LifecycleModelMixin, hook

class RoomType(models.TextChoices):
    BASIC = 'basic', 'Basic'
    STANDARD = 'standard', 'Standard'
    DELUXE = 'deluxe', 'Deluxe'
    ROYAL = 'royal', 'Royal'
    EXTREME = 'extreme', 'Extreme'


class GuestType(models.TextChoices):
    # Common travelers
    PEASANT = 'peasant', 'Peasant'
    MERCHANT = 'merchant', 'Merchant'
    NOBLE = 'noble', 'Noble'
    ADVENTURER = 'adventurer', 'Adventurer'

    # Magical types
    WIZARD = 'wizard', 'Wizard'
    SORCERER = 'sorcerer', 'Sorcerer'
    WITCH = 'witch', 'Witch'
    ALCHEMIST = 'alchemist', 'Alchemist'
    NECROMANCER = 'necromancer', 'Necromancer'

    # Warriors
    KNIGHT = 'knight', 'Knight'
    PALADIN = 'paladin', 'Paladin'
    RANGER = 'ranger', 'Ranger'
    BARBARIAN = 'barbarian', 'Barbarian'
    SAMURAI = 'samurai', 'Samurai'

    # Rogues/Outlaws
    BANDIT = 'bandit', 'Bandit'
    THIEF = 'thief', 'Thief'
    ASSASSIN = 'assassin', 'Assassin'
    SMUGGLER = 'smuggler', 'Smuggler'

    # Religious/Spiritual
    MONK = 'monk', 'Monk'
    PRIEST = 'priest', 'Priest'
    CLERIC = 'cleric', 'Cleric'
    DRUID = 'druid', 'Druid'

    # Entertainers
    BARD = 'bard', 'Bard'
    JESTER = 'jester', 'Jester'
    MINSTREL = 'minstrel', 'Minstrel'
    ACTOR = 'actor', 'Actor'

    # Craftspeople
    BLACKSMITH = 'blacksmith', 'Blacksmith'
    CARPENTER = 'carpenter', 'Carpenter'
    JEWELER = 'jeweler', 'Jeweler'
    TAILOR = 'tailor', 'Tailor'

    # Scholars
    SCHOLAR = 'scholar', 'Scholar'
    SCRIBE = 'scribe', 'Scribe'
    LIBRARIAN = 'librarian', 'Librarian'
    HISTORIAN = 'historian', 'Historian'

    # Exotic/Rare
    DRAGON_DISGUISED = 'dragon_disguised', 'Dragon (Disguised)'
    VAMPIRE = 'vampire', 'Vampire'
    WEREWOLF = 'werewolf', 'Werewolf'
    ELF = 'elf', 'Elf'
    DWARF = 'dwarf', 'Dwarf'
    HALFLING = 'halfling', 'Halfling'
    ORC = 'orc', 'Orc'

    # Special
    BEGGAR = 'beggar', 'Beggar'
    PRINCE = 'prince', 'Prince'
    PIRATE = 'pirate', 'Pirate'
    SPY = 'spy', 'Spy'
    DRUNK = 'drunk', 'Drunk'
    GHOST = 'ghost', 'Ghost'


class GuestSpecies(models.TextChoices):
    """Guest species/races from Faerun (D&D) and Daggerheart"""

    # ========================================================================
    # COMMON RACES (appear frequently)
    # ========================================================================
    HUMAN = 'human', 'Human'
    ELF = 'elf', 'Elf'
    DWARF = 'dwarf', 'Dwarf'
    HALFLING = 'halfling', 'Halfling'
    GNOME = 'gnome', 'Gnome'
    HALF_ELF = 'half_elf', 'Half-Elf'
    HALF_ORC = 'half_orc', 'Half-Orc'
    ORC = 'orc', 'Orc'

    # ========================================================================
    # FAERUN RACES (D&D Forgotten Realms)
    # ========================================================================

    # Elven subraces
    HIGH_ELF = 'high_elf', 'High Elf'
    WOOD_ELF = 'wood_elf', 'Wood Elf'
    DROW = 'drow', 'Drow (Dark Elf)'
    ELADRIN = 'eladrin', 'Eladrin'
    SEA_ELF = 'sea_elf', 'Sea Elf'

    # Dwarven subraces
    MOUNTAIN_DWARF = 'mountain_dwarf', 'Mountain Dwarf'
    HILL_DWARF = 'hill_dwarf', 'Hill Dwarf'
    DUERGAR = 'duergar', 'Duergar (Gray Dwarf)'

    # Halfling subraces
    LIGHTFOOT_HALFLING = 'lightfoot_halfling', 'Lightfoot Halfling'
    STOUT_HALFLING = 'stout_halfling', 'Stout Halfling'
    GHOSTWISE_HALFLING = 'ghostwise_halfling', 'Ghostwise Halfling'

    # Gnome subraces
    ROCK_GNOME = 'rock_gnome', 'Rock Gnome'
    FOREST_GNOME = 'forest_gnome', 'Forest Gnome'
    DEEP_GNOME = 'deep_gnome', 'Deep Gnome (Svirfneblin)'

    # Exotic D&D races
    DRAGONBORN = 'dragonborn', 'Dragonborn'
    TIEFLING = 'tiefling', 'Tiefling'
    AASIMAR = 'aasimar', 'Aasimar'
    GOLIATH = 'goliath', 'Goliath'
    FIRBOLG = 'firbolg', 'Firbolg'
    KENKU = 'kenku', 'Kenku'
    TABAXI = 'tabaxi', 'Tabaxi'
    TORTLE = 'tortle', 'Tortle'
    LIZARDFOLK = 'lizardfolk', 'Lizardfolk'
    AARAKOCRA = 'aarakocra', 'Aarakocra'
    TRITON = 'triton', 'Triton'
    WARFORGED = 'warforged', 'Warforged'
    CHANGELING = 'changeling', 'Changeling'
    KALASHTAR = 'kalashtar', 'Kalashtar'
    SHIFTER = 'shifter', 'Shifter'
    YUAN_TI_PUREBLOOD = 'yuan_ti_pureblood', 'Yuan-ti Pureblood'

    # Genasi (elemental-touched)
    FIRE_GENASI = 'fire_genasi', 'Fire Genasi'
    WATER_GENASI = 'water_genasi', 'Water Genasi'
    AIR_GENASI = 'air_genasi', 'Air Genasi'
    EARTH_GENASI = 'earth_genasi', 'Earth Genasi'

    # Monstrous races
    GOBLIN = 'goblin', 'Goblin'
    HOBGOBLIN = 'hobgoblin', 'Hobgoblin'
    BUGBEAR = 'bugbear', 'Bugbear'
    KOBOLD = 'kobold', 'Kobold'
    MINOTAUR = 'minotaur', 'Minotaur'
    CENTAUR = 'centaur', 'Centaur'
    SATYR = 'satyr', 'Satyr'
    HARENGON = 'harengon', 'Harengon (Rabbitfolk)'
    OWLIN = 'owlin', 'Owlin'
    FAIRY = 'fairy', 'Fairy'

    # ========================================================================
    # DAGGERHEART RACES (Critical Role)
    # ========================================================================
    FAERIE = 'faerie', 'Faerie'  # Daggerheart fey
    DAEMON = 'daemon', 'Daemon'  # Daggerheart demon-touched
    DRAKONA = 'drakona', 'Drakona'  # Daggerheart dragonborn
    CLANK = 'clank', 'Clank'  # Daggerheart construct/robot
    GALAPA = 'galapa', 'Galapa'  # Daggerheart turtle people
    RIBBET = 'ribbet', 'Ribbet'  # Daggerheart frog people
    SIMIAH = 'simiah', 'Simiah'  # Daggerheart ape people
    INFERIS = 'inferis', 'Inferis'  # Daggerheart infernal
    KATARI = 'katari', 'Katari'  # Daggerheart cat people
    FUNGRIL = 'fungril', 'Fungril'  # Daggerheart mushroom people

    # ========================================================================
    # RARE/LEGENDARY SPECIES
    # ========================================================================
    DRAGON = 'dragon', 'Dragon (Polymorphed)'
    VAMPIRE = 'vampire', 'Vampire'
    LYCANTHROPE = 'lycanthrope', 'Lycanthrope'
    LICH = 'lich', 'Lich'
    REVENANT = 'revenant', 'Revenant'
    GITHYANKI = 'githyanki', 'Githyanki'
    GITHZERAI = 'githzerai', 'Githzerai'
    MODRON = 'modron', 'Modron'
    PLASMOID = 'plasmoid', 'Plasmoid'
    AUTOGNOME = 'autognome', 'Autognome'
    HADOZEE = 'hadozee', 'Hadozee'
    THRI_KREEN = 'thri_kreen', 'Thri-kreen'
    GIFF = 'giff', 'Giff'


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
    cost = models.FloatField(default=0.0)  # Cost in gold (for free upgrades)
    effect_type = models.CharField(max_length=50)
    effect_value = models.FloatField(default=0.0)

    # Premium/monetization fields
    is_premium = models.BooleanField(default=False)  # Requires real money purchase
    premium_price_cents = models.IntegerField(default=0)  # Price in USD cents (e.g., 99 = $0.99)

    # Temporary buff fields
    duration_seconds = models.IntegerField(default=0)  # 0 = permanent, >0 = temporary buff
    is_consumable = models.BooleanField(default=False)  # Can be purchased multiple times

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
        if self.is_premium:
            return f"{self.name} (${self.premium_price_cents/100:.2f})"
        return f"{self.name} ({self.cost:.0f}g)"


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

class GameState(LifecycleModelMixin, models.Model):
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

    # Offline timer settings (in hours)
    max_offline_hours = models.FloatField(default=12.0)  # Can be upgraded to 24, 48
    last_online = models.DateTimeField(default=timezone.now)
    last_offline_earnings = models.FloatField(default=0.0)  # For display purposes
    last_offline_hours = models.FloatField(default=0.0)  # For display purposes

    # Map location
    map_world = models.CharField(max_length=1000, default="toril")
    map_x = models.IntegerField(default=0)  # X coordinate on the map
    map_y = models.IntegerField(default=0)  # Y coordinate on the map
    inn_name = models.CharField(max_length=1000, default="Inn")

    # Inventories (stored as JSON)
    item_inventory = models.JSONField(default=dict)  # {item_id: quantity}
    ingredient_inventory = models.JSONField(default=dict)  # {ingredient_id: quantity}

    class Meta:
        verbose_name = "Game State"
        verbose_name_plural = "Game States"
        ordering = ['-last_update']

    def __str__(self):
        return f"Game State: {self.player_id} (Gold: {self.gold:.0f})"


    #@hook('after_update')
    #def on_after_update(obj):
    #    from game_api.serializers import GameStateSerializer
    #    from game_api.mqtt_service import get_mqtt_service
    #    mqtt_service = get_mqtt_service()
    #    serializer = GameStateSerializer(obj)
    #    data = serializer.data
    #    mqtt_service.publish_game_state(obj.player_id, data)





class ActiveBuff(models.Model):
    """Active temporary buffs on a player's game state"""
    game_state = models.ForeignKey(GameState, on_delete=models.CASCADE, related_name='active_buffs')
    upgrade_template = models.ForeignKey(UpgradeTemplate, on_delete=models.PROTECT, related_name='active_instances')

    # Timing
    activated_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()  # When the buff expires

    # Status
    active = models.BooleanField(default=True)  # False if manually deactivated or expired

    class Meta:
        verbose_name = "Active Buff"
        verbose_name_plural = "Active Buffs"
        ordering = ['-activated_at']
        indexes = [
            models.Index(fields=['game_state', 'active', 'expires_at']),
        ]

    def is_expired(self):
        """Check if buff has expired"""
        return timezone.now() >= self.expires_at

    def __str__(self):
        status = "Active" if self.active and not self.is_expired() else "Expired"
        return f"{status}: {self.upgrade_template.name} for {self.game_state.player_id}"


class PremiumPurchase(models.Model):
    """Track real money purchases via Stripe"""

    class PurchaseStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'
        REFUNDED = 'refunded', 'Refunded'

    game_state = models.ForeignKey(GameState, on_delete=models.CASCADE, related_name='premium_purchases')
    upgrade_template = models.ForeignKey(UpgradeTemplate, on_delete=models.PROTECT, related_name='purchases')

    # Stripe info
    stripe_payment_intent_id = models.CharField(max_length=200, unique=True, db_index=True)
    stripe_checkout_session_id = models.CharField(max_length=200, blank=True, default='')

    # Purchase details
    amount_cents = models.IntegerField()  # Amount in cents
    currency = models.CharField(max_length=3, default='usd')
    status = models.CharField(max_length=20, choices=PurchaseStatus.choices, default=PurchaseStatus.PENDING)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    # Metadata
    metadata = models.JSONField(default=dict, blank=True)  # For storing extra info

    class Meta:
        verbose_name = "Premium Purchase"
        verbose_name_plural = "Premium Purchases"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['stripe_payment_intent_id']),
            models.Index(fields=['game_state', 'status']),
        ]

    def __str__(self):
        return f"{self.game_state.player_id} - {self.upgrade_template.name} (${self.amount_cents/100:.2f}) - {self.status}"


class Room(models.Model):
    """Inn rooms - player-specific instances"""
    game_state = models.ForeignKey(GameState, on_delete=models.CASCADE, related_name='rooms')
    room_template = models.ForeignKey(RoomTypeTemplate, on_delete=models.PROTECT, related_name='instances')

    # Player-specific attributes
    level = models.IntegerField(default=1)
    occupied = models.BooleanField(default=False)
    cleanliness = models.FloatField(default=100.0)
    customers_served = models.IntegerField(default=0)  # Track customers for auto-leveling

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"

    def check_and_level_up(self):
        """Check if room should level up based on customers served"""
        # Level thresholds: 10, 100, 1000 customers
        thresholds = [
            (1, 10),    # Level 1 -> 2 at 10 customers
            (2, 100),   # Level 2 -> 3 at 100 customers
            (3, 1000),  # Level 3 -> 4 at 1000 customers
        ]

        for current_level, threshold in thresholds:
            if self.level == current_level and self.customers_served >= threshold:
                self.level += 1
                return True  # Leveled up

        return False  # No level up

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
    species = models.CharField(max_length=30, choices=GuestSpecies.choices, default=GuestSpecies.HUMAN)

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

    # Market availability and pricing
    is_purchasable = models.BooleanField(default=False)  # Can be bought in store
    market_price = models.FloatField(default=0.0)  # Price in gold (0 if not purchasable)

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
