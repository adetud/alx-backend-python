#!/usr/bin/env python3
"""Utility functions for accessing nested maps."""

from typing import Any, Mapping, Tuple


def access_nested_map(nested_map: Mapping, path: Tuple[str, ...]) -> Any:
    """Access a nested map based on a path of keys."""
    current = nested_map
    for key in path:
        current = current[key]
    return current