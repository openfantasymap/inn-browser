# MQTT Setup Guide

## Overview

The Fantasy Inn Tycoon application uses MQTT (Message Queue Telemetry Transport) for real-time communication between the backend and frontend. This replaces the previous HTTP polling mechanism with a more efficient pub/sub architecture.

## Architecture

### Backend (Publisher)
- **Technology**: Python Django with `paho-mqtt` library
- **Role**: Publishes game state updates to MQTT topics whenever state changes occur
- **Topics**:
  - `fantasy_inn/game_state/{player_id}` - Game state updates
  - `fantasy_inn/notifications/{player_id}` - Player notifications

### Frontend (Subscriber)
- **Technology**: Angular with `mqtt` and `ngx-mqtt` libraries
- **Role**: Subscribes to MQTT topics and receives real-time updates
- **Connection**: WebSocket on port 9001

## MQTT Broker Setup

### Option 1: Mosquitto (Recommended for Development)

1. **Install Mosquitto**:
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install mosquitto mosquitto-clients

   # macOS
   brew install mosquitto

   # Docker
   docker run -d -p 1883:1883 -p 9001:9001 --name mosquitto eclipse-mosquitto
   ```

2. **Configure Mosquitto** (`/etc/mosquitto/mosquitto.conf`):
   ```
   # Default MQTT port
   listener 1883
   protocol mqtt

   # WebSocket port for browsers
   listener 9001
   protocol websockets

   # Allow anonymous connections (dev only!)
   allow_anonymous true
   ```

3. **Start Mosquitto**:
   ```bash
   # System service
   sudo systemctl start mosquitto
   sudo systemctl enable mosquitto

   # Or run manually
   mosquitto -c /etc/mosquitto/mosquitto.conf

   # Docker
   docker start mosquitto
   ```

### Option 2: Docker Compose

Add to your `docker-compose.yml`:

```yaml
services:
  mosquitto:
    image: eclipse-mosquitto:latest
    ports:
      - "1883:1883"  # MQTT
      - "9001:9001"  # WebSocket
    volumes:
      - ./mosquitto.conf:/mosquitto/config/mosquitto.conf
    restart: unless-stopped
```

### Option 3: Cloud MQTT Broker

For production, consider managed MQTT services:
- **HiveMQ Cloud** (Free tier available)
- **CloudMQTT** (Free tier available)
- **AWS IoT Core**
- **Azure IoT Hub**

## Backend Configuration

### Django Settings

Configure MQTT in `backend_django/inn_project/settings.py`:

```python
# MQTT Configuration
MQTT_BROKER_HOST = os.environ.get('MQTT_BROKER_HOST', 'localhost')
MQTT_BROKER_PORT = int(os.environ.get('MQTT_BROKER_PORT', '1883'))
MQTT_USERNAME = os.environ.get('MQTT_USERNAME', '')
MQTT_PASSWORD = os.environ.get('MQTT_PASSWORD', '')
MQTT_USE_TLS = os.environ.get('MQTT_USE_TLS', 'false').lower() == 'true'
```

### Environment Variables

Create a `.env` file in your backend directory:

```env
MQTT_BROKER_HOST=localhost
MQTT_BROKER_PORT=1883
MQTT_USERNAME=
MQTT_PASSWORD=
MQTT_USE_TLS=false
```

For production:

```env
MQTT_BROKER_HOST=your-mqtt-broker.com
MQTT_BROKER_PORT=8883
MQTT_USERNAME=your_username
MQTT_PASSWORD=your_secure_password
MQTT_USE_TLS=true
```

## Frontend Configuration

The MQTT service is configured in `frontend/src/app/services/mqtt.service.ts`:

```typescript
private brokerUrl = 'ws://localhost:9001'; // WebSocket port
```

For production, update this to your production MQTT broker WebSocket URL:

```typescript
private brokerUrl = 'wss://your-mqtt-broker.com:443/mqtt';
```

## Testing the MQTT Connection

### 1. Test Backend Publishing

```bash
# Subscribe to all game state topics (requires mosquitto-clients)
mosquitto_sub -h localhost -p 1883 -t "fantasy_inn/#" -v

# In another terminal, trigger a game action via API
curl -X POST http://localhost:8001/api/game/player_1

