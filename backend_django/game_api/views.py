from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .game_service import GameService
from .serializers import GameStateSerializer


@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return Response({'status': 'healthy', 'backend': 'Django + DRF'})


@api_view(['GET', 'POST'])
def game_state(request, player_id):
    """Get or create game state for a player"""
    try:
        if request.method == 'POST':
            game_state = GameService.create_or_get_game_state(player_id)
        else:
            game_state = GameService.create_or_get_game_state(player_id)

        serializer = GameStateSerializer(game_state)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def process_tick(request, player_id):
    """Process one game tick"""
    try:
        game_state = GameService.process_tick(player_id)
        serializer = GameStateSerializer(game_state)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_room(request, player_id):
    """Add a new room to the inn"""
    try:
        room_type = request.data.get('room_type', 'basic')
        game_state = GameService.add_room(player_id, room_type)
        serializer = GameStateSerializer(game_state)
        return Response(serializer.data)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def assign_guest(request, player_id):
    """Assign a waiting guest to an available room"""
    try:
        guest_id = request.data.get('guest_id')
        room_id = request.data.get('room_id')

        if not guest_id or not room_id:
            return Response(
                {'error': 'guest_id and room_id are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        game_state = GameService.assign_guest_to_room(player_id, int(guest_id), int(room_id))
        serializer = GameStateSerializer(game_state)
        return Response(serializer.data)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def clean_room(request, player_id, room_id):
    """Clean a specific room"""
    try:
        game_state = GameService.clean_room(player_id, room_id)
        serializer = GameStateSerializer(game_state)
        return Response(serializer.data)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def purchase_upgrade(request, player_id, upgrade_id):
    """Purchase an upgrade"""
    try:
        game_state = GameService.purchase_upgrade(player_id, upgrade_id)
        serializer = GameStateSerializer(game_state)
        return Response(serializer.data)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def unlock_recipe(request, player_id, recipe_id):
    """Unlock a recipe"""
    try:
        game_state = GameService.unlock_recipe(player_id, recipe_id)
        serializer = GameStateSerializer(game_state)
        return Response(serializer.data)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def craft_item(request, player_id):
    """Craft tavern items"""
    try:
        item_id = request.query_params.get('item_id')
        quantity = int(request.query_params.get('quantity', 1))

        if not item_id:
            return Response({'error': 'item_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        game_state = GameService.craft_item(player_id, item_id, quantity)
        serializer = GameStateSerializer(game_state)
        return Response(serializer.data)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def serve_guest(request, player_id):
    """Serve food or drink to a guest"""
    try:
        guest_id = request.query_params.get('guest_id')
        item_id = request.query_params.get('item_id')

        if not guest_id or not item_id:
            return Response({'error': 'guest_id and item_id are required'}, status=status.HTTP_400_BAD_REQUEST)

        game_state = GameService.serve_guest(player_id, guest_id, item_id)
        serializer = GameStateSerializer(game_state)
        return Response(serializer.data)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def purchase_ingredient(request, player_id):
    """Purchase ingredients from the store"""
    try:
        ingredient_id = request.data.get('ingredient_id')
        quantity = request.data.get('quantity', 1)

        if not ingredient_id:
            return Response({'error': 'ingredient_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(quantity, int) or quantity < 1:
            return Response({'error': 'quantity must be a positive integer'}, status=status.HTTP_400_BAD_REQUEST)

        game_state = GameService.purchase_ingredient(player_id, ingredient_id, quantity)
        serializer = GameStateSerializer(game_state)
        return Response(serializer.data)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def experiment_with_ingredients(request, player_id):
    """Experiment with ingredient combinations to discover recipes"""
    try:
        ingredient_ids = request.data.get('ingredient_ids', [])

        if not isinstance(ingredient_ids, list):
            return Response({'error': 'ingredient_ids must be a list'}, status=status.HTTP_400_BAD_REQUEST)

        result = GameService.experiment_with_ingredients(player_id, ingredient_ids)

        # Serialize game state
        game_state = result.pop('game_state')
        serializer = GameStateSerializer(game_state)

        # Return result with serialized game state
        response_data = {
            **result,
            'game_state': serializer.data
        }

        return Response(response_data)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
