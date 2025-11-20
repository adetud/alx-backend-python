#!/usr/bin/env python3
"""Utility functions."""

from typing import Mapping, Tuple, Any, Dict
import requests

def access_nested_map(nested_map: Mapping, path: Tuple[str, ...]) -> Any:
    """Access a nested map using a tuple path. Raises KeyError if path invalid."""
    current = nested_map
    for key in path:
        if not isinstance(current, dict) or key not in current:
            raise KeyError(key)
        current = current[key]
    return current


def get_json(url: str) -> Dict:
    """Return JSON payload from a given URL."""
    response = requests.get(url)
    return response.json()