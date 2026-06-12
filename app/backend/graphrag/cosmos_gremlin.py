"""Thin async wrapper over Cosmos DB Gremlin API. Stubs out cleanly when not configured."""
from __future__ import annotations

import logging
import os
from typing import Any

logger = logging.getLogger(__name__)


class CosmosGremlin:
    def __init__(self, account: str | None = None, database: str | None = None, graph: str | None = None) -> None:
        self.account = account or os.getenv("AZURE_COSMOSDB_ACCOUNT")
        self.database = database or os.getenv("AZURE_COSMOSDB_GRAPH_DATABASE", "kg")
        self.graph = graph or os.getenv("AZURE_COSMOSDB_GRAPH_CONTAINER", "graph")
        self._client = None

    def _connect(self):
        if self._client is not None:
            return self._client
        if not self.account:
            return None
        try:
            from gremlin_python.driver import client, serializer

            uri = f"wss://{self.account}.gremlin.cosmos.azure.com:443/"
            key = os.getenv("AZURE_COSMOSDB_KEY", "")
            self._client = client.Client(
                uri,
                "g",
                username=f"/dbs/{self.database}/colls/{self.graph}",
                password=key,
                message_serializer=serializer.GraphSONSerializersV2d0(),
            )
        except Exception:
            logger.exception("Cosmos Gremlin connect failed")
        return self._client

    async def upsert_node(self, node_id: str, label: str, properties: dict[str, Any]) -> None:
        c = self._connect()
        if not c:
            return
        props = " ".join(f".property('{k}', '{str(v).replace(chr(39), chr(34))}')" for k, v in properties.items())
        gremlin = f"g.V('{node_id}').fold().coalesce(unfold(), addV('{label}').property('id', '{node_id}'){props})"
        c.submit(gremlin).all().result()

    async def upsert_edge(self, source: str, target: str, label: str, properties: dict[str, Any] | None = None) -> None:
        c = self._connect()
        if not c:
            return
        props = properties or {}
        prop_str = " ".join(f".property('{k}', '{v}')" for k, v in props.items())
        gremlin = (
            f"g.V('{source}').as('a').V('{target}').coalesce(__.inE('{label}').where(outV().as('a')), "
            f"addE('{label}').from('a').to(V('{target}'))){prop_str}"
        )
        c.submit(gremlin).all().result()

    async def neighbors(self, node_id: str, hops: int = 2) -> dict[str, Any]:
        c = self._connect()
        if not c:
            return {"nodes": [], "edges": []}
        gremlin = f"g.V('{node_id}').repeat(bothE().subgraph('sg').otherV()).times({hops}).cap('sg').next()"
        try:
            result = c.submit(gremlin).all().result()
            return {"raw": result}
        except Exception:
            logger.exception("Cosmos Gremlin neighbors query failed")
            return {"nodes": [], "edges": []}
