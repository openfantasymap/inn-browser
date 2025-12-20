export enum RoomType {
  BASIC = 'basic',
  STANDARD = 'standard',
  DELUXE = 'deluxe',
  ROYAL = 'royal'
}

export enum GuestType {
  // Common travelers
  PEASANT = 'peasant',
  MERCHANT = 'merchant',
  NOBLE = 'noble',
  ADVENTURER = 'adventurer',

  // Magical types
  WIZARD = 'wizard',
  SORCERER = 'sorcerer',
  WITCH = 'witch',
  ALCHEMIST = 'alchemist',
  NECROMANCER = 'necromancer',

  // Warriors
  KNIGHT = 'knight',
  PALADIN = 'paladin',
  RANGER = 'ranger',
  BARBARIAN = 'barbarian',
  SAMURAI = 'samurai',

  // Rogues/Outlaws
  BANDIT = 'bandit',
  THIEF = 'thief',
  ASSASSIN = 'assassin',
  SMUGGLER = 'smuggler',

  // Religious/Spiritual
  MONK = 'monk',
  PRIEST = 'priest',
  CLERIC = 'cleric',
  DRUID = 'druid',

  // Entertainers
  BARD = 'bard',
  JESTER = 'jester',
  MINSTREL = 'minstrel',
  ACTOR = 'actor',

  // Craftspeople
  BLACKSMITH = 'blacksmith',
  CARPENTER = 'carpenter',
  JEWELER = 'jeweler',
  TAILOR = 'tailor',

  // Scholars
  SCHOLAR = 'scholar',
  SCRIBE = 'scribe',
  LIBRARIAN = 'librarian',
  HISTORIAN = 'historian',

  // Exotic/Rare
  DRAGON_DISGUISED = 'dragon_disguised',
  VAMPIRE = 'vampire',
  WEREWOLF = 'werewolf',
  ELF = 'elf',
  DWARF = 'dwarf',
  HALFLING = 'halfling',
  ORC = 'orc',

  // Special
  BEGGAR = 'beggar',
  PRINCE = 'prince',
  PIRATE = 'pirate',
  SPY = 'spy',
  DRUNK = 'drunk',
  GHOST = 'ghost'
}

export interface Room {
  id: string;
  room_type: RoomType;
  level: number;
  occupied: boolean;
  current_guest: string | null;
  income_rate: number;
  cleanliness: number;
  customers_served: number;
}

export interface RoomTypeTemplate {
  id: string;
  name: string;
  description: string;
  base_cost: number;
  income_multiplier: number;
  emoji: string;
  required_upgrade_id: string | null;
  species_bonuses: { [species: string]: number };
  type_bonuses: { [type: string]: number };
}

export enum ItemType {
  FOOD = 'food',
  BEVERAGE = 'beverage'
}

export enum ItemQuality {
  BASIC = 'basic',
  GOOD = 'good',
  FINE = 'fine',
  EXQUISITE = 'exquisite',
  LEGENDARY = 'legendary'
}

export interface TavernItem {
  id: string;
  name: string;
  item_type: ItemType;
  quality: ItemQuality;
  cost: number;
  gold_bonus: number;
  patience_bonus: number;
  reputation_bonus: number;
  satisfaction_bonus: number;
  description: string;
}

export interface IngredientRequirement {
  ingredient_id: string;
  quantity: number;
}

export interface Recipe {
  id: string;
  name: string;
  item_id: string;
  unlocked: boolean;
  discovered: boolean;
  cost_to_unlock: number;
  ingredients_cost: number;
  required_ingredients: IngredientRequirement[];
  times_crafted: number;
  discovered_at: string | null;
  unlocked_at: string | null;
}

export enum IngredientRarity {
  COMMON = 'common',
  UNCOMMON = 'uncommon',
  RARE = 'rare',
  EPIC = 'epic',
  LEGENDARY = 'legendary'
}

export interface Ingredient {
  id: string;
  name: string;
  rarity: IngredientRarity;
  description: string;
  base_drop_chance: number;
  is_purchasable: boolean;
  market_price: number;
}

export interface ExperimentResult {
  success: boolean;
  message: string;
  discovered_recipe?: {
    recipe_id: string;
    name: string;
    item_name: string;
    unlocked: boolean;
    cost_to_unlock: number;
  };
  consumed_ingredients?: boolean;
  game_state: InnState;
}

export interface Inventory {
  items: { [key: string]: number };
  ingredients: { [key: string]: number };
}

export interface Guest {
  id: string;
  name: string;
  guest_type: GuestType;
  species: string;
  room_id: string | null;
  patience: number;
  gold_per_tick: number;
  reputation_bonus: number;
  check_in_time: string | null;
  stay_duration: number;
  fed: boolean;
  served_drink: boolean;
  satisfaction: number;
  food_served: string | null;
  beverage_served: string | null;
}

export interface Upgrade {
  id: string;
  name: string;
  description: string;
  cost: number;
  purchased: boolean;
  effect_type: string;
  effect_value: number;
  operational_cost_per_tick?: number;
  // Premium upgrade fields
  is_premium?: boolean;
  premium_price_cents?: number;
  premium_price_usd?: number;
  duration_seconds?: number;
  is_consumable?: boolean;
}

export interface Resources {
  gold: number;
  reputation: number;
  max_guests: number;
}

export interface Location {
  map: string;
  x: number;
  y: number;
}

export interface OfflineProgress {
  earnings: number;
  hours: number;
}

export interface Achievement {
  id: string;
  name: string;
  description: string;
  requirement_type: string;
  requirement_value: number;
  requirement_metadata: any;
  icon: string;
  reward_upgrade_id: string | null;
  reward_upgrade_name: string | null;
}

export interface PlayerAchievement {
  achievement: Achievement;
  progress: number;
  earned_at: string;
  is_completed: boolean;
}

export interface AchievementWithProgress {
  id: string;
  name: string;
  description: string;
  requirement_type: string;
  requirement_value: number;
  requirement_metadata: any;
  icon: string;
  reward_upgrade_id: string | null;
  reward_upgrade_name: string | null;
  progress: number;
  is_completed: boolean;
  earned_at: string | null;
}

export interface InnState {
  resources: Resources;
  rooms: Room[];
  guests: Guest[];
  upgrades: Upgrade[];
  total_income_multiplier: number;
  auto_clean_enabled: boolean;
  last_update: string;
  game_speed: number;
  tavern_items: TavernItem[];
  recipes: Recipe[];
  inventory: Inventory;
  tavern_unlocked: boolean;
  available_ingredients: Ingredient[];
  room_types: RoomTypeTemplate[];
  location: Location;
  offline_progress: OfflineProgress;
  max_offline_hours: number;
  achievements: PlayerAchievement[];
  all_achievements: AchievementWithProgress[];
  premium_upgrades: Upgrade[];
}
