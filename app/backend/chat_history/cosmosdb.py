"""Cosmos DB SQL chat history blueprint. Persists threads per user."""
from __future__ import annotations

import logging
import os
from typing import Any

from quart import Blueprint, jsonify, request

logger = logging.getLogger(__name__)

chat_history_cosmosdb_bp = Blueprint("chat_history_cosmosdb", __name__, url_prefix="/chat_history")


def _client():
    try:
        from azure.cosmos.aio import CosmosClient
    except Exception:
        return None
    endpoint = os.getenv("AZURE_COSMOSDB_ENDPOINT")
    key = os.getenv("AZURE_COSMOSDB_KEY")
    if not (endpoint and key):
        return None
    return CosmosClient(endpoint, credential=key)


@chat_history_cosmosdb_bp.route("/", methods=["GET"])
async def list_threads():
    client = _client()
    if not client:
        return jsonify({"items": []})
    db = client.get_database_client(os.getenv("AZURE_COSMOSDB_CHAT_DATABASE", "chat"))
    container = db.get_container_client(os.getenv("AZURE_COSMOSDB_CHAT_CONTAINER", "history"))
    items = [i async for i in container.query_items("SELECT TOP 50 * FROM c ORDER BY c.updated_at DESC", enable_cross_partition_query=True)]
    return jsonify({"items": items})


@chat_history_cosmosdb_bp.route("/", methods=["POST"])
async def save_thread():
    body = await request.get_json()
    client = _client()
    if not client:
        return jsonify({"ok": False, "reason": "cosmos not configured"}), 503
    db = client.get_database_client(os.getenv("AZURE_COSMOSDB_CHAT_DATABASE", "chat"))
    container = db.get_container_client(os.getenv("AZURE_COSMOSDB_CHAT_CONTAINER", "history"))
    await container.upsert_item(body)
    return jsonify({"ok": True})
