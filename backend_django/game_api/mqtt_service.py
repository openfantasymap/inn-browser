"""
MQTT Service for real-time game state updates
"""
import orjson as json
import os
import paho.mqtt.client as mqtt
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class MQTTService:
    """Service for publishing game state updates via MQTT"""

    _instance = None
    _client = None
    _connected = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MQTTService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._client:
            self._setup_client()

    def _setup_client(self):
        """Initialize MQTT client"""
        # Get MQTT broker settings from environment or use defaults
        self.broker_host = os.environ.get('MQTT_BROKER_HOST', 'broker.hivemq.com')
        self.broker_port = int(os.environ.get('MQTT_BROKER_PORT', '1883'))
        self.username = os.environ.get('MQTT_USERNAME')
        self.password = os.environ.get('MQTT_PASSWORD')

        # Create MQTT client
        self._client = mqtt.Client(client_id="fantasy_inn_backend", protocol=mqtt.MQTTv5)

        # Set callbacks
        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect
        self._client.on_publish = self._on_publish

        # Set credentials if provided
        if self.username and self.password:
            self._client.username_pw_set(self.username, self.password)

        # Connect to broker (non-blocking)
        try:
            self._client.connect_async(self.broker_host, self.broker_port, keepalive=60)
            self._client.loop_start()  # Start background thread
            logger.info(f"MQTT client connecting to {self.broker_host}:{self.broker_port}")
        except Exception as e:
            logger.error(f"Failed to connect to MQTT broker: {e}")
            self._connected = False

    def _on_connect(self, client, userdata, flags, rc, properties=None):
        """Callback when connected to MQTT broker"""
        if rc == 0:
            self._connected = True
            logger.info("Successfully connected to MQTT broker")
        else:
            self._connected = False
            logger.error(f"Failed to connect to MQTT broker. Return code: {rc}")

    def _on_disconnect(self, client, userdata, rc, properties=None):
        """Callback when disconnected from MQTT broker"""
        self._connected = False
        if rc != 0:
            logger.warning(f"Unexpected disconnect from MQTT broker. Code: {rc}")
        else:
            logger.info("Disconnected from MQTT broker")

    def _on_publish(self, client, userdata, mid, rc=None, properties=None):
        """Callback when message is published"""
        logger.debug(f"Message published: {mid}")

    def publish_game_state(self, player_id: str, game_state_data: dict):
        """
        Publish game state update for a specific player

        Args:
            player_id: Unique player identifier
            game_state_data: Serialized game state dictionary
        """
        if not self._connected:
            logger.warning("MQTT client not connected. Skipping publish.")
            return False

        topic = f"fantasy_inn/game_state/{player_id}"
        payload = json.dumps(game_state_data)

        try:
            result = self._client.publish(topic, payload, qos=1, retain=False)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logger.debug(f"Published game state to {topic}")
                return True
            else:
                logger.error(f"Failed to publish to {topic}. RC: {result.rc}")
                return False
        except Exception as e:
            logger.error(f"Error publishing to MQTT: {e}")
            return False

    def publish_notification(self, player_id: str, notification: dict):
        """
        Publish notification for a specific player

        Args:
            player_id: Unique player identifier
            notification: Notification data (type, message, etc.)
        """
        if not self._connected:
            logger.warning("MQTT client not connected. Skipping notification publish.")
            return False

        topic = f"fantasy_inn/notifications/{player_id}"
        payload = json.dumps(notification)

        try:
            result = self._client.publish(topic, payload, qos=1, retain=False)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logger.debug(f"Published notification to {topic}")
                return True
            else:
                logger.error(f"Failed to publish notification. RC: {result.rc}")
                return False
        except Exception as e:
            logger.error(f"Error publishing notification: {e}")
            return False

    def disconnect(self):
        """Disconnect from MQTT broker"""
        if self._client:
            self._client.loop_stop()
            self._client.disconnect()
            logger.info("MQTT client disconnected")

    @property
    def is_connected(self):
        """Check if MQTT client is connected"""
        return self._connected


# Singleton instance
def get_mqtt_service():
    """Get MQTT service singleton instance"""
    return MQTTService()
