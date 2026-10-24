"""Local-only HTTP wrapper around the Vertex AI reasoning-engine demo."""
from __future__ import annotations

from typing import Any

from local_reasoning_engine import query_local_orchestrator
from pydantic import BaseModel, ValidationError
from quart import Quart, jsonify, request

app = Quart(__name__)


class QueryRequest(BaseModel):
    input: str


def _serialize_output(result: Any) -> Any:
    if isinstance(result, (dict, list, str, int, float, bool)) or result is None:
        return result
    return str(result)


@app.post("/predict")
async def predict():
    payload = await request.get_json(silent=True)
    if payload is None:
        return jsonify({"status": "error", "detail": "JSON request body is required."}), 400

    try:
        query = QueryRequest.model_validate(payload)
        result = query_local_orchestrator(query.input)
    except ValidationError as exc:
        return jsonify({"status": "error", "detail": exc.errors()}), 400
    except ValueError as exc:
        return jsonify({"status": "error", "detail": str(exc)}), 400
    except Exception as exc:  # pragma: no cover - defensive runtime wrapper
        return jsonify({"status": "error", "detail": str(exc)}), 500

    return jsonify({"status": "success", "output": _serialize_output(result)})


if __name__ == "__main__":
    app.run(port=8080, debug=True)
