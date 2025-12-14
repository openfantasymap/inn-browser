from rest_framework import serializers
from .models import (
    GameState, Room, Guest, TavernItem, Ingredient, PlayerRecipe, Upgrade, UpgradeTemplate,
    ActiveBuff, PremiumPurchase
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


class GameStateSerializer(serializers.ModelSerializer):
    """Serializer for GameState model"""
    rooms = RoomSerializer(many=True, read_only=True)
    guests = GuestSerializer(many=True, read_only=True)
    upgrades = serializers.SerializerMethodField()  # Return all templates with purchase status
    recipes = serializers.SerializerMethodField()  # Changed to use player_recipes

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

    class Meta:
        model = GameState
        fields = ['resources', 'rooms', 'guests', 'upgrades', 'recipes',
                  'total_income_multiplier', 'auto_clean_enabled',
                  'game_speed', 'last_update', 'tavern_unlocked',
                  'tavern_items', 'inventory', 'available_ingredients',
                  'location', 'offline_progress', 'max_offline_hours',
                  'active_buffs', 'buff_multipliers', 'premium_upgrades']

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
        """Get all available tavern items"""
        items = TavernItem.objects.all()
        return TavernItemSerializer(items, many=True).data

    def get_available_ingredients(self, obj):
        """Get all available ingredients"""
        ingredients = Ingredient.objects.all()
        return IngredientSerializer(ingredients, many=True).data

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
        """Get all premium upgrade templates (purchasable with real money)"""
        premium_templates = UpgradeTemplate.objects.filter(is_premium=True)
        premium_data = []

        for template in premium_templates:
            premium_data.append({
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

        return premium_data

    def get_upgrades(self, obj):
        """Get all upgrade templates with purchase status for this player (non-premium only)"""
        all_templates = UpgradeTemplate.objects.filter(is_premium=False)
        upgrades_data = []

        for template in all_templates:
            # Check if this upgrade has been purchased by this player
            purchase = obj.purchased_upgrades.filter(upgrade_template=template).first()

            upgrades_data.append({
                'upgrade_id': template.upgrade_id,
                'name': template.name,
                'description': template.description,
                'cost': template.cost,
                'effect_type': template.effect_type,
                'effect_value': template.effect_value,
                'purchased': purchase is not None,
                'purchased_at': purchase.purchased_at if purchase else None,
                'is_premium': template.is_premium,
                'premium_price_cents': template.premium_price_cents,
                'duration_seconds': template.duration_seconds,
                'is_consumable': template.is_consumable
            })

        return upgrades_data


class GameStateListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing game states"""
    room_count = serializers.IntegerField(source='rooms.count', read_only=True)
    guest_count = serializers.IntegerField(source='guests.count', read_only=True)

    class Meta:
        model = GameState
        fields = ['player_id', 'gold', 'reputation', 'max_guests',
                  'tavern_unlocked', 'room_count', 'guest_count', 'last_update']
