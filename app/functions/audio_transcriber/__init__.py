"""Custom skill: transcribes an audio blob and emits utterance JSON."""
import json

import azure.functions as func


async def main(req: func.HttpRequest) -> func.HttpResponse:
    body = req.get_json()
    values = body.get("values", [])
    out = {"values": []}
    for record in values:
        rid = record.get("recordId")
        audio_url = record.get("data", {}).get("audio_url")
        utterances = [
            {"speaker": "Speaker 1", "start": 0.0, "end": 5.0, "text": f"[stub transcript for {audio_url}]"}
        ]
        out["values"].append({"recordId": rid, "data": {"utterances": utterances}, "errors": [], "warnings": []})
    return func.HttpResponse(json.dumps(out), mimetype="application/json")
