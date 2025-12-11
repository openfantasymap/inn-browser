from django.contrib import admin
from django.utils.html import format_html
from .models import (
    GameState, Room, Guest, TavernItem, Ingredient, PlayerRecipe, Upgrade,
    RoomTypeTemplate, UpgradeTemplate, RecipeTemplate
)


@admin.register(GameState)
class GameStateAdmin(admin.ModelAdmin):
    list_display = ['player_id', 'gold_display', 'reputation_display', 'max_guests',
                    'tavern_unlocked', 'room_count', 'guest_count', 'last_update']
    list_filter = ['tavern_unlocked', 'auto_clean_enabled', 'created_at']
    search_fields = ['player_id']
    readonly_fields = ['created_at', 'last_update']

    fieldsets = (
        ('Player Info', {
            'fields': ('player_id', 'created_at', 'last_update')
        }),
        ('Resources', {
            'fields': ('gold', 'reputation', 'max_guests')
        }),
        ('Game Settings', {
            'fields': ('total_income_multiplier', 'auto_clean_enabled', 'game_speed', 'tavern_unlocked')
        }),
        ('Inventories', {
            'fields': ('item_inventory', 'ingredient_inventory'),
            'classes': ('collapse',)
        }),
    )

    def gold_display(self, obj):
        return format_html(f'<strong>💰 {obj.gold}</strong>')
    gold_display.short_description = 'Gold'

    def reputation_display(self, obj):
        color = 'green' if obj.reputation > 0 else 'red'
        return format_html(f'<span style="color: {color};">⭐ {obj.reputation}</span>')
    reputation_display.short_description = 'Reputation'

    def room_count(self, obj):
        return obj.rooms.count()
    room_count.short_description = 'Rooms'

    def guest_count(self, obj):
        return obj.guests.count()
    guest_count.short_description = 'Guests'


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'game_state', 'room_template', 'level', 'occupied_display',
                    'income_rate', 'cleanliness_display']
    list_filter = ['room_template', 'occupied', 'game_state']
    search_fields = ['game_state__player_id']

    def room_type(self, obj):
        return obj.room_type
    room_type.short_description = 'Type'

    def occupied_display(self, obj):
        if obj.occupied:
            return format_html('<span style="color: red;">🔴 Occupied</span>')
        return format_html('<span style="color: green;">🟢 Empty</span>')
    occupied_display.short_description = 'Status'

    def cleanliness_display(self, obj):
        if obj.cleanliness >= 80:
            color = 'green'
            icon = '✨'
        elif obj.cleanliness >= 50:
            color = 'orange'
            icon = '🧹'
        else:
            color = 'red'
            icon = '💩'
        return format_html('<span style="color: {};">{} {:.0f}%</span>', color, icon, obj.cleanliness)
    cleanliness_display.short_description = 'Cleanliness'


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ['name', 'guest_type', 'game_state', 'room', 'patience_display',
                    'satisfaction_display', 'gold_per_tick', 'fed_display', 'served_drink_display']
    list_filter = ['guest_type', 'fed', 'served_drink', 'game_state']
    search_fields = ['name', 'game_state__player_id']
    readonly_fields = ['created_at', 'check_in_time']

    fieldsets = (
        ('Basic Info', {
            'fields': ('game_state', 'room', 'name', 'guest_type')
        }),
        ('Stats', {
            'fields': ('patience', 'satisfaction', 'gold_per_tick', 'reputation_bonus', 'stay_duration')
        }),
        ('Service', {
            'fields': ('fed', 'served_drink', 'food_served', 'beverage_served')
        }),
        ('Timestamps', {
            'fields': ('check_in_time', 'created_at')
        }),
    )

    def patience_display(self, obj):
        if obj.patience >= 70:
            color = 'green'
        elif obj.patience >= 40:
            color = 'orange'
        else:
            color = 'red'
        return format_html('<span style="color: {};">{}%</span>', color, obj.patience)
    patience_display.short_description = 'Patience'

    def satisfaction_display(self, obj):
        if obj.satisfaction >= 80:
            return format_html('<span style="color: green;">😊 {:.0f}%</span>', obj.satisfaction)
        elif obj.satisfaction >= 50:
            return format_html('<span style="color: orange;">😐 {}%</span>', obj.satisfaction)
        return format_html('<span style="color: red;">😠 {:.0f}%</span>', obj.satisfaction)
    satisfaction_display.short_description = 'Satisfaction'

    def fed_display(self, obj):
        return '🍖' if obj.fed else '❌'
    fed_display.short_description = 'Fed'

    def served_drink_display(self, obj):
        return '🍺' if obj.served_drink else '❌'
    served_drink_display.short_description = 'Drink'


