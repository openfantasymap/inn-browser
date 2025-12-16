import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject, map } from 'rxjs';
import { InnState, RoomType, ExperimentResult, Upgrade } from '../models/game.models';
import { AuthService } from '../core/auth/auth.service';
import { MqttService } from './mqtt.service';

@Injectable({
  providedIn: 'root'
})
export class GameService {
  private apiUrl = 'http://51.15.160.236:9898/api';  // Django backend on port 8001
  private playerId = 'player_1'; // In a real app, this would come from auth
  private gameStateSubject = new BehaviorSubject<InnState | null>(null);
  public gameState$ = this.gameStateSubject.asObservable();

  upgrades: Upgrade[] = [];

  constructor(
    private http: HttpClient,
    private auth: AuthService,
    private mqttService: MqttService
  ) {
    this.playerId = auth.getUserId();

    // Connect to MQTT broker
    this.mqttService.connect();

    // Subscribe to game state updates via MQTT
    this.mqttService.subscribeToGameState(this.playerId);

    this.getUpgrades().subscribe(ups=>{
      this.upgrades = ups;
      // Pipe MQTT game state updates to our local subject
      this.mqttService.gameState$.subscribe(state => {      
        if (state) {
          let injectedUpgrades: Upgrade[] = [];
          state.upgrades.map(x=>{
            const nx = this.upgrades.filter(y => y.id === x.id);
            if(nx.length>0){
              injectedUpgrades.push({...nx[0], ...x});
            } else {
              injectedUpgrades.push(nx[0]);
            }
          });
          state.upgrades = injectedUpgrades; 
          this.gameStateSubject.next(state);
        }
      });
    })

    

    setInterval(()=>{this.processTick().subscribe(data=>{console.log('processing tick')})}, 5000);
  }

  getGameState(): Observable<InnState> {
    // MQTT will handle state updates, just return the HTTP response
    return this.http.get<InnState>(`${this.apiUrl}/game/${this.playerId}`);
  }

  startNewGame(): Observable<InnState> {
    // MQTT will handle state updates, just return the HTTP response
    return this.http.post<InnState>(`${this.apiUrl}/game/${this.playerId}`, {});
  }

  processTick(): Observable<InnState> {
    // MQTT will handle state updates, just return the HTTP response
    return this.http.post<InnState>(`${this.apiUrl}/tick/${this.playerId}`, {});
  }

  assignGuestToRoom(guestId: string, roomId: string): Observable<InnState> {
    // MQTT will handle state updates
    return this.http.post<InnState>(
      `${this.apiUrl}/assign-guest/${this.playerId}`,
      { guest_id: parseInt(guestId, 10), room_id: parseInt(roomId, 10) }
    );
  }

  cleanRoom(roomId: string): Observable<InnState> {
    // MQTT will handle state updates
    return this.http.post<InnState>(
      `${this.apiUrl}/clean-room/${this.playerId}/${roomId}`,
      {}
    );
  }

  purchaseUpgrade(upgradeId: string): Observable<InnState> {
    // MQTT will handle state updates
    return this.http.post<InnState>(
      `${this.apiUrl}/purchase-upgrade/${this.playerId}/${upgradeId}`,
      {}
    );
  }

  buildRoom(roomType: RoomType): Observable<InnState> {
    // MQTT will handle state updates
    return this.http.post<InnState>(
      `${this.apiUrl}/add-room/${this.playerId}`,
      { room_type: roomType }
    );
  }

  unlockRecipe(recipeId: string): Observable<InnState> {
    // MQTT will handle state updates
    return this.http.post<InnState>(
      `${this.apiUrl}/unlock-recipe/${this.playerId}/${recipeId}`,
      {}
    );
  }

  craftItem(itemId: string, quantity: number = 1): Observable<InnState> {
    // MQTT will handle state updates
    return this.http.post<InnState>(
      `${this.apiUrl}/craft-item/${this.playerId}`,
      null,
      { params: { item_id: itemId, quantity: quantity.toString() } }
    );
  }

  serveGuest(guestId: string, itemId: string): Observable<InnState> {
    // MQTT will handle state updates
    return this.http.post<InnState>(
      `${this.apiUrl}/serve-guest/${this.playerId}`,
      null,
      { params: { guest_id: guestId, item_id: itemId } }
    );
  }

  experimentWithIngredients(ingredientIds: string[]): Observable<ExperimentResult> {
    // MQTT will handle state updates
    return this.http.post<ExperimentResult>(
      `${this.apiUrl}/experiment/${this.playerId}`,
      { ingredient_ids: ingredientIds }
    );
  }

  // Helper method to check if a room type is unlocked based on upgrades
  isRoomTypeUnlocked(roomType: RoomType, gameState: InnState | null): boolean {
    if (!gameState) return false;

    const roomRequirements: { [key in RoomType]: string | null } = {
      [RoomType.BASIC]: null, // Always available
      [RoomType.STANDARD]: 'upgrade_room_standard',
      [RoomType.DELUXE]: 'upgrade_room_deluxe',
      [RoomType.ROYAL]: 'upgrade_room_royal'
    };

    const requiredUpgradeId = roomRequirements[roomType];
    if (!requiredUpgradeId) return true; // No requirement

    return gameState.upgrades.some(
      upgrade => upgrade.id === requiredUpgradeId && upgrade.purchased
    );
  }

  // Helper method to get discovered but not unlocked recipes
  getDiscoveredRecipes(gameState: InnState | null): any[] {
    if (!gameState) return [];
    return gameState.recipes.filter(r => r.discovered && !r.unlocked);
  }

  // Helper method to get unlocked recipes
  getUnlockedRecipes(gameState: InnState | null): any[] {
    if (!gameState) return [];
    return gameState.recipes.filter(r => r.unlocked);
  }

  purchaseIngredient(ingredientId: string, quantity: number): Observable<InnState> {
    // MQTT will handle state updates
    return this.http.post<InnState>(
      `${this.apiUrl}/purchase-ingredient/${this.playerId}`,
      { ingredient_id: ingredientId, quantity: quantity }
    );
  }

  getUpgrades(){
    return this.http.get<Upgrade[]>(
      `${this.apiUrl}/upgrades`
    );
  }

  // Helper method to get available (not purchased) upgrades
  getAvailableUpgrades(gameState: InnState | null): Upgrade[] {
    if (!gameState) return [];
    return gameState.upgrades.filter(upgrade => !upgrade.purchased);
  }

  // Helper method to get acquired (purchased) upgrades
  getAcquiredUpgrades(gameState: InnState | null): Upgrade[] {
    if (!gameState) return [];
    return gameState.upgrades.filter(upgrade => upgrade.purchased);
  }
}
