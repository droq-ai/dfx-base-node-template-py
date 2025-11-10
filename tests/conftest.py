"""Pytest configuration and fixtures for testing."""

import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture(scope="session")
def nats_server():
    """
    Fixture to start NATS server using docker-compose.
    Only starts if NATS_URL environment variable is not set.
    """
    compose_file = Path(__file__).parent.parent / "compose.yml"
    nats_url = os.getenv("NATS_URL", "nats://localhost:4222")

    # Check if NATS is already running
    try:
        import socket

        host, port = nats_url.replace("nats://", "").split(":")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, int(port)))
        sock.close()
        if result == 0:
            # NATS is already running
            yield nats_url
            return
    except Exception:
        pass

    # Start NATS using docker-compose
    try:
        # Start only the NATS service
        subprocess.run(
            ["docker", "compose", "-f", str(compose_file), "up", "-d", "nats"],
            check=True,
            capture_output=True,
        )

        # Wait for NATS to be ready
        max_attempts = 30
        for i in range(max_attempts):
            try:
                import socket

                host, port = nats_url.replace("nats://", "").split(":")
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((host, int(port)))
                sock.close()
                if result == 0:
                    break
            except Exception:
                pass
            time.sleep(0.5)
        else:
            pytest.fail("NATS server did not start in time")

        yield nats_url

    finally:
        # Stop NATS after tests
        subprocess.run(
            ["docker", "compose", "-f", str(compose_file), "stop", "nats"],
            capture_output=True,
        )


@pytest.fixture
def nats_url(nats_server):
    """Fixture that provides NATS URL."""
    return nats_server