@admin.register(TavernItem)
class TavernItemAdmin(admin.ModelAdmin):
    list_display = ['item_id', 'name', 'item_type', 'quality_display', 'cost',
                    'gold_bonus', 'satisfaction_bonus']
    list_filter = ['item_type', 'quality']
    search_fields = ['name', 'item_id']

    def quality_display(self, obj):
        colors = {
            'basic': 'gray',
            'good': 'blue',
            'fine': 'purple',
            'exquisite': 'orange',
            'legendary': 'red'
        }
        color = colors.get(obj.quality, 'black')
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>',
                          color, obj.get_quality_display())
    quality_display.short_description = 'Quality'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['ingredient_id', 'name', 'rarity_display', 'base_drop_chance_display']
    list_filter = ['rarity']
    search_fields = ['name', 'ingredient_id']

    def rarity_display(self, obj):
        colors = {
            'common': 'gray',
            'uncommon': 'green',
            'rare': 'blue',
            'epic': 'purple',
            'legendary': 'orange'
        }
        color = colors.get(obj.rarity, 'black')
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>',
                          color, obj.get_rarity_display())
    rarity_display.short_description = 'Rarity'

    def base_drop_chance_display(self, obj):
        return f"{obj.base_drop_chance * 100:.1f}%"
    base_drop_chance_display.short_description = 'Drop Chance'


@admin.register(PlayerRecipe)
class PlayerRecipeAdmin(admin.ModelAdmin):
    list_display = ['recipe_id', 'name', 'item_name', 'game_state', 'status_display',
                    'times_crafted', 'discovered_at']
    list_filter = ['unlocked', 'discovered', 'recipe_template', 'game_state']
    search_fields = ['recipe_template__name', 'recipe_template__recipe_id', 'game_state__player_id']
    readonly_fields = ['discovered_at', 'unlocked_at', 'times_crafted']

    def recipe_id(self, obj):
        return obj.recipe_id
    recipe_id.short_description = 'Recipe ID'

    def name(self, obj):
        return obj.name
    name.short_description = 'Name'

    def item_name(self, obj):
        return obj.item.name
    item_name.short_description = 'Item'

    def status_display(self, obj):
        if obj.unlocked:
            return format_html('<span style="color: green;">✓ Unlocked</span>')
        elif obj.discovered:
            return format_html('<span style="color: orange;">🔍 Discovered</span>')
        return format_html('<span style="color: gray;">❓ Hidden</span>')
    status_display.short_description = 'Status'


@admin.register(Upgrade)
class UpgradeAdmin(admin.ModelAdmin):
    list_display = ['upgrade_id', 'name', 'game_state', 'purchased_display',
                    'cost', 'effect_type_display']
    list_filter = ['purchased', 'upgrade_template', 'game_state']
    search_fields = ['upgrade_template__name', 'upgrade_template__upgrade_id']

    def upgrade_id(self, obj):
        return obj.upgrade_id
    upgrade_id.short_description = 'ID'

    def name(self, obj):
        return obj.name
    name.short_description = 'Name'

    def cost(self, obj):
        return obj.cost
    cost.short_description = 'Cost'

    def effect_type_display(self, obj):
        return obj.effect_type
    effect_type_display.short_description = 'Effect Type'

    def purchased_display(self, obj):
        if obj.purchased:
            return format_html('<span style="color: green;">✓ Purchased</span>')
        return format_html('<span style="color: gray;">Not Purchased</span>')
    purchased_display.short_description = 'Status'


# ============================================================================
# TEMPLATE ADMIN - Global templates shared across all players
# ============================================================================

