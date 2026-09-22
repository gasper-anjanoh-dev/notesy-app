import os
import time

import boto3


ssm = None

_cache = {}
CACHE_TTL = 60  # seconds


def get_flag(flag_name):
    """Read a feature flag from SSM Parameter Store with caching."""
    now = time.time()

    if flag_name in _cache:
        value, timestamp = _cache[flag_name]
        if now - timestamp < CACHE_TTL:
            return value

    try:
        global ssm
        if ssm is None:
            ssm = boto3.client("ssm", region_name=os.environ.get("AWS_REGION", "us-east-1"))
        response = ssm.get_parameter(Name=f"/notesy/dev/features/{flag_name}")
        value = response["Parameter"]["Value"]
        _cache[flag_name] = (value, now)
        return value
    except Exception:
        return "false"


def is_enabled(flag_name, user_id=None):
    """Return whether a feature flag is enabled for the given user."""
    raw = get_flag(flag_name).lower().strip()

    if raw == "true":
        return True
    if raw == "false":
        return False
    if raw.endswith("%") and user_id is not None:
        pct = int(raw.replace("%", ""))
        return (abs(hash(str(user_id))) % 100) < pct
    return False
