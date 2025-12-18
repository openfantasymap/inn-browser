from rest_framework import serializers
from django.core.cache import cache
from .models import (
    GameState, Room, Guest, TavernItem, Ingredient, PlayerRecipe, Upgrade, UpgradeTemplate,
    ActiveBuff, PremiumPurchase, Achievement, PlayerAchievement
)


class RoomSerializer(serializers.ModelSerializer):
    """Serializer for Room model"""
    current_guest = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ['id', 'room_type', 'level', 'occupied', 'current_guest',
                  'income_rate', 'cleanliness', 'customers_served']

    def get_current_guest(self, obj):
        """Get the ID of the guest currently in this room"""
        guest = obj.current_guest.first()
        return str(guest.id) if guest else None


class GuestSerializer(serializers.ModelSerializer):
    """Serializer for Guest model"""
    room_id = serializers.CharField(source='room.id', read_only=True, allow_null=True)
    check_in_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    
    class Meta:
        model = Guest
        fields = ['id', 'name', 'guest_type', 'species', 'room_id', 'patience',
                  'gold_per_tick', 'reputation_bonus', 'check_in_time',
                  'stay_duration', 'fed', 'served_drink', 'satisfaction',
                  'food_served', 'beverage_served']


class TavernItemSerializer(serializers.ModelSerializer):
    """Serializer for TavernItem model"""
    id = serializers.CharField(source='item_id', read_only=True)

    class Meta:
        model = TavernItem
        fields = ['id', 'name', 'item_type', 'quality', 'cost',
                  'gold_bonus', 'patience_bonus', 'reputation_bonus',
                  'satisfaction_bonus', 'description']


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for Ingredient model"""
    id = serializers.CharField(source='ingredient_id', read_only=True)

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'rarity', 'description', 'base_drop_chance',
                  'is_purchasable', 'market_price']


class PlayerRecipeSerializer(serializers.ModelSerializer):
    """Serializer for PlayerRecipe model"""
    id = serializers.CharField(source='recipe_id', read_only=True)
    item_id = serializers.CharField(source='item.item_id', read_only=True)
    unlocked_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = PlayerRecipe
        fields = ['id', 'name', 'item_id', 'unlocked', 'discovered',
                  'cost_to_unlock', 'ingredients_cost', 'required_ingredients',
                  'times_crafted', 'discovered_at', 'unlocked_at']


class ActiveBuffSerializer(serializers.ModelSerializer):
    """Serializer for ActiveBuff model"""
    upgrade_id = serializers.CharField(source='upgrade_template.upgrade_id', read_only=True)
    name = serializers.CharField(source='upgrade_template.name', read_only=True)
    effect_type = serializers.CharField(source='upgrade_template.effect_type', read_only=True)
    effect_value = serializers.FloatField(source='upgrade_template.effect_value', read_only=True)
    time_remaining_seconds = serializers.SerializerMethodField()
    activated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    expires_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = ActiveBuff
        fields = ['id', 'upgrade_id', 'name', 'effect_type', 'effect_value',
                  'activated_at', 'expires_at', 'time_remaining_seconds']

    def get_time_remaining_seconds(self, obj):
        """Calculate seconds remaining until buff expires"""
        from django.utils import timezone
        if obj.is_expired():
            return 0
        remaining = obj.expires_at - timezone.now()
        return max(0, int(remaining.total_seconds()))


class PremiumPurchaseSerializer(serializers.ModelSerializer):
    """Serializer for PremiumPurchase model"""
    upgrade_id = serializers.CharField(source='upgrade_template.upgrade_id', read_only=True)
    upgrade_name = serializers.CharField(source='upgrade_template.name', read_only=True)
    amount_usd = serializers.SerializerMethodField()

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    completed_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")


    class Meta:
        model = PremiumPurchase
        fields = ['id', 'upgrade_id', 'upgrade_name', 'amount_cents', 'amount_usd',
                  'currency', 'status', 'created_at', 'completed_at']

    def get_amount_usd(self, obj):
        """Convert cents to dollars"""
        return obj.amount_cents / 100


class UpgradeTemplateSerializer(serializers.Serializer):
    """Serializer for UpgradeTemplate with purchase status"""
    id = serializers.CharField(source='upgrade_id', read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    cost = serializers.FloatField(read_only=True)
    effect_type = serializers.CharField(read_only=True)
    effect_value = serializers.FloatField(read_only=True)
    operational_cost_per_tick = serializers.FloatField(read_only=True)
    purchased = serializers.BooleanField(read_only=True)
    purchased_at = serializers.DateTimeField(read_only=True, allow_null=True)

    # Premium fields
    is_premium = serializers.BooleanField(read_only=True)
    premium_price_cents = serializers.IntegerField(read_only=True)
    premium_price_usd = serializers.SerializerMethodField()
    duration_seconds = serializers.IntegerField(read_only=True)
    is_consumable = serializers.BooleanField(read_only=True)

    def get_premium_price_usd(self, obj):
        """Convert cents to dollars"""
        return obj.premium_price_cents / 100 if hasattr(obj, 'premium_price_cents') else 0


class AchievementSerializer(serializers.ModelSerializer):
    """Serializer for Achievement"""
    id = serializers.CharField(source='achievement_id', read_only=True)
    reward_upgrade_id = serializers.CharField(source='reward_upgrade.upgrade_id', read_only=True, allow_null=True)
    reward_upgrade_name = serializers.CharField(source='reward_upgrade.name', read_only=True, allow_null=True)

    class Meta:
        model = Achievement
        fields = ['id', 'name', 'description', 'requirement_type', 'requirement_value',
                  'requirement_metadata', 'icon', 'reward_upgrade_id', 'reward_upgrade_name']


class PlayerAchievementSerializer(serializers.ModelSerializer):
    """Serializer for PlayerAchievement with achievement details"""
    achievement = AchievementSerializer(read_only=True)
    earned_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = PlayerAchievement
        fields = ['achievement', 'progress', 'earned_at', 'is_completed']

    def get_is_completed(self, obj):
        """Check if achievement is completed"""
        return obj.progress >= obj.achievement.requirement_value


class GameStateSerializer(serializers.ModelSerializer):
    """Serializer for GameState model"""
    rooms = RoomSerializer(many=True, read_only=True)
    guests = GuestSerializer(many=True, read_only=True)
    upgrades = serializers.SerializerMethodField()  # Return all templates with purchase status
    recipes = serializers.SerializerMethodField()  # Changed to use player_recipes
    last_update = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    # Premium/buff fields
    active_buffs = serializers.SerializerMethodField()
    buff_multipliers = serializers.SerializerMethodField()
    premium_upgrades = serializers.SerializerMethodField()

    # Angular expects these field names
    tavern_items = serializers.SerializerMethodField()
    available_ingredients = serializers.SerializerMethodField()
    resources = serializers.SerializerMethodField()
    inventory = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    offline_progress = serializers.SerializerMethodField()
    achievements = serializers.SerializerMethodField()

    class Meta:
        model = GameState
        fields = ['resources', 'rooms', 'guests', 'upgrades', 'recipes',
                  'total_income_multiplier', 'auto_clean_enabled',
                  'game_speed', 'last_update', 'tavern_unlocked',
                  'tavern_items', 'inventory', 'available_ingredients',
                  'location', 'offline_progress', 'max_offline_hours',
                  'active_buffs', 'buff_multipliers', 'premium_upgrades', 'achievements']

    def get_resources(self, obj):
        """Get resources in the format expected by Angular frontend"""
        return {
            'gold': obj.gold,
            'reputation': obj.reputation,
            'max_guests': obj.max_guests
        }

    def get_location(self, obj):
        """Get inn location on the map"""
        return {
            'x': obj.map_x,
            'y': obj.map_y
        }

    def get_offline_progress(self, obj):
        """Get offline earnings information"""
        return {
            'earnings': obj.last_offline_earnings,
            'hours': obj.last_offline_hours
        }

    def get_inventory(self, obj):
        """Get inventory in the format expected by Angular frontend"""
        return {
            'items': obj.item_inventory
        }

    def get_tavern_items(self, obj):
        """Get all available tavern items (cached for 1 hour)"""
        cache_key = 'all_tavern_items_serialized'
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return cached_data

        items = TavernItem.objects.all()
        data = TavernItemSerializer(items, many=True).data
        cache.set(cache_key, data, timeout=3600)  # Cache for 1 hour
        return data

    def get_available_ingredients(self, obj):
        """Get all available ingredients (cached for 1 hour)"""
        cache_key = 'all_ingredients_serialized'
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return cached_data

        ingredients = Ingredient.objects.all()
        data = IngredientSerializer(ingredients, many=True).data
        cache.set(cache_key, data, timeout=3600)  # Cache for 1 hour
        return data

    def get_recipes(self, obj):
        """Get player's recipes (discovered and unlocked)"""
        player_recipes = obj.player_recipes.all()
        return PlayerRecipeSerializer(player_recipes, many=True).data

    def get_active_buffs(self, obj):
        """Get active temporary buffs"""
        from game_api.game_service import GameService
        buffs = GameService.get_active_buffs(obj)
        return ActiveBuffSerializer(buffs, many=True).data

    def get_buff_multipliers(self, obj):
        """Get calculated buff multipliers"""
        from game_api.game_service import GameService
        return GameService.calculate_buff_multipliers(obj)

    def get_premium_upgrades(self, obj):
        """Get all premium upgrade templates (cached for 1 hour)"""
        cache_key = 'all_premium_upgrades_serialized'
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return cached_data

        premium_templates = UpgradeTemplate.objects.filter(is_premium=True)
        premium_data = []

        for template in premium_templates:
            premium_data.append({
                'id': template.upgrade_id,  # Frontend expects 'id'
                'upgrade_id': template.upgrade_id,
                'name': template.name,
                'description': template.description,
                'premium_price_cents': template.premium_price_cents,
                'premium_price_usd': template.premium_price_cents / 100,
                'effect_type': template.effect_type,
                'effect_value': template.effect_value,
                'duration_seconds': template.duration_seconds,
                'is_consumable': template.is_consumable
            })

        cache.set(cache_key, premium_data, timeout=3600)  # Cache for 1 hour
        return premium_data

    def get_upgrades(self, obj):
        """Get all upgrade templates with purchase status for this player (non-premium only)"""
        # Cache non-premium upgrade templates (static data)
        cache_key = 'all_non_premium_upgrade_templates'
        all_templates = cache.get(cache_key)
        if all_templates is None:
            all_templates = list(UpgradeTemplate.objects.filter(is_premium=False))
            cache.set(cache_key, all_templates, timeout=3600)  # Cache for 1 hour

        # Fetch all purchases at once to avoid N+1 queries
        purchases = obj.purchased_upgrades.select_related('upgrade_template').all()
        purchases_dict = {p.upgrade_template.upgrade_id: p for p in purchases}

        upgrades_data = []
        for template in all_templates:
            purchase = purchases_dict.get(template.upgrade_id)
            upgrades_data.append({
                'id': template.upgrade_id,  # Frontend expects 'id'
                'purchased': purchase is not None,
                'purchased_at': purchase.purchased_at if purchase else None,
            })

        return upgrades_data

    def get_achievements(self, obj):
        """Get all player achievements with progress"""
        player_achievements = obj.achievements.select_related('achievement', 'achievement__reward_upgrade').all()
        return PlayerAchievementSerializer(player_achievements, many=True).data


class GameStateListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing game states"""
    room_count = serializers.IntegerField(source='rooms.count', read_only=True)
    guest_count = serializers.IntegerField(source='guests.count', read_only=True)

    class Meta:
        model = GameState
        fields = ['player_id', 'gold', 'reputation', 'max_guests',
                  'tavern_unlocked', 'room_count', 'guest_count', 'last_update']
