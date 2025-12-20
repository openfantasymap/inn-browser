import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { GameService } from './services/game.service';
import { AuthService, User } from './core/auth/auth.service';
import { LoginComponent } from './core/auth/login/login.component';
import { HeaderComponent } from './shared/header/header.component';
import { ResourcesPanelComponent } from './shared/resources-panel/resources-panel.component';
import { TabNavigationComponent } from './shared/tab-navigation/tab-navigation.component';
import { InnState, Room, Guest, Upgrade, RoomType, TavernItem, Recipe, ItemType, ItemQuality, Ingredient, ExperimentResult, PlayerAchievement } from './models/game.models';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    LoginComponent,
    HeaderComponent,
    ResourcesPanelComponent,
    TabNavigationComponent,
],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy {
  title = 'Fantasy Inn Tycoon';
  gameState: InnState | null = null;
  selectedGuest: Guest | null = null;
  RoomType = RoomType;

  // Authentication
  currentUser: User | null = null;
  isAuthenticated: boolean = false;

  // Tab state
  activeTab: 'inn' | 'tavern' = 'inn';

  // Offline notification state
  offlineNotificationDismissed: boolean = false;

  // Achievement notifications
  achievementNotifications: Array<{achievement: PlayerAchievement, id: number}> = [];
  private nextNotificationId = 0;
  private previousAchievements: Map<string, boolean> = new Map();
  private shownAchievements: Set<string> = new Set(); // Track achievements that have been shown to prevent duplicates
  private readonly SHOWN_ACHIEVEMENTS_KEY = 'shown_achievements';

  // Drag and drop state
  draggedGuest: Guest | null = null;
  dragOverRoomId: string | null = null;

  activeUpgradeTab: 'available' | 'purchased' | 'premium' = 'available';

  constructor(
    private gameService: GameService,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    // Load previously shown achievements from localStorage
    this.loadShownAchievements();

    // Subscribe to authentication state
    this.authService.user$.subscribe(user => {
      this.currentUser = user;
      this.isAuthenticated = user !== null;

      // If authenticated, initialize game
      if (this.isAuthenticated) {
        this.initializeGame();
      }
    });
  }

  private loadShownAchievements(): void {
    try {
      const stored = localStorage.getItem(this.SHOWN_ACHIEVEMENTS_KEY);
      if (stored) {
        const achievementIds = JSON.parse(stored);
        this.shownAchievements = new Set(achievementIds);
      }
    } catch (error) {
      console.error('Failed to load shown achievements:', error);
      this.shownAchievements = new Set();
    }
  }

  private saveShownAchievements(): void {
    try {
      const achievementIds = Array.from(this.shownAchievements);
      localStorage.setItem(this.SHOWN_ACHIEVEMENTS_KEY, JSON.stringify(achievementIds));
    } catch (error) {
      console.error('Failed to save shown achievements:', error);
    }
  }

  private initializeGame(): void {
    this.gameService.gameState$.subscribe(state => {
      if (state) {
        // Check for newly completed achievements
        this.checkForNewAchievements(state);
        this.gameState = state;
      }
    });

    // Initial game state fetch - updates will come via MQTT
    this.gameService.getGameState().subscribe();
  }

  private checkForNewAchievements(newState: InnState): void {
    if (!newState.achievements) return;

    newState.achievements.forEach(playerAchievement => {
      const achievementId = playerAchievement.achievement.id;
      const wasCompleted = this.previousAchievements.get(achievementId);
      const isNowCompleted = playerAchievement.is_completed;
      const alreadyShown = this.shownAchievements.has(achievementId);

      // If achievement was not completed before but is now, and hasn't been shown yet, show notification
      if (!wasCompleted && isNowCompleted && !alreadyShown) {
        this.showAchievementNotification(playerAchievement);
      }

      // Update the tracking map
      this.previousAchievements.set(achievementId, isNowCompleted);
    });
  }

  private showAchievementNotification(achievement: PlayerAchievement): void {
    const achievementId = achievement.achievement.id;

    // Mark as shown and persist to localStorage
    this.shownAchievements.add(achievementId);
    this.saveShownAchievements();

    const notification = {
      achievement,
      id: this.nextNotificationId++
    };

    this.achievementNotifications.push(notification);

    // Auto-dismiss after 5 seconds
    setTimeout(() => {
      this.dismissAchievementNotification(notification.id);
    }, 5000);
  }

  dismissAchievementNotification(id: number): void {
    this.achievementNotifications = this.achievementNotifications.filter(n => n.id !== id);
  }

  ngOnDestroy(): void {
    // MQTT connection cleanup is handled by the service
  }

  startNewGame(): void {
    this.gameService.startNewGame().subscribe();
  }

  signOut(): void {
    this.authService.signOut();
    this.gameState = null;
  }

  switchTab(tab: 'inn' | 'tavern'): void {
    this.activeTab = tab;
  }

  dismissOfflineNotification(): void {
    this.offlineNotificationDismissed = true;
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

  // Drag and Drop methods
  onGuestDragStart(event: DragEvent, guest: Guest): void {
    if (guest.room_id) return; // Only allow dragging waiting guests

    this.draggedGuest = guest;
    if (event.dataTransfer) {
      event.dataTransfer.effectAllowed = 'move';
      event.dataTransfer.setData('text/plain', guest.id);
    }

    // Add visual feedback
    const target = event.target as HTMLElement;
    target.style.opacity = '0.5';
  }

  onGuestDragEnd(event: DragEvent): void {
    const target = event.target as HTMLElement;
    target.style.opacity = '1';
    this.draggedGuest = null;
    this.dragOverRoomId = null;
  }

  onRoomDragOver(event: DragEvent, room: Room): void {
    if (!this.draggedGuest || room.occupied) return;

    event.preventDefault(); // Allow drop
    if (event.dataTransfer) {
      event.dataTransfer.dropEffect = 'move';
    }
    this.dragOverRoomId = room.id;
  }

  onRoomDragLeave(event: DragEvent, room: Room): void {
    if (this.dragOverRoomId === room.id) {
      this.dragOverRoomId = null;
    }
  }

  onRoomDrop(event: DragEvent, room: Room): void {
    event.preventDefault();
    this.dragOverRoomId = null;

    if (!this.draggedGuest || room.occupied || this.draggedGuest.room_id) {
      this.draggedGuest = null;
      return;
    }

    // Assign the guest to the room
    this.gameService.assignGuestToRoom(this.draggedGuest.id, room.id).subscribe();
    this.draggedGuest = null;
    this.selectedGuest = null;
  }

  cleanRoom(room: Room): void {
    this.gameService.cleanRoom(room.id).subscribe();
  }

  purchaseUpgrade(upgrade: Upgrade): void {
    if (!upgrade.purchased && this.gameState && this.gameState.resources.gold >= upgrade.cost) {
      this.gameService.purchaseUpgrade(upgrade.id).subscribe();
    }
  }

  purchasePremiumUpgrade(upgrade: Upgrade): void {
    // TODO: Implement Stripe checkout flow
    console.log('Premium upgrade purchase:', upgrade);
    alert(`Premium purchase coming soon!\n\nUpgrade: ${upgrade.name}\nPrice: $${upgrade.premium_price_usd?.toFixed(2)}\n\nStripe integration will be implemented in a future update.`);
  }

  buildRoom(roomType: RoomType): void {
    if (this.isRoomTypeUnlocked(roomType)) {
      this.gameService.buildRoom(roomType).subscribe();
    }
  }

  isRoomTypeUnlocked(roomType: RoomType): boolean {
    return this.gameService.isRoomTypeUnlocked(roomType, this.gameState);
  }

  getRoomTypeRequirement(roomType: RoomType): string {
    const requirements: { [key in RoomType]: string } = {
      [RoomType.BASIC]: 'Always available',
      [RoomType.STANDARD]: 'Unlock Standard Rooms',
      [RoomType.DELUXE]: 'Unlock Deluxe Rooms',
      [RoomType.ROYAL]: 'Unlock Royal Suites'
    };
    return requirements[roomType];
  }

  getSortedRooms(){
    return this.gameState?.rooms.sort((a:Room, b:Room)=> (parseInt(a.id)-parseInt(b.id)));
  }

  getSortedRoomTypes() {
    if (!this.gameState || !this.gameState.room_types) {
      return [];
    }
    // Sort by base_cost ascending
    return this.gameState.room_types.sort((a, b) => a.base_cost - b.base_cost);
  }

  buildRoomByType(roomTypeId: string): void {
    if (this.gameState) {
      this.gameService.buildRoom(roomTypeId as RoomType).subscribe();
    }
  }

  canAffordRoomByTemplate(roomTemplate: any): boolean {
    return this.gameState ? this.gameState.resources.gold >= roomTemplate.base_cost : false;
  }

  isRoomTypeUnlockedByTemplate(roomTemplate: any): boolean {
    if (!roomTemplate.required_upgrade_id) {
      return true; // No requirement, always unlocked
    }

    if (!this.gameState) {
      return false;
    }

    // Check if the required upgrade is purchased
    return this.gameState.upgrades.some(u =>
      u.id === roomTemplate.required_upgrade_id && u.purchased
    );
  }

  getRoomBonusDisplayByTemplate(roomTemplate: any): string {
    const bonuses: string[] = [];

    // Species bonuses
    if (roomTemplate.species_bonuses && Object.keys(roomTemplate.species_bonuses).length > 0) {
      for (const [species, bonus] of Object.entries(roomTemplate.species_bonuses)) {
        bonuses.push(`${species}: ${bonus}x`);
      }
    }

    // Type bonuses
    if (roomTemplate.type_bonuses && Object.keys(roomTemplate.type_bonuses).length > 0) {
      for (const [type, bonus] of Object.entries(roomTemplate.type_bonuses)) {
        bonuses.push(`${type}: ${bonus}x`);
      }
    }

    return bonuses.length > 0 ? bonuses.join(', ') : '';
  }

  getWaitingGuests(): Guest[] {
    return this.gameState?.guests.filter(g => !g.room_id) || [];
  }

  getGuestInRoom(roomId: string): Guest | null {
    if (!this.gameState) return null;
    //@ts-ignore
    return this.gameState.guests.find(g => g.room_id && parseInt(g.room_id) === roomId) || null;
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

  getRoomTemplate(roomType: RoomType): any {
    if (!this.gameState || !this.gameState.room_types) {
      return null;
    }
    return this.gameState.room_types.find(rt => rt.id === roomType);
  }

  getRoomTypeDisplay(roomType: RoomType): string {
    const roomTemplate = this.getRoomTemplate(roomType);
    if (roomTemplate) {
      return `${roomTemplate.emoji} ${roomTemplate.name}`;
    }

    // Fallback to hardcoded values if room_types not loaded yet
    const displays: { [key in RoomType]: string } = {
      [RoomType.BASIC]: '🛏️ Basic',
      [RoomType.STANDARD]: '🏠 Standard',
      [RoomType.DELUXE]: '🏰 Deluxe',
      [RoomType.ROYAL]: '👑 Royal'
    };
    return displays[roomType] || roomType;
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
    if (!this.gameState || !this.gameState.room_types) {
      return 0;
    }
    const roomTemplate = this.gameState.room_types.find(rt => rt.id === roomType);
    return roomTemplate ? roomTemplate.base_cost : 0;
  }

  canAffordRoom(roomType: RoomType): boolean {
    return this.gameState ? this.gameState.resources.gold >= this.getRoomCost(roomType) : false;
  }

  getRoomBonus(room: Room, guest: Guest | null): number {
    if (!guest || !this.gameState || !this.gameState.room_types) {
      return 1.0;
    }

    const roomTemplate = this.gameState.room_types.find(rt => rt.id === room.room_type);
    if (!roomTemplate) {
      return 1.0;
    }

    let bonus = 1.0;

    // Check species bonuses
    if (roomTemplate.species_bonuses && guest.species in roomTemplate.species_bonuses) {
      const speciesBonus = roomTemplate.species_bonuses[guest.species];
      bonus = Math.max(bonus, speciesBonus);
    }

    // Check type bonuses
    if (roomTemplate.type_bonuses && guest.guest_type in roomTemplate.type_bonuses) {
      const typeBonus = roomTemplate.type_bonuses[guest.guest_type];
      bonus = Math.max(bonus, typeBonus);
    }

    return bonus;
  }

  getRoomBonusDisplay(roomType: RoomType): string {
    if (!this.gameState || !this.gameState.room_types) {
      return '';
    }

    const roomTemplate = this.gameState.room_types.find(rt => rt.id === roomType);
    if (!roomTemplate) {
      return '';
    }

    const bonuses: string[] = [];

    // Species bonuses
    if (roomTemplate.species_bonuses && Object.keys(roomTemplate.species_bonuses).length > 0) {
      for (const [species, bonus] of Object.entries(roomTemplate.species_bonuses)) {
        bonuses.push(`${species}: x${bonus}`);
      }
    }

    // Type bonuses
    if (roomTemplate.type_bonuses && Object.keys(roomTemplate.type_bonuses).length > 0) {
      for (const [type, bonus] of Object.entries(roomTemplate.type_bonuses)) {
        bonuses.push(`${type}: x${bonus}`);
      }
    }

    return bonuses.length > 0 ? bonuses.join(', ') : '';
  }

  // Tavern functions
  selectedGuestForServing: Guest | null = null;
  ItemType = ItemType;

  // Recipe discovery
  selectedIngredients: string[] = [];
  experimentMessage: string = '';
  showExperimentResult: boolean = false;

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

  // Recipe discovery methods
  toggleIngredientSelection(ingredientId: string): void {
    const index = this.selectedIngredients.indexOf(ingredientId);
    if (index > -1) {
      this.selectedIngredients.splice(index, 1);
    } else {
      this.selectedIngredients.push(ingredientId);
    }
  }

  isIngredientSelected(ingredientId: string): boolean {
    return this.selectedIngredients.includes(ingredientId);
  }

  experimentWithIngredients(): void {
    if (this.selectedIngredients.length === 0) {
      this.experimentMessage = 'Select at least one ingredient!';
      this.showExperimentResult = true;
      setTimeout(() => this.showExperimentResult = false, 3000);
      return;
    }

    this.gameService.experimentWithIngredients(this.selectedIngredients).subscribe({
      next: (result: ExperimentResult) => {
        if (result.success && result.discovered_recipe) {
          this.experimentMessage = `🎉 ${result.message}\n${result.discovered_recipe.item_name} recipe discovered!`;
          if (!result.discovered_recipe.unlocked) {
            this.experimentMessage += `\nUnlock cost: ${result.discovered_recipe.cost_to_unlock} gold`;
          }
        } else {
          this.experimentMessage = `❌ ${result.message}`;
        }
        this.showExperimentResult = true;
        this.selectedIngredients = [];
        setTimeout(() => this.showExperimentResult = false, 5000);
      },
      error: (err) => {
        this.experimentMessage = `Error: ${err.error?.error || 'Experiment failed'}`;
        this.showExperimentResult = true;
        setTimeout(() => this.showExperimentResult = false, 3000);
      }
    });
  }

  clearSelectedIngredients(): void {
    this.selectedIngredients = [];
  }

  getDiscoveredRecipes(): Recipe[] {
    return this.gameService.getDiscoveredRecipes(this.gameState);
  }

  getUnlockedRecipes(): Recipe[] {
    return this.gameService.getUnlockedRecipes(this.gameState);
  }

  getIngredientRarityColor(rarity: string): string {
    switch (rarity) {
      case 'common': return '#9ca3af';
      case 'uncommon': return '#22c55e';
      case 'rare': return '#3b82f6';
      case 'epic': return '#a855f7';
      case 'legendary': return '#f97316';
      default: return '#6b7280';
    }
  }

  hasEnoughIngredients(recipe: Recipe): boolean {
    if (!this.gameState) return false;
    // For now, we'll just check if the recipe is unlocked
    // In a real implementation, you'd check the ingredient_inventory
    return recipe.unlocked;
  }

  getAvailableIngredients(): Ingredient[] {
    return this.gameState?.available_ingredients || [];
  }

  getIngredientQuantity(ingredientId: string): number {
    return this.gameState?.inventory.items[ingredientId] || 0;
  }

  getIngredientName(ingredientId: string): string {
    const ingredient = this.gameState?.available_ingredients.find(i => i.id === ingredientId);
    return ingredient?.name || ingredientId;
  }

  craftItemByRecipe(recipe: Recipe, quantity: number): void {
    if (!this.gameState) return;

    const totalCost = recipe.ingredients_cost * quantity;
    if (this.gameState.resources.gold >= totalCost) {
      // Find the tavern item associated with this recipe
      const item = this.gameState.tavern_items.find(i => i.id === recipe.item_id);
      if (item) {
        this.craftItem(item, quantity);
      }
    }
  }

  getAssignedGuests(): Guest[] {
    return this.gameState?.guests.filter(g => g.room_id !== null) || [];
  }

  // Ingredient Store methods
  getStoreIngredients(): Ingredient[] {
    // Only show purchasable ingredients in the store (based on backend)
    return this.gameState?.available_ingredients.filter(
      i => i.is_purchasable
    ) || [];
  }

  getIngredientPrice(ingredient: Ingredient): number {
    // Use backend market price
    return ingredient.market_price;
  }

  buyIngredient(ingredient: Ingredient, quantity: number): void {
    const totalCost = this.getIngredientPrice(ingredient) * quantity;
    if (this.gameState && this.gameState.resources.gold >= totalCost) {
      this.gameService.purchaseIngredient(ingredient.id, quantity).subscribe();
    }
  }

  canAffordIngredient(ingredient: Ingredient, quantity: number): boolean {
    if (!this.gameState) return false;
    const totalCost = this.getIngredientPrice(ingredient) * quantity;
    return this.gameState.resources.gold >= totalCost;
  }

  // Room leveling helpers
  getNextLevelThreshold(currentLevel: number): number {
    const thresholds: { [key: number]: number } = {
      1: 10,
      2: 100,
      3: 1000,
      4: 9999  // Max level
    };
    return thresholds[currentLevel] || 9999;
  }

  getLevelProgress(customersServed: number, currentLevel: number): number {
    if (currentLevel >= 4) return 100;  // Max level reached

    const threshold = this.getNextLevelThreshold(currentLevel);
    const progress = (customersServed / threshold) * 100;
    return Math.min(progress, 100);
  }

  // Upgrade filtering helpers
  getAvailableUpgrades(): Upgrade[] {
    return this.gameService.getAvailableUpgrades(this.gameState);
  }

  getAcquiredUpgrades(): Upgrade[] {
    return this.gameService.getAcquiredUpgrades(this.gameState);
  }

  getPremiumUpgrades(): Upgrade[] {
    if (!this.gameState || !this.gameState.premium_upgrades) return [];
    return this.gameState.premium_upgrades;
  }
}
