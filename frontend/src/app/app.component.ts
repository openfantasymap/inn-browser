import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { GameService } from './services/game.service';
import { InnState, Room, Guest, Upgrade, RoomType, TavernItem, Recipe, ItemType, ItemQuality } from './models/game.models';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy {
  title = 'Fantasy Inn Tycoon';
  gameState: InnState | null = null;
  selectedGuest: Guest | null = null;
  RoomType = RoomType;

  constructor(private gameService: GameService) {}

  ngOnInit(): void {
    this.gameService.gameState$.subscribe(state => {
      this.gameState = state;
    });

    this.gameService.getGameState().subscribe();
    this.gameService.startAutoTick();
  }

  ngOnDestroy(): void {
    this.gameService.stopAutoTick();
  }

  startNewGame(): void {
    this.gameService.startNewGame().subscribe();
  }

  assignGuestToRoom(guest: Guest, room: Room): void {
    if (!room.occupied && !guest.room_id) {
      this.gameService.assignGuestToRoom(guest.id, room.id).subscribe();
      this.selectedGuest = null;
    }
  }

  selectGuest(guest: Guest): void {
    if (!guest.room_id) {
      this.selectedGuest = guest;
    }
  }

  cleanRoom(room: Room): void {
    this.gameService.cleanRoom(room.id).subscribe();
  }

  purchaseUpgrade(upgrade: Upgrade): void {
    if (!upgrade.purchased && this.gameState && this.gameState.resources.gold >= upgrade.cost) {
      this.gameService.purchaseUpgrade(upgrade.id).subscribe();
    }
  }

  buildRoom(roomType: RoomType): void {
    this.gameService.buildRoom(roomType).subscribe();
  }

  getWaitingGuests(): Guest[] {
    return this.gameState?.guests.filter(g => !g.room_id) || [];
  }

  getGuestInRoom(roomId: string): Guest | null {
    if (!this.gameState) return null;
    return this.gameState.guests.find(g => g.room_id === roomId) || null;
  }

  getCleanlinessColor(cleanliness: number): string {
    if (cleanliness >= 80) return '#4ade80';
    if (cleanliness >= 50) return '#fbbf24';
    return '#f87171';
  }

  getPatienceColor(patience: number): string {
    if (patience >= 70) return '#4ade80';
    if (patience >= 40) return '#fbbf24';
    return '#f87171';
  }

  getRoomTypeDisplay(roomType: RoomType): string {
    const displays: { [key in RoomType]: string } = {
      [RoomType.BASIC]: '🛏️ Basic',
      [RoomType.STANDARD]: '🏠 Standard',
      [RoomType.DELUXE]: '🏰 Deluxe',
      [RoomType.ROYAL]: '👑 Royal'
    };
    return displays[roomType];
  }

  getGuestTypeDisplay(guestType: string): string {
    const displays: { [key: string]: string } = {
      'peasant': '🧑‍🌾',
      'merchant': '💼',
      'noble': '👔',
      'adventurer': '⚔️',
      'wizard': '🧙',
      'bandit': '🗡️',
      'monk': '🙏',
      'bard': '🎵',
      'dragon_disguised': '🐉',
      'beggar': '🤲',
      'prince': '🤴',
      'thief': '🥷',
      'scholar': '📚',
      'drunk': '🍺',
      'ghost': '👻'
    };
    return displays[guestType] || '👤';
  }

  getGuestTypeName(guestType: string): string {
    const names: { [key: string]: string } = {
      'peasant': 'Peasant',
      'merchant': 'Merchant',
      'noble': 'Noble',
      'adventurer': 'Adventurer',
      'wizard': 'Wizard',
      'bandit': 'Bandit',
      'monk': 'Monk',
      'bard': 'Bard',
      'dragon_disguised': 'Dragon',
      'beggar': 'Beggar',
      'prince': 'Prince',
      'thief': 'Thief',
      'scholar': 'Scholar',
      'drunk': 'Drunk',
      'ghost': 'Ghost'
    };
    return names[guestType] || 'Guest';
  }

  getReputationColor(reputation: number): string {
    if (reputation >= 1.0) return '#10b981';  // Green for high rep
    if (reputation >= 0.5) return '#3b82f6';  // Blue for good rep
    if (reputation >= 0) return '#6b7280';    // Gray for neutral
    return '#ef4444';  // Red for negative rep
  }

  getGoldColor(gold: number): string {
    if (gold >= 5.0) return '#f59e0b';   // Orange for very high
    if (gold >= 2.0) return '#fbbf24';   // Yellow for high
    if (gold >= 1.0) return '#84cc16';   // Light green for medium
    return '#9ca3af';  // Gray for low
  }

  getRoomCost(roomType: RoomType): number {
    const costs = {
      [RoomType.BASIC]: 50,
      [RoomType.STANDARD]: 200,
      [RoomType.DELUXE]: 800,
      [RoomType.ROYAL]: 3000
    };
    return costs[roomType];
  }

  canAffordRoom(roomType: RoomType): boolean {
    return this.gameState ? this.gameState.resources.gold >= this.getRoomCost(roomType) : false;
  }

  // Tavern functions
  selectedGuestForServing: Guest | null = null;
  ItemType = ItemType;

  unlockRecipe(recipe: Recipe): void {
    if (this.gameState && this.gameState.resources.gold >= recipe.cost_to_unlock) {
      this.gameService.unlockRecipe(recipe.id).subscribe();
    }
  }

  craftItem(item: TavernItem, quantity: number = 1): void {
    const recipe = this.gameState?.recipes.find(r => r.item_id === item.id);
    if (recipe && recipe.unlocked && this.gameState) {
      const cost = recipe.ingredients_cost * quantity;
      if (this.gameState.resources.gold >= cost) {
        this.gameService.craftItem(item.id, quantity).subscribe();
      }
    }
  }

  serveItem(guest: Guest, item: TavernItem): void {
    if (this.hasItemInInventory(item.id)) {
      this.gameService.serveGuest(guest.id, item.id).subscribe();
      this.selectedGuestForServing = null;
    }
  }

  getItemCount(itemId: string): number {
    return this.gameState?.inventory.items[itemId] || 0;
  }

  hasItemInInventory(itemId: string): boolean {
    return this.getItemCount(itemId) > 0;
  }

  getItemEmoji(item: TavernItem): string {
    if (item.item_type === ItemType.FOOD) {
      switch (item.quality) {
        case ItemQuality.BASIC: return '🍞';
        case ItemQuality.GOOD: return '🍗';
        case ItemQuality.FINE: return '🍖';
        case ItemQuality.EXQUISITE: return '🐉';
        default: return '🍴';
      }
    } else {
      switch (item.quality) {
        case ItemQuality.BASIC: return '🍺';
        case ItemQuality.GOOD: return '🍷';
        case ItemQuality.FINE: return '🧉';
        case ItemQuality.LEGENDARY: return '🍾';
        default: return '🥤';
      }
    }
  }

  getQualityColor(quality: ItemQuality): string {
    switch (quality) {
      case ItemQuality.BASIC: return '#9ca3af';
      case ItemQuality.GOOD: return '#3b82f6';
      case ItemQuality.FINE: return '#8b5cf6';
      case ItemQuality.EXQUISITE: return '#f59e0b';
      case ItemQuality.LEGENDARY: return '#ef4444';
      default: return '#6b7280';
    }
  }

  getFoodItems(): TavernItem[] {
    return this.gameState?.tavern_items.filter(i => i.item_type === ItemType.FOOD) || [];
  }

  getBeverageItems(): TavernItem[] {
    return this.gameState?.tavern_items.filter(i => i.item_type === ItemType.BEVERAGE) || [];
  }

  canServeFood(guest: Guest): boolean {
    return !guest.fed;
  }

  canServeDrink(guest: Guest): boolean {
    return !guest.served_drink;
  }
}
