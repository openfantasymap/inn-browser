from django.urls import path
from . import views

urlpatterns = [
    # Health check
    path('health/', views.health_check, name='health'),

    # Game state
    path('game/<str:player_id>', views.game_state, name='game_state'),
    path('game/state/<str:player_id>', views.game_state, name='game_state'),

    # Game actions
    path('tick/<str:player_id>', views.process_tick, name='process_tick'),
    path('game/tick/<str:player_id>', views.process_tick, name='process_tick'),
    path('add-room/<str:player_id>', views.add_room, name='add_room'),
    path('game/build-room/<str:player_id>', views.add_room, name='build_room'),
    path('assign-guest/<str:player_id>', views.assign_guest, name='assign_guest'),
    path('game/assign-guest/<str:player_id>', views.assign_guest, name='g_assign_guest'),
    path('clean-room/<str:player_id>/<str:room_id>', views.clean_room, name='clean_room'),
    path('game/clean-room/<str:player_id>/<str:room_id>', views.clean_room, name='g_clean_room'),
    path('purchase-upgrade/<str:player_id>/<str:upgrade_id>', views.purchase_upgrade, name='purchase_upgrade'),
    path('upgrades', views.get_upgrades, name="get_upgrades"),

    # Tavern actions
    path('unlock-recipe/<str:player_id>/<str:recipe_id>', views.unlock_recipe, name='unlock_recipe'),
    path('craft-item/<str:player_id>', views.craft_item, name='craft_item'),
    path('serve-guest/<str:player_id>', views.serve_guest, name='serve_guest'),
    path('purchase-ingredient/<str:player_id>', views.purchase_ingredient, name='purchase_ingredient'),
    path('experiment/<str:player_id>', views.experiment_with_ingredients, name='experiment_ingredients'),

    # Premium/Stripe endpoints
    path('premium/upgrades/', views.get_premium_upgrades, name='get_premium_upgrades'),
    path('premium/create-checkout/<str:player_id>', views.create_checkout_session, name='create_checkout_session'),
    path('premium/webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('buffs/<str:player_id>', views.get_active_buffs, name='get_active_buffs'),
]
