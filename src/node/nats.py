"""NATS client helper for publishing and consuming messages."""

import asyncio
import json
import logging
import os
from collections.abc import Callable
from typing import Any

import nats
from nats.aio.client import Client as NATS
from nats.js import JetStreamContext
from nats.js.api import RetentionPolicy, StorageType, StreamConfig

logger = logging.getLogger(__name__)


class NATSClient:
    """NATS client wrapper for easy publishing and consuming."""

    def __init__(
        self,
        nats_url: str | None = None,
        stream_name: str | None = None,
    ):
        """
        Initialize NATS client.

        Args:
            nats_url: NATS server URL (defaults to NATS_URL env var)
            stream_name: JetStream name (defaults to STREAM_NAME env var)
        """
        self.nats_url = nats_url or os.getenv("NATS_URL", "nats://localhost:4222")
        self.stream_name = stream_name or os.getenv("STREAM_NAME", "droq-stream")
        self.nc: NATS | None = None
        self.js: JetStreamContext | None = None

    async def connect(self) -> None:
        """Connect to NATS server and initialize JetStream."""
        try:
            logger.info(f"Connecting to NATS at {self.nats_url}")
            self.nc = await nats.connect(self.nats_url)
            self.js = self.nc.jetstream()

            # Ensure stream exists
            await self._ensure_stream()

            logger.info("Connected to NATS and JetStream initialized")
        except Exception as e:
            logger.error(f"Failed to connect to NATS: {e}")
            raise

    async def _ensure_stream(self) -> None:
        """Ensure the JetStream exists, create if it doesn't."""
        try:
            # Try to get stream info
            await self.js.stream_info(self.stream_name)
            logger.info(f"Stream '{self.stream_name}' already exists")
        except Exception:
            # Stream doesn't exist, create it
            logger.info(f"Creating stream '{self.stream_name}'")
            await self.js.add_stream(
                StreamConfig(
                    name=self.stream_name,
                    subjects=[f"{self.stream_name}.>"],
                    retention=RetentionPolicy.WORK_QUEUE,
                    storage=StorageType.FILE,
                )
            )
            logger.info(f"Stream '{self.stream_name}' created")

    async def publish(
        self,
        subject: str,
        data: dict[str, Any],
        headers: dict[str, str] | None = None,
    ) -> None:
        """
        Publish a message to a NATS subject.

        Args:
            subject: NATS subject to publish to
            data: Data to publish (will be JSON encoded)
            headers: Optional headers to include
        """
        if not self.js:
            raise RuntimeError("Not connected to NATS. Call connect() first.")

        try:
            # Full subject with stream prefix
            full_subject = f"{self.stream_name}.{subject}"

            # Encode data as JSON
            payload = json.dumps(data).encode()

            # Publish with headers if provided
            if headers:
                await self.js.publish(full_subject, payload, headers=headers)
            else:
                await self.js.publish(full_subject, payload)

            logger.debug(f"Published message to {full_subject}")
        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
            raise

    async def subscribe(
        self,
        subject: str,
        callback: Callable[[dict[str, Any], dict[str, str]], None],
        queue: str | None = None,
    ) -> None:
        """
        Subscribe to a NATS subject and consume messages.

        Args:
            subject: NATS subject to subscribe to
            callback: Async function to call with (data, headers)
            queue: Optional queue group name for load balancing
        """
        if not self.js:
            raise RuntimeError("Not connected to NATS. Call connect() first.")

        try:
            # Full subject with stream prefix
            full_subject = f"{self.stream_name}.{subject}"

            # Create consumer if queue is specified
            if queue:
                consumer_name = f"{subject}-{queue}"
                try:
                    # Try to get existing consumer
                    await self.js.consumer_info(self.stream_name, consumer_name)
                except Exception:
                    # Create consumer for queue group
                    from nats.js.api import ConsumerConfig

                    await self.js.add_consumer(
                        self.stream_name,
                        ConsumerConfig(
                            durable_name=consumer_name,
                            deliver_group=queue,
                        ),
                    )

            async def message_handler(msg):
                """Handle incoming messages."""
                try:
                    # Decode message
                    data = json.loads(msg.data.decode())
                    headers = dict(msg.headers) if msg.headers else {}

                    # Call user callback
                    await callback(data, headers)

                    # Acknowledge message
                    await msg.ack()
                except Exception as e:
                    logger.error(f"Error processing message: {e}", exc_info=True)
                    # Optionally: implement retry logic or dead letter queue

            # Subscribe to subject
            if queue:
                # For queue groups, use pull_subscribe
                sub = await self.js.pull_subscribe(
                    full_subject,
                    queue,
                    stream=self.stream_name,
                )
                # Start consuming messages
                while True:
                    try:
                        msgs = await sub.fetch(1, timeout=1.0)
                        for msg in msgs:
                            await message_handler(msg)
                    except TimeoutError:
                        continue
            else:
                # Simple subscribe without queue - use push subscribe
                sub = await self.js.subscribe(full_subject, cb=message_handler)
                logger.info(f"Subscribed to {full_subject}")
                # Keep the subscription alive (this function doesn't return)
                await asyncio.Event().wait()

        except Exception as e:
            logger.error(f"Failed to subscribe: {e}")
            raise

    async def close(self) -> None:
        """Close NATS connection."""
        if self.nc:
            await self.nc.close()
            logger.info("NATS connection closed")
