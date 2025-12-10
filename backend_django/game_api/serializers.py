from rest_framework import serializers
from .models import GameState, Room, Guest, TavernItem, Ingredient, Recipe, Upgrade


class RoomSerializer(serializers.ModelSerializer):
    """Serializer for Room model"""
    current_guest = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ['id', 'room_type', 'level', 'occupied', 'current_guest',
                  'income_rate', 'cleanliness']

    def get_current_guest(self, obj):
        """Get the ID of the guest currently in this room"""
        guest = obj.current_guest.first()
        return str(guest.id) if guest else None


class GuestSerializer(serializers.ModelSerializer):
    """Serializer for Guest model"""
    room_id = serializers.CharField(source='room.id', read_only=True, allow_null=True)

    class Meta:
        model = Guest
        fields = ['id', 'name', 'guest_type', 'room_id', 'patience',
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
        fields = ['id', 'name', 'rarity', 'description', 'base_drop_chance']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe model"""
    id = serializers.CharField(source='recipe_id', read_only=True)
    item_id = serializers.CharField(source='item.item_id', read_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'item_id', 'unlocked', 'discovered',
                  'cost_to_unlock', 'ingredients_cost', 'required_ingredients']


class UpgradeSerializer(serializers.ModelSerializer):
    """Serializer for Upgrade model"""
    id = serializers.CharField(source='upgrade_id', read_only=True)

    class Meta:
        model = Upgrade
        fields = ['id', 'name', 'description', 'cost', 'purchased',
                  'effect_type', 'effect_value']


class GameStateSerializer(serializers.ModelSerializer):
    """Serializer for GameState model"""
    rooms = RoomSerializer(many=True, read_only=True)
    guests = GuestSerializer(many=True, read_only=True)
    upgrades = UpgradeSerializer(many=True, read_only=True)
    recipes = RecipeSerializer(many=True, read_only=True)

    # Angular expects these field names
    tavern_items = serializers.SerializerMethodField()
    available_ingredients = serializers.SerializerMethodField()
    resources = serializers.SerializerMethodField()
    inventory = serializers.SerializerMethodField()

    class Meta:
        model = GameState
        fields = ['resources', 'rooms', 'guests', 'upgrades', 'recipes',
                  'total_income_multiplier', 'auto_clean_enabled',
                  'game_speed', 'last_update', 'tavern_unlocked',
                  'tavern_items', 'inventory', 'available_ingredients']

    def get_resources(self, obj):
        """Get resources in the format expected by Angular frontend"""
        return {
            'gold': obj.gold,
            'reputation': obj.reputation,
            'max_guests': obj.max_guests
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


class GameStateListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing game states"""
    room_count = serializers.IntegerField(source='rooms.count', read_only=True)
    guest_count = serializers.IntegerField(source='guests.count', read_only=True)

    class Meta:
        model = GameState
        fields = ['player_id', 'gold', 'reputation', 'max_guests',
                  'tavern_unlocked', 'room_count', 'guest_count', 'last_update']
