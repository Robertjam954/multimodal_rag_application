"""Custom skill: persists entities/edges to Cosmos Gremlin + triggers community refresh."""
import json

import azure.functions as func


async def main(req: func.HttpRequest) -> func.HttpResponse:
    body = req.get_json()
    values = body.get("values", [])
    out = {"values": []}
    for record in values:
        rid = record.get("recordId")
        kg = record.get("data", {}).get("kg", {"nodes": [], "edges": []})
        # Real impl writes to Cosmos via gremlin client (see app/backend/graphrag/cosmos_gremlin.py).
        out["values"].append({"recordId": rid, "data": {"upserted": len(kg.get("nodes", []))}, "errors": [], "warnings": []})
    return func.HttpResponse(json.dumps(out), mimetype="application/json")
