"""Custom skill: extracts text + figure metadata from a blob using Azure Document Intelligence."""
import io
import json
import logging

import azure.functions as func

from prepdocslib.pdfparser import PdfParser

logger = logging.getLogger(__name__)


async def main(req: func.HttpRequest) -> func.HttpResponse:
    body = req.get_json()
    values = body.get("values", [])
    out = {"values": []}
    parser = PdfParser()
    for record in values:
        record_id = record.get("recordId")
        data = record.get("data", {})
        blob_url = data.get("blob_url")
        # Production: download blob via SDK. Skeleton: just acknowledge.
        markdown = f"[document_extractor stub for {blob_url}]"
        figures = []
        out["values"].append(
            {"recordId": record_id, "data": {"markdown": markdown, "figures": figures}, "errors": [], "warnings": []}
        )
    return func.HttpResponse(json.dumps(out), mimetype="application/json")
