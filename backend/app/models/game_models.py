from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum
from datetime import datetime


class RoomType(str, Enum):
    BASIC = "basic"
    STANDARD = "standard"
    DELUXE = "deluxe"
    ROYAL = "royal"


class GuestType(str, Enum):
    PEASANT = "peasant"
    MERCHANT = "merchant"
    NOBLE = "noble"
    ADVENTURER = "adventurer"
    WIZARD = "wizard"
    BANDIT = "bandit"  # Alto guadagno, bassa reputazione
    MONK = "monk"  # Basso guadagno, alta reputazione
    BARD = "bard"  # Medio guadagno, alta reputazione
    DRAGON_DISGUISED = "dragon_disguised"  # Altissimo guadagno, reputazione casuale
    BEGGAR = "beggar"  # Bassissimo guadagno, media reputazione
    PRINCE = "prince"  # Alto guadagno, altissima reputazione
    THIEF = "thief"  # Alto guadagno, reputazione negativa
    SCHOLAR = "scholar"  # Basso guadagno, alta reputazione
    DRUNK = "drunk"  # Medio guadagno, bassa reputazione
    GHOST = "ghost"  # Nessun guadagno, alta reputazione (speciale)


class Room(BaseModel):
    id: str
    room_type: RoomType
    level: int = 1
    occupied: bool = False
    current_guest: Optional[str] = None
    income_rate: float = Field(default=1.0)
    cleanliness: float = Field(default=100.0, ge=0, le=100)


class ItemType(str, Enum):
    FOOD = "food"
    BEVERAGE = "beverage"


class ItemQuality(str, Enum):
    BASIC = "basic"
    GOOD = "good"
    FINE = "fine"
    EXQUISITE = "exquisite"
    LEGENDARY = "legendary"


class IngredientRarity(str, Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


class Ingredient(BaseModel):
    id: str
    name: str
    rarity: IngredientRarity
    description: str = ""
    # Drop chances from guests
    base_drop_chance: float = 0.1  # 10% base chance


class IngredientRequirement(BaseModel):
    ingredient_id: str
    quantity: int = 1


class TavernItem(BaseModel):
    id: str
    name: str
    item_type: ItemType
    quality: ItemQuality
    cost: float  # Cost to produce/buy
    gold_bonus: float = 0.0  # Extra gold per tick when served
    patience_bonus: float = 0.0  # Patience restored
    reputation_bonus: float = 0.0  # Extra reputation
    satisfaction_bonus: float = 0.0  # Overall satisfaction increase
    description: str = ""


class Recipe(BaseModel):
    id: str
    name: str
    item_id: str  # The item this recipe creates
    unlocked: bool = False
    discovered: bool = False  # Has player discovered this recipe?
    cost_to_unlock: float = 0.0
    ingredients_cost: float = 0.0  # Cost in gold to craft (legacy, still used)
    required_ingredients: List[IngredientRequirement] = Field(default_factory=list)
    # If empty, uses ingredients_cost as gold-only recipe


class Inventory(BaseModel):
    items: Dict[str, int] = Field(default_factory=dict)  # item_id -> quantity


class IngredientInventory(BaseModel):
    ingredients: Dict[str, int] = Field(default_factory=dict)  # ingredient_id -> quantity


class Guest(BaseModel):
    id: str
    name: str
    guest_type: GuestType
    room_id: Optional[str] = None
    patience: float = Field(default=100.0, ge=0, le=100)
    gold_per_tick: float = 1.0
    reputation_bonus: float = 0.1
    check_in_time: Optional[datetime] = None
    stay_duration: int = 10  # ticks
    fed: bool = False  # Has been served food
    served_drink: bool = False  # Has been served beverage
    satisfaction: float = Field(default=50.0, ge=0, le=100)  # Guest satisfaction
    food_served: Optional[str] = None  # ID of food item served
    beverage_served: Optional[str] = None  # ID of beverage served


class Upgrade(BaseModel):
    id: str
    name: str
    description: str
    cost: float
    purchased: bool = False
    effect_type: str  # "income_multiplier", "auto_clean", "guest_capacity", etc.
    effect_value: float


class Resources(BaseModel):
    gold: float = Field(default=100.0)
    reputation: float = Field(default=0.0)
    max_guests: int = Field(default=5)


class InnState(BaseModel):
    resources: Resources = Field(default_factory=Resources)
    rooms: List[Room] = Field(default_factory=list)
    guests: List[Guest] = Field(default_factory=list)
    upgrades: List[Upgrade] = Field(default_factory=list)
    total_income_multiplier: float = 1.0
    auto_clean_enabled: bool = False
    last_update: datetime = Field(default_factory=datetime.utcnow)
    game_speed: float = 1.0  # Ticks per second
    # Tavern system
    tavern_items: List[TavernItem] = Field(default_factory=list)
    recipes: List[Recipe] = Field(default_factory=list)
    inventory: Inventory = Field(default_factory=Inventory)
    tavern_unlocked: bool = False
    # Ingredient system
    available_ingredients: List[Ingredient] = Field(default_factory=list)
    ingredient_inventory: IngredientInventory = Field(default_factory=IngredientInventory)


class GameAction(BaseModel):
    action_type: str
    target_id: Optional[str] = None
    data: Optional[dict] = None
