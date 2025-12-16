# MQTT Game Ticker Guide

## Overview

The MQTT Game Ticker is a Django management command that continuously processes game ticks for all active player game states and publishes updates via MQTT. This eliminates the need for manual tick triggering and ensures all players receive real-time updates.

## Available Commands

### 1. Basic Ticker (`mqtt_game_ticker`)

Simple version for development and testing.

**Usage:**
```bash
python manage.py mqtt_game_ticker
```

**Options:**
- `--interval SECONDS` - Tick interval in seconds (default: 1.0)
- `--active-only` - Only process games active in last 24 hours
- `--player-id PLAYER_ID` - Process only a specific player

**Examples:**
```bash
# Run with default 1-second interval
python manage.py mqtt_game_ticker

# Run with 2-second interval
python manage.py mqtt_game_ticker --interval 2.0

# Process only active games
python manage.py mqtt_game_ticker --active-only

# Process only a specific player
python manage.py mqtt_game_ticker --player-id player_123
```

### 2. Optimized Ticker (`mqtt_game_ticker_optimized`)

Production-ready version with multi-threading and batch processing.

**Usage:**
```bash
python manage.py mqtt_game_ticker_optimized
```

**Options:**
- `--interval SECONDS` - Tick interval in seconds (default: 1.0)
- `--workers N` - Number of worker threads (default: 4)
- `--batch-size N` - Max games to process per tick (default: 100)
- `--active-hours N` - Only process games active within N hours (default: 24, 0 = all)
- `--min-delay SECONDS` - Delay between individual game processing (default: 0.01)

**Examples:**
```bash
# Run with default settings
python manage.py mqtt_game_ticker_optimized

# High-performance setup for many players
python manage.py mqtt_game_ticker_optimized --workers 8 --batch-size 200

# Process all games regardless of activity
python manage.py mqtt_game_ticker_optimized --active-hours 0

# Slower, more conservative processing
python manage.py mqtt_game_ticker_optimized --interval 2.0 --workers 2
```

## Running as a Service

### Systemd Service (Linux)

Create `/etc/systemd/system/fantasy-inn-ticker.service`:

```ini
[Unit]
Description=Fantasy Inn MQTT Game Ticker
After=network.target postgresql.service mosquitto.service
Requires=postgresql.service mosquitto.service

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/inn-browser/backend_django
Environment="DJANGO_SETTINGS_MODULE=inn_project.settings"
Environment="PYTHONUNBUFFERED=1"

# Use optimized version for production
ExecStart=/var/www/inn-browser/venv/bin/python manage.py mqtt_game_ticker_optimized --workers 4 --batch-size 100 --active-hours 24

# Restart policy
Restart=always
RestartSec=10

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=fantasy-inn-ticker

# Resource limits
LimitNOFILE=65536
MemoryLimit=1G

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable fantasy-inn-ticker
sudo systemctl start fantasy-inn-ticker
```

**Manage service:**
```bash
# Check status
sudo systemctl status fantasy-inn-ticker

# View logs
sudo journalctl -u fantasy-inn-ticker -f

# Restart service
sudo systemctl restart fantasy-inn-ticker

# Stop service
sudo systemctl stop fantasy-inn-ticker
```

### Docker Compose

Add to your `docker-compose.yml`:

```yaml
services:
  game-ticker:
    build: ./backend_django
    command: python manage.py mqtt_game_ticker_optimized --workers 4
    depends_on:
      - db
      - mosquitto
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/fantasy_inn
      - MQTT_BROKER_HOST=mosquitto
      - MQTT_BROKER_PORT=1883
    restart: unless-stopped
    mem_limit: 1g
```

### Supervisor (Alternative)

Create `/etc/supervisor/conf.d/fantasy-inn-ticker.conf`:

```ini
[program:fantasy-inn-ticker]
command=/var/www/inn-browser/venv/bin/python manage.py mqtt_game_ticker_optimized
directory=/var/www/inn-browser/backend_django
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/fantasy-inn/ticker.log
environment=DJANGO_SETTINGS_MODULE="inn_project.settings"
```

**Start:**
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start fantasy-inn-ticker
```

## Performance Tuning

### Database Optimization

**Enable connection pooling:**
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'pool': True,
            'pool_size': 20,
            'max_overflow': 10,
        }
    }
}
```

**Add database indexes:**
```bash
python manage.py dbshell
```
```sql
CREATE INDEX idx_gamestate_last_tick ON game_api_gamestate(last_tick DESC);
CREATE INDEX idx_gamestate_player_id ON game_api_gamestate(player_id);
```

### MQTT Optimization

**Adjust QoS for performance:**
```python
# mqtt_service.py
# Change QoS from 1 to 0 for higher throughput (less reliability)
result = self._client.publish(topic, payload, qos=0, retain=False)
```

**Connection pooling:**
```python
# Consider using separate MQTT clients for ticker vs. web requests
```

### Resource Limits

