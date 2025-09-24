import asyncio
from functools import partial
from confluent_kafka import Consumer, KafkaException
from .config import get_config
from .logging import logger
from .clients import oauth_manager

class MessageBusConsumer:
    """A simplified, generic Kafka consumer for the message bus."""

    def __init__(self, sync_client, async_client):
        self.config = get_config()
        self.sync_client = sync_client
        self.async_client = async_client
        self.consumer = self._initialize_consumer()

    def _get_token_callback(self, _):
        logger.debug("Refreshing Kafka consumer token.")
        token = self.sync_client.fetch_token()
        return token["access_token"], token["expires_at"]

    def _initialize_consumer(self) -> Consumer:
        """Sets up the Kafka consumer with configuration from environment variables."""
        consumer_config = {
            "bootstrap.servers": self.config["kafka_bootstrap_servers"],
            "group.id": f'{self.config["kafka_group_id_prefix"]}-{self.config["iam_client_id"]}',
            "auto.offset.reset": "latest",
            "security.protocol": "SASL_SSL",
            "sasl.mechanisms": "OAUTHBEARER",
            "oauth_cb": self._get_token_callback,
            "ssl.ca.location": self.config["kafka_ca_cert_path"],
        }
        try:
            consumer = Consumer(consumer_config)
            topic = self.config["kafka_topic"]
            consumer.subscribe([topic])
            logger.info(f"Successfully subscribed to Kafka topic: {topic}")
            return consumer
        except KafkaException as e:
            logger.critical(f"Failed to initialize or subscribe Kafka consumer: {e}")
            # In a real app, you might want to handle this more gracefully
            raise

    async def consume_messages(self):
        """Continuously consumes messages from the subscribed topic."""
        logger.info("Starting message consumption loop...")
        while True:
            try:
                # The consume call is blocking, so we run it in a separate thread
                # to avoid blocking the main async event loop.
                msg = await asyncio.to_thread(self.consumer.consume, num_messages=1, timeout=1.0)
                
                if not msg:
                    continue # Timeout
                if msg[0].error():
                    logger.error(f"Kafka consumer error: {msg[0].error()}")
                    continue

                message_data = msg[0].value()
                logger.debug(f"Received message of size {len(message_data)} bytes.")

                # TODO: Implement your message processing logic here.
                # This could involve:
                # 1. Getting a schema_id from the message headers.
                # 2. Fetching the schema from the Schema Registry.
                # 3. Deserializing the message_data using the schema.
                # 4. Acting on the deserialized data.

            except asyncio.CancelledError:
                logger.info("Message consumption cancelled. Shutting down consumer.")
                break
            except Exception as e:
                logger.error(f"An error occurred in the consumption loop: {e}")
                await asyncio.sleep(5) # Wait before retrying
        
        self.consumer.close()