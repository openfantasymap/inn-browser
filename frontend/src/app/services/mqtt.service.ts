import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import mqtt from 'mqtt';
import { InnState } from '../models/game.models';
import { AuthService } from '../core/auth/auth.service';

@Injectable({
  providedIn: 'root'
})
export class MqttService {
  private client: mqtt.MqttClient | null = null;
  private gameStateSubject = new BehaviorSubject<InnState | null>(null);
  public gameState$ = this.gameStateSubject.asObservable();

  private connectionStatusSubject = new BehaviorSubject<boolean>(false);
  public connectionStatus$ = this.connectionStatusSubject.asObservable();

  private brokerUrl = 'ws://broker.hivemq.com:8000/mqtt'; // WebSocket port for MQTT
  private connected = false;

  constructor(
    private auth: AuthService
  ) {}

  /**
   * Connect to MQTT broker
   */
  connect(): void {
    const pid = this.auth.getUserId();
    if (this.client) {
      console.log('MQTT client already exists');
      return;
    }

    try {
      // Connect to MQTT broker via WebSocket
      this.client = mqtt.connect(this.brokerUrl, {
        clientId: `fantasy_inn_web_${pid}`,
        clean: false,
        reconnectPeriod: 5000, // Reconnect every 5 seconds if disconnected
        connectTimeout: 30000,
        rejectUnauthorized: false,
        
      });

      // Connection event handlers
      this.client.on('connect', () => {
        console.log('Connected to MQTT broker');
        this.connected = true;
        this.connectionStatusSubject.next(true);
      });

      this.client.on('error', (error) => {
        console.error('MQTT connection error:', error);
        this.connectionStatusSubject.next(false);
      });

      this.client.on('close', () => {
        console.log('MQTT connection closed');
        this.connected = false;
        this.connectionStatusSubject.next(false);
      });

      this.client.on('reconnect', () => {
        console.log('Reconnecting to MQTT broker...');
      });

      this.client.on('message', (topic, message) => {
        this.handleMessage(topic, message);
      });

    } catch (error) {
      console.error('Failed to connect to MQTT broker:', error);
      this.connectionStatusSubject.next(false);
    }
  }

  /**
   * Subscribe to game state updates for a specific player
   */
  subscribeToGameState(playerId: string): void {
    if (!this.client || !this.connected) {
      console.warn('MQTT client not connected. Call connect() first.');
      // Try to connect
      this.connect();
      // Wait a bit and try to subscribe
      setTimeout(() => this.subscribeToGameState(playerId), 1000);
      return;
    }

    const topic = `fantasy_inn/game_state/${playerId}`;
    this.client.subscribe(topic, { qos: 1 }, (error) => {
      if (error) {
        console.error(`Failed to subscribe to ${topic}:`, error);
      } else {
        console.log(`Subscribed to ${topic}`);
      }
    });
  }

  /**
   * Unsubscribe from game state updates
   */
  unsubscribeFromGameState(playerId: string): void {
    if (!this.client) return;

    const topic = `fantasy_inn/game_state/${playerId}`;
    this.client.unsubscribe(topic, (error) => {
      if (error) {
        console.error(`Failed to unsubscribe from ${topic}:`, error);
      } else {
        console.log(`Unsubscribed from ${topic}`);
      }
    });
  }

  /**
   * Handle incoming MQTT messages
   */
  private handleMessage(topic: string, message: Buffer): void {
    try {
      const payload = message.toString();
      console.log(`Received message on ${topic}`);

      if (topic.startsWith('fantasy_inn/game_state/')) {
        const gameState = JSON.parse(payload) as InnState;
        this.gameStateSubject.next(gameState);
      } else if (topic.startsWith('fantasy_inn/notifications/')) {
        const notification = JSON.parse(payload);
        console.log('Received notification:', notification);
        // Handle notifications (could add a separate subject for this)
      }
    } catch (error) {
      console.error('Error handling MQTT message:', error);
    }
  }

  /**
   * Disconnect from MQTT broker
   */
  disconnect(): void {
    if (this.client) {
      this.client.end();
      this.client = null;
      this.connected = false;
      this.connectionStatusSubject.next(false);
      console.log('Disconnected from MQTT broker');
    }
  }

  /**
   * Check if connected
   */
  isConnected(): boolean {
    return this.connected;
  }
}
