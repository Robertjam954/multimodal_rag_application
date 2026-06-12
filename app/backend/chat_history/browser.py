"""Browser localStorage fallback for chat history. Backend is no-op; the frontend reads/writes its own store."""

NOTE = (
    "When USE_CHAT_HISTORY_COSMOS=false and USE_CHAT_HISTORY_BROWSER=true, "
    "the frontend persists threads in localStorage at key 'mmrag.history' and "
    "the backend exposes no /chat_history endpoints."
)
