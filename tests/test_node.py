"""Basic tests for the node template."""

import sys
from pathlib import Path

import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from node.main import run_node, shutdown_event


def test_imports():
    """Test that the module can be imported."""
    from node import main

    assert main is not None


@pytest.mark.asyncio
async def test_run_node(nats_url):
    """Test that run_node can be called (basic smoke test)."""
    import os

    # Set NATS URL for the test
    os.environ["NATS_URL"] = nats_url

    # Clear shutdown event first
    shutdown_event.clear()
    # Set shutdown event to exit quickly
    shutdown_event.set()

    # Should not raise an exception
    await run_node()


def test_shutdown_event():
    """Test shutdown event functionality."""
    # Reset to known state
    shutdown_event.clear()
    assert shutdown_event.is_set() is False

    shutdown_event.set()
    assert shutdown_event.is_set() is True

    shutdown_event.clear()
    assert shutdown_event.is_set() is False
