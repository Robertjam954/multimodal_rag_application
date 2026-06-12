"""Custom skill: enriches each figure with description + (optional) embedding."""
import json

import azure.functions as func


async def main(req: func.HttpRequest) -> func.HttpResponse:
    body = req.get_json()
    values = body.get("values", [])
    out = {"values": []}
    for record in values:
        rid = record.get("recordId")
        image_url = record.get("data", {}).get("image_url")
        description = f"[stub figure description for {image_url}]"
        embedding: list[float] = []
        out["values"].append(
            {"recordId": rid, "data": {"description": description, "embedding": embedding}, "errors": [], "warnings": []}
        )
    return func.HttpResponse(json.dumps(out), mimetype="application/json")
