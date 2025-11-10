#!/usr/bin/env python3
"""
Main entry point for the node.

This is an agnostic template - replace this with your node logic.
Includes examples for NATS JetStream and HTTP I/O.
"""

import asyncio
import logging
import os
import signal
import sys

# Optional: Use the logger helper
try:
    from .logger import setup_logging
except ImportError:
    setup_logging = None

# Optional: Import NATS and HTTP clients
try:
    from .nats import NATSClient
except ImportError:
    NATSClient = None

try:
    from .http import HTTPClient
except ImportError:
    HTTPClient = None


# Global flag for graceful shutdown
shutdown_event = asyncio.Event()


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    logging.info(f"Received signal {signum}, initiating shutdown...")
    shutdown_event.set()


async def run_node():
    """
    Main node logic.

    Replace this function with your actual node implementation.
    Examples below show how to use NATS JetStream and HTTP clients.
    """
    logger = logging.getLogger(__name__)
    logger.info("Node starting...")

    # Example: Read environment variables
    node_name = os.getenv("NODE_NAME", "droq-node")
    log_level = os.getenv("LOG_LEVEL", "INFO")

    logger.info(f"Node name: {node_name}")
    logger.info(f"Log level: {log_level}")

    # Initialize clients
    nats_client = None
    http_client = None

    try:
        # Example 1: Connect to NATS JetStream
        if NATSClient:
            try:
                nats_client = NATSClient()
                await nats_client.connect()
                logger.info("Connected to NATS JetStream")
            except Exception as e:
                logger.warning(
                    f"Could not connect to NATS (this is OK if NATS is not running): {e}"
                )
                nats_client = None

            # Example: Subscribe to messages
            async def handle_message(data: dict, headers: dict):
                """Handle incoming NATS messages."""
                logger.info(f"Received message: {data}")
                # Process your message here

            # Subscribe to a subject (runs in background)
            # Uncomment to enable:
            # asyncio.create_task(
            #     nats_client.subscribe("input", handle_message, queue="node-queue")
            # )

            # Example: Publish a message
            # await nats_client.publish(
            #     "output",
            #     {"message": "Hello from node", "timestamp": "2024-01-01T00:00:00Z"}
            # )

        # Example 2: Use HTTP client
        if HTTPClient:
            async with HTTPClient():
                # Example: Make GET request
                # response = await http.get("/api/endpoint")
                # logger.info(f"API response: {response}")

                # Example: Make POST request
                # response = await http.post(
                #     "/api/endpoint",
                #     json_data={"key": "value"}
                # )
                pass

        # Main processing loop
        while not shutdown_event.is_set():
            logger.debug("Node running...")

            # Your processing logic here
            # Examples:
            # - Process messages from NATS
            # - Poll APIs and publish to NATS
            # - Transform data between systems
            # - Connect to databases
            # - etc.

            # Example: Publish periodic updates
            # if nats_client:
            #     await nats_client.publish(
            #         "status",
            #         {"status": "running", "node": node_name}
            #     )

            # Wait a bit before next iteration
            try:
                await asyncio.wait_for(shutdown_event.wait(), timeout=1.0)
            except TimeoutError:
                continue

    except Exception as e:
        logger.error(f"Error in node execution: {e}", exc_info=True)
        raise
    finally:
        # Cleanup
        if nats_client:
            await nats_client.close()
        if http_client:
            await http_client.close()
        logger.info("Node shutting down...")


def main():
    """
    Main entry point.

    Sets up logging, signal handlers, and runs the node.
    """
    # Setup logging
    if setup_logging:
        setup_logging()
    else:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

    logger = logging.getLogger(__name__)

    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        # Run the node
        asyncio.run(run_node())
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
