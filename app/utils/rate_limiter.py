import time
from collections import defaultdict

# key -> list of timestamps (in seconds) when a request was made
request_log: dict[str, list[float]] = defaultdict(list)

def is_rate_limited(key: str, max_requests: int, window_seconds: int) -> bool:
    now = time.time()
    window_start = now - window_seconds

    # keep only timestamps that are still within the window
    request_log[key] = [ts for ts in request_log[key] if ts > window_start]

    if len(request_log[key]) >= max_requests:
        return True  # limit exceeded

    request_log[key].append(now)
    return False  # allowed