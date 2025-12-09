from fastapi import APIRouter, HTTPException
from app.models.game_models import InnState, GameAction, RoomType
from app.services.game_service import game_service

router = APIRouter(prefix="/api/game", tags=["game"])


@router.get("/state/{player_id}", response_model=InnState)
async def get_game_state(player_id: str):
    """Get current game state for a player"""
    return game_service.get_game_state(player_id)


@router.post("/new/{player_id}", response_model=InnState)
async def new_game(player_id: str):
    """Start a new game"""
    return game_service.create_new_game(player_id)


@router.post("/tick/{player_id}", response_model=InnState)
async def process_tick(player_id: str):
    """Process game tick and return updated state"""
    return game_service.process_tick(player_id)


@router.post("/assign-guest/{player_id}", response_model=InnState)
async def assign_guest(player_id: str, guest_id: str, room_id: str):
    """Assign a guest to a room"""
    return game_service.assign_guest_to_room(player_id, guest_id, room_id)


@router.post("/clean-room/{player_id}/{room_id}", response_model=InnState)
async def clean_room(player_id: str, room_id: str):
    """Clean a room manually"""
    return game_service.clean_room(player_id, room_id)


@router.post("/purchase-upgrade/{player_id}/{upgrade_id}", response_model=InnState)
async def purchase_upgrade(player_id: str, upgrade_id: str):
    """Purchase an upgrade"""
    return game_service.purchase_upgrade(player_id, upgrade_id)


@router.post("/build-room/{player_id}", response_model=InnState)
async def build_room(player_id: str, room_type: RoomType):
    """Build a new room"""
    return game_service.build_room(player_id, room_type)
