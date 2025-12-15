from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import stripe
import json

from .game_service import GameService
from .serializers import GameStateSerializer
from .models import UpgradeTemplate, GameState
from .mqtt_service import get_mqtt_service

# Configure Stripe
stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', 'sk_test_placeholder')

# Get MQTT service instance
mqtt_service = get_mqtt_service()


def serialize_and_publish(game_state, player_id):
    """Helper to serialize game state and publish via MQTT"""
    serializer = GameStateSerializer(game_state)
    data = serializer.data

    # Publish to MQTT for real-time updates
    mqtt_service.publish_game_state(player_id, data)

    return data


@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return Response({'status': 'healthy', 'backend': 'Django + DRF'})


@api_view(['GET', 'POST'])
def game_state(request, player_id):
    """Get or create game state for a player"""
    try:
        game_state = GameService.create_or_get_game_state(player_id)
        data = serialize_and_publish(game_state, player_id)
        return Response(data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def process_tick(request, player_id):
    """Process one game tick and publish via MQTT"""
    try:
        game_state = GameService.process_tick(player_id)
        data = serialize_and_publish(game_state, player_id)
        return Response(data)
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


# ============================================================================
# PREMIUM/STRIPE ENDPOINTS
# ============================================================================

@api_view(['POST'])
def create_checkout_session(request, player_id):
    """
    Create a Stripe checkout session for purchasing a premium upgrade

    POST body: {
        "upgrade_id": "premium_2x_speed_1h",
        "success_url": "https://yourgame.com/success",
        "cancel_url": "https://yourgame.com/cancel"
    }
    """
    try:
        upgrade_id = request.data.get('upgrade_id')
        success_url = request.data.get('success_url', 'http://localhost:4200/success')
        cancel_url = request.data.get('cancel_url', 'http://localhost:4200/cancel')

        if not upgrade_id:
            return Response({'error': 'upgrade_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the upgrade template
        try:
            upgrade_template = UpgradeTemplate.objects.get(upgrade_id=upgrade_id)
        except UpgradeTemplate.DoesNotExist:
            return Response({'error': f'Upgrade {upgrade_id} not found'}, status=status.HTTP_404_NOT_FOUND)

        # Verify it's a premium upgrade
        if not upgrade_template.is_premium:
            return Response({'error': 'This upgrade is not a premium item'}, status=status.HTTP_400_BAD_REQUEST)

        # Get or create game state
        game_state = GameService.create_or_get_game_state(player_id)

        # Create Stripe checkout session
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': upgrade_template.name,
                            'description': upgrade_template.description,
                        },
                        'unit_amount': upgrade_template.premium_price_cents,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=success_url + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=cancel_url,
                client_reference_id=player_id,
                metadata={
                    'player_id': player_id,
                    'upgrade_id': upgrade_id,
                }
            )

            return Response({
                'checkout_session_id': checkout_session.id,
                'checkout_url': checkout_session.url
            })

        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
def stripe_webhook(request):
    """
    Handle Stripe webhook events for payment confirmation

    This endpoint should be registered in your Stripe dashboard
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    webhook_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', '')

    try:
        # Verify webhook signature
        if webhook_secret:
            try:
                event = stripe.Webhook.construct_event(
                    payload, sig_header, webhook_secret
                )
            except ValueError:
                return HttpResponse(status=400)
            except stripe.error.SignatureVerificationError:
                return HttpResponse(status=400)
        else:
            # For development without webhook secret
            event = json.loads(payload)

        # Handle the checkout.session.completed event
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']

            # Extract metadata
            player_id = session.get('metadata', {}).get('player_id')
            upgrade_id = session.get('metadata', {}).get('upgrade_id')
            payment_intent_id = session.get('payment_intent', 'unknown')

            if player_id and upgrade_id:
                # Get game state
                game_state = GameService.create_or_get_game_state(player_id)

                # Purchase and activate the upgrade
                result = GameService.purchase_premium_upgrade(
                    game_state,
                    upgrade_id,
                    payment_intent_id,
                    session.get('id', '')
                )

                if not result['success']:
                    print(f"Warning: Payment succeeded but activation failed: {result['message']}")

        return HttpResponse(status=200)

    except Exception as e:
        print(f"Webhook error: {str(e)}")
        return HttpResponse(status=500)


@api_view(['GET'])
def get_premium_upgrades(request):
    """
    Get all available premium upgrades
    """
    try:
        premium_upgrades = UpgradeTemplate.objects.filter(is_premium=True)

        upgrades_data = []
        for upgrade in premium_upgrades:
            upgrades_data.append({
                'upgrade_id': upgrade.upgrade_id,
                'name': upgrade.name,
                'description': upgrade.description,
                'premium_price_cents': upgrade.premium_price_cents,
                'premium_price_usd': upgrade.premium_price_cents / 100,
                'effect_type': upgrade.effect_type,
                'effect_value': upgrade.effect_value,
                'duration_seconds': upgrade.duration_seconds,
                'is_consumable': upgrade.is_consumable,
            })

        return Response(upgrades_data)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_active_buffs(request, player_id):
    """
    Get all active buffs for a player
    """
    try:
        game_state = GameService.create_or_get_game_state(player_id)
        buffs = GameService.get_active_buffs(game_state)

        from .serializers import ActiveBuffSerializer
        serializer = ActiveBuffSerializer(buffs, many=True)

        return Response(serializer.data)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