# You should see messages published to the topic
```

### 2. Test Frontend Subscription

1. Start the Angular development server:
   ```bash
   cd frontend
   npm start
   ```

2. Open browser console and watch for MQTT connection logs:
   ```
   Connected to MQTT broker
   Subscribed to topic: fantasy_inn/game_state/player_1
   ```

3. Perform game actions and verify updates arrive via MQTT

### 3. Monitor MQTT Traffic

Use MQTT Explorer (GUI tool):
```bash
# Download from: http://mqtt-explorer.com/
# Connect to localhost:1883
# Browse topics under fantasy_inn/
```

## Message Format

### Game State Updates

**Topic**: `fantasy_inn/game_state/{player_id}`

**Payload** (JSON):
```json
{
  "resources": {
    "gold": 100.5,
    "reputation": 1.0
  },
  "rooms": [...],
  "guests": [...],
  "upgrades": [...],
  "tavern_items": [...],
  "recipes": [...],
  "inventory": {...}
}
```

**QoS**: 1 (At least once delivery)

### Notifications

**Topic**: `fantasy_inn/notifications/{player_id}`

**Payload** (JSON):
```json
{
  "type": "success|warning|error|info",
  "message": "Guest checked out and paid 50 gold!",
  "timestamp": "2025-12-15T13:30:00Z"
}
```

## Troubleshooting

### Frontend Can't Connect

**Symptom**: Console shows connection errors

**Solutions**:
1. Verify Mosquitto is running: `sudo systemctl status mosquitto`
2. Check WebSocket listener is configured on port 9001
3. Test WebSocket connection: `wscat -c ws://localhost:9001`
4. Check browser console for CORS issues
5. Verify firewall allows port 9001

### Backend Can't Publish

**Symptom**: Backend logs show MQTT errors

**Solutions**:
1. Check MQTT broker is running: `telnet localhost 1883`
2. Verify environment variables are loaded
3. Check broker credentials (if authentication enabled)
4. Review Django logs for connection errors
5. Test with mosquitto_pub: `mosquitto_pub -h localhost -p 1883 -t test -m "hello"`

### Messages Not Received

**Symptom**: Frontend connected but not receiving updates

**Solutions**:
1. Verify topics match between publisher and subscriber
2. Check QoS settings (should be 1 or 2)
3. Monitor broker logs: `sudo journalctl -u mosquitto -f`
4. Use MQTT Explorer to verify messages are being published
5. Check player_id matches between backend and frontend

### Reconnection Issues

**Symptom**: Connection drops and doesn't reconnect

**Solutions**:
1. Frontend has automatic reconnection (5 second interval)
2. Check `reconnectPeriod` in mqtt.service.ts
3. Verify broker supports persistent connections
4. Review browser network tab for WebSocket failures

## Security Considerations

### Development
- ✅ Anonymous connections allowed
- ✅ No TLS required
- ✅ localhost only

### Production
- ❌ **Never** allow anonymous connections
- ✅ Require username/password authentication
- ✅ Use TLS/SSL (wss:// for WebSocket)
- ✅ Implement access control lists (ACLs)
- ✅ Use separate credentials per service
- ✅ Rotate credentials regularly
- ✅ Monitor for unusual traffic patterns

### Production Mosquitto Config

```
# Disable anonymous
allow_anonymous false

# Password file
password_file /etc/mosquitto/passwd

# TLS configuration
listener 8883
protocol mqtt
cafile /etc/mosquitto/ca_certificates/ca.crt
certfile /etc/mosquitto/certs/server.crt
keyfile /etc/mosquitto/certs/server.key

# WebSocket with TLS
listener 443
protocol websockets
cafile /etc/mosquitto/ca_certificates/ca.crt
certfile /etc/mosquitto/certs/server.crt
keyfile /etc/mosquitto/certs/server.key

# ACL file
acl_file /etc/mosquitto/acl
```

## Performance Tuning

### Backend
- Connection pooling handled by singleton pattern
- Automatic reconnection on failure
- QoS 1 for reliability without excessive overhead

### Frontend
- Single connection per client
- Automatic reconnection with exponential backoff
- BehaviorSubject for state management (latest value cached)

### Broker
- Adjust `max_connections` based on expected concurrent users
- Configure `max_queued_messages` for offline clients
- Enable persistence for message durability
- Monitor memory usage and adjust `memory_limit`

## Migration from HTTP Polling

### What Changed

**Before**:
- Frontend polled backend every 1 second via HTTP
- High server load and latency
- Unnecessary requests when no state changes

**After**:
- Backend pushes updates only when state changes
- Persistent WebSocket connection
- Near-instant updates with minimal overhead

### Removed Code

- `startAutoTick()` method (game.service.ts)
- `stopAutoTick()` method (game.service.ts)
- `tap()` operators updating local state
- `interval()` polling mechanism

### New Code

- `MqttService` (mqtt.service.ts) - Frontend MQTT client
- `MQTTService` (mqtt_service.py) - Backend MQTT publisher
- `serialize_and_publish()` helper in views.py
- Automatic MQTT subscription in GameService constructor

## Additional Resources

- [MQTT.org](https://mqtt.org/) - Official MQTT specification
- [Eclipse Mosquitto](https://mosquitto.org/) - Open source MQTT broker
- [HiveMQ](https://www.hivemq.com/mqtt-essentials/) - MQTT essentials guide
- [Paho MQTT Python](https://eclipse.dev/paho/index.php?page=clients/python/index.php)
- [MQTT.js Documentation](https://github.com/mqttjs/MQTT.js)
