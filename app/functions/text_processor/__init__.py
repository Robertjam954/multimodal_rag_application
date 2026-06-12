"""Custom skill: merges figures back into the text, chunks, embeds, returns chunks for AI Search ingestion."""
import json

import azure.functions as func

from prepdocslib.textsplitter import split_text


async def main(req: func.HttpRequest) -> func.HttpResponse:
    body = req.get_json()
    values = body.get("values", [])
    out = {"values": []}
    for record in values:
        rid = record.get("recordId")
        markdown = record.get("data", {}).get("markdown", "")
        chunks = [{"content": c} for c in split_text(markdown)]
        out["values"].append({"recordId": rid, "data": {"chunks": chunks}, "errors": [], "warnings": []})
    return func.HttpResponse(json.dumps(out), mimetype="application/json")
