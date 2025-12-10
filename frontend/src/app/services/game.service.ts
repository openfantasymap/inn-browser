import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, interval, Subject, BehaviorSubject } from 'rxjs';
import { switchMap, tap } from 'rxjs/operators';
import { InnState, RoomType } from '../models/game.models';

@Injectable({
  providedIn: 'root'
})
export class GameService {
  private apiUrl = 'http://localhost:8001/api';  // Django backend on port 8001
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
    // Django backend auto-assigns guests, so this just returns current state
    // Keep the method for compatibility but don't actually call backend
    return this.getGameState();
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
}
