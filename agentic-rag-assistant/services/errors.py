from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


class QuotaExceededError(Exception):
    """Raised when API quota is genuinely exhausted (not transient)."""
    pass


def next_quota_reset_message() -> str:
    pacific = ZoneInfo("America/Los_Angeles")
    now_pt = datetime.now(pacific)
    reset_time = (now_pt + timedelta(days=1)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    return reset_time.strftime("%B %d, %Y at %I:%M %p Pacific Time")