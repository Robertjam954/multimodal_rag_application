"""Error helpers shared by routes."""
import logging
from typing import Any

from quart import jsonify

logger = logging.getLogger(__name__)


def error_dict(message: str, code: str = "generic_error", status: int = 500) -> dict[str, Any]:
    return {"error": {"code": code, "message": message, "status": status}}


def error_response(message: str, code: str = "generic_error", status: int = 500):
    logger.warning("error_response %s %s %s", status, code, message)
    return jsonify(error_dict(message, code, status)), status
