"""Tests for python-melcloud."""

from pathlib import Path


def load_fixture(filename: str) -> str:
    """Load a fixture file as text."""
    return (Path(__file__).parent / "fixtures" / filename).read_text()
