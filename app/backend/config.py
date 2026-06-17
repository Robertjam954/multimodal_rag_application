"""Config constant keys stored on app.config[...]. Mirrors azure-search-openai-demo pattern."""

CONFIG_CREDENTIAL = "credential"
CONFIG_OPENAI_CLIENT = "openai_client"
CONFIG_SEARCH_CLIENT = "search_client"
CONFIG_KNOWLEDGEBASE_CLIENT = "knowledgebase_client"
CONFIG_KNOWLEDGEBASE_CLIENT_WITH_WEB = "knowledgebase_client_with_web"
CONFIG_KNOWLEDGEBASE_CLIENT_WITH_SHAREPOINT = "knowledgebase_client_with_sharepoint"
CONFIG_KNOWLEDGEBASE_CLIENT_WITH_WEB_AND_SHAREPOINT = "knowledgebase_client_with_web_and_sharepoint"

CONFIG_GLOBAL_BLOB_MANAGER = "global_blob_manager"
CONFIG_USER_BLOB_MANAGER = "user_blob_manager"
CONFIG_INGESTER = "ingester"
CONFIG_AUTH_CLIENT = "auth_client"

CONFIG_CHAT_APPROACH = "chat_approach"
CONFIG_MULTIAGENT_APPROACH = "multiagent_approach"
CONFIG_SQL_APPROACH = "sql_approach"

# Feature flags
CONFIG_AGENTIC_KNOWLEDGEBASE_ENABLED = "agentic_knowledgebase_enabled"
CONFIG_MULTIMODAL_ENABLED = "multimodal_enabled"
CONFIG_GRAPHRAG_ENABLED = "graphrag_enabled"
CONFIG_VERIFIER_ENABLED = "verifier_enabled"
CONFIG_VOICE_DEMO_ENABLED = "voice_demo_enabled"
CONFIG_SQL_DEMO_ENABLED = "sql_demo_enabled"
CONFIG_CONTENT_SAFETY_ENABLED = "content_safety_enabled"
CONFIG_PII_REDACTION_ENABLED = "pii_redaction_enabled"
CONFIG_FEEDBACK_ENABLED = "feedback_enabled"
CONFIG_LANGUAGE_PICKER_ENABLED = "language_picker_enabled"
CONFIG_USER_UPLOAD_ENABLED = "user_upload_enabled"
CONFIG_CHAT_HISTORY_COSMOS_ENABLED = "chat_history_cosmos_enabled"
CONFIG_CHAT_HISTORY_BROWSER_ENABLED = "chat_history_browser_enabled"

# Streaming + reasoning
CONFIG_STREAMING_ENABLED = "streaming_enabled"
CONFIG_REASONING_EFFORT_ENABLED = "reasoning_effort_enabled"
CONFIG_REASONING_EFFORT_OPTIONS = "reasoning_effort_options"
CONFIG_DEFAULT_REASONING_EFFORT = "default_reasoning_effort"
CONFIG_DEFAULT_RETRIEVAL_REASONING_EFFORT = "default_retrieval_reasoning_effort"

# RAG vector + image flags
CONFIG_VECTOR_SEARCH_ENABLED = "vector_search_enabled"
CONFIG_SEMANTIC_RANKER_DEPLOYED = "semantic_ranker_deployed"
CONFIG_QUERY_REWRITING_ENABLED = "query_rewriting_enabled"
CONFIG_RAG_SEARCH_TEXT_EMBEDDINGS = "rag_search_text_embeddings"
CONFIG_RAG_SEARCH_IMAGE_EMBEDDINGS = "rag_search_image_embeddings"
CONFIG_RAG_SEND_TEXT_SOURCES = "rag_send_text_sources"
CONFIG_RAG_SEND_IMAGE_SOURCES = "rag_send_image_sources"

# Knowledge sources
CONFIG_WEB_SOURCE_ENABLED = "web_source_enabled"
CONFIG_SHAREPOINT_SOURCE_ENABLED = "sharepoint_source_enabled"

# Voice
CONFIG_SPEECH_INPUT_ENABLED = "speech_input_enabled"
CONFIG_SPEECH_OUTPUT_AZURE_ENABLED = "speech_output_azure_enabled"
CONFIG_SPEECH_OUTPUT_BROWSER_ENABLED = "speech_output_browser_enabled"
CONFIG_SPEECH_SERVICE_ID = "speech_service_id"
CONFIG_SPEECH_SERVICE_LOCATION = "speech_service_location"
CONFIG_SPEECH_SERVICE_TOKEN = "speech_service_token"
CONFIG_SPEECH_SERVICE_VOICE = "speech_service_voice"

# Cost / rate
CONFIG_COST_METER = "cost_meter"
CONFIG_RATE_LIMITER = "rate_limiter"

# Tracing
CONFIG_LANGSMITH_CLIENT = "langsmith_client"
