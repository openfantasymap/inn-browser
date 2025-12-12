import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, interval, Subject, BehaviorSubject } from 'rxjs';
import { switchMap, tap } from 'rxjs/operators';
import { InnState, RoomType, ExperimentResult } from '../models/game.models';

@Injectable({
  providedIn: 'root'
})
export class GameService {
  private apiUrl = 'http://51.15.160.236/api';  // Django backend on port 8001
  private playerId = 'player_1'; // In a real app, this would come from auth
  private gameStateSubject = new BehaviorSubject<InnState | null>(null);
  public gameState$ = this.gameStateSubject.asObservable();

  private tickInterval = 1000; // 1 second
  private autoTickSubscription: any;

  constructor(private http: HttpClient) {}

  getGameState(): Observable<InnState> {
    return this.http.get<InnState>(`${this.apiUrl}/game/${this.playerId}`).pipe(
      tap(state => this.gameStateSubject.next(state))
    );
  }

  startNewGame(): Observable<InnState> {
    return this.http.post<InnState>(`${this.apiUrl}/game/${this.playerId}`, {}).pipe(
      tap(state => this.gameStateSubject.next(state))
    );
  }

  processTick(): Observable<InnState> {
    return this.http.post<InnState>(`${this.apiUrl}/tick/${this.playerId}`, {}).pipe(
      tap(state => this.gameStateSubject.next(state))
    );
  }

  startAutoTick(): void {
    this.autoTickSubscription = interval(this.tickInterval)
      .pipe(switchMap(() => this.processTick()))
      .subscribe();
  }

  stopAutoTick(): void {
    if (this.autoTickSubscription) {
      this.autoTickSubscription.unsubscribe();
    }
  }

  assignGuestToRoom(guestId: string, roomId: string): Observable<InnState> {
    return this.http.post<InnState>(
      `${this.apiUrl}/assign-guest/${this.playerId}`,
      { guest_id: parseInt(guestId, 10), room_id: parseInt(roomId, 10) }
    ).pipe(
      tap(state => this.gameStateSubject.next(state))
    );
  }

  cleanRoom(roomId: string): Observable<InnState> {
    return this.http.post<InnState>(
      `${this.apiUrl}/clean-room/${this.playerId}/${roomId}`,
      {}
    ).pipe(
      tap(state => this.gameStateSubject.next(state))
    );
  }

  purchaseUpgrade(upgradeId: string): Observable<InnState> {
    return this.http.post<InnState>(
      `${this.apiUrl}/purchase-upgrade/${this.playerId}/${upgradeId}`,
      {}
    ).pipe(
      tap(state => this.gameStateSubject.next(state))
    );
  }

  buildRoom(roomType: RoomType): Observable<InnState> {
    return this.http.post<InnState>(
      `${this.apiUrl}/add-room/${this.playerId}`,
      { room_type: roomType }
    ).pipe(
      tap(state => this.gameStateSubject.next(state))
    );
  }

  unlockRecipe(recipeId: string): Observable<InnState> {
    return this.http.post<InnState>(
      `${this.apiUrl}/unlock-recipe/${this.playerId}/${recipeId}`,
      {}
    ).pipe(
      tap(state => this.gameStateSubject.next(state))
    );
  }

  craftItem(itemId: string, quantity: number = 1): Observable<InnState> {
    return this.http.post<InnState>(
      `${this.apiUrl}/craft-item/${this.playerId}`,
      null,
      { params: { item_id: itemId, quantity: quantity.toString() } }
    ).pipe(
      tap(state => this.gameStateSubject.next(state))
    );
  }

  serveGuest(guestId: string, itemId: string): Observable<InnState> {
    return this.http.post<InnState>(
      `${this.apiUrl}/serve-guest/${this.playerId}`,
      null,
      { params: { guest_id: guestId, item_id: itemId } }
    ).pipe(
      tap(state => this.gameStateSubject.next(state))
    );
  }

  experimentWithIngredients(ingredientIds: string[]): Observable<ExperimentResult> {
    return this.http.post<ExperimentResult>(
      `${this.apiUrl}/experiment/${this.playerId}`,
      { ingredient_ids: ingredientIds }
    ).pipe(
      tap(result => {
        if (result.game_state) {
          this.gameStateSubject.next(result.game_state);
        }
      })
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
    return this.http.post<InnState>(
      `${this.apiUrl}/purchase-ingredient/${this.playerId}`,
      { ingredient_id: ingredientId, quantity: quantity }
    ).pipe(
      tap(state => this.gameStateSubject.next(state))
    );
  }
}
