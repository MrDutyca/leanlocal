"""Read-only localhost probe for AMD Lemonade Server.

This module deliberately sends no prompts, files, credentials, or private
project data. It only reads a small amount of non-identifying metadata from
a Lemonade Server listening on the loopback interface.
"""

from __future__ import annotations

import json
from urllib.request import urlopen

_BASE_URL = "http://127.0.0.1:13305"


def _get_json(path: str) -> dict:
    with urlopen(_BASE_URL + path, timeout=2) as response:
        return json.load(response)


def lemonade_probe() -> dict:
    """Return a privacy-minimised summary of a local Lemonade Server."""
    result = {
        "local_only": True,
        "base_url": _BASE_URL,
        "reachable": False,
        "queried_endpoints": ["/v1/health", "/v1/models"],
        "sends_prompts": False,
        "reads_user_files": False,
    }

    try:
        health = _get_json("/v1/health")
    except (OSError, ValueError, json.JSONDecodeError):
        result["note"] = "Lemonade Server was not reachable on localhost:13305."
        return result

    result["reachable"] = True
    result["status"] = health.get("status")
    result["version"] = health.get("version")
    telemetry = health.get("telemetry")
    if isinstance(telemetry, dict):
        result["telemetry_enabled"] = bool(telemetry.get("enabled", False))

    loaded = health.get("all_models_loaded")
    if isinstance(loaded, list):
        result["loaded_model_count"] = len(loaded)

    try:
        models = _get_json("/v1/models")
    except (OSError, ValueError, json.JSONDecodeError):
        result["available_model_count"] = None
        return result

    data = models.get("data") if isinstance(models, dict) else None
    result["available_model_count"] = len(data) if isinstance(data, list) else None
    return result
