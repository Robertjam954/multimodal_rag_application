"""Shared service setup helpers (Search index schema, OpenAI client, etc.)."""
from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

# text-embedding-3-large; override via AZURE_SEARCH_DIMENSIONS if the deployment changes.
DEFAULT_EMBEDDING_DIMENSIONS = 3072


def search_index_schema(name: str, multimodal: bool = False):
    """Build the Azure AI Search index as SDK model objects.

    `SearchIndexClient.create_or_update_index` requires a `SearchIndex` model,
    not a raw dict. Vector fields cannot live inside complex collections, so the
    multimodal image embedding is a top-level `image_vector` field and `images`
    holds only url/description.
    """
    from azure.search.documents.indexes.models import (
        ComplexField,
        HnswAlgorithmConfiguration,
        HnswParameters,
        SearchableField,
        SearchField,
        SearchFieldDataType,
        SearchIndex,
        SemanticConfiguration,
        SemanticField,
        SemanticPrioritizedFields,
        SemanticSearch,
        SimpleField,
        VectorSearch,
        VectorSearchAlgorithmMetric,
        VectorSearchProfile,
    )

    dimensions = int(os.getenv("AZURE_SEARCH_DIMENSIONS", str(DEFAULT_EMBEDDING_DIMENSIONS)))

    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True, filterable=True),
        SimpleField(name="parent_id", type=SearchFieldDataType.String, filterable=True),
        SearchableField(name="content", type=SearchFieldDataType.String),
        SimpleField(name="category", type=SearchFieldDataType.String, filterable=True, facetable=True),
        SimpleField(name="source_type", type=SearchFieldDataType.String, filterable=True, facetable=True),
        SimpleField(name="sourcefile", type=SearchFieldDataType.String, filterable=True),
        SimpleField(name="sourcepage", type=SearchFieldDataType.String),
        SimpleField(name="storageUrl", type=SearchFieldDataType.String),
        SearchField(
            name="embedding",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=dimensions,
            vector_search_profile_name="default",
        ),
        SimpleField(
            name="acls",
            type=SearchFieldDataType.Collection(SearchFieldDataType.String),
            filterable=True,
        ),
    ]
    if multimodal:
        fields.append(
            ComplexField(
                name="images",
                collection=True,
                fields=[
                    SimpleField(name="url", type=SearchFieldDataType.String),
                    SearchableField(name="description", type=SearchFieldDataType.String),
                ],
            )
        )
        fields.append(
            SearchField(
                name="image_vector",
                type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                searchable=True,
                vector_search_dimensions=int(os.getenv("AZURE_SEARCH_IMAGE_DIMENSIONS", "1024")),
                vector_search_profile_name="default",
            )
        )

    return SearchIndex(
        name=name,
        fields=fields,
        vector_search=VectorSearch(
            algorithms=[
                HnswAlgorithmConfiguration(
                    name="hnsw",
                    parameters=HnswParameters(metric=VectorSearchAlgorithmMetric.COSINE),
                )
            ],
            profiles=[VectorSearchProfile(name="default", algorithm_configuration_name="hnsw")],
        ),
        semantic_search=SemanticSearch(
            configurations=[
                SemanticConfiguration(
                    name="default",
                    prioritized_fields=SemanticPrioritizedFields(
                        content_fields=[SemanticField(field_name="content")]
                    ),
                )
            ]
        ),
    )