**CPU and Memory:**
```bash
# Monitor resource usage
top -p $(pgrep -f mqtt_game_ticker)

# Adjust worker count based on CPU cores
--workers $(nproc)
```

**Recommended settings by load:**

| Players | Workers | Batch Size | Interval | Memory |
|---------|---------|------------|----------|--------|
| < 100   | 2       | 50         | 1.0s     | 256MB  |
| 100-500 | 4       | 100        | 1.0s     | 512MB  |
| 500-2K  | 8       | 200        | 1.0s     | 1GB    |
| 2K-10K  | 16      | 500        | 1.0s     | 2GB    |
| > 10K   | 32      | 1000       | 2.0s     | 4GB    |

## Monitoring

### Health Checks

**Check if ticker is running:**
```bash
ps aux | grep mqtt_game_ticker
```

**Check tick rate:**
```bash
# Watch systemd logs for tick output
journalctl -u fantasy-inn-ticker -f | grep "Tick"
```

### Metrics to Monitor

1. **Tick duration** - Should be < interval
2. **Error rate** - Should be < 1%
3. **Games processed per tick** - Stable count
4. **Memory usage** - Should not grow unbounded
5. **CPU usage** - Should be reasonable for worker count
6. **MQTT publish rate** - Messages per second
7. **Database connection pool** - Available connections

### Logging

**Enable detailed logging:**
```python
# settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/fantasy-inn/ticker.log',
        },
    },
    'loggers': {
        'game_api': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },
}
```

## Troubleshooting

### Ticker Not Processing Games

**Check database connection:**
```bash
python manage.py dbshell
SELECT COUNT(*) FROM game_api_gamestate;
```

**Check MQTT connection:**
```bash
mosquitto_sub -h localhost -p 1883 -t "fantasy_inn/#" -v
```

### High CPU Usage

- Reduce worker count
- Increase tick interval
- Enable batch size limits
- Check for slow database queries

### High Memory Usage

- Reduce batch size
- Optimize queryset prefetching
- Check for memory leaks in GameService
- Monitor with `memory_profiler`

### Games Not Updating

**Verify ticker is running:**
```bash
sudo systemctl status fantasy-inn-ticker
```

**Check logs for errors:**
```bash
sudo journalctl -u fantasy-inn-ticker -n 100
```

**Test MQTT publishing:**
```bash
# Subscribe to MQTT topic
mosquitto_sub -h localhost -t "fantasy_inn/game_state/#"

# Manually trigger a tick
python manage.py shell
>>> from game_api.services.game_service import GameService
>>> GameService.process_tick('player_1')
```

### Database Lock Contention

If you see database lock errors:

1. Reduce worker count
2. Increase `min-delay` between processing
3. Use database transaction isolation levels
4. Consider sharding by player_id

## Best Practices

1. **Start Conservative** - Begin with low worker count and increase gradually
2. **Monitor First** - Run with logging enabled for first 24 hours
3. **Gradual Rollout** - Test with `--player-id` for specific players first
4. **Active Hours Filter** - Use `--active-hours` to avoid processing inactive games
5. **Alerting** - Set up alerts for high error rates or slow ticks
6. **Backups** - Ensure database backups before deploying ticker
7. **Graceful Shutdown** - Always use Ctrl+C or `systemctl stop` (not `kill -9`)

## Development Tips

**Run in debug mode:**
```bash
python manage.py mqtt_game_ticker --player-id test_player --interval 0.5
```

**Test with mock MQTT:**
```bash
# Terminal 1: Subscribe
mosquitto_sub -h localhost -t "fantasy_inn/#" -v

# Terminal 2: Run ticker
python manage.py mqtt_game_ticker --player-id player_1
```

**Profile performance:**
```bash
python -m cProfile -o ticker.prof manage.py mqtt_game_ticker
python -m pstats ticker.prof
```

## Migration Strategy

### From HTTP Polling to Ticker

1. Deploy MQTT infrastructure first
2. Test ticker with `--player-id` for select users
3. Run ticker alongside HTTP polling initially
4. Monitor for discrepancies
5. Gradually increase ticker coverage
6. Disable HTTP auto-tick once ticker is stable

## Security Considerations

- Run ticker as non-root user (www-data)
- Limit memory and CPU with systemd
- Use MQTT authentication in production
- Monitor for unusual tick patterns
- Rate limit MQTT publishing if needed
- Encrypt MQTT traffic with TLS

## Scaling Horizontally

For very large deployments:

1. **Shard by Player ID** - Run multiple tickers with different player ranges
2. **Regional Deployment** - Deploy tickers per geographic region
3. **Load Balancing** - Use MQTT broker clustering
4. **Database Replication** - Read from replicas for game state
5. **Caching** - Cache frequently accessed game data

## Summary

The MQTT Game Ticker provides automated, real-time game state processing for all players. Use the basic version for development and the optimized version for production. Monitor performance metrics and tune worker count and batch size based on your player load.
