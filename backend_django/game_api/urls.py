from django.urls import path
from . import views

urlpatterns = [
    # Health check
    path('health/', views.health_check, name='health'),

    # Game state
    path('game/<str:player_id>', views.game_state, name='game_state'),

    # Game actions
    path('tick/<str:player_id>', views.process_tick, name='process_tick'),
    path('add-room/<str:player_id>', views.add_room, name='add_room'),
    path('clean-room/<str:player_id>/<str:room_id>', views.clean_room, name='clean_room'),
    path('purchase-upgrade/<str:player_id>/<str:upgrade_id>', views.purchase_upgrade, name='purchase_upgrade'),

    # Tavern actions
    path('unlock-recipe/<str:player_id>/<str:recipe_id>', views.unlock_recipe, name='unlock_recipe'),
    path('craft-item/<str:player_id>', views.craft_item, name='craft_item'),
    path('serve-guest/<str:player_id>', views.serve_guest, name='serve_guest'),
]
