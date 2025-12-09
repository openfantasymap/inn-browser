export enum RoomType {
  BASIC = 'basic',
  STANDARD = 'standard',
  DELUXE = 'deluxe',
  ROYAL = 'royal'
}

export enum GuestType {
  PEASANT = 'peasant',
  MERCHANT = 'merchant',
  NOBLE = 'noble',
  ADVENTURER = 'adventurer',
  WIZARD = 'wizard',
  BANDIT = 'bandit',
  MONK = 'monk',
  BARD = 'bard',
  DRAGON_DISGUISED = 'dragon_disguised',
  BEGGAR = 'beggar',
  PRINCE = 'prince',
  THIEF = 'thief',
  SCHOLAR = 'scholar',
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

export interface Recipe {
  id: string;
  name: string;
  item_id: string;
  unlocked: boolean;
  cost_to_unlock: number;
  ingredients_cost: number;
}

export interface Inventory {
  items: { [key: string]: number };
}

export interface Guest {
  id: string;
  name: string;
  guest_type: GuestType;
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
}

export interface Resources {
  gold: number;
  reputation: number;
  max_guests: number;
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
}
