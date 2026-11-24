import logging
import sys
import json
from datetime import datetime, timezone

# Setup logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("genstudio")

def audit_log(action: str, user_id: str = None, details: dict = None, ip_address: str = None):
    """Structured audit log entry."""
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "user_id": user_id,
        "ip_address": ip_address,
        "details": details or {}
    }
    logger.info(f"AUDIT: {json.dumps(entry)}")
