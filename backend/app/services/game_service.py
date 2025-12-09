import uuid
import random
from datetime import datetime, timedelta
from typing import Dict, List
from app.models.game_models import (
    InnState, Room, Guest, Upgrade, Resources,
    RoomType, GuestType
)


class GameService:
    def __init__(self):
        self.game_states: Dict[str, InnState] = {}
        self.guest_names = [
            "Aldric", "Brunhilde", "Cedric", "Elara", "Finnian",
            "Gwendolyn", "Thorne", "Isolde", "Magnus", "Rosalind",
            "Gareth", "Freya", "Ragnar", "Sylvia", "Oswald",
            "Bjorn", "Aria", "Dorian", "Lyra", "Cassius",
            "Seraphina", "Orion", "Luna", "Dante", "Aurora",
            "Zephyr", "Celeste", "Raven", "Phoenix", "Sage",
            "Grimwald", "Mystique", "Shadow", "Titus", "Ophelia"
        ]

    def create_new_game(self, player_id: str) -> InnState:
        """Initialize a new game state"""
        initial_rooms = [
            Room(
                id=str(uuid.uuid4()),
                room_type=RoomType.BASIC,
                level=1,
                income_rate=1.0
            ) for _ in range(3)
        ]

        initial_upgrades = self._generate_initial_upgrades()

        game_state = InnState(
            resources=Resources(gold=100.0, reputation=0.0, max_guests=5),
            rooms=initial_rooms,
            guests=[],
            upgrades=initial_upgrades,
            total_income_multiplier=1.0,
            auto_clean_enabled=False,
            last_update=datetime.utcnow(),
            game_speed=1.0
        )

        self.game_states[player_id] = game_state
        return game_state

    def get_game_state(self, player_id: str) -> InnState:
        """Get current game state or create new one"""
        if player_id not in self.game_states:
            return self.create_new_game(player_id)
        return self.game_states[player_id]

    def _generate_initial_upgrades(self) -> List[Upgrade]:
        """Generate available upgrades"""
        return [
            Upgrade(
                id="upgrade_income_1",
                name="Better Beds",
                description="Increase income from all rooms by 50%",
                cost=200.0,
                effect_type="income_multiplier",
                effect_value=1.5
            ),
            Upgrade(
                id="upgrade_auto_clean",
                name="Hire Cleaning Staff",
                description="Automatically clean rooms over time",
                cost=300.0,
                effect_type="auto_clean",
                effect_value=1.0
            ),
            Upgrade(
                id="upgrade_capacity_1",
                name="Expand Inn",
                description="Increase max guest capacity by 5",
                cost=400.0,
                effect_type="guest_capacity",
                effect_value=5.0
            ),
            Upgrade(
                id="upgrade_room_standard",
                name="Standard Room",
                description="Unlock Standard room type (2x income)",
                cost=500.0,
                effect_type="unlock_room",
                effect_value=2.0
            ),
            Upgrade(
                id="upgrade_income_2",
                name="Luxury Furnishings",
                description="Increase income from all rooms by 100%",
                cost=1000.0,
                effect_type="income_multiplier",
                effect_value=2.0
            ),
            Upgrade(
                id="upgrade_room_deluxe",
                name="Deluxe Room",
                description="Unlock Deluxe room type (4x income)",
                cost=2000.0,
                effect_type="unlock_room",
                effect_value=4.0
            ),
        ]

    def process_tick(self, player_id: str) -> InnState:
        """Process one game tick"""
        game_state = self.get_game_state(player_id)
        now = datetime.utcnow()

        # Calculate time delta for incremental progress
        time_delta = (now - game_state.last_update).total_seconds()
        ticks = max(1, int(time_delta * game_state.game_speed))

        # Process each tick
        for _ in range(ticks):
            self._process_single_tick(game_state)

        game_state.last_update = now
        return game_state

    def _process_single_tick(self, game_state: InnState):
        """Process a single game tick"""
        # Generate income from occupied rooms
        for room in game_state.rooms:
            if room.occupied and room.current_guest:
                guest = next((g for g in game_state.guests if g.id == room.current_guest), None)
                if guest:
                    income = room.income_rate * guest.gold_per_tick * game_state.total_income_multiplier
                    game_state.resources.gold += income

                    # Decrease room cleanliness
                    room.cleanliness = max(0, room.cleanliness - 0.5)

                    # Decrease guest patience if room is dirty
                    if room.cleanliness < 50:
                        guest.patience = max(0, guest.patience - 1.0)

        # Auto-clean if enabled
        if game_state.auto_clean_enabled:
            for room in game_state.rooms:
                room.cleanliness = min(100, room.cleanliness + 2.0)

        # Check for guests leaving
        guests_to_remove = []
        for guest in game_state.guests:
            if guest.patience <= 0 or guest.check_in_time and \
               (datetime.utcnow() - guest.check_in_time).total_seconds() > guest.stay_duration:
                # Guest leaves
                if guest.room_id:
                    room = next((r for r in game_state.rooms if r.id == guest.room_id), None)
                    if room:
                        room.occupied = False
                        room.current_guest = None

                # Add reputation bonus if guest was happy
                if guest.patience > 70:
                    game_state.resources.reputation += guest.reputation_bonus

                guests_to_remove.append(guest.id)

        game_state.guests = [g for g in game_state.guests if g.id not in guests_to_remove]

        # Potentially spawn new guest
        if len(game_state.guests) < game_state.resources.max_guests and random.random() < 0.1:
            self._spawn_guest(game_state)

    def _spawn_guest(self, game_state: InnState):
        """Spawn a new guest with randomized attributes"""
        guest_type = random.choice(list(GuestType))

        # Base attributes for each guest type with ranges for randomization
        # Format: (base_gold_min, base_gold_max, base_rep_min, base_rep_max, rarity_weight)
        type_configs = {
            GuestType.PEASANT: (0.3, 0.7, 0.05, 0.15, 10),  # Comune
            GuestType.MERCHANT: (1.0, 2.0, 0.2, 0.4, 8),  # Comune
            GuestType.NOBLE: (2.5, 4.0, 0.4, 0.7, 5),  # Non comune
            GuestType.ADVENTURER: (1.5, 2.5, 0.3, 0.5, 7),  # Comune
            GuestType.WIZARD: (3.0, 5.0, 0.6, 1.0, 4),  # Raro
            GuestType.BANDIT: (2.0, 4.0, -0.3, 0.1, 6),  # Alto oro, bassa/negativa rep
            GuestType.MONK: (0.2, 0.5, 0.8, 1.5, 5),  # Basso oro, alta rep
            GuestType.BARD: (1.0, 1.5, 0.7, 1.2, 6),  # Medio oro, alta rep
            GuestType.DRAGON_DISGUISED: (8.0, 15.0, -0.5, 2.0, 1),  # Rarissimo, stats estremi
            GuestType.BEGGAR: (0.1, 0.3, 0.2, 0.4, 8),  # Bassissimo oro
            GuestType.PRINCE: (4.0, 7.0, 1.5, 3.0, 2),  # Molto raro, ottimi stats
            GuestType.THIEF: (2.5, 4.5, -0.5, -0.1, 5),  # Alto oro, rep negativa
            GuestType.SCHOLAR: (0.5, 1.0, 0.9, 1.6, 6),  # Basso oro, alta rep
            GuestType.DRUNK: (1.2, 2.0, -0.2, 0.2, 7),  # Medio oro, bassa rep
            GuestType.GHOST: (0.0, 0.1, 1.0, 2.5, 3),  # Quasi nessun oro, altissima rep
        }

        # Weighted random selection based on rarity
        types_list = list(type_configs.keys())
        weights = [type_configs[t][4] for t in types_list]
        guest_type = random.choices(types_list, weights=weights)[0]

        config = type_configs[guest_type]

        # Generate random attributes within the type's range
        gold_per_tick = round(random.uniform(config[0], config[1]), 2)
        reputation_bonus = round(random.uniform(config[2], config[3]), 2)

        # Add some extra randomization (±20%) to make each guest unique
        variation = random.uniform(0.8, 1.2)
        gold_per_tick = max(0, round(gold_per_tick * variation, 2))
        reputation_bonus = round(reputation_bonus * variation, 2)

        # Random stay duration based on guest type
        if guest_type in [GuestType.BEGGAR, GuestType.DRUNK]:
            stay_duration = random.randint(3, 8)  # Short stay
        elif guest_type in [GuestType.NOBLE, GuestType.PRINCE, GuestType.WIZARD]:
            stay_duration = random.randint(15, 30)  # Long stay
        else:
            stay_duration = random.randint(8, 20)  # Normal stay

        guest = Guest(
            id=str(uuid.uuid4()),
            name=random.choice(self.guest_names),
            guest_type=guest_type,
            patience=100.0,
            gold_per_tick=gold_per_tick,
            reputation_bonus=reputation_bonus,
            stay_duration=stay_duration
        )

        game_state.guests.append(guest)

    def assign_guest_to_room(self, player_id: str, guest_id: str, room_id: str) -> InnState:
        """Assign a guest to a room"""
        game_state = self.get_game_state(player_id)

        guest = next((g for g in game_state.guests if g.id == guest_id), None)
        room = next((r for r in game_state.rooms if r.id == room_id), None)

        if guest and room and not room.occupied:
            guest.room_id = room_id
            guest.check_in_time = datetime.utcnow()
            room.occupied = True
            room.current_guest = guest_id

        return game_state

    def clean_room(self, player_id: str, room_id: str) -> InnState:
        """Manually clean a room"""
        game_state = self.get_game_state(player_id)

        room = next((r for r in game_state.rooms if r.id == room_id), None)
        if room:
            room.cleanliness = 100.0

        return game_state

    def purchase_upgrade(self, player_id: str, upgrade_id: str) -> InnState:
        """Purchase an upgrade"""
        game_state = self.get_game_state(player_id)

        upgrade = next((u for u in game_state.upgrades if u.id == upgrade_id), None)

        if upgrade and not upgrade.purchased and game_state.resources.gold >= upgrade.cost:
            game_state.resources.gold -= upgrade.cost
            upgrade.purchased = True

            # Apply upgrade effect
            if upgrade.effect_type == "income_multiplier":
                game_state.total_income_multiplier *= upgrade.effect_value
            elif upgrade.effect_type == "auto_clean":
                game_state.auto_clean_enabled = True
            elif upgrade.effect_type == "guest_capacity":
                game_state.resources.max_guests += int(upgrade.effect_value)
            elif upgrade.effect_type == "unlock_room":
                # Add new room of unlocked type
                new_room_type = RoomType.STANDARD if "standard" in upgrade_id else RoomType.DELUXE
                new_room = Room(
                    id=str(uuid.uuid4()),
                    room_type=new_room_type,
                    level=1,
                    income_rate=upgrade.effect_value
                )
                game_state.rooms.append(new_room)

        return game_state

    def build_room(self, player_id: str, room_type: RoomType) -> InnState:
        """Build a new room"""
        game_state = self.get_game_state(player_id)

        # Room costs
        costs = {
            RoomType.BASIC: 50,
            RoomType.STANDARD: 200,
            RoomType.DELUXE: 800,
            RoomType.ROYAL: 3000
        }

        income_rates = {
            RoomType.BASIC: 1.0,
            RoomType.STANDARD: 2.0,
            RoomType.DELUXE: 4.0,
            RoomType.ROYAL: 8.0
        }

        cost = costs.get(room_type, 100)

        if game_state.resources.gold >= cost:
            game_state.resources.gold -= cost
            new_room = Room(
                id=str(uuid.uuid4()),
                room_type=room_type,
                level=1,
                income_rate=income_rates.get(room_type, 1.0)
            )
            game_state.rooms.append(new_room)

        return game_state


# Global instance
game_service = GameService()
