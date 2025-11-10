"""Droq Node Template - Agnostic Python node template."""

__version__ = "0.1.0"

# Export main components
from .main import main, run_node, shutdown_event

__all__ = ["main", "run_node", "shutdown_event"]
