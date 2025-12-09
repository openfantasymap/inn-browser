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
  WIZARD = 'wizard'
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
}
