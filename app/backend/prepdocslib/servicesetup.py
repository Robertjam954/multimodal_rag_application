"""Shared service setup helpers (Search index schema, OpenAI client, etc.)."""
from __future__ import annotations

import logging
import os
from typing import Any

logger = logging.getLogger(__name__)


def search_index_schema(name: str, multimodal: bool = False) -> dict[str, Any]:
    fields = [
        {"name": "id", "type": "Edm.String", "key": True},
        {"name": "content", "type": "Edm.String", "searchable": True},
        {"name": "category", "type": "Edm.String", "filterable": True, "facetable": True},
        {"name": "sourcefile", "type": "Edm.String", "filterable": True},
        {"name": "sourcepage", "type": "Edm.String"},
        {"name": "storageUrl", "type": "Edm.String"},
        {"name": "embedding", "type": "Collection(Edm.Single)", "dimensions": 3072, "vectorSearchProfile": "default"},
        {"name": "acls", "type": "Collection(Edm.String)", "filterable": True},
        {"name": "parent_id", "type": "Edm.String", "filterable": True},
    ]
    if multimodal:
        fields.append(
            {
                "name": "images",
                "type": "Collection(Edm.ComplexType)",
                "fields": [
                    {"name": "url", "type": "Edm.String"},
                    {"name": "description", "type": "Edm.String"},
                    {"name": "embedding", "type": "Collection(Edm.Single)", "dimensions": 1024},
                ],
            }
        )
    return {
        "name": name,
        "fields": fields,
        "vectorSearch": {"profiles": [{"name": "default", "algorithm": "hnsw"}], "algorithms": [{"name": "hnsw", "kind": "hnsw"}]},
        "semantic": {"configurations": [{"name": "default", "prioritizedFields": {"contentFields": [{"fieldName": "content"}]}}]},
    }
