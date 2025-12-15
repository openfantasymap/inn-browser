import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

export interface User {
  id: string;
  email: string;
  name: string;
  picture?: string;
  googleId?: string;
}

declare const google: any;

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private userSubject: BehaviorSubject<User | null>;
  public user$: Observable<User | null>;
  private readonly STORAGE_KEY = 'fantasy_inn_user';

  constructor() {
    // Load user from localStorage if available
    const storedUser = localStorage.getItem(this.STORAGE_KEY);
    const initialUser = storedUser ? JSON.parse(storedUser) : null;
    this.userSubject = new BehaviorSubject<User | null>(initialUser);
    this.user$ = this.userSubject.asObservable();
  }

  /**
   * Initialize Google Sign-In
   * Call this from the component after the Google API script is loaded
   */
  initializeGoogleSignIn(clientId: string): void {
    if (typeof google !== 'undefined' && google.accounts) {
      google.accounts.id.initialize({
        client_id: clientId,
        callback: (response: any) => this.handleGoogleCallback(response)
      });
    }
  }

  /**
   * Render Google Sign-In button
   */
  renderGoogleButton(element: HTMLElement): void {
    if (typeof google !== 'undefined' && google.accounts) {
      google.accounts.id.renderButton(
        element,
        {
          theme: 'filled_blue',
          size: 'large',
          text: 'signin_with',
          shape: 'rectangular',
          width: 250
        }
      );
    }
  }

  /**
   * Handle Google Sign-In callback
   */
  private handleGoogleCallback(response: any): void {
    if (response.credential) {
      // Decode JWT token to get user info
      const payload = this.decodeJwt(response.credential);

      const user: User = {
        id: payload.sub,
        email: payload.email,
        name: payload.name,
        picture: payload.picture,
        googleId: payload.sub
      };

      this.setUser(user);
    }
  }

  /**
   * Decode JWT token (simple base64 decode)
   */
  private decodeJwt(token: string): any {
    try {
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      );
      return JSON.parse(jsonPayload);
    } catch (error) {
      console.error('Error decoding JWT:', error);
      return null;
    }
  }

  /**
   * Set current user
   */
  private setUser(user: User): void {
    localStorage.setItem(this.STORAGE_KEY, JSON.stringify(user));
    this.userSubject.next(user);
  }

  /**
   * Get current user value (synchronous)
   */
  get currentUser(): User | null {
    return this.userSubject.value;
  }

  /**
   * Get user ID (for API calls)
   */
  getUserId(): string {
    return this.currentUser?.id || 'guest';
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return this.currentUser !== null;
  }

  /**
   * Sign out
   */
  signOut(): void {
    localStorage.removeItem(this.STORAGE_KEY);
    this.userSubject.next(null);

    // Sign out from Google
    if (typeof google !== 'undefined' && google.accounts) {
      google.accounts.id.disableAutoSelect();
    }
  }

  /**
   * Continue as guest (without authentication)
   */
  continueAsGuest(): void {
    const guestUser: User = {
      id: 'guest_' + Date.now(),
      email: 'guest@fantasy-inn.local',
      name: 'Guest Player'
    };
    this.setUser(guestUser);
  }
}