@admin.register(RoomTypeTemplate)
class RoomTypeTemplateAdmin(admin.ModelAdmin):
    list_display = ['room_type_id', 'emoji_display', 'name', 'base_cost',
                    'income_multiplier', 'required_upgrade_display', 'instance_count']
    list_filter = ['required_upgrade']
    search_fields = ['name', 'room_type_id']
    ordering = ['base_cost']

    fieldsets = (
        ('Basic Info', {
            'fields': ('room_type_id', 'name', 'emoji', 'description')
        }),
        ('Attributes', {
            'fields': ('base_cost', 'income_multiplier')
        }),
        ('Requirements', {
            'fields': ('required_upgrade',),
            'classes': ('collapse',)
        }),
    )

    def emoji_display(self, obj):
        return format_html('<span style="font-size: 1.5em;">{}</span>', obj.emoji)
    emoji_display.short_description = ''

    def required_upgrade_display(self, obj):
        if obj.required_upgrade:
            return format_html('<span style="color: orange;">🔒 {}</span>', obj.required_upgrade.name)
        return format_html('<span style="color: green;">✓ Always available</span>')
    required_upgrade_display.short_description = 'Requires'

    def instance_count(self, obj):
        count = obj.instances.count()
        return format_html('<strong>{}</strong> rooms', count)
    instance_count.short_description = 'In Use'


@admin.register(UpgradeTemplate)
class UpgradeTemplateAdmin(admin.ModelAdmin):
    list_display = ['upgrade_id', 'name', 'cost', 'effect_display', 'instance_count']
    list_filter = ['effect_type']
    search_fields = ['name', 'upgrade_id', 'description']
    ordering = ['cost']

    fieldsets = (
        ('Basic Info', {
            'fields': ('upgrade_id', 'name', 'description')
        }),
        ('Cost & Effects', {
            'fields': ('cost', 'effect_type', 'effect_value')
        }),
        ('Requirements', {
            'fields': ('required_upgrade',),
            'classes': ('collapse',)
        }),
    )

    def effect_display(self, obj):
        return format_html('<code>{}:</code> <strong>{}</strong>',
                          obj.effect_type, obj.effect_value)
    effect_display.short_description = 'Effect'

    def instance_count(self, obj):
        total = obj.instances.count()
        purchased = obj.instances.filter(purchased=True).count()
        return format_html('{} / <strong>{}</strong> purchased', purchased, total)
    instance_count.short_description = 'Usage'


@admin.register(RecipeTemplate)
class RecipeTemplateAdmin(admin.ModelAdmin):
    list_display = ['recipe_id', 'name', 'item_name', 'ingredient_count',
                    'discoverable_display', 'auto_unlocked_display', 'instance_count']
    list_filter = ['discoverable', 'auto_unlocked', 'item__item_type', 'item__quality']
    search_fields = ['name', 'recipe_id', 'item__name']
    ordering = ['item__quality', 'name']

    fieldsets = (
        ('Basic Info', {
            'fields': ('recipe_id', 'name', 'item')
        }),
        ('Ingredients', {
            'fields': ('required_ingredients',),
            'description': 'Format: [{"ingredient_id": "ing_flour", "quantity": 2}, ...]'
        }),
        ('Costs', {
            'fields': ('cost_to_unlock', 'ingredients_cost')
        }),
        ('Discovery Settings', {
            'fields': ('discoverable', 'auto_unlocked')
        }),
    )

    def item_name(self, obj):
        return obj.item.name
    item_name.short_description = 'Creates Item'

    def ingredient_count(self, obj):
        count = len(obj.required_ingredients)
        return format_html('<strong>{}</strong> ingredients', count)
    ingredient_count.short_description = 'Ingredients'

    def discoverable_display(self, obj):
        if obj.discoverable:
            return format_html('<span style="color: green;">✓ Can discover</span>')
        return format_html('<span style="color: gray;">Manual only</span>')
    discoverable_display.short_description = 'Discoverable'

    def auto_unlocked_display(self, obj):
        return '⭐' if obj.auto_unlocked else '🔒'
    auto_unlocked_display.short_description = 'Auto'

    def instance_count(self, obj):
        total = obj.player_instances.count()
        discovered = obj.player_instances.filter(discovered=True).count()
        unlocked = obj.player_instances.filter(unlocked=True).count()
        return format_html(
            '<strong>{}</strong> unlocked / {} discovered / {} total',
            unlocked, discovered, total
        )
    instance_count.short_description = 'Player Stats'


# ============================================================================
# ADMIN SITE CUSTOMIZATION
# ============================================================================

# Customize admin site
admin.site.site_header = "🏰 Fantasy Inn Tycoon Admin"
admin.site.site_title = "Fantasy Inn Admin"
admin.site.index_title = "Game Management Dashboard"
