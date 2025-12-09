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
