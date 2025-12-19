from django.contrib import admin
from django.utils.html import format_html
from .models import (
    GameState, Room, Guest, TavernItem, Ingredient, PlayerRecipe, Upgrade,
    RoomTypeTemplate, UpgradeTemplate, RecipeTemplate, ActiveBuff, PremiumPurchase,
    Achievement, PlayerAchievement
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
    list_display = ['name', 'species_display', 'guest_type', 'game_state', 'room', 'patience_display',
                    'satisfaction_display', 'gold_per_tick', 'fed_display', 'served_drink_display']
    list_filter = ['guest_type', 'species', 'fed', 'served_drink', 'game_state']
    search_fields = ['name', 'game_state__player_id']
    readonly_fields = ['created_at', 'check_in_time']

    fieldsets = (
        ('Basic Info', {
            'fields': ('game_state', 'room', 'name', 'guest_type', 'species')
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

    def species_display(self, obj):
        return obj.get_species_display()
    species_display.short_description = 'Species'


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
    list_display = ['upgrade_id', 'name', 'game_state', 'purchased_at',
                    'cost', 'effect_type_display']
    list_filter = ['upgrade_template', 'game_state', 'purchased_at']
    search_fields = ['upgrade_template__name', 'upgrade_template__upgrade_id']
    readonly_fields = ['purchased_at']

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


@admin.register(ActiveBuff)
class ActiveBuffAdmin(admin.ModelAdmin):
    list_display = ['id', 'game_state', 'buff_name', 'activated_at', 'expires_at',
                    'status_display', 'time_remaining_display']
    list_filter = ['active', 'upgrade_template', 'game_state']
    search_fields = ['game_state__player_id', 'upgrade_template__name']
    readonly_fields = ['activated_at', 'is_expired']
    ordering = ['-activated_at']

    fieldsets = (
        ('Buff Info', {
            'fields': ('game_state', 'upgrade_template')
        }),
        ('Timing', {
            'fields': ('activated_at', 'expires_at')
        }),
        ('Status', {
            'fields': ('active', 'is_expired')
        }),
    )

    def buff_name(self, obj):
        return obj.upgrade_template.name
    buff_name.short_description = 'Buff'

    def status_display(self, obj):
        if not obj.active:
            return format_html('<span style="color: gray;">⏸️ Deactivated</span>')
        if obj.is_expired():
            return format_html('<span style="color: red;">⌛ Expired</span>')
        return format_html('<span style="color: green;">✓ Active</span>')
    status_display.short_description = 'Status'

    def time_remaining_display(self, obj):
        if obj.is_expired():
            return format_html('<span style="color: gray;">—</span>')
        from django.utils import timezone
        remaining = obj.expires_at - timezone.now()
        total_seconds = int(remaining.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        if hours > 0:
            return format_html('<span style="color: orange;">{} h {} min</span>', hours, minutes)
        return format_html('<span style="color: orange;">{} min</span>', minutes)
    time_remaining_display.short_description = 'Time Left'


@admin.register(PremiumPurchase)
class PremiumPurchaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'game_state', 'purchase_name', 'amount_display',
                    'status_display', 'created_at', 'stripe_payment_intent_id']
    list_filter = ['status', 'upgrade_template', 'created_at']
    search_fields = ['game_state__player_id', 'stripe_payment_intent_id',
                     'stripe_checkout_session_id', 'upgrade_template__name']
    readonly_fields = ['created_at', 'completed_at', 'stripe_payment_intent_id',
                       'stripe_checkout_session_id']
    ordering = ['-created_at']

    fieldsets = (
        ('Purchase Info', {
            'fields': ('game_state', 'upgrade_template', 'status')
        }),
        ('Payment Details', {
            'fields': ('amount_cents', 'currency', 'stripe_payment_intent_id',
                      'stripe_checkout_session_id')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'completed_at')
        }),
        ('Metadata', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
    )

    def purchase_name(self, obj):
        return obj.upgrade_template.name
    purchase_name.short_description = 'Item'

    def amount_display(self, obj):
        return format_html('<strong>${:.2f}</strong> {}', obj.amount_cents / 100, obj.currency.upper())
    amount_display.short_description = 'Amount'

    def status_display(self, obj):
        colors = {
            'pending': 'orange',
            'completed': 'green',
            'failed': 'red',
            'refunded': 'gray'
        }
        icons = {
            'pending': '⏳',
            'completed': '✓',
            'failed': '✗',
            'refunded': '↩️'
        }
        color = colors.get(obj.status, 'black')
        icon = icons.get(obj.status, '?')
        return format_html('<span style="color: {};">{} {}</span>',
                          color, icon, obj.get_status_display())
    status_display.short_description = 'Status'


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
    list_display = ['upgrade_id', 'name', 'type_display', 'cost_display', 'effect_display',
                    'duration_display', 'instance_count']
    list_filter = ['effect_type', 'is_premium', 'is_consumable']
    search_fields = ['name', 'upgrade_id', 'description']
    ordering = ['cost', 'premium_price_cents']

    fieldsets = (
        ('Basic Info', {
            'fields': ('upgrade_id', 'name', 'description')
        }),
        ('Cost & Effects', {
            'fields': ('cost', 'effect_type', 'effect_value')
        }),
        ('Premium/Monetization', {
            'fields': ('is_premium', 'premium_price_cents', 'is_consumable'),
            'description': 'Set is_premium=True for real money purchases. Price in cents (e.g., 99 = $0.99)'
        }),
        ('Temporary Buffs', {
            'fields': ('duration_seconds',),
            'description': 'Duration in seconds. 0 = permanent, >0 = temporary buff'
        }),
        ('Requirements', {
            'fields': ('required_upgrade',),
            'classes': ('collapse',)
        }),
    )

    def type_display(self, obj):
        if obj.is_premium:
            return format_html('<span style="color: gold; font-weight: bold;">💎 PREMIUM</span>')
        return format_html('<span style="color: green;">💰 Gold</span>')
    type_display.short_description = 'Type'

    def cost_display(self, obj):
        if obj.is_premium:
            return format_html('<strong>${}</strong>', obj.premium_price_cents / 100)
        return format_html('{}g', obj.cost)
    cost_display.short_description = 'Cost'

    def effect_display(self, obj):
        return format_html('<code>{}:</code> <strong>{}</strong>',
                          obj.effect_type, obj.effect_value)
    effect_display.short_description = 'Effect'

    def duration_display(self, obj):
        if obj.duration_seconds == 0:
            return format_html('<span style="color: green;">♾️ Permanent</span>')
        hours = obj.duration_seconds / 3600
        if hours >= 1:
            return format_html('<span style="color: orange;">⏱️ {}h</span>', hours)
        minutes = obj.duration_seconds / 60
        return format_html('<span style="color: orange;">⏱️ {}m</span>', minutes)
    duration_display.short_description = 'Duration'

    def instance_count(self, obj):
        purchased = obj.player_purchases.count()
        return format_html('<strong>{}</strong> players purchased', purchased)
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


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['achievement_id', 'icon_display', 'name', 'requirement_display',
                    'reward_display', 'player_count']
    list_filter = ['requirement_type', 'reward_upgrade']
    search_fields = ['name', 'achievement_id', 'description']
    ordering = ['requirement_type', 'requirement_value']

    fieldsets = (
        ('Basic Info', {
            'fields': ('achievement_id', 'name', 'description', 'icon')
        }),
        ('Requirements', {
            'fields': ('requirement_type', 'requirement_value', 'requirement_metadata')
        }),
        ('Reward', {
            'fields': ('reward_upgrade',),
            'description': 'Optional upgrade unlocked when achievement is completed'
        }),
    )

    def icon_display(self, obj):
        return format_html('<span style="font-size: 1.5em;">{}</span>', obj.icon)
    icon_display.short_description = ''

    def requirement_display(self, obj):
        req_type = obj.requirement_type.replace('_', ' ').title()
        metadata = ''
        if obj.requirement_metadata:
            if 'patience_min' in obj.requirement_metadata:
                metadata = f" (patience ≥{obj.requirement_metadata['patience_min']}%)"
            elif 'patience_max' in obj.requirement_metadata:
                metadata = f" (patience ≤{obj.requirement_metadata['patience_max']}%)"
            elif 'race' in obj.requirement_metadata:
                metadata = f" ({obj.requirement_metadata['race']})"
            elif 'guest_type' in obj.requirement_metadata:
                metadata = f" ({obj.requirement_metadata['guest_type']})"
        return format_html('<strong>{}</strong>: {}{}'.format(
            req_type, obj.requirement_value, metadata))
    requirement_display.short_description = 'Requirement'

    def reward_display(self, obj):
        if obj.reward_upgrade:
            return format_html('<span style="color: purple;">🎁 {}</span>', obj.reward_upgrade.name)
        return format_html('<span style="color: gray;">—</span>')
    reward_display.short_description = 'Reward'

    def player_count(self, obj):
        completed = obj.player_achievements.filter(
            progress__gte=obj.requirement_value
        ).count()
        total = obj.player_achievements.count()
        if completed == 0:
            return format_html('<span style="color: gray;">{} tracking</span>', total)
        return format_html('<strong>{}</strong> completed / {} tracking', completed, total)
    player_count.short_description = 'Players'


@admin.register(PlayerAchievement)
class PlayerAchievementAdmin(admin.ModelAdmin):
    list_display = ['achievement_display', 'game_state', 'progress_display',
                    'completion_status', 'earned_at']
    list_filter = ['achievement', 'game_state']
    search_fields = ['game_state__player_id', 'achievement__name', 'achievement__achievement_id']
    readonly_fields = ['earned_at']
    ordering = ['-earned_at', '-progress']

    fieldsets = (
        ('Achievement Info', {
            'fields': ('game_state', 'achievement')
        }),
        ('Progress', {
            'fields': ('progress', 'earned_at')
        }),
    )

    def achievement_display(self, obj):
        return format_html('{} {}', obj.achievement.icon, obj.achievement.name)
    achievement_display.short_description = 'Achievement'

    def progress_display(self, obj):
        target = obj.achievement.requirement_value
        progress = obj.progress
        percentage = min(100, (progress / target * 100)) if target > 0 else 0

        if progress >= target:
            color = 'green'
            bar = '█' * 10
        else:
            color = 'orange'
            filled = int((progress / target) * 10)
            bar = '█' * filled + '░' * (10 - filled)

        return format_html(
            '<span style="color: {};">{}</span> <code>{}/{}</code> ({}%)',
            color, bar, progress, target, int(percentage)
        )
    progress_display.short_description = 'Progress'

    def completion_status(self, obj):
        if obj.progress >= obj.achievement.requirement_value:
            return format_html('<span style="color: green; font-weight: bold;">✓ Completed</span>')
        return format_html('<span style="color: gray;">In Progress</span>')
    completion_status.short_description = 'Status'


# ============================================================================
# ADMIN SITE CUSTOMIZATION
# ============================================================================

# Customize admin site
admin.site.site_header = "🏰 Fantasy Inn Tycoon Admin"
admin.site.site_title = "Fantasy Inn Admin"
admin.site.index_title = "Game Management Dashboard"
